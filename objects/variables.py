"""
Contains product variable, which able to
get data by dot ('.') for each row, imports
all environmental variables, has information
for column `type` in DB by enum format.
"""

from dataclasses import dataclass
from datetime import datetime
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


def create_time_from_str(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")


def create_str_from_time(time: datetime) -> str:
    return time.isoformat("T", "milliseconds") + "Z"


@dataclass
class Product:
    id: str
    name: str
    type: str
    parent_id: str
    price: int
    date: datetime


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
        date=create_time_from_str(time),
    )
