from variables import get_env_vars
from exceptions import DBError

from functools import lru_cache
from typing import Callable

from sqlalchemy import create_engine
import sqlalchemy.engine


@lru_cache
def get_engine() -> sqlalchemy.engine.Engine:
    var = get_env_vars()
    print(var)
    engine = create_engine(
        f"postgresql+psycopg2://{var['PGUSER']}:{var['PGPASSWD']}@"
        f"{var['PGHOST']}:{var['PGPORT']}/{var['PGDB']}",
        echo=True,
    )
    return engine


def connect_to_db(function: Callable):
    def wrapper(values: dict = None):
        engine = get_engine()
        try:
            with engine.begin() as connection:
                result = function(connection, values)
                if result[1] != 200:
                    raise DBError("32!")
        except DBError:
            ...
        return result
    return wrapper


if __name__ == "__main__":
    print(get_engine())
