from fastapi import APIRouter
from backend.app.api.routes.repo_routes import router as repo_router
from backend.app.api.routes.health_routes import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(repo_router)