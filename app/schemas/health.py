"""
Modelos Pydantic para diagn?stico e healthcheck da API.
"""
from typing import Dict, List
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(..., description="Estado do servi?o ('healthy')")
    service: str = Field(..., description="Nome da aplica??o")
    version: str = Field(..., description="Vers?o atual")
    environment: str = Field(..., description="Ambiente de execu??o")
    llm_configured: bool = Field(..., description="True se a chave GEMINI_API_KEY foi informada")
    llm_model: str = Field(..., description="Modelo Gemini ativo")
    active_projects: List[str] = Field(..., description="Lista de project_ids registrados")
