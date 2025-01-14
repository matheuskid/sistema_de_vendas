from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import func
from Models.models import Cliente, PaginatedResponse
from database import get_session
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=Cliente, description="Insere um novo cliente no sistema.")
def inserir_cliente(cliente: Cliente, session: Session = Depends(get_session)) -> Cliente:
    try:
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")
    

@router.get("/", response_model=PaginatedResponse[Cliente], description="Lista todos os clientes com paginação")
def listar_clientes(
    page: int = Query(default=1, ge=1, description="Número da página"),
    size: int = Query(default=10, ge=1, le=100, description="Itens por página"),
    session: Session = Depends(get_session)
) -> PaginatedResponse[Cliente]:
    try:
        # Calcula o offset
        offset = (page - 1) * size
        
        # Busca total de registros
        total = session.exec(select(func.count(Cliente.id))).one()
        
        # Busca items da página atual
        query = select(Cliente).offset(offset).limit(size)
        items = session.exec(query).all()
        
        # Verifica se há itens
        if not items:
            print("Nenhum cliente encontrado")  # Debug
        else:
            print(f"Encontrados {len(items)} clientes")  # Debug
        
        # Calcula total de páginas
        pages = -(-total // size)  # Divisão arredondada para cima
        
        # Cria resposta
        response = PaginatedResponse(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
        # Debug
        print(f"Response: {response}")
        
        return response
    
    except Exception as e:
        print(f"Erro ao listar clientes: {e}")  # Debug
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router.get("/{cliente_id}", description="Retorna um cliente existente.")
def listar_clientes(cliente_id: int, session: Session = Depends(get_session)) -> Cliente:
    try:
        cliente = session.get(Cliente, cliente_id)
        return cliente
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router.put("/{cliente_id}", response_model=Cliente, description="Atualiza as informações de um cliente existente.")
def atualizar_cliente(cliente_id: int, cliente_atualizado: Cliente, session: Session = Depends(get_session)) -> Cliente :
    try:
        if cliente_id is None or cliente_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido.")
        
        db_cliente = session.get(Cliente, cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        cliente_data = cliente_atualizado.model_dump(exclude_unset=True)
        db_cliente.sqlmodel_update(cliente_data)
        session.add(db_cliente)
        session.commit()
        session.refresh(db_cliente)
        return {"message": "Cliente atualizado com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

@router.delete("/{cliente_id}", description="Remove um cliente do sistema.")
def deletar_cliente(cliente_id: int, session: Session = Depends(get_session)):
    try:
        if cliente_id is None or cliente_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido.")
        
        cliente = session.get(Cliente, cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        session.delete(cliente)
        session.commit()
        return {"message": "Cliente removido com sucesso"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover cliente: {str(e)}")

@router.get("/quantidade", description="Retorna a quantidade total de clientes cadastrados.")
def quantidade_clientes(session: Session = Depends(get_session)):
    try:
        return {"quantidade": session.exec(select(func.count()).select_from(Cliente)).one()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar clientes: {str(e)}")

@router.get("/clientes_por_estado/{estado}", description="Retorna clientes por estado.")
def quantidade_clientes(estado: str, session: Session = Depends(get_session)) -> list[Cliente]:
    try:
        return session.exec(select(Cliente).where(Cliente.estado.like(estado))).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao retornar clientes: {str(e)}")
        
@router.get("/busca/{nome}", description="Busca clientes por nome parcial")
def buscar_clientes_por_nome(nome: str, session: Session = Depends(get_session)) -> list[Cliente]:
    try:
        return session.exec(select(Cliente).where(Cliente.nome.like(f"%{nome}%"))).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")
