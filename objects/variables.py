"""
Contains product variable, which able to
get data by dot ('.') for each row, imports
all environmental variables, has information
for column `type` in DB by enum format.
"""

from dataclasses import dataclass
from enum import Enum
import os

from dotenv import load_dotenv


load_dotenv()


def get_env_vars() -> dict:
    """
    Loads all data from '.env' for PostgresSQL database.
    """

    return dict(
        PGUSER=os.getenv("PGUSER"),
        PGPASSWD=os.getenv("PGPASSWD"),
        PGHOST=os.getenv("PGHOST"),
        PGPORT=os.getenv("PGPORT"),
        PGDB=os.getenv("PGDB"),
    )


@dataclass
class Product:
    id: str
    name: str
    type: str
    parent_id: str
    price: int
    date: str


class Type(Enum):
    OFFER: str = "OFFER"
    CATEGORY: str = "CATEGORY"


def create_product_from_dict(item: dict, time: str) -> Product:
    return Product(
        id=item.get("id"),
        name=item.get("name"),
        type=item.get("type"),
        parent_id=item.get("parentId"),
        price=item.get("price"),
        date=time,
    )


if __name__ == "__main__":
    print(Product(*["a", "b", "c", "d", 101, "f"]))
    print([el.value for el in Type])
    print(Type.OFFER.name)
    print(Type.OFFER.value)
