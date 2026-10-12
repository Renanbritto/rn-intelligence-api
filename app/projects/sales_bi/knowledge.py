"""
Base de Conhecimento e Prompts do Sales BI.
"""

SYSTEM_PROMPT = """Voc? ? o RN Intelligence, o agente de intelig?ncia anal?tica e BI corporativo.
Sua miss?o ? responder perguntas executivas com m?xima precis?o sobre qualquer m?trica ou dimens?o do Sales BI.

DIRETRIZES FUNDAMENTAIS DE RESPOSTA:
1. NUNCA ALUCINE DADOS OU N?MEROS. Todas as respostas devem ser fundamentadas rigorosamente nos dados reais da opera??o.
2. Padr?o Estrutural Limpo e Executivo:
   - Primeira frase: Declara??o direta da m?trica principal ou resposta objetiva (sem emojis em t?tulos).
   - Linha em branco.
   - Marcadores com "? " para listar m?tricas complementares (ex: "? Volume de Pedidos: 13.236 transa??es faturadas").
   - Ponto de aten??o ou a??o recomendada breve ao final quando pertinente.
3. N?O USE ASTERISCOS DUPLOS (**) nos textos ou listas. Mantenha o texto limpo e direto.
4. Formata??o monet?ria: R$ 1.234.567,89 (padr?o brasileiro).
5. Percentuais: com duas casas decimais (ex: 43,05%).
"""

BI_KNOWLEDGE_BASE = {
    "kpis": (
        "O painel possui 4 cards executivos principais no topo: "
        "1. Faturamento L?quido (R$ 39.035.677,55, com crescimento de +18,4% YoY). "
        "2. Margem de Contribui??o (43,05% / R$ 16.806.501,55 brutos frente ? meta de 40,0%). "
        "3. Volume de Pedidos (13.236 pedidos faturados de 40 clientes corporativos ativos). "
        "4. Ticket M?dio (R$ 2.949,21 por pedido, superando a meta global em 477%)."
    ),
    "briefing": (
        "O Briefing Executivo Di?rio destaca 3 pilares estrat?gicos: "
        "1. Alavanca de Receita: Forte tra??o no canal B2B Enterprise (R$ 16,4M) e Regional Sudeste (50,4% do share). "
        "2. Risco de Margem: Concess?o m?dia de descontos no canal Canais & Parceiros (12,4%), reduzindo a margem para 38,6%, al?m de produtos de Hardware com margem estreita (15-18%). "
        "3. A??o Recomendada: Foco na expans?o da Su?te de Governan?a nos 40 clientes ativos e teto de desconto de 7,5% em parceiros."
    ),
    "what_if": (
        "O Simulador What-If permite modelar cen?rios projetados alterando vari?veis de pre?o, volume e custos a partir da base real de R$ 39,0M em faturamento e 43,0% de margem."
    ),
    "produtos": (
        "O portf?lio possui 8 produtos divididos na Curva ABC e Matriz BCG: "
        "- Classe A: Enterprise Analytics Platform (SKU-902), Cloud Migration (SKU-814), Data Warehouse Dedicated Node (SKU-772) e Executive Analytics Templates (SKU-650). "
        "- Classe B: ETL Connector Hub (SKU-504) e Consultoria em Governan?a (SKU-441). "
        "- Classe C: Servidor On-Premise Rack 2U (SKU-312) e Switches Gigabit (SKU-205). "
        "Maior margem: Executive Analytics Templates (68%). Maior receita: Enterprise Analytics Platform."
    ),
    "vendedores": (
        "A equipe de vendas conta com 5 profissionais com quotas anuais e mensais: "
        "1. Beatriz Silveira (Sudeste) - Top 1 em faturamento (R$ 11.025.331,32, 3.677 pedidos). "
        "2. Carlos Eduardo Mendes (Sul) - Top 2 (R$ 9.513.715,81, 3.294 pedidos). "
        "3. Mariana Albuquerque (Sudeste) - Top 3 (R$ 8.499.922,64, 2.870 pedidos). "
        "4. Lucas Fontes (Nordeste) - Top 4 (R$ 5.535.406,77, 1.924 pedidos). "
        "5. Fernanda Rocha (Centro-Oeste) - Top 5 (R$ 4.461.301,01, 1.471 pedidos)."
    ),
    "canais": (
        "4 canais comerciais: "
        "1. B2B Enterprise (Direto): R$ 16,4M, ticket R$ 3.353, margem 44,2%. "
        "2. E-commerce Direto (Digital): R$ 11,7M, ticket R$ 2.708, margem 42,8%. "
        "3. Grandes Contas (Direto): R$ 6,25M, ticket R$ 3.511, margem 45,0%. "
        "4. Canais & Parceiros (Indireto): R$ 4,68M, desconto 12,4%, margem 38,6%."
    ),
    "regioes": (
        "Desempenho Geogr?fico: "
        "- Sudeste: 50,4% do faturamento (R$ 19,68M, 6.630 pedidos, 14 clientes). "
        "- Sul: 24,2% do faturamento (R$ 9,45M, 3.180 pedidos, 10 clientes). "
        "- Nordeste: 14,9% do faturamento (R$ 5,82M, 1.980 pedidos, 9 clientes). "
        "- Centro-Oeste: 10,5% do faturamento (R$ 4,08M, 1.446 pedidos, 7 clientes)."
    ),
    "clientes": (
        "Base de 40 clientes corporativos ativos distribu?dos em 6 segmentos: "
        "Tecnologia (R$ 9,85M), Financeiro (R$ 8,40M), Ind?stria (R$ 7,20M), Varejo (R$ 6,10M), Sa?de (R$ 4,50M) e Log?stica (R$ 2,98M). "
        "Top clientes: Nexus Solu??es Digitais (R$ 1,85M) e Titanium Seguros (R$ 1,68M)."
    ),
    "funil": (
        "Funil de Vendas Corporativo (B2B Pipeline): 14.200 leads MQL (R$ 48,5M), 5.200 SQL (R$ 26,2M), "
        "2.450 propostas (R$ 16,4M), 1.480 em negocia??o (R$ 11,8M), 890 contratos fechados (R$ 8,95M). "
        "Taxa de convers?o global MQL -> Contrato de 6,27%."
    )
}

SCHEMA_CONTEXT = """
### TABELAS E ESTRUTURA DIMENSIONAL (MODELO ESTRELA):
- **d_calendario**: data_id (INT, YYYYMMDD), data (DATE), ano (INT), mes (INT), nome_mes (VARCHAR), trimestre (INT), dia_semana (INT)
- **d_produtos**: produto_id (INT), nome_produto (VARCHAR), categoria (VARCHAR), classe_abc (VARCHAR: A, B ou C), preco_unitario (DECIMAL), custo_unitario (DECIMAL)
- **d_vendedores**: vendedor_id (INT), nome_vendedor (VARCHAR), regional (VARCHAR), cargo (VARCHAR), status (VARCHAR)
- **d_clientes**: cliente_id (INT), razao_social (VARCHAR), segmento (VARCHAR), porte (VARCHAR), estado (VARCHAR), regiao (VARCHAR)
- **d_canais**: canal_id (INT), nome_canal (VARCHAR), tipo_canal (VARCHAR)
- **f_metas**: meta_id (INT), ano (INT), mes (INT), vendedor_id (INT), meta_faturamento (DECIMAL), meta_margem_pct (DECIMAL)
- **f_vendas**: venda_id (BIGINT), numero_pedido (VARCHAR), data_id (INT), produto_id (INT), vendedor_id (INT), cliente_id (INT), canal_id (INT), quantidade (INT), valor_liquido (DECIMAL), custo_total (DECIMAL), margem_contribuicao_valor (DECIMAL), margem_contribuicao_pct (DECIMAL), status_pedido (VARCHAR: 'Faturado', 'Cancelado', 'Devolvido')

### REGRAS ANAL?TICAS PRINCIPAIS:
1. Sempre filtre status_pedido = 'Faturado' para c?lculo de faturamento e margem real.
2. Faturamento L?quido = SUM(valor_liquido).
3. Margem de Contribui??o Valor = SUM(margem_contribuicao_valor).
4. Margem de Contribui??o % = (SUM(margem_contribuicao_valor) / SUM(valor_liquido)) * 100.
5. Ticket M?dio = SUM(valor_liquido) / COUNT(DISTINCT numero_pedido).
"""
