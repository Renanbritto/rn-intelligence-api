"""
Interface Base para Adaptadores de Projeto no RN Intelligence.
Padr?o Strategy + Plugin Architecture.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class BaseProjectAdapter(ABC):
    """
    Contrato base que cada projeto implementa para se plugar ao RN Intelligence Engine.
    Permite total isolamento de regras de neg?cio, esquemas de dados e inten??es.
    """

    @property
    @abstractmethod
    def project_id(self) -> str:
        """Identificador slug ?nico do projeto (ex: 'sales-bi')."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome descritivo amig?vel (ex: 'Sales BI Analytics')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descri??o executiva do projeto e do seu escopo anal?tico."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Categoria do projeto (ex: 'Business Intelligence', 'Finan?as', 'Machine Learning')."""
        pass

    @property
    @abstractmethod
    def tags(self) -> List[str]:
        """Tags t?cnicas (ex: ['DuckDB', 'Vendas', 'DAX'])."""
        pass

    @property
    @abstractmethod
    def suggested_questions(self) -> List[str]:
        """Perguntas sugeridas (chips) para exibir na interface de chat."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Persona executiva e diretrizes de resposta do agente para este dom?nio."""
        pass

    @abstractmethod
    def get_rag_context(self) -> str:
        """Base consolidada de conhecimento (KPIs, regras de neg?cio, premissas)."""
        pass

    @abstractmethod
    def get_schema_context(self) -> str:
        """Schema dimensional e relacionamentos de dados para a LLM gerar/entender SQL."""
        pass

    @abstractmethod
    def execute_query(self, query: str, max_rows: int = 100) -> List[Dict[str, Any]]:
        """Executa uma consulta SQL segura no banco de dados espec?fico do projeto."""
        pass

    @abstractmethod
    def resolve_analytical_query(self, question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
        """
        Motor anal?tico determin?stico / RAG local.
        Retorna: (resposta_executiva, query_sql_utilizada, resultados_reais).
        Serve como resolu??o r?pida ou fallback resiliente se a LLM estiver indispon?vel.
        """
        pass
