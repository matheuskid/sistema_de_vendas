from typing import Union
from typing import List
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()


class Cliente(BaseModel):
    id: int
    nome: str
    sexo: str
    endereco: str
    email: str
    telefone: str



def to_dataframe(cliente: Cliente):
    return pd.DataFrame({"id": [cliente.id],
                        "nome": [cliente.nome],
                        "sexo": [cliente.sexo],
                        "endereco": [cliente.endereco],
                        "email": [cliente.email],
                        "telefone": [cliente.telefone]})


clientes = pd.read_csv('clientes.csv', dtype={'id': 'Int32', 'nome': 'str', 'sexo': 'str', 'endereco': 'str', 'email': 'str', 'telefone': 'str'})


def ler_csv():
    clientes = pd.read_csv('clientes.csv', dtype={'id': 'Int32', 'nome': 'str', 'sexo': 'str', 'endereco': 'str', 'email': 'str', 'telefone': 'str'})


@app.post("/clientes/", response_model=Cliente, status_code=HTTPStatus.CREATED)
def adicionar_cliente(cliente: Cliente):
    if any(cliente_atual["id"] == cliente.id for index, cliente_atual in clientes.iterrows()):
        raise HTTPException(status_code=400, detail="ID já existe.")
    pd.concat([clientes, to_dataframe(cliente)], ignore_index=True).to_csv("clientes.csv", index=False)
    ler_csv()
    return cliente

@app.get("/clientes/", response_model=List[Cliente])
def retorna_clientes():
    clientes_list: List[Cliente] = pd.read_csv("clientes.csv").values.tolist()
    return clientes_list

