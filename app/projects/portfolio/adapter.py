"""
Base de Conhecimento e Adaptador para o Portf?lio de Renan Nocelli.
"""
from typing import Any, Dict, List, Tuple
from app.interfaces.adapter import BaseProjectAdapter

PORTFOLIO_SYSTEM_PROMPT = """Voc? ? o RN Intelligence, o assistente inteligente oficial do portf?lio de Renan Nocelli.
Sua miss?o ? apresentar a trajet?ria profissional, projetos de dados, compet?ncias t?cnicas e diferenciais de Renan para recrutadores, l?deres t?cnicos e clientes.

DIRETRIZES:
1. Tom profissional, elegante, acolhedor e seguro.
2. Destaque projetos reais, n?meros de impacto e dom?nio pr?tico de ponta a ponta (engenharia de dados, BI, ML e IA fullstack).
3. Sempre que relevante, direcione para os links do GitHub ou demonstre como entrar em contato.
"""

PORTFOLIO_KNOWLEDGE = {
    "perfil": (
        "Renan Nocelli ? Engenheiro de Analytics e Especialista em BI & IA Aplicada. "
        "Une vis?o anal?tica de neg?cios a engenharia de software de alta performance, "
        "construindo pipelines robustos (SQL/Python), modelos estrela dimensionais (Star Schema/DAX), "
        "dashboards interativos (Next.js/React) e motores de intelig?ncia artificial com RAG (FastAPI/Gemini/DuckDB)."
    ),
    "projetos": (
        "Principais Projetos em Destaque:\n"
        "1. Sales BI & AI Copilot: Dashboard comercial em modelo estrela com OLAP DuckDB em tempo real, "
        "   FastAPI, Google Gemini e interface executiva Next.js (Live: https://sales-bi-ai-copilot.vercel.app).\n"
        "2. Automa??o ETL & Concilia??o Financeira com DRE: Redu??o de 40 horas manuais para 4,8 segundos "
        "   com batimento de 48.700 transa??es banc?rias e gera??o de DRE/EBITDA em tempo real.\n"
        "3. Segmenta??o de Clientes & Preven??o de Churn: Clusteriza??o K-Means (Silhouette 0.68) e RFM em Scikit-Learn, "
        "   com redu??o comprovada de 22,4% no churn de clientes VIPs.\n"
        "4. An?lise de Cesta de Compras (Market Basket): Algoritmo Apriori em 12.800 transa??es de varejo "
        "   gerando regras de associa??o com Lift de at? 5.14x para cross-sell.\n"
        "5. RN Intelligence API: Motor anal?tico multi-tenant que unifica o RAG e o racioc?nio de IA para m?ltiplos projetos."
    ),
    "tech_stack": (
        "Stack Tecnol?gica e Ferramentas:\n"
        "? Linguagens: Python (Avan?ado), SQL (Avan?ado), TypeScript/JavaScript.\n"
        "? Dados & OLAP: DuckDB, PostgreSQL, SQLite, Pandas, Polars, Scikit-Learn.\n"
        "? Backend & IA: FastAPI, Uvicorn, Google Gemini API, RAG Architecture, Pydantic.\n"
        "? Frontend: Next.js 15, React 19, Tailwind CSS, Lucide Icons, Recharts.\n"
        "? BI & Analytics: Modelagem Dimensional Star Schema, DAX, Power BI, Estat?stica Descritiva."
    ),
    "contato": (
        "Canais de Contato e Conex?o:\n"
        "? GitHub: https://github.com/Renanbritto\n"
        "? Email: renan.nocelli@gmail.com\n"
        "? Portf?lio Live: https://renan.dev (ou vercel)"
    )
}

def process_portfolio_query(question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
    q = question.lower()
    
    if any(k in q for k in ["projeto", "projetos", "case", "cases", "trabalho", "experiencia"]):
        reply = (
            "Renan Nocelli desenvolveu projetos de dados de alto impacto combinando engenharia e IA:\n\n"
            "? Sales BI & AI Copilot: Dashboard de vendas com DuckDB real-time e o agente RN Intelligence (https://sales-bi-ai-copilot.vercel.app)\n"
            "? Automa??o Financeira: Pipeline de concilia??o banc?ria autom?tica com DRE e EBITDA (99,8% de acur?cia)\n"
            "? Preven??o de Churn: Segmenta??o K-Means + RFM com -22% de churn em contas VIPs\n"
            "? Market Basket: Minera??o de regras de compra com Apriori e Lift de at? 5.14x\n"
            "? RN Intelligence API: A plataforma centralizada de IA anal?tica que voc? est? usando agora mesmo!"
        )
        return reply, "-- Consulta de portf?lio", []

    elif any(k in q for k in ["stack", "tecnologia", "tecnologias", "ferramenta", "linguagem", "habilidade"]):
        reply = (
            "A stack tecnol?gica principal do Renan ? centrada em dados modernos e engenharia fullstack:\n\n"
            "? Linguagens: Python 3 (FastAPI, Pandas, Scikit-Learn), SQL anal?tico avan?ado e TypeScript\n"
            "? Dados & Bancos: DuckDB, PostgreSQL, SQLite e modelagem Star Schema dimensional\n"
            "? IA & RAG: Arquitetura RAG avan?ada, Google Gemini API, engenharia de prompts anal?ticos\n"
            "? Frontend: Next.js, React e Tailwind CSS para interfaces anal?ticas premium\n"
            "? BI: Power BI, DAX e pipelines de ETL automatizados."
        )
        return reply, "-- Consulta de skills", []

    elif any(k in q for k in ["contato", "email", "github", "linkedin", "falar", "contratar"]):
        reply = (
            "Voc? pode se conectar e conversar diretamente com o Renan atrav?s dos canais:\n\n"
            "? GitHub: https://github.com/Renanbritto\n"
            "? E-mail: renan.nocelli@gmail.com\n"
            "? Foco: Oportunidades em Analytics Engineering, Data Science e Desenvolvimento de Aplica??es de IA."
        )
        return reply, "-- Consulta de contato", []

    else:
        reply = (
            "Ol?! Eu sou o RN Intelligence, o agente de IA que apresenta o portf?lio de Renan Nocelli.\n\n"
            "? Especialidade: Engenheiro de Analytics & Desenvolvedor de IA focado em solu??es de dados de ponta a ponta\n"
            "? Destaques: Projetos com DuckDB, pipelines ETL em Python, modelos preditivos e copilots anal?ticos com Gemini\n"
            "? GitHub: https://github.com/Renanbritto\n"
            "? Como posso ajudar? Voc? pode perguntar sobre os projetos, a stack t?cnica ou casos de neg?cio resolvidos!"
        )
        return reply, "-- Consulta geral", []


class PortfolioAdapter(BaseProjectAdapter):
    @property
    def project_id(self) -> str:
        return "portfolio"

    @property
    def name(self) -> str:
        return "Portf?lio Renan Nocelli"

    @property
    def description(self) -> str:
        return (
            "Agente institucional para apresenta??o profissional de Renan Nocelli, "
            "detalhando compet?ncias em Analytics Engineering, projetos em produ??o e stack t?cnica."
        )

    @property
    def category(self) -> str:
        return "Apresenta??o & Perfil Profissional"

    @property
    def tags(self) -> List[str]:
        return ["Analytics Engineering", "FastAPI", "Python", "DuckDB", "Next.js", "Google Gemini"]

    @property
    def suggested_questions(self) -> List[str]:
        return [
            "Quais s?o os principais projetos desenvolvidos por Renan?",
            "Qual ? a stack de tecnologia e ferramentas que ele domina?",
            "Como funciona a arquitetura do Sales BI com DuckDB?",
            "Quais os canais de contato e links do GitHub?",
            "Qual ? a proposta do RN Intelligence como plataforma?"
        ]

    def get_system_prompt(self) -> str:
        return PORTFOLIO_SYSTEM_PROMPT

    def get_rag_context(self) -> str:
        return "\n\n".join([f"[{k.upper()}]\n{v}" for k, v in PORTFOLIO_KNOWLEDGE.items()])

    def get_schema_context(self) -> str:
        return "Entidades: Perfil, Projetos, Skills, Contato."

    def execute_query(self, query: str, max_rows: int = 100) -> List[Dict[str, Any]]:
        return []

    def resolve_analytical_query(self, question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
        return process_portfolio_query(question)
