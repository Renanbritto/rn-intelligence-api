# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Tuple
from app.interfaces.adapter import BaseProjectAdapter
from app.projects.sales_bi.knowledge import SYSTEM_PROMPT, BI_KNOWLEDGE_BASE, SCHEMA_CONTEXT
from app.projects.sales_bi.database import execute_sales_query
from app.projects.sales_bi.rag_engine import process_rag_query

class SalesBIAdapter(BaseProjectAdapter):
    @property
    def project_id(self) -> str:
        return "sales-bi"

    @property
    def name(self) -> str:
        return "Sales BI Analytics"

    @property
    def description(self) -> str:
        return (
            "Copilot analítico de inteligência comercial com KPIs executivos, "
            "análise de margem, curva ABC de produtos, funil de vendas e ranking de vendedores."
        )

    @property
    def category(self) -> str:
        return "Business Intelligence"

    @property
    def tags(self) -> List[str]:
        return ["DuckDB", "Star Schema", "DAX", "Vendas", "Curva ABC", "Pipeline B2B"]

    @property
    def suggested_questions(self) -> List[str]:
        return [
            "Qual é o faturamento líquido total e a margem?",
            "Quem é o vendedor líder em faturamento?",
            "Quais são os produtos Classe A da curva ABC?",
            "Qual o ticket médio e volume de pedidos?",
            "Qual a conversão do funil de vendas B2B?"
        ]

    def get_system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def get_rag_context(self) -> str:
        return "\n\n".join([f"[{k.upper()}]\n{v}" for k, v in BI_KNOWLEDGE_BASE.items()])

    def get_schema_context(self) -> str:
        return SCHEMA_CONTEXT

    def execute_query(self, query: str, max_rows: int = 100) -> List[Dict[str, Any]]:
        return execute_sales_query(query, max_rows=max_rows)

    def resolve_analytical_query(self, question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
        return process_rag_query(question)
