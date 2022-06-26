from dataclasses import dataclass
from enum import Enum
import os

from dotenv import load_dotenv

load_dotenv()


def get_env_vars() -> dict:
    return dict(
        PGUSER=os.getenv("PGUSER"),
        PGPASSWD=os.getenv("PGPASSWD"),
        PGHOST=os.getenv("PGHOST"),
        PGPORT=os.getenv("PGPORT"),
        PGDB=os.getenv("PGDB"),
    )


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
