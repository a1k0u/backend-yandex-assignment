import datetime
from typing import NamedTuple
import datetime


class Product:
    uuid: str
    name: str
    group: str
    parent_id: str = None
    price: int
    date: datetime.datetime
