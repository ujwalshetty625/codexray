import asyncio
import logging
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models.repository import Repository
from backend.app.models.analysis_job import AnalysisJob
from backend.app.models.file_record import FileRecord
from backend.app.models.dependency import Dependency
from backend.app.models.architecture import Architecture
from backend.app.services.repo_service.repo_validator import validate_and_parse, RepoValidationError
from backend.app.workers.analysis_worker import AnalysisWorker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/repos", tags=["Repositories"])

analysis_worker = AnalysisWorker()


class AnalyzeRequest(BaseModel):
    repo_url: str


class AnalyzeResponse(BaseModel):
    repo_id: str
    status: str


@router.post("/analyze", response_model=AnalyzeResponse, status_code=202)
async def analyze_repository(
    payload: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        parsed = validate_and_parse(payload.repo_url)
    except RepoValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    repo_url = parsed.url

    existing = await db.execute(
        select(Repository).where(Repository.repo_url == repo_url)
    )
    repo = existing.scalar_one_or_none()

    if repo:
        logger.info("Repository '%s' already exists, returning existing record.", repo.id)
        return AnalyzeResponse(repo_id=repo.id, status=repo.status)

    repo_id = str(uuid.uuid4())

    repository = Repository(
        id=repo_id,
        repo_url=repo_url,
        name=parsed.name,
        owner=parsed.owner,
        default_branch="main",
        status="processing",
        created_at=datetime.utcnow(),
    )

    job = AnalysisJob(
        id=str(uuid.uuid4()),
        repo_id=repo_id,
        status="queued",
        started_at=datetime.utcnow(),
    )

    db.add(repository)
    db.add(job)

    try:
        await db.commit()
        logger.info("Repository '%s' and analysis job committed to database.", repo_id)
    except Exception as e:
        await db.rollback()
        logger.exception("DB commit failed for repo '%s'.", repo_id)
        raise HTTPException(status_code=500, detail=str(e))

    asyncio.create_task(analysis_worker.run_analysis(repo_url, repo_id))
    logger.info("Analysis task dispatched for repo '%s'.", repo_id)

    return AnalyzeResponse(repo_id=repo_id, status="processing")


@router.get("/{repo_id}/status")
async def get_status(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repository).where(Repository.id == repo_id)
    )
    repo = result.scalar_one_or_none()

    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")

    job_result = await db.execute(
        select(AnalysisJob)
        .where(AnalysisJob.repo_id == repo_id)
        .order_by(AnalysisJob.started_at.desc())
        .limit(1)
    )
    job = job_result.scalar_one_or_none()

    return {
        "repo_id": repo.id,
        "status": repo.status,
        "job_status": job.status if job else None,
        "started_at": job.started_at if job else None,
        "completed_at": job.completed_at if job else None,
    }


@router.get("/{repo_id}/structure")
async def get_structure(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(FileRecord).where(FileRecord.repo_id == repo_id)
    )
    files = result.scalars().all()

    if not files:
        raise HTTPException(status_code=404, detail="No file structure found for this repository.")

    return {
        "repo_id": repo_id,
        "files": [
            {
                "path": f.path,
                "extension": f.extension,
                "language": f.language,
                "size": f.size,
            }
            for f in files
        ],
    }


@router.get("/{repo_id}/dependencies")
async def get_dependencies(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dependency).where(Dependency.repo_id == repo_id)
    )
    deps = result.scalars().all()

    if not deps:
        raise HTTPException(status_code=404, detail="No dependencies found for this repository.")

    return {
        "repo_id": repo_id,
        "dependencies": [
            {
                "source": d.source_file,
                "target": d.target_file,
                "type": d.dependency_type,
            }
            for d in deps
        ],
    }


@router.get("/{repo_id}/graph")
async def get_graph(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Dependency).where(Dependency.repo_id == repo_id)
    )
    deps = result.scalars().all()

    if not deps:
        raise HTTPException(status_code=404, detail="No dependency graph found for this repository.")

    seen_nodes: set[str] = set()
    nodes: list[dict] = []
    edges: list[dict] = []

    for dep in deps:
        for file in (dep.source_file, dep.target_file):
            if file not in seen_nodes:
                nodes.append({"id": file})
                seen_nodes.add(file)

        edges.append({
            "source": dep.source_file,
            "target": dep.target_file,
        })

    return {
        "repo_id": repo_id,
        "nodes": nodes,
        "edges": edges,
    }

@router.get("/{repo_id}/review")
async def get_review(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    from backend.app.models.engineering_review import EngineeringReview

    result = await db.execute(
        select(EngineeringReview).where(EngineeringReview.repo_id == repo_id)
    )
    review = result.scalar_one_or_none()

    if not review:
        raise HTTPException(status_code=404, detail="No review found for this repository.")

    return {
        "repo_id":     repo_id,
        "summary":     review.summary,
        "strengths":   json.loads(review.strengths),
        "weaknesses":  json.loads(review.weaknesses),
        "suggestions": json.loads(review.suggestions),
        "created_at":  review.created_at,
    }


@router.get("/{repo_id}/architecture")
async def get_architecture(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Architecture).where(Architecture.repo_id == repo_id)
    )
    arch = result.scalar_one_or_none()

    if not arch:
        raise HTTPException(status_code=404, detail="No architecture result found for this repository.")

    return {
        "repo_id": repo_id,
        "architecture": {
            "type": arch.architecture_type,
            "confidence": arch.confidence_score,
        },
    }