"""
Base de Conhecimento, Regras Cont?beis e Adaptador para Automa??o Financeira & DRE.
"""
import re
from typing import Any, Dict, List, Tuple
from app.interfaces.adapter import BaseProjectAdapter

FINANCIAL_SYSTEM_PROMPT = """Voc? ? o RN Intelligence para Finan?as Corporativas.
Sua miss?o ? atuar como CFO / Controller anal?tico s?nior, respondendo d?vidas sobre DRE Gerencial, concilia??o banc?ria, EBITDA, margens operacionais e fluxo de caixa.

DIRETRIZES:
1. Rigor cont?bil e num?rico absoluto.
2. Estruture as respostas com clareza executiva:
   - Resposta direta com o valor principal.
   - Detalhamento de contas cont?beis e varia??es percentuais.
   - A??o financeira ou alerta de caixa/despesa.
3. Formate moeda como R$ 1.234.567,89 e percentuais com duas casas decimais (ex: 28,40%).
"""

FINANCIAL_KNOWLEDGE_BASE = {
    "dre": (
        "DRE Gerencial Consolidada (Exerc?cio Anual):\n"
        "? Receita Bruta: R$ 52.480.000,00\n"
        "? Dedu??es e Impostos sobre Venda (18,2%): R$ 9.551.360,00\n"
        "? Receita Operacional L?quida (ROL): R$ 42.928.640,00\n"
        "? Custo dos Servi?os/Produtos Vendidos (CPV/CSP): R$ 22.322.892,80 (52,0% da ROL)\n"
        "? Lucro Bruto: R$ 20.605.747,20 (Margem Bruta de 48,00%)\n"
        "? Despesas Operacionais (OPEX): R$ 8.585.728,00 (SG&A: R$ 4,8M | P&D: R$ 2,2M | Gerais: R$ 1,58M)\n"
        "? EBITDA / LAJIDA: R$ 12.020.019,20 (Margem EBITDA de 28,00%)\n"
        "? Deprecia??o e Amortiza??o: R$ 1.287.859,20\n"
        "? EBIT / LAJIR: R$ 10.732.160,00 (Margem Operacional de 25,00%)\n"
        "? Resultado Financeiro L?quido: -R$ 858.572,80\n"
        "? Lucro L?quido do Exerc?cio: R$ 6.516.567,36 (Margem L?quida de 15,18%)."
    ),
    "conciliacao": (
        "Painel de Concilia??o Banc?ria Automatizada:\n"
        "? Volume Total de Transa??es Processadas: 48.720 lan?amentos/m?s\n"
        "? Taxa de Concilia??o Autom?tica no Primeiro Batimento (Straight-Through): 99,82%\n"
        "? Tempo M?dio de Execu??o do Pipeline ETL: 4,8 segundos por arquivo CNAB/OFX\n"
        "? Diverg?ncias Identificadas em Quarentena: 88 lan?amentos (0,18% do volume)\n"
        "? Principais Motivos de Diverg?ncia: Varia??o de tarifa banc?ria n?o provisionada e centavos de juros/multa."
    ),
    "fluxo_caixa": (
        "Vis?o de Fluxo de Caixa e Capital de Giro:\n"
        "? Saldo de Caixa Dispon?vel: R$ 7.840.000,00\n"
        "? Prazo M?dio de Recebimento (PMR): 38 dias\n"
        "? Prazo M?dio de Pagamento (PMP): 45 dias\n"
        "? Ciclo Financeiro: -7 dias (opera??o financiada por fornecedores favor?vel ? liquidez)\n"
        "? ?ndice de Liquidez Corrente: 1,84 (saud?vel, acima de 1,5)."
    )
}

SCHEMA_FINANCIAL = """
### TABELAS FINANCEIRAS E PLANO DE CONTAS:
- **d_plano_contas**: conta_id, codigo_contabil, nome_conta, tipo_conta ('RECEITA', 'CUSTO', 'DESPESA', 'IMPOSTO')
- **d_bancos**: banco_id, codigo_bacen, nome_banco, agencia, conta_corrente
- **f_lancamentos_contabeis**: lancamento_id, data_id, conta_id, valor, debito_credito, historico
- **f_conciliacao_bancaria**: conciliacao_id, data_id, transacao_id, valor_extrato, valor_erp, status ('CONCILIADO', 'DIVERGENTE')
"""

def process_financial_query(question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
    q = question.lower()
    
    if any(k in q for k in ["ebitda", "lajida", "margem operacional", "lucro operacional"]):
        reply = (
            "O EBITDA consolidado do exerc?cio ? de R$ 12.020.019,20, representando uma Margem EBITDA de 28,00% sobre a Receita L?quida.\n\n"
            "? Receita L?quida (ROL): R$ 42.928.640,00\n"
            "? Lucro Bruto: R$ 20.605.747,20 (48,00%)\n"
            "? Total OPEX: R$ 8.585.728,00\n"
            "? Ponto Focal: A opera??o mant?m alta efici?ncia operacional, superando o benchmark setorial de 24% de margem EBITDA."
        )
        sql = "SELECT SUM(receita_liquida) AS rol, SUM(lucro_bruto) AS lb, SUM(ebitda) AS ebitda FROM f_dre_mensal;"
        data = [{"rol": 42928640.0, "lucro_bruto": 20605747.2, "ebitda": 12020019.2, "margem_ebitda_pct": 28.0}]
        return reply, sql, data

    elif any(k in q for k in ["concilia??o", "conciliacao", "diverg?ncia", "divergencia", "extrato", "cnab"]):
        reply = (
            "O pipeline de concilia??o banc?ria autom?tica opera com taxa de acerto de 99,82% em mais de 48.700 transa??es mensais.\n\n"
            "? Transa??es Conciliadas: 48.632 itens (99,82%)\n"
            "? Itens em Quarentena/Diverg?ncia: 88 lan?amentos (0,18%)\n"
            "? Tempo M?dio de Processamento: 4,8 segundos por lote\n"
            "? Status: Fechamento di?rio realizado sem atraso ou necessidade de confer?ncia manual de extratos."
        )
        sql = "SELECT status, COUNT(*) AS qtd, ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct FROM f_conciliacao GROUP BY status;"
        data = [{"status": "CONCILIADO", "qtd": 48632, "pct": 99.82}, {"status": "DIVERGENTE", "qtd": 88, "pct": 0.18}]
        return reply, sql, data

    elif any(k in q for k in ["lucro l?quido", "lucro liquido", "resultado l?quido", "resultado liquido"]):
        reply = (
            "O Lucro L?quido consolidado ? de R$ 6.516.567,36, atingindo uma Margem L?quida de 15,18% sobre a Receita Operacional L?quida.\n\n"
            "? Receita Operacional L?quida: R$ 42.928.640,00\n"
            "? Custo dos Servi?os (CPV): R$ 22.322.892,80\n"
            "? Despesas Financeiras L?quidas: -R$ 858.572,80\n"
            "? Al?quota Efetiva de IRPJ/CSLL: 34,00% sobre o LAIR."
        )
        sql = "SELECT lucro_liquido, margem_liquida_pct FROM f_dre_anual WHERE ano = 2025;"
        data = [{"lucro_liquido": 6516567.36, "margem_liquida_pct": 15.18}]
        return reply, sql, data

    else:
        # Default DRE Completa
        reply = (
            "A Demonstra??o do Resultado do Exerc?cio (DRE Gerencial) aponta Receita L?quida de R$ 42.928.640,00 e EBITDA de R$ 12.020.019,20 (28,00%).\n\n"
            "? Receita Bruta: R$ 52.480.000,00\n"
            "? Margem Bruta: 48,00% (R$ 20.605.747,20)\n"
            "? EBITDA: R$ 12.020.019,20 (28,00% de margem)\n"
            "? Lucro L?quido: R$ 6.516.567,36 (15,18% de margem)\n"
            "? Efici?ncia de Concilia??o: 99,82% dos extratos conciliados sem interven??o manual."
        )
        sql = "SELECT receita_bruta, receita_liquida, ebitda, lucro_liquido FROM f_dre_consolidada;"
        data = [{"receita_bruta": 52480000.0, "receita_liquida": 42928640.0, "ebitda": 12020019.2, "lucro_liquido": 6516567.36}]
        return reply, sql, data


class FinancialAutomationAdapter(BaseProjectAdapter):
    @property
    def project_id(self) -> str:
        return "automacao-financeira"

    @property
    def name(self) -> str:
        return "Automa??o Financeira & DRE"

    @property
    def description(self) -> str:
        return (
            "Copilot anal?tico de finan?as corporativas cobrindo DRE Gerencial, concilia??o banc?ria, "
            "EBITDA, margem operacional, fluxo de caixa e gest?o de despesas."
        )

    @property
    def category(self) -> str:
        return "Finan?as Corporativas"

    @property
    def tags(self) -> List[str]:
        return ["DRE Cont?bil", "EBITDA", "Concilia??o Banc?ria", "Fluxo de Caixa", "Python ETL"]

    @property
    def suggested_questions(self) -> List[str]:
        return [
            "Qual ? o EBITDA consolidado e a margem EBITDA?",
            "Qual o status da concilia??o banc?ria e diverg?ncias?",
            "Apresente o resumo completo da DRE gerencial.",
            "Qual ? o lucro l?quido e a margem l?quida?",
            "Qual o prazo m?dio de recebimento e ciclo financeiro?"
        ]

    def get_system_prompt(self) -> str:
        return FINANCIAL_SYSTEM_PROMPT

    def get_rag_context(self) -> str:
        return "\n\n".join([f"[{k.upper()}]\n{v}" for k, v in FINANCIAL_KNOWLEDGE_BASE.items()])

    def get_schema_context(self) -> str:
        return SCHEMA_FINANCIAL

    def execute_query(self, query: str, max_rows: int = 100) -> List[Dict[str, Any]]:
        # Por padr?o retorna o mock estruturado se n?o houver banco financeiro isolado
        return [{"status": "success", "rows_analyzed": 48720}]

    def resolve_analytical_query(self, question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
        return process_financial_query(question)
