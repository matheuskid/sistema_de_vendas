from fastapi import FastAPI, HTTPException
from Models.models import Cliente, Produto
from Utils.utils import (
    ler_csv, 
    escrever_csv, 
    atualizar_csv, 
    remover_do_csv, 
    contar_registros, 
    compactar_csv, 
    calcular_hash
)

app = FastAPI()
CSV_FILE_CLIENTES = "clientes.csv"
CSV_FILE_PRODUTOS = "produtos.csv"

# Função genérica para salvar no CSV
def salvar_no_csv(filename: str, item: Cliente | Produto):
    try:
        # Verifica o último id e incrementa
        registros = ler_csv(filename, item.__class__)  # Lê todos os registros
        last_id = max([registro.id for registro in registros], default=0)  # Pega o último ID
        item.id = last_id + 1  # Atribui um novo id
       
        escrever_csv(filename, item)  # Salva no CSV
        return {"message": f"{item.__class__.__name__} inserido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir {item.__class__.__name__}: {str(e)}")
    
    

# F1: Inserir cliente
@app.post("/clientes/", description="Insere um novo cliente no sistema.")
def inserir_cliente(cliente: Cliente):
    return salvar_no_csv(CSV_FILE_CLIENTES, cliente)

# F2: Retornar todos os clientes
@app.get("/clientes/", description="Retorna a lista de todos os clientes cadastrados.")
def listar_clientes():
    try:
        return ler_csv(CSV_FILE_CLIENTES, Cliente)  # Passa a classe Cliente como modelo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

# F3: Atualizar cliente
@app.put("/clientes/{cliente_id}", description="Atualiza as informações de um cliente existente.")
def atualizar_cliente(cliente_id: int, cliente: Cliente):
    try:
        atualizado = atualizar_csv(CSV_FILE_CLIENTES, cliente_id, cliente)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"message": "Cliente atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

# F4: Remover cliente
@app.delete("/clientes/{cliente_id}", description="Remove um cliente do sistema.")
def deletar_cliente(cliente_id: int):
    try:
        removido = remover_do_csv(CSV_FILE_CLIENTES, cliente_id)
        if not removido:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"message": "Cliente removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover cliente: {str(e)}")

# F5: Quantidade de clientes
@app.get("/clientes/quantidade", description="Retorna a quantidade total de clientes cadastrados.")
def quantidade_clientes():
    try:
        return {"quantidade": contar_registros(CSV_FILE_CLIENTES)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar clientes: {str(e)}")

# F6: Compactar CSV
@app.get("/clientes/compactar", description="Compacta o arquivo CSV que contém os dados dos clientes.")
def compactar_cliente_csv():
    try:
        compactar_csv(CSV_FILE_CLIENTES)
        return {"message": "Arquivo CSV compactado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compactar arquivo CSV: {str(e)}")

# F7: Calcular Hash SHA256
@app.get("/clientes/hash", description="Calcula o hash SHA256 do arquivo CSV dos clientes.")
def hash_cliente_csv():
    try:
        return {"hash": calcular_hash(CSV_FILE_CLIENTES)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash do CSV: {str(e)}")

# Endpoints para Produtos (usando as mesmas funções)
@app.post("/produtos/", description="Insere um novo produto no sistema.")
def inserir_produto(produto: Produto):
    return salvar_no_csv(CSV_FILE_PRODUTOS, produto)

@app.get("/produtos/", description="Retorna a lista de todos os produtos cadastrados.")
def listar_produtos():
    try:
        return ler_csv(CSV_FILE_PRODUTOS)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

@app.put("/produtos/{produto_id}", description="Atualiza as informações de um produto existente.")
def atualizar_produto(produto_id: int, produto: Produto):
    try:
        atualizado = atualizar_csv(CSV_FILE_PRODUTOS, produto_id, produto)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"message": "Produto atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar produto: {str(e)}")

@app.delete("/produtos/{produto_id}", description="Remove um produto do sistema.")
def deletar_produto(produto_id: int):
    try:
        removido = remover_do_csv(CSV_FILE_PRODUTOS, produto_id)
        if not removido:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"message": "Produto removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao remover produto: {str(e)}")

@app.get("/produtos/quantidade", description="Retorna a quantidade total de produtos cadastrados.")
def quantidade_produtos():
    try:
        return {"quantidade": contar_registros(CSV_FILE_PRODUTOS)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao contar produtos: {str(e)}")

@app.get("/produtos/compactar", description="Compacta o arquivo CSV que contém os dados dos produtos.")
def compactar_produto_csv():
    try:
        compactar_csv(CSV_FILE_PRODUTOS)
        return {"message": "Arquivo CSV compactado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao compactar arquivo CSV: {str(e)}")

@app.get("/produtos/hash", description="Calcula o hash SHA256 do arquivo CSV dos produtos.")
def hash_produto_csv():
    try:
        return {"hash": calcular_hash(CSV_FILE_PRODUTOS)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular hash do CSV: {str(e)}")
