from sqlalchemy import DateTime, Float, Integer, String

from app.model import Produto


def test_tablename_is_produtos():
    assert Produto.__tablename__ == "produtos"


def test_required_columns_and_types():
    columns = Produto.__table__.columns

    assert isinstance(columns["id"].type, Integer)
    assert isinstance(columns["nome"].type, String)
    assert isinstance(columns["descricao"].type, String)
    assert isinstance(columns["preco"].type, Float)
    assert isinstance(columns["quantidade"].type, Integer)
    assert isinstance(columns["criado_em"].type, DateTime)
    assert isinstance(columns["atualizado_em"].type, DateTime)



def test_nullable_constraints():
    columns = Produto.__table__.columns

    assert columns["nome"].nullable is False
    assert columns["preco"].nullable is False
    assert columns["quantidade"].nullable is False
    assert columns["descricao"].nullable is True


def test_defaults_and_update_hooks_are_configured():
    columns = Produto.__table__.columns

    assert columns["criado_em"].server_default is not None
    assert columns["atualizado_em"].onupdate is not None

