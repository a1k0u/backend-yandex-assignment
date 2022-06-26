from models import Product
from exceptions import DBError
from typing import Callable
import os

from tables import Goods
from sqlalchemy import select, insert, delete, update


def insert_item_into_db(conn, product: Product):
    stmt = insert(Goods).values(
        id_=product.uuid,
        name_=product.name,
        type_=product.group,
        parent_id_=product.parent_id,
        price_=product.price,
        time_=product.date,
    )
    conn.execute(stmt)
    return None


def update_item_in_db(conn, product: Product):
    stmt = update(Goods).\
        where(Goods.id_ == product.uuid).\
        values(
            id_=product.uuid,
            name_=product.name,
            type_=product.group,
            parent_id_=product.parent_id,
            price_=product.price,
            time_=product.date,
        )
    conn.execute(stmt)
    return None


def check_item_in_db(conn, product: Product):
    stmt = select(Goods.id_, Goods.type_).where(Goods.id_ == product.uuid)
    return conn.execute(stmt).fetchall()


def delete_item_from_db(conn, uuid):
    stmt = delete(Goods).where(Goods.id_ == uuid)
    conn.execute(stmt)
    return None


def take_element_by_uuid(conn, uuid):
    stmt = select(Goods).where(Goods.id_ == uuid)
    return conn.execute(stmt).fetchall()


def find_by_parent_id(conn, uuid):
    stmt = select(Goods.id_, Goods.type_).where(Goods.parent_id_ == uuid)
    return conn.execute(stmt).fetchall()
