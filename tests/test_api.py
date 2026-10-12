# -*- coding: utf-8 -*-
"""
Testes automatizados da RN Intelligence API.
Validação de endpoints síncronos e streaming SSE, isolamento multi-tenant e segurança SQL.
"""
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import validate_safe_sql, SecurityValidationError

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "RN Intelligence API"
    assert data["status"] == "online"

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "sales-bi" in data["active_projects"]

def test_list_projects():
    response = client.get("/api/v1/projects")
    assert response.status_code == 200
    projects = response.json()
    ids = [p["project_id"] for p in projects]
    assert "sales-bi" in ids
    assert "automacao-financeira" in ids
    assert "churn-ml" in ids
    assert "portfolio" in ids

def test_get_project_detail():
    response = client.get("/api/v1/projects/sales-bi")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Sales BI Analytics"
    assert len(data["suggested_questions"]) > 0

def test_chat_sales_bi():
    payload = {
        "project_id": "sales-bi",
        "message": "Qual é o faturamento total consolidado?"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == "sales-bi"
    assert "39.035.677,55" in data["reply"] or "Faturamento" in data["reply"]
    assert "SELECT" in data["sql_query"].upper()
    assert len(data["query_results"]) > 0

def test_chat_portfolio():
    payload = {
        "project_id": "portfolio",
        "message": "Quais são os principais projetos desenvolvidos por Renan?"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == "portfolio"
    assert "Sales BI" in data["reply"]

def test_chat_invalid_project():
    payload = {
        "project_id": "projeto-inexistente-xyz",
        "message": "Olá mundo"
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 404

def test_chat_stream_sales_bi():
    payload = {
        "project_id": "sales-bi",
        "message": "Qual é a margem de contribuição?"
    }
    response = client.post("/api/v1/chat/stream", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    events = []
    for line in response.iter_lines():
        if line.startswith("data: "):
            raw = line[6:]
            event = json.loads(raw)
            events.append(event)
            
    assert len(events) >= 3
    event_types = [e["type"] for e in events]
    assert "metadata" in event_types
    assert "chunk" in event_types
    assert "done" in event_types
    
    # Valida metadados
    meta = next(e for e in events if e["type"] == "metadata")
    assert meta["project_id"] == "sales-bi"
    assert "SELECT" in meta["sql_query"].upper()

def test_chat_stream_invalid_project():
    payload = {
        "project_id": "projeto-desconhecido",
        "message": "Teste stream"
    }
    response = client.post("/api/v1/chat/stream", json=payload)
    assert response.status_code == 404

def test_sql_security_valid():
    validate_safe_sql("SELECT * FROM f_vendas WHERE status = 'Faturado';")
    validate_safe_sql("WITH cte AS (SELECT 1) SELECT * FROM cte;")

def test_sql_security_forbidden():
    with pytest.raises(SecurityValidationError):
        validate_safe_sql("DROP TABLE f_vendas;")

    with pytest.raises(SecurityValidationError):
        validate_safe_sql("DELETE FROM d_clientes;")

    with pytest.raises(SecurityValidationError):
        validate_safe_sql("UPDATE f_vendas SET valor = 0;")
