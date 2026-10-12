"""Router central da API v1."""
from fastapi import APIRouter
from app.api.v1.endpoints import health, projects, chat

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(projects.router)
api_v1_router.include_router(chat.router)
