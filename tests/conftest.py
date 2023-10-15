from datetime import date, timedelta

from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from cosmicpython.orm import registry, start_mappers


@fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    registry.metadata.create_all(engine)
    return engine


@fixture
def session(in_memory_db) -> Session:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@fixture
def tomorrow() -> date:
    return date.today() + timedelta(days=1)


@fixture
def today() -> date:
    return date.today()


@fixture
def later() -> date:
    return date.today() + timedelta(days=2)
