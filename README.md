# RN Intelligence API
> **Centralized Multi-Tenant AI Analytical Copilot & RAG Engine**  
> *Desenvolvido por [Renan Nocelli](https://github.com/Renanbritto)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-8E75B2.svg?style=flat&logo=google&logoColor=white)](https://aistudio.google.com)
[![DuckDB](https://img.shields.io/badge/DuckDB-OLAP%20Engine-FFF000.svg?style=flat&logo=duckdb&logoColor=black)](https://duckdb.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## Visao Geral

O **RN Intelligence API** e um microservico centralizado de inteligencia analitica projetado para alimentar assistentes conversacionais (Copilots) com **RAG (Retrieval-Augmented Generation)** em multiplos dashboards e aplicacoes de dados.

Em vez de replicar codigo, chaves de API e regras de negocio em multiplos repositorios, o **RN Intelligence** adota o padrao **Strategy + Multi-Tenant Registry**, permitindo que uma unica API atenda simultaneamente diferentes projetos com total isolamento de regras de negocio, esquemas de dados e personas.

```text
                           +-------------------------------+
                           |      RN Intelligence API      |
                           |   (FastAPI Central Service)   |
                           +---------------+---------------+
                                           |
                    +----------------------+----------------------+
                    |              Project Registry               |
                    +------+---------------+---------------+------+
                           |               |               |
            +--------------v-----+  +------v------+  +-----v--------------+
            |      sales-bi      |  |  churn-ml   |  | automacao-financeira|
            |  (DuckDB / Vendas) |  | (K-Means/RFM|  | (DRE / Conciliacao)|
            +--------------------+  +-------------+  +--------------------+
```

---

## Projetos Ativos no Catalogo

| Slug do Projeto | Nome | Dominio Analitico | Motor de Dados / RAG |
| :--- | :--- | :--- | :--- |
| `sales-bi` | **Sales BI Analytics** | Faturamento, Curva ABC, Vendedores, Funil B2B, Margem | DuckDB / SQLite Star Schema |
| `automacao-financeira` | **Automacao Financeira & DRE** | DRE Gerencial, EBITDA, Conciliacao Bancaria CNAB/OFX | Pipeline ETL Contabil |
| `churn-ml` | **Segmentacao RFM & Churn** | Clusters K-Means, Risco de Evasao, Clientes VIPs | Scikit-Learn RFM Scores |
| `portfolio` | **Portfolio Institucional** | Apresentacao profissional, competencias e cases de Renan Nocelli | Base de Conhecimento RAG |

---

## Arquitetura e Boas Praticas

- **Strategy Pattern (`BaseProjectAdapter`)**: Cada projeto implementa uma interface padronizada, encapsulando seu System Prompt, RAG Context, Schema Context e Execucao SQL.
- **Execucao Segura de Queries (`Safe SQL Engine`)**: Validacao rigorosa por Regex/AST que bloqueia comandos destrutivos (`DROP`, `DELETE`, `UPDATE`, `ALTER`, etc.), permitindo estritamente consultas de leitura analitica (`SELECT`, `WITH`).
- **Resiliencia Dual-Mode**:
  - **Modo Gemini RAG**: Quando configurada a `GEMINI_API_KEY`, a LLM sintetiza a resposta com base na consulta factual real.
  - **Modo Deterministico (Fallback)**: Caso a LLM esteja sem chave ou atinja rate limits, o motor RAG analitico local resolve a consulta instantaneamente sem falhar a requisicao.
- **Suporte Dual-Database**: DuckDB nativo em producao/cloud e fallback automatico para SQLite em ambientes restritos.

---

## Endpoints da API

### 1. Chat Analitico Multi-Tenant
`POST /api/v1/chat`

**Payload de Requisicao:**
```json
{
  "project_id": "sales-bi",
  "message": "Qual e o faturamento total consolidado e a margem de contribuicao?"
}
```

**Resposta:**
```json
{
  "project_id": "sales-bi",
  "reply": "O Faturamento Liquido Total consolidado e de R$ 39.035.677,55 (+18,4% YoY vs periodo anterior)...",
  "sql_query": "SELECT ROUND(SUM(valor_liquido), 2) AS faturamento_total... FROM f_vendas WHERE status_pedido = 'Faturado';",
  "query_results": [
    {
      "faturamento_total": 39035677.55,
      "total_pedidos": 13236,
      "margem_total": 16806501.55,
      "margem_pct": 43.05
    }
  ],
  "execution_time_ms": 12.4,
  "mode": "rag_analytical_engine"
}
```

### 2. Catalogo de Projetos
`GET /api/v1/projects`  
Retorna a lista de projetos registrados com perguntas sugeridas para preencher a interface de chat.

### 3. Diagnostico e Telemetria
`GET /api/v1/health`  
Retorna o status do servico, modelo de IA ativo e lista de projetos online.

---

## Como Rodar Localmente

### 1. Clonar o repositorio
```bash
git clone https://github.com/Renanbritto/rn-intelligence-api.git
cd rn-intelligence-api
```

### 2. Configurar variaveis de ambiente
```bash
cp .env.example .env
```
*(Insira sua chave `GEMINI_API_KEY` se desejar sintese generativa via Google Gemini).*

### 3. Instalar dependencias
```bash
pip install -r requirements-dev.txt
```

### 4. Executar os testes automatizados
```bash
pytest -v
```

### 5. Iniciar o servidor FastAPI
```bash
uvicorn app.main:app --reload --port 8000
```
Acesse a documentacao interativa em: `http://localhost:8000/docs`.

---

## Estrategia de Branches (Gitflow)

- `main`: Branch de producao estavel com releases versionadas (`v1.0.0`).
- `develop`: Branch de integracao continua.
- `feature/*`: Branches de novas funcionalidades e novos adaptadores de projeto.

---

## Licenca
Distribuido sob a licenca MIT. Veja `LICENSE` para mais informacoes.
