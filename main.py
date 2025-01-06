from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.responses import FileResponse
from Models.models import Cliente, Produto
from sqlmodel import SQLModel, Field, select, Session
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
import os
from Utils.utils import (
    ler_csv, 
    escrever_csv, 
    salvar_no_csv,
    atualizar_csv, 
    remover_do_csv, 
    contar_registros, 
    compactar_csv, 
    calcular_hash,
    validar_objeto
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

router_clientes = APIRouter(prefix="/clientes", tags=["Clientes"])
router_produtos = APIRouter(prefix="/produtos", tags=["Produtos"])

CSV_FILE_CLIENTES = "clientes.csv"
CSV_FILE_PRODUTOS = "produtos.csv"


# Rotas para Clientes
@router_clientes.post("/", response_model=Cliente, description="Insere um novo cliente no sistema.")
def inserir_cliente(cliente: Cliente, session: Session = Depends(get_session)) -> Cliente:
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

@router_clientes.get("/", description="Retorna a lista de todos os clientes cadastrados.")
def listar_clientes(session: Session = Depends(get_session)) -> list[Cliente]:
    try:
        clientes = session.exec(select(Cliente)).all()
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router_clientes.put("/{cliente_id}", response_model=Cliente, description="Atualiza as informações de um cliente existente.")
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

@router_clientes.delete("/{cliente_id}", description="Remove um cliente do sistema.")
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

@router_clientes.get("/quantidade", description="Retorna a quantidade total de clientes cadastrados.")
def quantidade_clientes():
    try:
        return {"quantidade": contar_registros(CSV_FILE_CLIENTES)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar clientes: {str(e)}")

@router_clientes.get("/compactar", description="Compacta o arquivo CSV dos clientes.")
def compactar_cliente_csv():
    try:
        zip_file = compactar_csv(CSV_FILE_CLIENTES)
        return FileResponse(zip_file, media_type="application/zip", filename=os.path.basename(zip_file))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compactar CSV: {str(e)}")

@router_clientes.get("/hash", description="Calcula o hash SHA256 do CSV dos clientes.")
def hash_cliente_csv():
    try:
        return {"hash": calcular_hash(CSV_FILE_CLIENTES)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash: {str(e)}")

# Rotas para Produtos
@router_produtos.post("/", description="Insere um novo produto no sistema.")
def inserir_produto(produto: Produto, session: Session = Depends(get_session)) -> Produto:
    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto

@router_produtos.get("/", description="Retorna a lista de todos os produtos cadastrados.")
def listar_produtos(session: Session = Depends(get_session)) -> list[Produto]:
    try:
        produtos = session.exec(select(Produto)).all()
        return produtos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

@router_produtos.put("/{produto_id}", description="Atualiza as informações de um produto existente.")
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

@router_produtos.delete("/{produto_id}", description="Remove um produto do sistema.")
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

@router_produtos.get("/quantidade", description="Retorna a quantidade total de produtos cadastrados.")
def quantidade_produtos():
    try:
        return {"quantidade": contar_registros(CSV_FILE_PRODUTOS)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar produtos: {str(e)}")

@router_produtos.get("/compactar", description="Compacta o arquivo CSV dos produtos.")
def compactar_produto_csv():
    try:
        zip_file = compactar_csv(CSV_FILE_PRODUTOS)
        return FileResponse(zip_file, media_type="application/zip", filename=os.path.basename(zip_file))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compactar CSV: {str(e)}")

@router_produtos.get("/hash", description="Calcula o hash SHA256 do CSV dos produtos.")
def hash_produto_csv():
    try:
        return {"hash": calcular_hash(CSV_FILE_PRODUTOS)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash: {str(e)}")

# Registrando os routers
app.include_router(router_clientes)
app.include_router(router_produtos)
