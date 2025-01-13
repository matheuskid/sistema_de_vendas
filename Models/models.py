from sqlmodel import SQLModel, Field

class Cliente(SQLModel, table=True):
    __tablename__ = 'Cliente'
    id: int | None = Field(..., primary_key=True, description="ID do cliente", schema_extra={'example': 1})
    nome: str = Field(..., description="Nome do cliente", schema_extra={'example': "João Silva"})
    data_nascimento: str = Field(..., description="Data de nascimento", schema_extra={'example': "1990-01-01"})
    email: str = Field(..., description="Email do cliente", schema_extra={'example': "joao@email.com"})
    telefone: str = Field(..., description="Telefone do cliente", schema_extra={'example': "(11) 99999-9999"})
    endereco: str = Field(..., description="Endereço do cliente", schema_extra={'example': "Rua Exemplo, 123"})
    cidade: str = Field(..., description="Cidade do cliente", schema_extra={'example': "São Paulo"})
    estado: str = Field(..., description="Estado do cliente", schema_extra={'example': "SP"})
    cep: str = Field(..., description="CEP do cliente", schema_extra={'example': "01000-000"})

class Produto(SQLModel, table=True):
    __tablename__ = 'Produto'
    id: int = Field(..., primary_key=True, description="ID do produto", schema_extra={'example': 101})
    nome: str = Field(..., description="Nome do produto", schema_extra={'example': "Produto X"})
    categoria: str = Field(..., description="Categoria do produto", schema_extra={'example': "Eletrônicos"})
    preco: float = Field(..., description="Preço do produto", schema_extra={'example': 199.99})
    estoque: int = Field(..., description="Quantidade em estoque", schema_extra={'example': 50})
