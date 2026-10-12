# -*- coding: utf-8 -*-
"""
RN Intelligence Analytical & RAG Engine.
Orquestra o contexto do adaptador de projeto, extração de dados e síntese com LLM.
Suporta execução síncrona e streaming em tempo real via Server-Sent Events (SSE).
"""
import asyncio
import json
import re
import time
from typing import Any, AsyncGenerator, Dict, List, Optional
from app.core.config import settings
from app.interfaces.adapter import BaseProjectAdapter

class RNIntelligenceEngine:
    """
    Motor analítico central de inteligência.
    Recebe um adaptador de projeto (Strategy) e executa o pipeline analítico RAG + LLM.
    """

    @classmethod
    async def process_chat(
        cls,
        adapter: BaseProjectAdapter,
        message: str,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executa o pipeline completo síncrono:
        1. Consulta analítica no adaptador (SQL real + dados).
        2. Síntese executiva com Google Gemini (se configurado).
        3. Fallback de alta resiliência para o motor analítico determinístico.
        """
        start_time = time.time()
        api_key = settings.GEMINI_API_KEY.strip()
        
        # 1. Modo Determinístico direto se não houver chave de API configurada
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

        # 2. Pipeline Gemini + Ground Truth Data (RAG Avançado)
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            # Executa RAG analítico primeiro para obter a verdade factual dos dados
            rag_reply, rag_sql, rag_data = adapter.resolve_analytical_query(message)
            rag_context = adapter.get_rag_context()
            schema_context = adapter.get_schema_context()
            system_prompt = adapter.get_system_prompt()
            
            prompt = (
                f"{system_prompt}\n\n"
                f"=== BASE DE CONHECIMENTO DO PROJETO (RAG) ===\n"
                f"{rag_context}\n\n"
                f"=== SCHEMA DIMENSIONAL E REGRAS ANALÍTICAS ===\n"
                f"{schema_context}\n\n"
                f"=== CONSULTA SQL REAL E RESULTADOS EXTRAÍDOS ===\n"
                f"SQL: {rag_sql}\n"
                f"Resultados Reais: {rag_data}\n\n"
                f"Pergunta do Usuário: {message}\n\n"
                f"Por favor, responda à pergunta do usuário baseando-se com rigor executivo nos dados reais acima. "
                f"Utilize números formatados no padrão brasileiro (R$, %) e destaque insights acionáveis."
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
            # Fallback seguro para o motor analítico determinístico
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

    @classmethod
    async def stream_chat(
        cls,
        adapter: BaseProjectAdapter,
        message: str,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Executa o pipeline com streaming em tempo real via Server-Sent Events (SSE).
        Emite:
        - metadata: {project_id, sql_query, query_results, mode}
        - chunk: {delta: "texto..."}
        - done: {execution_time_ms, mode}
        """
        start_time = time.time()
        api_key = settings.GEMINI_API_KEY.strip()

        # 1. Modo Determinístico Local com Digitação Fluida (Typewriter Stream)
        if not api_key or api_key == "your_gemini_api_key_here":
            reply, sql, data = adapter.resolve_analytical_query(message)
            
            # Envia metadados com a query SQL e resultados brutos do banco
            meta_event = {
                "type": "metadata",
                "project_id": adapter.project_id,
                "sql_query": sql,
                "query_results": data,
                "mode": "rag_analytical_engine"
            }
            yield f"data: {json.dumps(meta_event, ensure_ascii=False)}\n\n"

            # Transmite as palavras em fluxo contínuo
            tokens = re.findall(r"\S+|\n|\s+", reply)
            for token in tokens:
                chunk_event = {"type": "chunk", "delta": token}
                yield f"data: {json.dumps(chunk_event, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.008)

            elapsed = round((time.time() - start_time) * 1000, 2)
            done_event = {
                "type": "done",
                "execution_time_ms": elapsed,
                "mode": "rag_analytical_engine"
            }
            yield f"data: {json.dumps(done_event, ensure_ascii=False)}\n\n"
            return

        # 2. Pipeline Google Gemini Streaming
        try:
            from google import genai
            client = genai.Client(api_key=api_key)

            rag_reply, rag_sql, rag_data = adapter.resolve_analytical_query(message)
            meta_event = {
                "type": "metadata",
                "project_id": adapter.project_id,
                "sql_query": rag_sql,
                "query_results": rag_data,
                "mode": "gemini_rag_agent"
            }
            yield f"data: {json.dumps(meta_event, ensure_ascii=False)}\n\n"

            prompt = (
                f"{adapter.get_system_prompt()}\n\n"
                f"=== BASE DE CONHECIMENTO DO PROJETO (RAG) ===\n"
                f"{adapter.get_rag_context()}\n\n"
                f"=== SCHEMA DIMENSIONAL E REGRAS ANALÍTICAS ===\n"
                f"{adapter.get_schema_context()}\n\n"
                f"=== CONSULTA SQL REAL E RESULTADOS EXTRAÍDOS ===\n"
                f"SQL: {rag_sql}\n"
                f"Resultados Reais: {rag_data}\n\n"
                f"Pergunta do Usuário: {message}\n\n"
                f"Por favor, responda à pergunta do usuário baseando-se com rigor executivo nos dados reais acima. "
                f"Utilize números formatados no padrão brasileiro (R$, %) e destaque insights acionáveis."
            )

            response_stream = client.models.generate_content_stream(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )

            for chunk in response_stream:
                if chunk and chunk.text:
                    chunk_event = {"type": "chunk", "delta": chunk.text}
                    yield f"data: {json.dumps(chunk_event, ensure_ascii=False)}\n\n"

            elapsed = round((time.time() - start_time) * 1000, 2)
            done_event = {
                "type": "done",
                "execution_time_ms": elapsed,
                "mode": "gemini_rag_agent"
            }
            yield f"data: {json.dumps(done_event, ensure_ascii=False)}\n\n"

        except Exception:
            # Fallback seguro com streaming local
            reply, sql, data = adapter.resolve_analytical_query(message)
            meta_event = {
                "type": "metadata",
                "project_id": adapter.project_id,
                "sql_query": sql,
                "query_results": data,
                "mode": "rag_analytical_engine"
            }
            yield f"data: {json.dumps(meta_event, ensure_ascii=False)}\n\n"

            tokens = re.findall(r"\S+|\n|\s+", reply)
            for token in tokens:
                chunk_event = {"type": "chunk", "delta": token}
                yield f"data: {json.dumps(chunk_event, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.008)

            elapsed = round((time.time() - start_time) * 1000, 2)
            done_event = {
                "type": "done",
                "execution_time_ms": elapsed,
                "mode": "rag_analytical_engine"
            }
            yield f"data: {json.dumps(done_event, ensure_ascii=False)}\n\n"
