"""
This script file contains all database queries.
"""

import datetime
from typing import List

from sqlalchemy import select, insert, delete, update, and_

from objects.variables import Product, Type
from db.models import Goods


def insert_element(conn, product: Product) -> None:
    stmt = insert(Goods).values(
        id=product.id,
        name=product.name,
        type=product.type,
        parent_id=product.parent_id,
        price=product.price,
        date=product.date,
    )
    conn.execute(stmt)


def update_element_by_id(conn, product: Product) -> None:
    stmt = (
        update(Goods)
        .where(Goods.id == product.id)
        .values(
            id=product.id,
            name=product.name,
            type=product.type,
            parent_id=product.parent_id,
            price=product.price,
            date=product.date,
        )
    )
    conn.execute(stmt)


def update_element_time_by_id(conn, node_id: str, date: datetime) -> None:
    stmt = update(Goods).where(Goods.id == node_id).values(date=date)
    conn.execute(stmt)


def delete_element_by_id(conn, uuid: str) -> None:
    stmt = delete(Goods).where(Goods.id == uuid)
    conn.execute(stmt)


def get_element_by_id(conn, uuid: str) -> Product:
    stmt = select(Goods).where(Goods.id == uuid)
    result = conn.execute(stmt).fetchone()
    return result if not result else Product(*result)


def get_elements_by_parent_id(conn, uuid: str) -> List[Product]:
    stmt = select(Goods).where(Goods.parent_id == uuid)
    return [Product(*el) for el in conn.execute(stmt).fetchall()]


def get_offers_by_time_period(
    coon, date_start: datetime, date_end: datetime
) -> List[Product]:
    stmt = (
        select(Goods)
        .where(Goods.type == Type.OFFER.value)
        .where(and_(date_start <= Goods.date, Goods.date <= date_end))
    )
    return [Product(*el) for el in coon.execute(stmt).fetchall()]
