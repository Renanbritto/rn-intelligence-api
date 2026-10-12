"""
Cat?logo Central Multi-Tenant de Projetos (Registry Pattern).
"""
from typing import Dict, List, Optional
from app.interfaces.adapter import BaseProjectAdapter
from app.core.exceptions import ProjectNotFoundError
from app.schemas.project import ProjectSummary, ProjectDetail

class ProjectRegistry:
    """
    Gerenciador singleton de todos os adaptadores de projeto registrados.
    Permite busca r?pida por project_id e descoberta de capacidades.
    """

    def __init__(self):
        self._adapters: Dict[str, BaseProjectAdapter] = {}

    def register(self, adapter: BaseProjectAdapter) -> None:
        """Registra um novo adaptador de projeto no cat?logo."""
        self._adapters[adapter.project_id] = adapter

    def get(self, project_id: str) -> BaseProjectAdapter:
        """Recupera o adaptador do projeto pelo slug. Levanta ProjectNotFoundError se n?o existir."""
        adapter = self._adapters.get(project_id)
        if not adapter:
            raise ProjectNotFoundError(project_id)
        return adapter

    def list_projects(self) -> List[ProjectSummary]:
        """Retorna a lista resumida de todos os projetos dispon?veis."""
        return [
            ProjectSummary(
                project_id=a.project_id,
                name=a.name,
                category=a.category,
                description=a.description,
                tags=a.tags,
                suggested_questions=a.suggested_questions
            )
            for a in self._adapters.values()
        ]

    def get_project_detail(self, project_id: str) -> ProjectDetail:
        """Retorna os detalhes completos de um projeto espec?fico."""
        adapter = self.get(project_id)
        preview = adapter.get_system_prompt().strip().split("\n")[0]
        return ProjectDetail(
            project_id=adapter.project_id,
            name=adapter.name,
            category=adapter.category,
            description=adapter.description,
            tags=adapter.tags,
            suggested_questions=adapter.suggested_questions,
            has_database=True,
            system_prompt_preview=preview
        )

# Inst?ncia global do cat?logo
registry = ProjectRegistry()
