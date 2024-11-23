import csv
import hashlib
import zipfile
from typing import List, Type, TypeVar
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, APIRouter
from Models.models import Cliente, Produto
import zipfile
import os

# Definindo um tipo genérico para qualquer classe que herde de BaseModel
T = TypeVar("T", bound=BaseModel)

# Função de validação genérica
def validar_objeto(objeto):
    if objeto is None:
        raise HTTPException(status_code=400, detail="Dados não fornecidos.")
    
    # Valida se algum campo obrigatório está vazio
    for field, value in objeto.dict().items():
        if value is None or (isinstance(value, str) and not value.strip()):
            raise HTTPException(status_code=400, detail=f"O campo '{field}' não pode ser vazio.")


# Função genérica para salvar no CSV
def salvar_no_csv(filename: str, item: Cliente | Produto):
    try:
        registros = ler_csv(filename, item.__class__)  
        last_id = max([registro.id for registro in registros], default=0)
        item.id = last_id + 1  
        escrever_csv(filename, item)
        return {"message": f"{item.__class__.__name__} inserido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir {item.__class__.__name__}: {str(e)}")


def escrever_csv(filename: str, modelo: T):
    # Adiciona um novo objeto do tipo T ao arquivo CSV
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([getattr(modelo, field) for field in modelo.__annotations__])

def ler_csv(filename: str, modelo: Type[T]) -> List[T]:
    objetos = []

    if not os.path.exists(filename):
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Adiciona os campos do modelo como cabeçalhos no CSV
                writer.writerow(modelo.__annotations__.keys())
            print(f"Arquivo '{filename}' criado automaticamente com cabeçalhos.")

    try:
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            headers = next(reader, None)  # Lê a primeira linha como cabeçalho (se houver)
            
            # Verifica se o arquivo está vazio
            if headers is None:
                return objetos  # Retorna uma lista vazia se o arquivo estiver vazio

            # Depuração: Exibir o cabeçalho lido do arquivo CSV e os campos do modelo
            print(f"Cabeçalho do CSV: {headers}")
            print(f"Campos do Modelo: {modelo.__annotations__}")

            # Verifica se o número de colunas no CSV corresponde ao número de campos no modelo
            if len(headers) != len(modelo.__annotations__):
                raise ValueError(f"Número de colunas no CSV ({len(headers)}) não corresponde ao número de campos no modelo ({len(modelo.__annotations__)})")

            # Mapeia as colunas para os campos do modelo
            for row in reader:
                if row:  # Ignora linhas vazias
                    dados = {field: value for field, value in zip(modelo.__annotations__, row)}
                    objetos.append(modelo(**dados))  # Cria uma instância do modelo com os dados
        return objetos
    except Exception as e:
        raise Exception(f"Erro ao ler o arquivo CSV: {str(e)}")


def atualizar_csv(filename: str, id_value: int, modelo: T) -> bool:
    atualizado = False
    linhas = []
    
    # Lê o arquivo CSV
    with open(filename, "r") as file:
        reader = csv.reader(file)
        cabecalho = next(reader, None)  # Lê o cabeçalho (primeira linha)
        if cabecalho:  
            linhas.append(cabecalho)  # Adiciona o cabeçalho na nova lista

        for row in reader:
            if int(row[0]) == id_value:  # Assume que o ID está na primeira coluna
                # Atualiza a linha com os valores do modelo
                linhas.append([getattr(modelo, field) for field in modelo.__annotations__])
                atualizado = True
            else:
                linhas.append(row)
    
    # Reescreve o arquivo CSV, se algo foi atualizado
    if atualizado:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(linhas)
    
    return atualizado



def remover_do_csv(filename: str, id_value: int) -> bool:
    # Remove um objeto do CSV baseado no valor do ID
    removido = False
    linhas = []

    # Lê o arquivo CSV
    with open(filename, "r") as file:
        reader = csv.reader(file)
        cabecalho = next(reader, None)  # Lê o cabeçalho (se houver)
        if cabecalho:
            linhas.append(cabecalho)  # Adiciona o cabeçalho à nova lista

        for row in reader:
            if int(row[0]) != id_value:  # Assume que o ID está na primeira coluna
                linhas.append(row)
            else:
                removido = True

    # Reescreve o arquivo CSV se algo foi removido
    if removido:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(linhas)

    return removido


def contar_registros(filename: str) -> int:
    # Conta o número de registros no arquivo CSV, ignorando o cabeçalho
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Pula o cabeçalho
        return sum(1 for row in reader if row)  # Conta apenas as linhas não vazias


def compactar_csv(filename: str):
    # Compacta o arquivo CSV em um arquivo ZIP
    zip_filename = filename.replace(".csv", ".zip")
    with zipfile.ZipFile(zip_filename, "w") as zf:
        zf.write(filename)
    return zip_filename

def calcular_hash(filename: str) -> str:
    # Calcula o hash SHA256 do arquivo CSV
    sha256 = hashlib.sha256()
    with open(filename, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
