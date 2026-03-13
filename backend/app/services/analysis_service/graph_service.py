import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.models.dependency import Dependency

logger = logging.getLogger(__name__)


class GraphService:
    async def get_dependency_graph(self, repo_id: str, db: AsyncSession) -> dict:
        result = await db.execute(
            select(Dependency).where(Dependency.repo_id == repo_id)
        )
        records = result.scalars().all()

        if not records:
            logger.info("No dependency records found for repo '%s'.", repo_id)
            return {"nodes": [], "edges": []}

        nodes: set[str] = set()
        edges: list[dict] = []

        for record in records:
            nodes.add(record.source_file)
            nodes.add(record.target_file)
            edges.append({
                "source": record.source_file,
                "target": record.target_file,
            })

        logger.info(
            "Dependency graph built for repo '%s': %d nodes, %d edges.",
            repo_id, len(nodes), len(edges),
        )

        return {
            "nodes": sorted(nodes),
            "edges": edges,
        }