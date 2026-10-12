"""
Camada de Seguran?a e Valida??o de Queries Anal?ticas (Safe SQL Execution).
"""
import re
from app.core.exceptions import SecurityValidationError

FORBIDDEN_SQL_KEYWORDS = [
    r"\bDROP\b",
    r"\bDELETE\b",
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bALTER\b",
    r"\bATTACH\b",
    r"\bDETACH\b",
    r"\bCOPY\s+TO\b",
    r"\bEXPORT\s+DATABASE\b",
    r"\bPRAGMA\b",
    r"\bCREATE\b",
    r"\bREPLACE\b",
    r"\bTRUNCATE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
]

def validate_safe_sql(query: str) -> None:
    """
    Valida se uma consulta SQL ? estritamente de leitura (SELECT, WITH, DESCRIBE, EXPLAIN).
    Levanta SecurityValidationError se detectar comandos proibidos ou DDL/DML de escrita.
    """
    cleaned = query.strip()
    if not cleaned:
        raise SecurityValidationError("A consulta SQL n?o pode ser vazia.")
    
    # Remove coment?rios de linha (-- ...) e de bloco (/* ... */)
    normalized = re.sub(r"--.*?$", "", cleaned, flags=re.MULTILINE)
    normalized = re.sub(r"/\*.*?\*/", "", normalized, flags=re.DOTALL).strip()
    
    # Deve come?ar com opera??es de leitura
    if not normalized.upper().startswith(("SELECT", "WITH", "DESCRIBE", "EXPLAIN")):
        raise SecurityValidationError("Apenas consultas de leitura (SELECT, WITH, DESCRIBE, EXPLAIN) s?o permitidas.")
    
    # Procura palavras-chave de risco
    for pattern in FORBIDDEN_SQL_KEYWORDS:
        if re.search(pattern, normalized, re.IGNORECASE):
            raise SecurityValidationError("Comando SQL n?o autorizado ou de escrita detectado na consulta.")
