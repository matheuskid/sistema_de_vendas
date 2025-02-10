from fastapi import FastAPI
from contextlib import asynccontextmanager
from Context.database import create_db_and_tables
from routers import cliente_routes, produto_routes, pedido_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Criar tabelas ao iniciar
    create_db_and_tables()
    yield
    # Limpeza ao encerrar (se necessário)

app = FastAPI(
    title="Sistema de Vendas",
    description="API para gerenciamento de clientes e produtos.",
    version="1.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={    
        "docExpansion": "none",
        "defaultModelsExpandDepth": 0,
        "defaultModelExpandDepth": 0,
    }    
)

@app.get("/", description="Rota inicial com informações da API")
async def root():
    return {
        "message": "Bem-vindo à API do Sistema de Vendas",
        "docs": "/docs",
        "endpoints": {
            "clientes": "/clientes",
            "produtos": "/produtos",
            "pedidos": "/pedidos"
        }
    }

# Registra as rotas
app.include_router(cliente_routes.router)
app.include_router(produto_routes.router)
app.include_router(pedido_routes.router)