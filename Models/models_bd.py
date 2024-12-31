from sqlmodel import SQLModel, Field

class Cliente(SQLModel, table=True):
    __tablename__ = 'Cliente'
    id: int | None = Field(primary_key=True)
    nome: str = Field(str(50))
    data_nascimento: str = Field(str(50))
    email: str = Field(str(50))
    telefone: str = Field(str(50))
    endereco: str = Field(str(50))
    cidade: str = Field(str(50))
    estado: str = Field(str(50))
    cep: str = Field(str(50))

class Produto(SQLModel, table=True):
    __tablename__ = 'Produto'
    id: int | None = Field(primary_key=True)
    nome: str = Field(str(50))
    categoria: str = Field(str(50))
    preco: float = Field(float)
    estoque: int = Field(int)
