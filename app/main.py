"""
Ponto de entrada da aplica??o FastAPI RN Intelligence API.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import main_api_router
from app.registry.project_registry import registry

# Adaptadores de projeto
from app.projects.sales_bi.adapter import SalesBIAdapter
from app.projects.financial_automation.adapter import FinancialAutomationAdapter
from app.projects.customer_churn.adapter import CustomerChurnAdapter
from app.projects.portfolio.adapter import PortfolioAdapter

def register_default_adapters():
    """Garante registro idempotente dos adaptadores padr?o."""
    adapters = [
        SalesBIAdapter(),
        FinancialAutomationAdapter(),
        CustomerChurnAdapter(),
        PortfolioAdapter()
    ]
    for a in adapters:
        registry.register(a)

# Registra os adaptadores no carregamento da aplica??o
register_default_adapters()

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_default_adapters()
    active_count = len(registry.list_projects())
    print(f"[RN Intelligence] {active_count} projetos anal?ticos online!")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Motor anal?tico centralizado de intelig?ncia artificial com RAG multi-tenant.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_api_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
        "active_projects": [p.project_id for p in registry.list_projects()]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
