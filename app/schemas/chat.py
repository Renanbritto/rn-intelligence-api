"""
Modelos Pydantic para o fluxo de chat do RN Intelligence.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="Papel da mensagem: 'user' ou 'assistant'")
    content: str = Field(..., description="Conte?do do texto")

class ChatRequest(BaseModel):
    project_id: str = Field(
        ...,
        description="Slug do projeto de destino (ex: 'sales-bi', 'automacao-financeira', 'churn-ml', 'portfolio')",
        examples=["sales-bi"]
    )
    message: str = Field(
        ...,
        min_length=2,
        max_length=4000,
        description="Pergunta executiva ou anal?tica do usu?rio",
        examples=["Qual foi o faturamento total e a margem de contribui??o?"]
    )
    history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Hist?rico recente de mensagens para continuidade do contexto"
    )

class ChatResponse(BaseModel):
    project_id: str = Field(..., description="Projeto que processou a solicita??o")
    reply: str = Field(..., description="Resposta sintetizada executiva da RN Intelligence")
    sql_query: Optional[str] = Field(default="", description="Consulta SQL executada para fundamentar os dados")
    query_results: List[Dict[str, Any]] = Field(default_factory=list, description="Linhas retornadas pelo banco anal?tico")
    execution_time_ms: float = Field(..., description="Tempo total de execu??o em milissegundos")
    mode: str = Field(..., description="Modo de processamento: 'gemini_rag_agent' ou 'rag_analytical_engine'")
