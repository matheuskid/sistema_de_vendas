from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import func
from Models.models import Pedido, PaginatedResponse
from database import get_session
from typing import List

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=Pedido, description="Cria um novo pedido")
def criar_pedido(pedido: Pedido, session: Session = Depends(get_session)) -> Pedido:
    try:
        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")

# Rota paginada para Pedidos
@router.get("/", response_model=PaginatedResponse[Pedido], description="Lista todos os pedidos com paginação")
def listar_pedidos(
    page: int = Query(default=1, ge=1, description="Número da página"),
    size: int = Query(default=10, ge=1, le=100, description="Itens por página"),
    session: Session = Depends(get_session)
) -> PaginatedResponse[Pedido]:
    try:
        offset = (page - 1) * size
        total = session.exec(select(func.count(Pedido.id))).one()
        
        items = session.exec(
            select(Pedido)
            .offset(offset)
            .limit(size)
        ).all()
        
        pages = -(-total // size)
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")

@router.get("/cliente/{cliente_id}", description="Lista pedidos de um cliente específico")
def listar_pedidos_cliente(cliente_id: int, session: Session = Depends(get_session)) -> list[Pedido]:
    try:
        return session.exec(select(Pedido).where(Pedido.cliente_id == cliente_id)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")

@router.get("/data/{data}", description="Lista pedidos por data")
def listar_pedidos_por_data(data: str, session: Session = Depends(get_session)) -> list[Pedido]:
    try:
        data_pedido = datetime.strptime(data, "%Y-%m-%d").date()
        return session.exec(select(Pedido).where(func.date(Pedido.data_pedido) == data_pedido)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {str(e)}")
