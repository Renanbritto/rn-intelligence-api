"""
Modelos Pydantic para metadados de projetos cadastrados.
"""
from typing import List
from pydantic import BaseModel, Field

class ProjectSummary(BaseModel):
    project_id: str = Field(..., description="Slug identificador ?nico")
    name: str = Field(..., description="Nome de exibi??o do projeto")
    category: str = Field(..., description="Categoria anal?tica")
    description: str = Field(..., description="Resumo do escopo")
    tags: List[str] = Field(default_factory=list, description="Tecnologias e conceitos")
    suggested_questions: List[str] = Field(default_factory=list, description="Perguntas r?pidas sugeridas")

class ProjectDetail(ProjectSummary):
    has_database: bool = Field(..., description="Indica se possui banco anal?tico ativo associado")
    system_prompt_preview: str = Field(..., description="Pr?via da persona configurada")
