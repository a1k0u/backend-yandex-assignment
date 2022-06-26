from utils.variables import get_env_vars

from functools import lru_cache
from typing import Callable

from sqlalchemy import create_engine
import sqlalchemy.engine


@lru_cache
def get_engine() -> sqlalchemy.engine.Engine:
    var = get_env_vars()
    engine = create_engine(
        f"postgresql+psycopg2://{var['PGUSER']}:{var['PGPASSWD']}@"
        f"{var['PGHOST']}:{var['PGPORT']}/{var['PGDB']}",
        echo=True,
    )
    return engine


def connect(function: Callable):
    def wrapper():
        engine = get_engine()
        with engine.begin() as connection:
            return function(connection)

    return wrapper
