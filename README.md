# RN Intelligence API ???
> **Centralized Multi-Tenant AI Analytical Copilot & RAG Engine**  
> *Desenvolvido por [Renan Nocelli](https://github.com/Renanbritto)*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.14-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-8E75B2.svg?style=flat&logo=google&logoColor=white)](https://aistudio.google.com)
[![DuckDB](https://img.shields.io/badge/DuckDB-OLAP%20Engine-FFF000.svg?style=flat&logo=duckdb&logoColor=black)](https://duckdb.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ?? Vis?o Geral

O **RN Intelligence API** ? um microservi?o centralizado de intelig?ncia anal?tica projetado para alimentar assistentes conversacionais (Copilots) com **RAG (Retrieval-Augmented Generation)** em m?ltiplos dashboards e aplica??es de dados.

Em vez de replicar c?digo, chaves de API e regras de neg?cios em m?ltiplos reposit?rios, o **RN Intelligence** adota o padr?o **Strategy + Multi-Tenant Registry**, permitindo que uma ?nica API atenda simultaneamente diferentes projetos com total isolamento de regras de neg?cio, esquemas de dados e personas.

`
                           ?????????????????????????????????
                           ?      RN Intelligence API      ?
                           ?   (FastAPI Central Service)   ?
                           ?????????????????????????????????
                                           ?
                    ???????????????????????????????????????????????
                    ?              Project Registry               ?
                    ???????????????????????????????????????????????
                           ?               ?               ?
            ??????????????????????  ???????????????  ??????????????????????
            ?      sales-bi      ?  ?  churn-ml   ?  ? automacao-financeira?
            ?  (DuckDB / Vendas) ?  ? (K-Means/RFM?  ? (DRE / Concilia??o)?
            ??????????????????????  ???????????????  ??????????????????????
`

---

## ?? Projetos Ativos no Cat?logo

| Slug do Projeto | Nome | Dom?nio Anal?tico | Motor de Dados / RAG |
| :--- | :--- | :--- | :--- |
| sales-bi | **Sales BI Analytics** | Faturamento, Curva ABC, Vendedores, Funil B2B, Margem | DuckDB / SQLite Star Schema |
| utomacao-financeira | **Automa??o Financeira & DRE** | DRE Gerencial, EBITDA, Concilia??o Banc?ria CNAB/OFX | Pipeline ETL Cont?bil |
| churn-ml | **Segmenta??o RFM & Churn** | Clusters K-Means, Risco de Evas?o, Clientes VIPs | Scikit-Learn RFM Scores |
| portfolio | **Portf?lio Institucional** | Apresenta??o profissional, compet?ncias e cases de Renan Nocelli | Base de Conhecimento RAG |

---

## ??? Arquitetura e Boas Pr?ticas

- **Strategy Pattern (BaseProjectAdapter)**: Cada projeto implementa uma interface padronizada, encapsulando seu *System Prompt*, *RAG Context*, *Schema Context* e *Execu??o SQL*.
- **Execu??o Segura de Queries (Safe SQL Engine)**: Valida??o rigorosa por Regex/AST que bloqueia comandos destrutivos (DROP, DELETE, UPDATE, ALTER, etc.), permitindo estritamente consultas de leitura anal?tica (SELECT, WITH).
- **Resili?ncia Dual-Mode**:
  - **Modo Gemini RAG**: Quando configurada a GEMINI_API_KEY, a LLM sintetiza a resposta com base na consulta factual real.
  - **Modo Determin?stico (Fallback)**: Caso a LLM esteja sem chave ou atinja rate limits, o motor RAG anal?tico local resolve a consulta instantaneamente sem falhar a requisi??o.
- **Suporte Dual-Database**: DuckDB nativo em produ??o/cloud e fallback autom?tico para SQLite em ambientes restritos.

---

## ?? Endpoints da API

### 1. Chat Anal?tico Multi-Tenant
POST /api/v1/chat

**Payload de Requisi??o:**
`json
{
  "project_id": "sales-bi",
  "message": "Qual ? o faturamento total consolidado e a margem de contribui??o?"
}
`

**Resposta:**
`json
{
  "project_id": "sales-bi",
  "reply": "O Faturamento L?quido Total consolidado ? de R$ 39.035.677,55 (+18,4% YoY vs per?odo anterior)...",
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
`

### 2. Cat?logo de Projetos
GET /api/v1/projects
Retorna a lista de projetos registrados com perguntas sugeridas para preencher a interface de chat.

### 3. Diagn?stico e Telemetria
GET /api/v1/health
Retorna o status do servi?o, modelo de IA ativo e lista de projetos online.

---

## ?? Como Rodar Localmente

### 1. Clonar o reposit?rio
`ash
git clone https://github.com/Renanbritto/rn-intelligence-api.git
cd rn-intelligence-api
`

### 2. Configurar vari?veis de ambiente
`ash
cp .env.example .env
`
*(Insira sua chave GEMINI_API_KEY se desejar s?ntese generativa via Google Gemini).*

### 3. Instalar depend?ncias
`ash
pip install -r requirements-dev.txt
`

### 4. Executar os testes automatizados
`ash
pytest -v
`

### 5. Iniciar o servidor FastAPI
`ash
uvicorn app.main:app --reload --port 8000
`
Acesse a documenta??o interativa em: **http://localhost:8000/docs**.

---

## ?? Estrat?gia de Branches (Gitflow)

- main: Branch de produ??o est?vel com releases versionadas (1.0.0).
- develop: Branch de integra??o cont?nua.
- eature/*: Branches de novas funcionalidades e novos adaptadores de projeto.

---

## ?? Licen?a
Distribu?do sob a licen?a MIT. Veja LICENSE para mais informa??es.
