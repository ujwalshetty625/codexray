import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.services.analysis_service.graph_service import GraphService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/repos", tags=["Graph"])

_graph_service = GraphService()


@router.get("/{repo_id}/graph")
async def get_dependency_graph(
    repo_id: str,
    db: AsyncSession = Depends(get_db),
):
    if not repo_id or not repo_id.strip():
        raise HTTPException(status_code=400, detail="Invalid repo_id.")

    graph = await _graph_service.get_dependency_graph(repo_id=repo_id, db=db)

    if not graph["nodes"] and not graph["edges"]:
        raise HTTPException(
            status_code=404,
            detail=f"No dependency graph found for repository '{repo_id}'.",
        )

    return {"repo_id": repo_id, **graph}