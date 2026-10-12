"""
Exce??es customizadas para a RN Intelligence API.
"""

class RNIntelligenceException(Exception):
    """Exce??o base para o ecossistema RN Intelligence."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ProjectNotFoundError(RNIntelligenceException):
    """Lan?ada quando um project_id n?o est? registrado no registry."""
    def __init__(self, project_id: str):
        super().__init__(
            f"Projeto '{project_id}' n?o encontrado no cat?logo do RN Intelligence.",
            status_code=404
        )
        self.project_id = project_id


class SecurityValidationError(RNIntelligenceException):
    """Lan?ada quando uma query SQL cont?m comandos proibidos."""
    def __init__(self, message: str = "Comando SQL n?o autorizado detectado na consulta."):
        super().__init__(message, status_code=403)


class DatabaseExecutionError(RNIntelligenceException):
    """Lan?ada quando ocorre um erro na execu??o da consulta anal?tica."""
    def __init__(self, message: str):
        super().__init__(f"Erro ao executar consulta no banco anal?tico: {message}", status_code=500)
