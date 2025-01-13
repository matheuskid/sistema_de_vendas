from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        arbitrary_types_allowed = True


class Cliente(SQLModel, table=True):
    __tablename__ = "cliente"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    data_nascimento: str
    email: str
    telefone: str
    endereco: str
    cidade: str
    estado: str
    cep: str
    
    # Modificando a relação para usar List["Pedido"] com ForwardRef
    pedidos: List["Pedido"] = Relationship(back_populates="cliente", sa_relationship_kwargs={"lazy": "selectin"})

class Produto(SQLModel, table=True):
    __tablename__ = "produto"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    categoria: str
    preco: float
    estoque: int

class Pedido(SQLModel, table=True):
    __tablename__ = "pedido"
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(foreign_key="cliente.id")  
    data_pedido: datetime = Field(default_factory=datetime.now)
    valor_total: float
    status: str
    
    cliente: Optional["Cliente"] = Relationship(back_populates="pedidos")



