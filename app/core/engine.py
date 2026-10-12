"""
RN Intelligence Analytical & RAG Engine.
Orquestra o contexto do adaptador de projeto, extra??o de dados e s?ntese com LLM.
"""
import time
from typing import Any, AsyncGenerator, Dict, List, Optional
from app.core.config import settings
from app.interfaces.adapter import BaseProjectAdapter

class RNIntelligenceEngine:
    """
    Motor anal?tico central de intelig?ncia.
    Recebe um adaptador de projeto (Strategy) e executa o pipeline anal?tico RAG + LLM.
    """

    @classmethod
    async def process_chat(
        cls,
        adapter: BaseProjectAdapter,
        message: str,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executa o pipeline completo:
        1. Consulta anal?tica no adaptador (SQL real + dados).
        2. S?ntese executiva com Google Gemini (se configurado).
        3. Fallback de alta resili?ncia para o motor anal?tico determin?stico.
        """
        start_time = time.time()
        api_key = settings.GEMINI_API_KEY.strip()
        
        # 1. Modo Determin?stico direto se n?o houver chave de API configurada
        if not api_key or api_key == "your_gemini_api_key_here":
            reply, sql, data = adapter.resolve_analytical_query(message)
            elapsed = round((time.time() - start_time) * 1000, 2)
            return {
                "project_id": adapter.project_id,
                "reply": reply,
                "sql_query": sql,
                "query_results": data,
                "execution_time_ms": elapsed,
                "mode": "rag_analytical_engine"
            }

        # 2. Pipeline Gemini + Ground Truth Data (RAG Avan?ado)
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            # Executa RAG anal?tico primeiro para obter a verdade factual dos dados
            rag_reply, rag_sql, rag_data = adapter.resolve_analytical_query(message)
            rag_context = adapter.get_rag_context()
            schema_context = adapter.get_schema_context()
            system_prompt = adapter.get_system_prompt()
            
            prompt = (
                f"{system_prompt}\n\n"
                f"=== BASE DE CONHECIMENTO DO PROJETO (RAG) ===\n"
                f"{rag_context}\n\n"
                f"=== SCHEMA DIMENSIONAL E REGRAS ANAL?TICAS ===\n"
                f"{schema_context}\n\n"
                f"=== CONSULTA SQL REAL E RESULTADOS EXTRA?DOS ===\n"
                f"SQL: {rag_sql}\n"
                f"Resultados Reais: {rag_data}\n\n"
                f"Pergunta do Usu?rio: {message}\n\n"
                f"Por favor, responda ? pergunta do usu?rio baseando-se com rigor executivo nos dados reais acima. "
                f"Utilize n?meros formatados no padr?o brasileiro (R$, %) e destaque insights acion?veis."
            )
            
            resp = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )
            
            reply_text = resp.text.strip() if resp and resp.text else rag_reply
            elapsed = round((time.time() - start_time) * 1000, 2)
            
            return {
                "project_id": adapter.project_id,
                "reply": reply_text,
                "sql_query": rag_sql,
                "query_results": rag_data,
                "execution_time_ms": elapsed,
                "mode": "gemini_rag_agent"
            }
        except Exception:
            # Fallback seguro para o motor anal?tico determin?stico
            reply, sql, data = adapter.resolve_analytical_query(message)
            elapsed = round((time.time() - start_time) * 1000, 2)
            return {
                "project_id": adapter.project_id,
                "reply": reply,
                "sql_query": sql,
                "query_results": data,
                "execution_time_ms": elapsed,
                "mode": "rag_analytical_engine"
            }
