"""Endpoint de Healthcheck e Telemetria."""
from fastapi import APIRouter
from app.core.config import settings
from app.registry.project_registry import registry
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
def get_health():
    api_key = settings.GEMINI_API_KEY.strip()
    is_llm = bool(api_key and api_key != "your_gemini_api_key_here")
    projects = [p.project_id for p in registry.list_projects()]
    
    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        llm_configured=is_llm,
        llm_model=settings.GEMINI_MODEL,
        active_projects=projects
    )
