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

    def to_dataframe(self):
        return pd.DataFrame({"id": self.id,
                            "nome": self.nome,
                            "sexo": self.sexo,
                            "endereco": self.endereco,
                            "email": self.email,
                            "telefone": self.telefone})


clientes = pd.read_csv('clientes.csv', dtype={'id': 'Int32', 'nome': 'str', 'sexo': 'str', 'endereco': 'str', 'email': 'str', 'telefone': 'str'})



@app.post("/clientes/", response_model=Cliente, status_code=HTTPStatus.CREATED)
def adicionar_cliente(cliente: Cliente):
    if any(cliente_atual["id"] == cliente.id for index, cliente_atual in clientes.iterrows()):
        raise HTTPException(status_code=400, detail="ID já existe.")
    pd.concat([clientes, cliente.to_dataframe()], index="id")
    clientes.to_csv("clientes.csv")
    return cliente
