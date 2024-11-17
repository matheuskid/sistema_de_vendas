from fastapi import FastAPI, HTTPException, APIRouter
from Models.models import Cliente, Produto
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

app = FastAPI()
router_clientes = APIRouter(prefix="/clientes", tags=["Clientes"])
router_produtos = APIRouter(prefix="/produtos", tags=["Produtos"])

CSV_FILE_CLIENTES = "clientes.csv"
CSV_FILE_PRODUTOS = "produtos.csv"


# Rotas para Clientes
@router_clientes.post("/", description="Insere um novo cliente no sistema.")
def inserir_cliente(cliente: Cliente):
    validar_objeto(cliente)
    return salvar_no_csv(CSV_FILE_CLIENTES, cliente)

@router_clientes.get("/", description="Retorna a lista de todos os clientes cadastrados.")
def listar_clientes():
    try:
        return ler_csv(CSV_FILE_CLIENTES, Cliente)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@router_clientes.put("/{cliente_id}", description="Atualiza as informações de um cliente existente.")
def atualizar_cliente(cliente_id: int, cliente: Cliente):
    validar_objeto(cliente)
    try:
        if cliente_id is None or cliente_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido.")
        
        atualizado = atualizar_csv(CSV_FILE_CLIENTES, cliente_id, cliente)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"message": "Cliente atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

@router_clientes.delete("/{cliente_id}", description="Remove um cliente do sistema.")
def deletar_cliente(cliente_id: int):
    try:
        if cliente_id is None or cliente_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido.")
        
        removido = remover_do_csv(CSV_FILE_CLIENTES, cliente_id)
        if not removido:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
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
        compactar_csv(CSV_FILE_CLIENTES)
        return {"message": "Arquivo CSV compactado"}
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
def inserir_produto(produto: Produto):
    validar_objeto(produto)
    return salvar_no_csv(CSV_FILE_PRODUTOS, produto)

@router_produtos.get("/", description="Retorna a lista de todos os produtos cadastrados.")
def listar_produtos():
    try:
        return ler_csv(CSV_FILE_PRODUTOS, Produto)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

@router_produtos.put("/{produto_id}", description="Atualiza as informações de um produto existente.")
def atualizar_produto(produto_id: int, produto: Produto):
    validar_objeto(produto)
    try:
        if produto_id is None or produto_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido.")
        
        atualizado = atualizar_csv(CSV_FILE_PRODUTOS, produto_id, produto)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"message": "Produto atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")

@router_produtos.delete("/{produto_id}", description="Remove um produto do sistema.")
def deletar_produto(produto_id: int):
    try:
        if produto_id is None or produto_id <= 0:
            raise HTTPException(status_code=400, detail="ID do cliente inválido.")
        
        removido = remover_do_csv(CSV_FILE_PRODUTOS, produto_id)
        if not removido:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
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
        compactar_csv(CSV_FILE_PRODUTOS)
        return {"message": "Arquivo CSV compactado"}
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
