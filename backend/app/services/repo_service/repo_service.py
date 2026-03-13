import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.services.repo_service.repo_validator import validate_and_parse, RepoValidationError
from backend.app.services.repo_service.github_client import GitHubClient, GitHubAPIError
from backend.app.models.repository import Repository
from backend.app.models.analysis_job import AnalysisJob
from backend.app.workers.analysis_worker import dispatch_analysis_job
from backend.app.config import settings


class RepoAlreadyExistsError(Exception):
    pass


class RepoServiceError(Exception):
    pass


async def submit_repository(repo_url: str, db: AsyncSession) -> dict:
    try:
        parsed = validate_and_parse(repo_url)
    except RepoValidationError as e:
        raise RepoServiceError(str(e)) from e

    existing = await db.execute(
        select(Repository).where(Repository.repo_url == parsed.url)
    )
    if existing.scalar_one_or_none():
        raise RepoAlreadyExistsError(f"Repository '{parsed.url}' has already been submitted.")

    async with GitHubClient(token=settings.GITHUB_TOKEN) as client:
        try:
            metadata = await client.fetch_repo_metadata(parsed)
        except GitHubAPIError as e:
            raise RepoServiceError(str(e)) from e

    repo_id = str(uuid.uuid4())[:8]

    repo = Repository(
        id=repo_id,
        repo_url=parsed.url,
        name=metadata.name,
        owner=metadata.owner,
        default_branch=metadata.default_branch,
        status="pending",
    )
    db.add(repo)

    job = AnalysisJob(
        id=str(uuid.uuid4()),
        repo_id=repo_id,
        status="queued",
    )
    db.add(job)

    await db.commit()
    await db.refresh(repo)
    await db.refresh(job)

    await dispatch_analysis_job(repo_id=repo_id, job_id=job.id)

    return {"repo_id": repo_id, "status": "processing"}


async def get_repo_status(repo_id: str, db: AsyncSession) -> dict:
    result = await db.execute(
        select(Repository).where(Repository.id == repo_id)
    )
    repo = result.scalar_one_or_none()

    if not repo:
        return None

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