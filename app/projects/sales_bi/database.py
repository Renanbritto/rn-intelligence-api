"""
Provedor de Banco de Dados Anal?tico para o Sales BI.
Dual-Engine: DuckDB (quando dispon?vel) + SQLite (fallback local).
"""
import os
import sqlite3
from decimal import Decimal
from typing import Any, List, Dict
from app.core.security import validate_safe_sql

try:
    import duckdb
except Exception:
    duckdb = None

def get_db_paths() -> tuple[str, str]:
    """Retorna os caminhos dos arquivos duckdb e sqlite."""
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
    duck_path = os.path.join(base, "sales.duckdb")
    sqlite_path = os.path.join(base, "sales.db")
    return duck_path, sqlite_path

def execute_sales_query(query: str, max_rows: int = 100) -> List[Dict[str, Any]]:
    """
    Executa query validada estritamente no DuckDB ou no SQLite.
    """
    validate_safe_sql(query)
    duck_path, sqlite_path = get_db_paths()
    
    # 1. Tenta DuckDB se a lib puder ser carregada
    if duckdb is not None and os.path.exists(duck_path):
        try:
            con = duckdb.connect(duck_path, read_only=True)
            try:
                rel = con.sql(query)
                columns = rel.columns
                rows = rel.fetchall()
                results = []
                for row in rows[:max_rows]:
                    row_dict = {}
                    for col, val in zip(columns, row):
                        if hasattr(val, "isoformat"):
                            row_dict[col] = val.isoformat()
                        elif isinstance(val, Decimal):
                            row_dict[col] = float(val)
                        elif isinstance(val, (int, float, str, bool)) or val is None:
                            row_dict[col] = val
                        else:
                            try:
                                row_dict[col] = float(val)
                            except (ValueError, TypeError):
                                row_dict[col] = str(val)
                    results.append(row_dict)
                return results
            finally:
                con.close()
        except Exception:
            pass

    # 2. Executa no SQLite caso DuckDB n?o esteja dispon?vel no host Windows
    if os.path.exists(sqlite_path):
        con = sqlite3.connect(sqlite_path)
        try:
            cur = con.cursor()
            cur.execute(query)
            columns = [desc[0] for desc in cur.description] if cur.description else []
            rows = cur.fetchall()
            results = []
            for row in rows[:max_rows]:
                row_dict = {}
                for col, val in zip(columns, row):
                    if isinstance(val, (int, float, str, bool)) or val is None:
                        row_dict[col] = val
                    else:
                        try:
                            row_dict[col] = float(val)
                        except (ValueError, TypeError):
                            row_dict[col] = str(val)
                results.append(row_dict)
            return results
        finally:
            con.close()

    # 3. Retorna lista vazia se nenhum banco estiver presente
    return []
