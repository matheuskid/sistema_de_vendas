from datetime import datetime
from typing import Optional, List, TypeVar, Generic
from odmantic import Model
from pydantic import BaseModel
from enum import Enum

T = TypeVar('T')

class PaginatedResponse(Model, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

class Cliente(Model):
    nome: str 
    data_nascimento: str
    email: str
    telefone: str
    endereco: str
    cidade: str
    estado: str
    cep: str
    
class ClienteAtualizado(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None

class Produto(Model):
    nome: str
    categoria: str
    preco: float
    estoque: int

'''
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

'''

