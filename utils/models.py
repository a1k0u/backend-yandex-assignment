from typing import NamedTuple
import datetime


class Product(NamedTuple):
    uuid: str
    name: str
    group: str
    parent_id: str
    price: int
    date: str


def create_product(item: dict, time: str) -> Product:
    return Product(
        uuid=item["id"],
        name=item["name"],
        group=item["type"],
        parent_id=item["parentId"],
        price=item["price"],
        date=time,
    )
