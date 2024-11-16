import csv
import hashlib
import zipfile
from typing import List, Type, TypeVar
from pydantic import BaseModel

# Definindo um tipo genérico para qualquer classe que herde de BaseModel
T = TypeVar("T", bound=BaseModel)

def escrever_csv(filename: str, modelo: T):
    # Adiciona um novo objeto do tipo T ao arquivo CSV
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([getattr(modelo, field) for field in modelo.__annotations__])

def ler_csv(filename: str, modelo: Type[T]) -> List[T]:
    objetos = []
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


def atualizar_csv(filename: str, id_field: str, id_value: int, modelo: T) -> bool:
    # Atualiza um objeto do tipo T no CSV baseado no valor do id_field
    atualizado = False
    linhas = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[0]) == id_value:  # Assume que o ID está na primeira coluna
                linhas.append([getattr(modelo, field) for field in modelo.__annotations__])
                atualizado = True
            else:
                linhas.append(row)
    
    if atualizado:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(linhas)
    return atualizado

def remover_do_csv(filename: str, id_field: str, id_value: int) -> bool:
    # Remove um objeto do tipo T do CSV baseado no valor do id_field
    removido = False
    linhas = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if int(row[0]) != id_value:  # Assume que o ID está na primeira coluna
                linhas.append(row)
            else:
                removido = True
    
    if removido:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(linhas)
    return removido

def contar_registros(filename: str) -> int:
    # Conta o número de registros no arquivo CSV
    with open(filename, "r") as file:
        return sum(1 for row in csv.reader(file) if row)

def compactar_csv(filename: str):
    # Compacta o arquivo CSV em um arquivo ZIP
    zip_filename = filename.replace(".csv", ".zip")
    with zipfile.ZipFile(zip_filename, "w") as zf:
        zf.write(filename)

def calcular_hash(filename: str) -> str:
    # Calcula o hash SHA256 do arquivo CSV
    sha256 = hashlib.sha256()
    with open(filename, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
