from typing import List

from sqlalchemy import select, insert, delete, update

from objects.variables import Product, create_product
from db.models import Goods


def insert_item_into_db(conn, product: Product) -> None:
    stmt = insert(Goods).values(
        id=product.id,
        name=product.name,
        type=product.type,
        parent_id=product.parent_id,
        price=product.price,
        date=product.date,
    )
    conn.execute(stmt)


def update_item_in_db(conn, product: Product) -> None:
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


def update_item_time_in_db(conn, node_id, time) -> None:
    stmt = update(Goods).where(Goods.id == node_id).values(date=time)
    conn.execute(stmt)


def delete_item_from_db(conn, uuid: str) -> None:
    stmt = delete(Goods).where(Goods.id == uuid)
    conn.execute(stmt)


def get_element_by_uuid(conn, uuid: str) -> Product:
    stmt = select(Goods).where(Goods.id == uuid)
    result = conn.execute(stmt).fetchone()
    if not result:
        return result

    return create_product(
        dict(
            id=result[0],
            name=result[1],
            type=result[2],
            parentId=result[3],
            price=result[4],
        ),
        result[5],
    )


def find_by_parent_id(conn, uuid: str) -> List[Product]:
    stmt = select(Goods.id, Goods.type).where(Goods.parent_id == uuid)
    return [
        create_product(dict(id=el[0], type=el[1]), "")
        for el in conn.execute(stmt).fetchall()
    ]
