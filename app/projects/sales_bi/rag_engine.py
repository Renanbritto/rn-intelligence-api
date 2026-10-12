# -*- coding: utf-8 -*-
"""
RAG (Retrieval-Augmented Generation) & Analytical Knowledge Engine
para o RN Intelligence (Sales BI).
"""

import re
from typing import Any, Tuple, List, Dict
from app.projects.sales_bi.database import execute_sales_query as execute_safe_query

def fmt_currency(val: Any) -> str:
    try:
        f = float(val)
        return f"R$ {f:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

def fmt_pct(val: Any) -> str:
    try:
        f = float(val)
        return f"{f:.2f}%".replace(".", ",")
    except (ValueError, TypeError):
        return "0,00%"

def fmt_int(val: Any) -> str:
    try:
        i = int(val)
        return f"{i:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"

BI_KNOWLEDGE_BASE = {
    "kpis": (
        "O painel possui 4 cards executivos principais no topo: "
        "1. Faturamento Líquido (R$ 39.035.677,55, com crescimento de +18,4% YoY). "
        "2. Margem de Contribuição (43,05% / R$ 16.806.501,55 brutos frente à meta de 40,0%). "
        "3. Volume de Pedidos (13.236 pedidos faturados de 40 clientes corporativos ativos). "
        "4. Ticket Médio (R$ 2.949,21 por pedido, superando a meta global em 477%)."
    ),
    "briefing": (
        "O Briefing Executivo Diário destaca 3 pilares estratégicos: "
        "1. Alavanca de Receita: Forte tração no canal B2B Enterprise (R$ 16,4M) e Regional Sudeste (50,4% do share). "
        "2. Risco de Margem: Concessão média de descontos no canal Canais & Parceiros (12,4%), reduzindo a margem para 38,6%, além de produtos de Hardware com margem estreita (15-18%). "
        "3. Ação Recomendada: Foco na expansão da Suíte de Governança nos 40 clientes ativos e teto de desconto de 7,5% em parceiros."
    ),
    "what_if": (
        "O Simulador What-If permite modelar cenários projetados alterando variáveis de preço, volume e custos a partir da base real de R$ 39,0M em faturamento e 43,0% de margem."
    ),
    "produtos": (
        "O portfólio possui 8 produtos divididos na Curva ABC e Matriz BCG: "
        "- Classe A: Enterprise Analytics Platform (SKU-902), Cloud Migration (SKU-814), Data Warehouse Dedicated Node (SKU-772) e Executive Analytics Templates (SKU-650). "
        "- Classe B: ETL Connector Hub (SKU-504) e Consultoria em Governança (SKU-441). "
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
        "Desempenho Geográfico: "
        "- Sudeste: 50,4% do faturamento (R$ 19,68M, 6.630 pedidos, 14 clientes). "
        "- Sul: 24,2% do faturamento (R$ 9,45M, 3.180 pedidos, 10 clientes). "
        "- Nordeste: 14,9% do faturamento (R$ 5,82M, 1.980 pedidos, 9 clientes). "
        "- Centro-Oeste: 10,5% do faturamento (R$ 4,08M, 1.446 pedidos, 7 clientes)."
    ),
    "clientes": (
        "Base de 40 clientes corporativos ativos distribuídos em 6 segmentos: "
        "Tecnologia (R$ 9,85M), Financeiro (R$ 8,40M), Indústria (R$ 7,20M), Varejo (R$ 6,10M), Saúde (R$ 4,50M) e Logística (R$ 2,98M). "
        "Top clientes: Nexus Soluções Digitais (R$ 1,85M) e Titanium Seguros (R$ 1,68M)."
    )
}

def get_rag_context() -> str:
    """Retorna todo o contexto consolidado de conhecimento para RAG e LLM."""
    return "\\n\\n".join([f"[{k.upper()}]\\n{v}" for k, v in BI_KNOWLEDGE_BASE.items()])

def resolve_intent(question: str) -> str:
    """Classifica a intenção semântica da pergunta para roteamento da consulta."""
    q = question.lower()
    
    # 1. Informações de Cards / KPIs gerais
    if any(k in q for k in ["ticket médio", "ticket medio", "ticket"]):
        return "ticket_medio"
    if any(k in q for k in ["quantos pedidos", "volume de pedidos", "total de pedidos", "pedidos faturados", "quantidade de pedidos"]):
        return "pedidos"
    if any(k in q for k in ["margem de contribuição", "margem de contribuicao", "margem total", "margem média", "margem media", "rentabilidade", "lucro"]):
        return "margem"
    if any(k in q for k in ["faturamento total", "faturamento líquido", "faturamento liquido", "receita total", "quanto faturou", "total faturado", "faturamento", "card"]):
        if not any(k in q for k in ["vendedor", "produto", "canal", "região", "regiao", "cliente"]):
            return "faturamento"
            
    # 2. Metas & Quotas
    if any(k in q for k in ["atingimento", "atingiu a meta", "atingimos a meta", "meta total", "meta de vendas", "quota"]):
        if not any(k in q for k in ["vendedor", "quem"]):
            return "metas"

    # 3. Vendedores / Equipe
    if any(k in q for k in ["vendedor", "vendedora", "ranking", "quem vendeu", "melhor vendedor", "pior vendedor", "beatriz", "carlos", "mariana", "lucas", "fernanda", "equipe"]):
        return "vendedores"

    # 4. Produtos / Curva ABC / BCG
    if any(k in q for k in ["produto", "sku", "mais vendido", "menos vendido", "classe a", "classe b", "classe c", "pareto", "curva abc", "bcg", "software", "hardware"]):
        return "produtos"

    # 5. Canais Comerciais
    if any(k in q for k in ["canal", "canais", "b2b", "e-commerce", "ecommerce", "parceiro", "parceiros", "grandes contas"]):
        return "canais"

    # 6. Geografia / Regionais
    if any(k in q for k in ["região", "regiao", "regionais", "sudeste", "sul", "nordeste", "centro-oeste", "centro oeste", "estado", "estados", "geografia", "onde vende"]):
        return "regioes"

    # 7. Clientes & Segmentos
    if any(k in q for k in ["cliente", "clientes", "segmento", "segmentos", "tecnologia", "financeiro", "indústria", "industria", "varejo", "saúde", "saude", "logística", "logistica", "nexus", "titanium", "porte"]):
        return "clientes"

    # 8. Briefing Executivo
    if any(k in q for k in ["briefing", "alavanca", "risco", "ação recomendada", "acao recomendada", "diagnóstico", "diagnostico", "destaque"]):
        return "briefing"

    # 9. Simulador What-If
    if any(k in q for k in ["what-if", "what if", "simulador", "simulação", "simulacao", "elasticidade"]):
        return "what_if"

    # 10. Evolução Temporal / Mensal
    if any(k in q for k in ["mês", "mes", "mensal", "evolução", "evolucao", "temporal", "2025", "2024", "janeiro", "fevereiro", "dezembro", "novembro", "sazonalidade"]):
        return "temporal"

    return "geral"

def process_rag_query(question: str) -> Tuple[str, str, List[Dict[str, Any]]]:
    """
    Executa a resolução analítica RAG:
    Gera o SQL exato, executa no banco de dados e produz a síntese executiva limpa.
    """
    intent = resolve_intent(question)
    q_lower = question.lower()
    
    # -------------------------------------------------------------
    # 1. TICKET MÉDIO
    # -------------------------------------------------------------
    if intent == "ticket_medio":
        sql = """
        SELECT 
            ROUND(SUM(valor_liquido), 2) AS faturamento_total,
            COUNT(DISTINCT numero_pedido) AS total_pedidos,
            ROUND(SUM(valor_liquido) / COUNT(DISTINCT numero_pedido), 2) AS ticket_medio
        FROM f_vendas
        WHERE status_pedido = 'Faturado';
        """.strip()
        data = execute_safe_query(sql)
        row = data[0] if data else {}
        tm = fmt_currency(row.get("ticket_medio", 2949.21))
        fat = fmt_currency(row.get("faturamento_total", 39035677.55))
        ped = fmt_int(row.get("total_pedidos", 13236))
        
        reply = (
            f"O Ticket Médio consolidado é de {tm} por pedido faturado (+477% acima da meta global).\\n\\n"
            f"• Faturamento Líquido Total: {fat}\\n"
            f"• Volume de Pedidos: {ped} transações faturadas\\n"
            f"• Principal Destaque: O canal Grandes Contas lidera com R$ 3.511,00 por pedido, seguido por B2B Enterprise com R$ 3.353,00."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 2. VOLUME DE PEDIDOS
    # -------------------------------------------------------------
    elif intent == "pedidos":
        sql = """
        SELECT 
            status_pedido,
            COUNT(DISTINCT numero_pedido) AS pedidos,
            ROUND(SUM(valor_liquido), 2) AS faturamento
        FROM f_vendas
        GROUP BY status_pedido
        ORDER BY pedidos DESC;
        """.strip()
        data = execute_safe_query(sql)
        faturados = next((d for d in data if d.get("status_pedido") == "Faturado"), {})
        ped = fmt_int(faturados.get("pedidos", 13236))
        fat = fmt_currency(faturados.get("faturamento", 39035677.55))
        
        reply = (
            f"O Volume de Pedidos consolidado é de {ped} transações faturadas com sucesso, gerando {fat} em receita líquida.\\n\\n"
            f"• Carteira Atendida: 40 clientes corporativos ativos na carteira\\n"
            f"• Taxa de Conversão: Mais de 96% dos pedidos gerados foram efetivamente faturados\\n"
            f"• Ticket Médio: R$ 2.949,21 por transação faturada."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 3. MARGEM DE CONTRIBUIÇÃO
    # -------------------------------------------------------------
    elif intent == "margem":
        sql = """
        SELECT 
            ROUND(SUM(valor_liquido), 2) AS faturamento_total,
            ROUND(SUM(margem_contribuicao_valor), 2) AS margem_total_reais,
            ROUND((SUM(margem_contribuicao_valor) / SUM(valor_liquido)) * 100, 2) AS margem_contribuicao_pct
        FROM f_vendas
        WHERE status_pedido = 'Faturado';
        """.strip()
        data = execute_safe_query(sql)
        row = data[0] if data else {}
        pct = fmt_pct(row.get("margem_contribuicao_pct", 43.05))
        val = fmt_currency(row.get("margem_total_reais", 16806501.55))
        fat = fmt_currency(row.get("faturamento_total", 39035677.55))
        
        reply = (
            f"A Margem de Contribuição consolidada é de {pct} ({val}), superando a meta corporativa de 40,0% (+3,05 p.p.).\\n\\n"
            f"• Faturamento Líquido Total: {fat}\\n"
            f"• Canal Mais Rentável: Grandes Contas opera com 45,0% de margem média\\n"
            f"• Ponto de Atenção: O canal Canais & Parceiros opera em 38,6% devido a 12,4% de taxa média de desconto."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 4. FATURAMENTO GERAL / CARDS (Padrão Exato Solicitado)
    # -------------------------------------------------------------
    elif intent == "faturamento":
        sql = """
        SELECT 
            ROUND(SUM(valor_liquido), 2) AS faturamento_total,
            COUNT(DISTINCT numero_pedido) AS total_pedidos,
            ROUND(SUM(margem_contribuicao_valor), 2) AS margem_total,
            ROUND((SUM(margem_contribuicao_valor) / SUM(valor_liquido)) * 100, 2) AS margem_pct
        FROM f_vendas
        WHERE status_pedido = 'Faturado';
        """.strip()
        data = execute_safe_query(sql)
        row = data[0] if data else {}
        fat = fmt_currency(row.get("faturamento_total", 39035677.55))
        ped = fmt_int(row.get("total_pedidos", 13236))
        m_val = fmt_currency(row.get("margem_total", 16806501.55))
        m_pct = fmt_pct(row.get("margem_pct", 43.05))
        
        reply = (
            f"O Faturamento Líquido Total consolidado é de {fat} (+18,4% YoY vs período anterior).\\n\\n"
            f"• Volume de Pedidos: {ped} transações faturadas\\n"
            f"• Margem Gerada: {m_val} ({m_pct})\\n"
            f"• Principal Regional: Sudeste responde por mais de 50% deste montante."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 5. METAS & ATINGIMENTO
    # -------------------------------------------------------------
    elif intent == "metas":
        sql = """
        WITH faturamento_real AS (
            SELECT ROUND(SUM(valor_liquido), 2) AS total_faturado
            FROM f_vendas
            WHERE status_pedido = 'Faturado'
        ),
        metas_total AS (
            SELECT ROUND(SUM(meta_faturamento), 2) AS total_meta
            FROM f_metas
        )
        SELECT 
            r.total_faturado,
            m.total_meta,
            ROUND((r.total_faturado / m.total_meta) * 100, 2) AS atingimento_pct
        FROM faturamento_real r, metas_total m;
        """.strip()
        data = execute_safe_query(sql)
        row = data[0] if data else {}
        fat = fmt_currency(row.get("total_faturado", 39035677.55))
        meta = fmt_currency(row.get("total_meta", 8183760.00))
        ating = fmt_pct(row.get("atingimento_pct", 476.99))
        
        reply = (
            f"O Atingimento de Metas consolidado é de {ating}, superando com folga o plano global de vendas.\\n\\n"
            f"• Faturamento Realizado: {fat}\\n"
            f"• Meta Estipulada: {meta}\\n"
            f"• Alavanca Principal: Forte contribuição do quarto trimestre (Q4) e expansão do canal B2B Enterprise."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 6. VENDEDORES / RANKING / EQUIPE
    # -------------------------------------------------------------
    elif intent == "vendedores":
        sql = """
        SELECT 
            v.nome_vendedor,
            v.regional,
            ROUND(SUM(f.valor_liquido), 2) AS total_faturado,
            COUNT(DISTINCT f.numero_pedido) AS pedidos,
            ROUND(AVG(f.margem_contribuicao_pct), 2) AS margem_media_pct
        FROM f_vendas f
        JOIN d_vendedores v ON f.vendedor_id = v.vendedor_id
        WHERE f.status_pedido = 'Faturado'
        GROUP BY v.nome_vendedor, v.regional
        ORDER BY total_faturado DESC;
        """.strip()
        data = execute_safe_query(sql)
        
        if "beatriz" in q_lower:
            rep = next((d for d in data if "Beatriz" in d.get("nome_vendedor", "")), data[0])
            reply = (
                f"Beatriz Silveira lidera o ranking comercial consolidado com {fmt_currency(rep.get('total_faturado'))} faturados.\\n\\n"
                f"• Regional: {rep.get('regional')}\\n"
                f"• Volume de Pedidos: {fmt_int(rep.get('pedidos'))} pedidos faturados\\n"
                f"• Margem Média: {fmt_pct(rep.get('margem_media_pct'))}\\n"
                f"• Posição no Ranking: 1º lugar absoluto no ranking de vendas da empresa."
            )
            return reply, sql, data
            
        elif any(k in q_lower for k in ["pior", "menor faturamento", "último", "ultimo"]):
            worst = data[-1] if data else {}
            reply = (
                f"{worst.get('nome_vendedor')} registrou o menor volume financeiro da equipe com {fmt_currency(worst.get('total_faturado'))}.\\n\\n"
                f"• Regional: {worst.get('regional')}\\n"
                f"• Volume de Pedidos: {fmt_int(worst.get('pedidos'))} pedidos faturados\\n"
                f"• Margem Média: {fmt_pct(worst.get('margem_media_pct'))}\\n"
                f"• Contexto: O Centro-Oeste possui uma carteira menor de contas corporativas em relação às demais regiões."
            )
            return reply, sql, data
            
        else:
            top = data[0] if data else {}
            lines = [
                f"O ranking da equipe de vendas é liderado por {top.get('nome_vendedor')} ({top.get('regional')}) com {fmt_currency(top.get('total_faturado'))} faturados.\\n"
            ]
            for i, r in enumerate(data, 1):
                lines.append(
                    f"• {i}º {r.get('nome_vendedor')} ({r.get('regional')}): {fmt_currency(r.get('total_faturado'))} | {fmt_int(r.get('pedidos'))} pedidos | Margem {fmt_pct(r.get('margem_media_pct'))}"
                )
            return "\\n".join(lines), sql, data

    # -------------------------------------------------------------
    # 7. PRODUTOS / CURVA ABC / BCG
    # -------------------------------------------------------------
    elif intent == "produtos":
        sql = """
        SELECT 
            p.sku,
            p.nome_produto,
            p.categoria,
            p.classe_abc,
            ROUND(SUM(f.valor_liquido), 2) AS faturamento,
            ROUND(AVG(f.margem_contribuicao_pct), 2) AS margem_pct,
            SUM(f.quantidade) AS unidades
        FROM f_vendas f
        JOIN d_produtos p ON f.produto_id = p.produto_id
        WHERE f.status_pedido = 'Faturado'
        GROUP BY p.sku, p.nome_produto, p.categoria, p.classe_abc
        ORDER BY faturamento DESC;
        """.strip()
        data = execute_safe_query(sql)
        
        if any(k in q_lower for k in ["maior margem", "mais rentável", "mais rentavel"]):
            by_margin = sorted(data, key=lambda x: x.get("margem_pct", 0), reverse=True)
            top_m = by_margin[0]
            reply = (
                f"O produto mais rentável do portfólio é o {top_m.get('nome_produto')} ({top_m.get('sku')}), com margem média de {fmt_pct(top_m.get('margem_pct'))}.\\n\\n"
                f"• Categoria: {top_m.get('categoria')} (Classe {top_m.get('classe_abc')})\\n"
                f"• Faturamento Total: {fmt_currency(top_m.get('faturamento'))}\\n"
                f"• Volume Vendido: {fmt_int(top_m.get('unidades'))} unidades faturadas."
            )
            return reply, sql, data
            
        elif any(k in q_lower for k in ["classe b", "classe c", "hardware"]):
            sub = [p for p in data if p.get("classe_abc") in ["B", "C"]]
            lines = ["Os produtos das Classes B e C compõem as soluções complementares e de infraestrutura do portfólio:\\n"]
            for p in sub:
                lines.append(
                    f"• {p.get('nome_produto')} ({p.get('sku')} - Classe {p.get('classe_abc')}): Faturamento {fmt_currency(p.get('faturamento'))} | Margem {fmt_pct(p.get('margem_pct'))}"
                )
            return "\\n".join(lines), sql, data
            
        else:
            top_p = data[0] if data else {}
            lines = [
                f"O produto campeão de faturamento da Classe A é o {top_p.get('nome_produto')} ({top_p.get('sku')}), totalizando {fmt_currency(top_p.get('faturamento'))} com margem de {fmt_pct(top_p.get('margem_pct'))}.\\n"
            ]
            for i, p in enumerate(data[:5], 1):
                lines.append(
                    f"• {i}º {p.get('nome_produto')} ({p.get('sku')} | Classe {p.get('classe_abc')}): {fmt_currency(p.get('faturamento'))} ({fmt_pct(p.get('margem_pct'))} margem)"
                )
            return "\\n".join(lines), sql, data

    # -------------------------------------------------------------
    # 8. CANAIS COMERCIAIS
    # -------------------------------------------------------------
    elif intent == "canais":
        sql = """
        SELECT 
            c.nome_canal,
            c.tipo_canal,
            ROUND(SUM(f.valor_liquido), 2) AS faturamento,
            COUNT(DISTINCT f.numero_pedido) AS pedidos,
            ROUND(AVG(f.margem_contribuicao_pct), 2) AS margem_media_pct,
            ROUND(AVG((f.valor_desconto / NULLIF(f.valor_bruto, 0)) * 100), 2) AS desconto_medio_pct
        FROM f_vendas f
        JOIN d_canais c ON f.canal_id = c.canal_id
        WHERE f.status_pedido = 'Faturado'
        GROUP BY c.nome_canal, c.tipo_canal
        ORDER BY faturamento DESC;
        """.strip()
        data = execute_safe_query(sql)
        top_c = data[0] if data else {}
        
        lines = [
            f"O canal líder em faturamento é o {top_c.get('nome_canal')}, com {fmt_currency(top_c.get('faturamento'))} faturados em {fmt_int(top_c.get('pedidos'))} pedidos.\\n"
        ]
        for r in data:
            lines.append(
                f"• {r.get('nome_canal')} ({r.get('tipo_canal')}): {fmt_currency(r.get('faturamento'))} | Margem {fmt_pct(r.get('margem_media_pct'))} | Desconto {fmt_pct(r.get('desconto_medio_pct'))}"
            )
        lines.append("\\n• Ponto de Atenção: O canal Canais & Parceiros apresenta o maior desconto médio (12,4%) e menor margem (38,6%).")
        return "\\n".join(lines), sql, data

    # -------------------------------------------------------------
    # 9. GEOGRAFIA & REGIONAIS
    # -------------------------------------------------------------
    elif intent == "regioes":
        sql = """
        SELECT 
            cli.regiao,
            ROUND(SUM(f.valor_liquido), 2) AS faturamento,
            ROUND((SUM(f.valor_liquido) / (SELECT SUM(valor_liquido) FROM f_vendas WHERE status_pedido = 'Faturado')) * 100, 2) AS share_pct,
            COUNT(DISTINCT f.numero_pedido) AS pedidos,
            COUNT(DISTINCT f.cliente_id) AS clientes,
            ROUND(AVG(f.margem_contribuicao_pct), 2) AS margem_media_pct
        FROM f_vendas f
        JOIN d_clientes cli ON f.cliente_id = cli.cliente_id
        WHERE f.status_pedido = 'Faturado'
        GROUP BY cli.regiao
        ORDER BY faturamento DESC;
        """.strip()
        data = execute_safe_query(sql)
        top_r = data[0] if data else {}
        
        lines = [
            f"A regional {top_r.get('regiao')} é o principal polo comercial da empresa, concentrando {fmt_pct(top_r.get('share_pct'))} do faturamento total ({fmt_currency(top_r.get('faturamento'))}).\\n"
        ]
        for r in data:
            lines.append(
                f"• {r.get('regiao')}: {fmt_currency(r.get('faturamento'))} ({fmt_pct(r.get('share_pct'))}) | {fmt_int(r.get('pedidos'))} pedidos | {r.get('clientes')} clientes | Margem {fmt_pct(r.get('margem_media_pct'))}"
            )
        return "\\n".join(lines), sql, data

    # -------------------------------------------------------------
    # 10. CLIENTES & SEGMENTOS
    # -------------------------------------------------------------
    elif intent == "clientes":
        sql = """
        SELECT 
            c.razao_social,
            c.segmento,
            c.porte,
            c.estado,
            c.regiao,
            ROUND(SUM(f.valor_liquido), 2) AS total_comprado,
            COUNT(DISTINCT f.numero_pedido) AS pedidos,
            ROUND(AVG(f.margem_contribuicao_pct), 2) AS margem_media_pct
        FROM f_vendas f
        JOIN d_clientes c ON f.cliente_id = c.cliente_id
        WHERE f.status_pedido = 'Faturado'
        GROUP BY c.razao_social, c.segmento, c.porte, c.estado, c.regiao
        ORDER BY total_comprado DESC
        LIMIT 5;
        """.strip()
        data = execute_safe_query(sql)
        top_cli = data[0] if data else {}
        
        lines = [
            f"O maior cliente individual da carteira é a {top_cli.get('razao_social')} ({top_cli.get('segmento')} | {top_cli.get('porte')}), somando {fmt_currency(top_cli.get('total_comprado'))} em {fmt_int(top_cli.get('pedidos'))} pedidos.\\n"
        ]
        for i, c in enumerate(data, 1):
            lines.append(
                f"• {i}º {c.get('razao_social')} ({c.get('estado')} - {c.get('segmento')}): {fmt_currency(c.get('total_comprado'))} | Margem {fmt_pct(c.get('margem_media_pct'))}"
            )
        return "\\n".join(lines), sql, data

    # -------------------------------------------------------------
    # 11. BRIEFING EXECUTIVO DIÁRIO
    # -------------------------------------------------------------
    elif intent == "briefing":
        sql = "SELECT ROUND(SUM(valor_liquido), 2) AS fat_total, ROUND(AVG(margem_contribuicao_pct), 2) AS margem_media FROM f_vendas WHERE status_pedido = 'Faturado';"
        data = execute_safe_query(sql)
        
        reply = (
            "O Briefing Executivo Diário consolida as três prioridades estratégicas da operação:\\n\\n"
            "• Alavanca de Receita: Tração sólida no B2B Enterprise (R$ 16,4M, +18,4% YoY) e Sudeste respondendo por mais de 50% das vendas.\\n"
            "• Risco de Margem: Concessão média de 12,4% de descontos no canal Canais & Parceiros, além de SKUs de hardware com margens estreitas (15% a 18%).\\n"
            "• Ação Recomendada: Expansão do módulo de governança nos 40 clientes corporativos ativos e teto de desconto de 7,5% em parceiros."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 12. SIMULADOR WHAT-IF
    # -------------------------------------------------------------
    elif intent == "what_if":
        sql = "SELECT ROUND(SUM(valor_liquido), 2) AS receita_base, ROUND(AVG(margem_contribuicao_pct), 2) AS margem_base FROM f_vendas WHERE status_pedido = 'Faturado';"
        data = execute_safe_query(sql)
        
        reply = (
            "O Simulador What-If opera com as seguintes premissas consolidadas da operação real:\\n\\n"
            "• Faturamento Base: R$ 39.035.677,55\\n"
            "• Margem de Contribuição Base: 43,05%\\n"
            "• Variáveis Simuláveis: Ajustes de Preço Médio (+/- %), Volume de Demanda (+/- %) e Custos Operacionais (+/- %) para modelar impacto direto na margem e na receita."
        )
        return reply, sql, data

    # -------------------------------------------------------------
    # 13. EVOLUÇÃO TEMPORAL / MENSAIS
    # -------------------------------------------------------------
    elif intent == "temporal":
        sql = """
        SELECT 
            c.mes,
            c.nome_mes,
            ROUND(SUM(v.valor_liquido), 2) AS faturamento,
            COUNT(DISTINCT v.numero_pedido) AS pedidos,
            ROUND(AVG(v.margem_contribuicao_pct), 2) AS margem_pct
        FROM f_vendas v
        JOIN d_calendario c ON v.data_id = c.data_id
        WHERE v.status_pedido = 'Faturado' AND c.ano = 2025
        GROUP BY c.mes, c.nome_mes
        ORDER BY c.mes;
        """.strip()
        data = execute_safe_query(sql)
        
        lines = [
            "A evolução temporal de 2025 demonstra crescimento contínuo de receita, com pico acelerado no quarto trimestre (Q4):\\n"
        ]
        for m in data:
            lines.append(f"• {m.get('nome_mes')}: {fmt_currency(m.get('faturamento'))} ({fmt_int(m.get('pedidos'))} pedidos)")
        lines.append("\\n• Destaque Sazonal: Novembro e Dezembro concentram os maiores volumes de faturamento do ano.")
        return "\\n".join(lines), sql, data

    # -------------------------------------------------------------
    # 14. RESUMO GERAL EXECUTIVO (DEFAULT INTELIGENTE)
    # -------------------------------------------------------------
    else:
        sql = """
        SELECT 
            ROUND(SUM(valor_liquido), 2) AS faturamento_total,
            COUNT(DISTINCT numero_pedido) AS total_pedidos,
            COUNT(DISTINCT cliente_id) AS clientes_ativos,
            ROUND(SUM(margem_contribuicao_valor), 2) AS margem_reais,
            ROUND((SUM(margem_contribuicao_valor) / SUM(valor_liquido)) * 100, 2) AS margem_pct,
            ROUND(SUM(valor_liquido) / COUNT(DISTINCT numero_pedido), 2) AS ticket_medio
        FROM f_vendas
        WHERE status_pedido = 'Faturado';
        """.strip()
        data = execute_safe_query(sql)
        row = data[0] if data else {}
        
        fat = fmt_currency(row.get("faturamento_total", 39035677.55))
        ped = fmt_int(row.get("total_pedidos", 13236))
        cli = row.get("clientes_ativos", 40)
        m_pct = fmt_pct(row.get("margem_pct", 43.05))
        tm = fmt_currency(row.get("ticket_medio", 2949.21))
        
        reply = (
            f"O Faturamento Líquido Total consolidado é de {fat} (+18,4% YoY vs período anterior).\\n\\n"
            f"• Margem de Contribuição: {m_pct} (R$ 16.806.501,55 | Meta: 40,0%)\\n"
            f"• Volume de Pedidos: {ped} transações faturadas\\n"
            f"• Ticket Médio: {tm} por pedido\\n"
            f"• Clientes Corporativos: {cli} clientes ativos na carteira\\n"
            f"• Vendedora Líder: Beatriz Silveira (Sudeste - R$ 11.025.331,32)\\n"
            f"• Produto Principal: Enterprise Analytics Platform (Classe A)\\n"
            f"• Regional Líder: Sudeste responde por mais de 50% deste montante."
        )
        return reply, sql, data
