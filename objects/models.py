from dataclasses import dataclass
from enum import Enum


@dataclass
class Product:
    uuid: str
    name: str
    group: str
    parent_id: str
    price: int
    date: str


class Type(Enum):
    OFFER: str = "OFFER"
    CATEGORY: str = "CATEGORY"


def create_product(item: dict, time: str) -> Product:
    return Product(
        uuid=item.get("id"),
        name=item.get("name"),
        group=item.get("type"),
        parent_id=item.get("parentId"),
        price=item.get("price"),
        date=time,
    )
