from pydantic import BaseModel, Field
from typing import Optional

class Cliente(BaseModel):
    id: int = Field(..., description="ID do cliente", example=1)
    nome: str = Field(..., description="Nome do cliente", example="João Silva")
    data_nascimento: str = Field(..., description="Data de nascimento", example="1990-01-01")
    email: str = Field(..., description="Email do cliente", example="joao@email.com")
    telefone: str = Field(..., description="Telefone do cliente", example="(11) 99999-9999")
    endereco: str = Field(..., description="Endereço do cliente", example="Rua Exemplo, 123")
    cidade: str = Field(..., description="Cidade do cliente", example="São Paulo")
    estado: str = Field(..., description="Estado do cliente", example="SP")
    cep: str = Field(..., description="CEP do cliente", example="01000-000")

class Produto(BaseModel):
    id: int = Field(..., description="ID do produto", example=101)
    nome: str = Field(..., description="Nome do produto", example="Produto X")
    categoria: str = Field(..., description="Categoria do produto", example="Eletrônicos")
    preco: float = Field(..., description="Preço do produto", example=199.99)
    estoque: int = Field(..., description="Quantidade em estoque", example=50)
