# models.py
from pydantic import BaseModel

class Cliente(BaseModel):
    id: int
    nome: str
    data_nascimento: str
    email: str
    telefone: str
    endereco: str
    cidade: str
    estado: str
    cep: str

class Produto(BaseModel):
    id: int
    nome: str
    categoria: str
    preco: float
    estoque: int
