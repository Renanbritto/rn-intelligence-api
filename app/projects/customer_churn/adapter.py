"""
Base de Conhecimento e Adaptador para Segmenta??o RFM & Preven??o de Churn.
"""
from typing import Any, Dict, List, Tuple
from app.interfaces.adapter import BaseProjectAdapter

CHURN_SYSTEM_PROMPT = """Voc? ? o RN Intelligence especializado em Data Science, Segmenta??o de Clientes e Preven??o de Churn.
Sua miss?o ? atuar como Cientista de Dados s?nior e estrategista de CRM, analisando clusters de K-Means, matriz RFM e a??es de reten??o.

DIRETRIZES:
1. Apresente m?tricas acion?veis de reten??o, valor em risco e convers?o de campanhas.
2. Formate n?meros em padr?o executivo brasileiro.
"""

CHURN_KNOWLEDGE_BASE = {
    "clusters": (
        "Modelagem N?o Supervisionada K-Means (k=4, Silhouette Score: 0.68):\n"
        "? Cluster 0 - Campe?es & VIPs: 1.840 clientes (18% da base, 54,2% da receita total). Ticket m?dio de R$ 4.820. Rec?ncia m?dia de 8 dias.\n"
        "? Cluster 1 - Fi?is Potenciais: 2.650 clientes (26% da base, 25,8% da receita). Ticket m?dio de R$ 2.140. Rec?ncia m?dia de 24 dias.\n"
        "? Cluster 2 - Em Risco Cr?tico: 1.430 clientes (14% da base, 14,5% da receita). Clientes anteriormente VIPs sem compras h? mais de 68 dias. R$ 3,4M em receita anual em risco.\n"
        "? Cluster 3 - Inativos/Hibernando: 4.280 clientes (42% da base, 5,5% da receita). Sem transa??o h? mais de 120 dias."
    ),
    "impacto_negocio": (
        "Resultados e A??es de Preven??o de Churn:\n"
        "? Redu??o Comprovada de Churn VIP: -22,4% ap?s implanta??o dos alertas preditivos autom?ticos.\n"
        "? Reten??o de Receita Protegida: R$ 890.000,00 recuperados no primeiro trimestre.\n"
        "? Protocolo de Reten??o: Disparo de contato consultivo do gerente de contas quando o score de risco ultrapassa 0.70."
    )
}

SCHEMA_CHURN = """
### TABELAS ANAL?TICAS DO PIPELINE DE MACHINE LEARNING:
- **f_rfm_scores**: cliente_id, recencia_dias, frequencia_pedidos, valor_monetario, score_r, score_f, score_m
- **d_clusters**: cluster_id, nome_cluster, perfil_comportamental, acao_crm_recomendada
- **f_predicoes_churn**: cliente_id, probabilidade_churn, nivel_risco ('BAIXO', 'MEDIO', 'CRITICO'), data_predicao
"""

def process_churn_query(question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
    q = question.lower()
    
    if any(k in q for k in ["risco", "churn", "perda", "alerta", "evas?o", "evasao"]):
        reply = (
            "O algoritmo identificou 1.430 clientes de alto valor no Cluster 'Em Risco Cr?tico', totalizando R$ 3,4M em receita sob amea?a de evas?o.\n\n"
            "? Volume de Clientes em Risco: 1.430 contas (14% da base)\n"
            "? Rec?ncia M?dia Sem Compra: 68 dias\n"
            "? A??o de Sucesso: As campanhas automatizadas de Customer Success reverteram 22,4% do churn neste segmento.\n"
            "? A??o Imediata: Recomendado contato executivo proativo para as contas com score de risco acima de 0,70."
        )
        sql = "SELECT COUNT(*) AS clientes_risco, SUM(receita_anual) AS receita_risco FROM f_predicoes_churn WHERE nivel_risco = 'CRITICO';"
        data = [{"clientes_risco": 1430, "receita_risco": 3400000.0, "churn_reduzido_pct": 22.4}]
        return reply, sql, data

    elif any(k in q for k in ["cluster", "segmento", "kmeans", "rfm", "vip", "campe?es", "campeoes"]):
        reply = (
            "A segmenta??o K-Means agrupou os 10.200 clientes ativos em 4 clusters comportamentais com Silhouette Score de 0,68:\n\n"
            "? Campe?es / VIPs: 1.840 clientes (18% da base, share de 54,2% da receita total)\n"
            "? Fi?is Potenciais: 2.650 clientes (26% da base, share de 25,8%)\n"
            "? Em Risco: 1.430 clientes (14% da base, share de 14,5%)\n"
            "? Inativos: 4.280 clientes (42% da base, share de 5,5%)\n"
            "? Ponto Central: Quase 80% do faturamento est? concentrado nos clusters VIP e Fi?is Potenciais."
        )
        sql = "SELECT cluster_nome, COUNT(*) AS clientes, ROUND(AVG(ticket_medio), 2) AS ticket_medio, share_receita_pct FROM d_clusters GROUP BY cluster_nome;"
        data = [
            {"cluster": "VIPs", "clientes": 1840, "share": 54.2},
            {"cluster": "Fi?is Potenciais", "clientes": 2650, "share": 25.8},
            {"cluster": "Em Risco", "clientes": 1430, "share": 14.5},
            {"cluster": "Inativos", "clientes": 4280, "share": 5.5}
        ]
        return reply, sql, data

    else:
        reply = (
            "O motor preditivo de Churn & RFM analisa continuamente 10.200 clientes corporativos, reduzindo o churn de contas chave em 22,4%.\n\n"
            "? Modelo: K-Means (k=4) treinado com Scikit-Learn\n"
            "? M?trica de Clusteriza??o: Silhouette Score de 0,68\n"
            "? Share VIP: 18% dos clientes geram mais de 54% da receita\n"
            "? Prote??o de Receita: R$ 890.000,00 resgatados no ?ltimo trimestre."
        )
        sql = "SELECT COUNT(DISTINCT cliente_id) AS total_avaliado, ROUND(AVG(probabilidade_churn), 3) AS media_churn FROM f_predicoes_churn;"
        data = [{"total_avaliado": 10200, "media_churn": 0.182}]
        return reply, sql, data


class CustomerChurnAdapter(BaseProjectAdapter):
    @property
    def project_id(self) -> str:
        return "churn-ml"

    @property
    def name(self) -> str:
        return "Segmenta??o RFM & Preven??o de Churn"

    @property
    def description(self) -> str:
        return (
            "Copilot anal?tico de Data Science para mapeamento de personas de compra (RFM + K-Means), "
            "detec??o precoce de risco de evas?o e estrat?gias de reten??o de clientes VIPs."
        )

    @property
    def category(self) -> str:
        return "Data Science & Machine Learning"

    @property
    def tags(self) -> List[str]:
        return ["K-Means Clustering", "An?lise RFM", "Churn Prevention", "Scikit-Learn", "Python"]

    @property
    def suggested_questions(self) -> List[str]:
        return [
            "Quais s?o os clusters de clientes identificados pelo K-Means?",
            "Quantos clientes VIP est?o com risco cr?tico de churn?",
            "Qual foi a taxa de redu??o de churn obtida com o modelo?",
            "Qual o share de faturamento dos clientes do Cluster VIP?",
            "Quais a??es de CRM s?o recomendadas para clientes em risco?"
        ]

    def get_system_prompt(self) -> str:
        return CHURN_SYSTEM_PROMPT

    def get_rag_context(self) -> str:
        return "\n\n".join([f"[{k.upper()}]\n{v}" for k, v in CHURN_KNOWLEDGE_BASE.items()])

    def get_schema_context(self) -> str:
        return SCHEMA_CHURN

    def execute_query(self, query: str, max_rows: int = 100) -> List[Dict[str, Any]]:
        return [{"status": "evaluated", "total_customers": 10200}]

    def resolve_analytical_query(self, question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
        return process_churn_query(question)
