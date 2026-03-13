import json
import logging
from pathlib import Path

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.pipeline.ingestion.workspace_manager import WorkspaceManager, WorkspaceError
from backend.app.pipeline.ingestion.repo_cloner import RepositoryCloner, RepoCloneError
from backend.app.pipeline.file_indexer.file_scanner import FileScanner, FileScanError
from backend.app.pipeline.file_indexer.file_registry import FileRegistry
from backend.app.pipeline.parser.parser_engine import ParserEngine
from backend.app.pipeline.graph_builder.graph_builder import GraphBuilder
from backend.app.pipeline.architecture.architecture_detector import ArchitectureDetector
from backend.app.pipeline.review.review_generator import generate_review
from backend.app.models.repository import Repository
from backend.app.models.file_record import FileRecord
from backend.app.models.dependency import Dependency
from backend.app.models.architecture import Architecture
from backend.app.models.engineering_review import EngineeringReview
from backend.app.db.session import AsyncSessionFactory

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    pass


class AnalysisWorker:
    def __init__(
        self,
        workspace_manager: WorkspaceManager | None = None,
        cloner: RepositoryCloner | None = None,
        scanner: FileScanner | None = None,
        file_registry: FileRegistry | None = None,
        parser_engine: ParserEngine | None = None,
        graph_builder: GraphBuilder | None = None,
        architecture_detector: ArchitectureDetector | None = None,
    ):
        self._workspace  = workspace_manager or WorkspaceManager()
        self._cloner     = cloner or RepositoryCloner(self._workspace)
        self._scanner    = scanner or FileScanner()
        self._registry   = file_registry or FileRegistry()
        self._parser     = parser_engine or ParserEngine()
        self._graph      = graph_builder or GraphBuilder()
        self._arch       = architecture_detector or ArchitectureDetector()

    async def run_analysis(self, repo_url: str, repo_id: str) -> dict:
        logger.info("Starting analysis for repo '%s'.", repo_id)
        try:
            async with AsyncSessionFactory() as db:
                return await self._run_pipeline(repo_url, repo_id, db)
        except (WorkspaceError, RepoCloneError, FileScanError) as e:
            logger.error("Pipeline failure for repo '%s': %s", repo_id, e)
            raise AnalysisError(str(e)) from e
        except Exception as e:
            logger.exception("Unexpected error during analysis of repo '%s'.", repo_id)
            raise AnalysisError(f"Unexpected error: {e}") from e
        finally:
            self._safe_cleanup(repo_id)

    async def _run_pipeline(self, repo_url: str, repo_id: str, db: AsyncSession) -> dict:
        self._workspace.ensure_repo_workspace(repo_id)
        logger.info("[%s] Workspace ready.", repo_id)

        repo_path = Path(self._cloner.clone_repository(repo_url, repo_id))
        logger.info("[%s] Repository cloned.", repo_id)

        raw_files = self._scanner.scan_repository(repo_path)
        logger.info("[%s] Scanned %d files.", repo_id, len(raw_files))

        file_records = self._registry.build_registry(raw_files)
        logger.info("[%s] File registry built with %d records.", repo_id, len(file_records))

        await self._persist_files(repo_id, file_records, db)

        parsed_dependencies = self._parser.parse_repository(repo_path, file_records)
        logger.info("[%s] Parsed %d files with dependencies.", repo_id, len(parsed_dependencies))

        graph      = self._graph.build_graph(parsed_dependencies)
        edge_count = len(graph.get("edges", []))
        logger.info("[%s] Dependency graph built: %d edges.", repo_id, edge_count)

        await self._persist_dependencies(repo_id, graph.get("edges", []), db)

        architecture = self._arch.detect_architecture(repo_path)
        logger.info("[%s] Architecture detected: %s.", repo_id, architecture.get("architecture"))

        await self._persist_architecture(repo_id, architecture, db)

        # Senior engineer review
        review = generate_review(
            repo_id=repo_id,
            files=file_records,
            edges=graph.get("edges", []),
            architecture=architecture,
        )
        await self._persist_review(repo_id, review, db)
        logger.info("[%s] Engineering review generated.", repo_id)

        await db.execute(
            update(Repository)
            .where(Repository.id == repo_id)
            .values(status="completed")
        )

        await db.commit()

        return {
            "repo_id":      repo_id,
            "files":        len(file_records),
            "dependencies": edge_count,
            "architecture": {
                "type":       architecture.get("architecture", "Unknown"),
                "confidence": architecture.get("confidence", 0.0),
            },
        }

    @staticmethod
    async def _persist_files(repo_id: str, file_records: list[dict], db: AsyncSession) -> None:
        for record in file_records:
            db.add(FileRecord(
                repo_id=repo_id,
                path=record["path"],
                extension=record.get("extension", ""),
                language=record.get("language", "Unknown"),
                size=record.get("size", 0),
            ))

    @staticmethod
    async def _persist_dependencies(repo_id: str, edges: list, db: AsyncSession) -> None:
        for edge in edges:
            if isinstance(edge, dict):
                source, target = edge.get("source"), edge.get("target")
            elif isinstance(edge, (tuple, list)) and len(edge) >= 2:
                source, target = edge[0], edge[1]
            else:
                continue
            if source and target:
                db.add(Dependency(
                    repo_id=repo_id,
                    source_file=source,
                    target_file=target,
                    dependency_type="import",
                ))

    @staticmethod
    async def _persist_architecture(repo_id: str, result: dict, db: AsyncSession) -> None:
        db.add(Architecture(
            repo_id=repo_id,
            architecture_type=result.get("architecture", "Unknown"),
            confidence_score=result.get("confidence", 0.0),
        ))

    @staticmethod
    async def _persist_review(repo_id: str, review: dict, db: AsyncSession) -> None:
        db.add(EngineeringReview(
            repo_id=repo_id,
            summary=review["summary"],
            strengths=json.dumps(review["strengths"]),
            weaknesses=json.dumps(review["weaknesses"]),
            suggestions=json.dumps(review["suggestions"]),
        ))

    def _safe_cleanup(self, repo_id: str) -> None:
        try:
            self._workspace.cleanup_repo_workspace(repo_id)
            logger.info("[%s] Workspace cleaned up.", repo_id)
        except WorkspaceError as e:
            logger.warning("[%s] Cleanup failed: %s", repo_id, e)


async def dispatch_analysis_job(repo_url: str, repo_id: str, job_id: str) -> None:
    import asyncio

    async def _run():
        logger.info("Dispatching job '%s' for repo '%s'.", job_id, repo_id)
        worker = AnalysisWorker()
        try:
            result = await worker.run_analysis(repo_url=repo_url, repo_id=repo_id)
            logger.info("Job '%s' completed: %s", job_id, result)
        except AnalysisError as e:
            logger.error("Job '%s' failed: %s", job_id, e)

    asyncio.create_task(_run())