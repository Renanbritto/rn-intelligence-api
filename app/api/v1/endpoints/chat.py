"""Endpoint Multi-Tenant do Chat RN Intelligence."""
from fastapi import APIRouter, HTTPException
from app.registry.project_registry import registry
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.engine import RNIntelligenceEngine
from app.core.exceptions import ProjectNotFoundError

router = APIRouter(prefix="/chat", tags=["RN Intelligence Chat"])

@router.post("", response_model=ChatResponse)
async def chat_with_copilot(req: ChatRequest):
    """
    Processa uma pergunta anal?tica para o projeto especificado em req.project_id.
    Executa RAG, consulta o banco e sintetiza a resposta executiva.
    """
    try:
        adapter = registry.get(req.project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    result = await RNIntelligenceEngine.process_chat(
        adapter=adapter,
        message=req.message,
        history=[h.model_dump() for h in req.history] if req.history else None
    )
    return ChatResponse(**result)
