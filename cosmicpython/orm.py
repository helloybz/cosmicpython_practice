from sqlalchemy import Column, Integer, String, Table, orm

from . import model

registry = orm.registry()
order_lines = Table(
    "order_lines",
    registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("order_id", String(255)),
)


def start_mappers() -> None:
    registry.map_imperatively(
        model.OrderLine,
        order_lines,
    )
