from sqlmodel import SQLModel, create_engine, Session
from Models.models import StatusPedido, StatusPedidoEnum
from sqlalchemy import select

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def criar_status_padrao(session):
    status_padrao = [
        StatusPedido(
            nome=StatusPedidoEnum.PENDENTE,
            descricao="Pedido registrado mas aguardando processamento"
        ),
        StatusPedido(
            nome=StatusPedidoEnum.EM_PROCESSAMENTO,
            descricao="Pedido está sendo processado"
        ),
        StatusPedido(
            nome=StatusPedidoEnum.PAGO,
            descricao="Pagamento confirmado"
        ),
        StatusPedido(
            nome=StatusPedidoEnum.ENVIADO,
            descricao="Pedido foi enviado para entrega"
        ),
        StatusPedido(
            nome=StatusPedidoEnum.ENTREGUE,
            descricao="Pedido entregue ao cliente"
        ),
        StatusPedido(
            nome=StatusPedidoEnum.CANCELADO,
            descricao="Pedido foi cancelado"
        )
    ]
    
    for status in status_padrao:
        existing = session.exec(
            select(StatusPedido).where(StatusPedido.nome == status.nome)
        ).first()
        if not existing:
            session.add(status)
    
    session.commit()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        criar_status_padrao(session)
