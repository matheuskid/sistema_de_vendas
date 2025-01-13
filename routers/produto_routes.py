from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import func
from Models.models import Produto, PaginatedResponse
from database import get_session
from typing import List

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", description="Insere um novo produto no sistema.")
def inserir_produto(produto: Produto, session: Session = Depends(get_session)) -> Produto:
    try:
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")

# Rota paginada para Produtos
@router.get("/", response_model=PaginatedResponse[Produto], description="Lista todos os produtos com paginação")
def listar_produtos(
    page: int = Query(default=1, ge=1, description="Número da página"),
    size: int = Query(default=10, ge=1, le=100, description="Itens por página"),
    session: Session = Depends(get_session)
) -> PaginatedResponse[Produto]:
    try:
        offset = (page - 1) * size
        total = session.exec(select(func.count(Produto.id))).one()
        
        items = session.exec(
            select(Produto)
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
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")
    
@router.get("/{produto_id}", description="Retorna um produto existente.")
def listar_clientes(produto_id: int, session: Session = Depends(get_session)) -> Produto:
    try:
        produto = session.get(Produto, produto_id)
        return produto
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router.put("/{produto_id}", description="Atualiza as informações de um produto existente.")
def atualizar_produto(produto_id: int, produto_atualizado: Produto, session: Session = Depends(get_session)) -> Produto :
    try:
        if produto_id is None or produto_id <= 0:
            raise HTTPException(status_code=400, detail="ID do produto inválido.")
        
        db_produto = session.get(Cliente, produto_id)
        if not db_produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        produto_data = produto_atualizado.model_dump(exclude_unset=True)
        db_produto.sqlmodel_update(produto_data)
        session.add(db_produto)
        session.commit()
        session.refresh(db_produto)
        return {"message": "Produto atualizado com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover produto: {str(e)}")

@router.delete("/{produto_id}", description="Remove um produto do sistema.")
def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
    try:
        if produto_id is None or produto_id <= 0:
            raise HTTPException(status_code=400, detail="ID do produto inválido.")
        
        produto = session.get(Produto, produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        session.delete(produto)
        session.commit()
        return {"message": "Produto removido com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover produto: {str(e)}")

@router.get("/quantidade", description="Retorna a quantidade total de produtos cadastrados.")
def quantidade_produtos(session: Session = Depends(get_session)):
    try:
        return {"quantidade": session.exec(select(func.count()).select_from(Produto)).one()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar produtos: {str(e)}")
    
@router.get("/categoria_qtd/{categoria}", description="Retorna a quantidade de produtos por categoria.")
def quantidade_clientes(categoria: str, session: Session = Depends(get_session)):
    try:
        return {"quantidade": session.exec(select(func.count()).select_from(Produto).where(Produto.categoria == categoria)).one()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar produtos por categoria: {str(e)}")

@router.get("/preco_maior_que/{preco}", description="Lista produtos com preço maior que o valor especificado")
def listar_produtos_por_preco(preco: float, session: Session = Depends(get_session)) -> list[Produto]:
    try:
        return session.exec(select(Produto).where(Produto.preco > preco)).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")




