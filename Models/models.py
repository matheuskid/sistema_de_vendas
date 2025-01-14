from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, TypeVar, Generic
from pydantic import BaseModel
from enum import Enum

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
    
    itens: List["ItemPedido"] = Relationship(back_populates="produto")

class StatusPedidoEnum(str, Enum):
    PENDENTE = "Pendente"
    EM_PROCESSAMENTO = "Em Processamento"
    PAGO = "Pago"
    ENVIADO = "Enviado"
    ENTREGUE = "Entregue"
    CANCELADO = "Cancelado"

class StatusPedido(SQLModel, table=True):
    __tablename__ = "status_pedido"
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: StatusPedidoEnum
    descricao: str
    
    pedidos: List["Pedido"] = Relationship(back_populates="status")

class Pedido(SQLModel, table=True):
    __tablename__ = "pedido"
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(foreign_key="cliente.id")
    status_id: Optional[int] = Field(foreign_key="status_pedido.id")
    data_pedido: datetime = Field(default_factory=datetime.now)
    valor_total: float
    
    cliente: Optional["Cliente"] = Relationship(back_populates="pedidos")
    status: Optional[StatusPedido] = Relationship(back_populates="pedidos")
    itens: List["ItemPedido"] = Relationship(back_populates="pedido")

class ItemPedido(SQLModel, table=True):
    __tablename__ = "item_pedido"
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: Optional[int] = Field(foreign_key="pedido.id")
    produto_id: Optional[int] = Field(foreign_key="produto.id")
    quantidade: int
    preco_unitario: float
    
    pedido: Optional["Pedido"] = Relationship(back_populates="itens")
    produto: Optional["Produto"] = Relationship(back_populates="itens")



