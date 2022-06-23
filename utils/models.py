from dataclasses import dataclass
import datetime


@dataclass
class Product:
    uuid: str
    name: str
    group: str
    parent_id: str
    price: int
    date: str


def create_product(item: dict, time: str) -> Product:
    return Product(
        uuid=item.get("id", None),
        name=item.get("name", None),
        group=item.get("type", None),
        parent_id=item.get("parentId", None),
        price=item.get("price", None),
        date=time,
    )
