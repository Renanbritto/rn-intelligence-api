"""Endpoints para Cat?logo e Descoberta de Projetos."""
from typing import List
from fastapi import APIRouter, HTTPException
from app.registry.project_registry import registry
from app.schemas.project import ProjectSummary, ProjectDetail
from app.core.exceptions import ProjectNotFoundError

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectSummary])
def list_projects():
    """Lista todos os projetos anal?ticos registrados com seus metadados."""
    return registry.list_projects()

@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: str):
    """Retorna os detalhes completos e a pr?via da persona de um projeto."""
    try:
        return registry.get_project_detail(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
