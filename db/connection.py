"""
Creates engine to database by sqlalchemy,
and decorator for functions, which work with database.
This decorator creates connection and after success executes
commits changes or rollback if programme got exceptions.
"""

from functools import lru_cache
from typing import Callable

from sqlalchemy import create_engine
import sqlalchemy.engine

from objects.variables import get_env_vars
from objects.exceptions import DBError


@lru_cache
def get_engine() -> sqlalchemy.engine.Engine:
    """Connecting to a database using env variables."""
    var = get_env_vars()
    print(var)
    engine = create_engine(
        f"postgresql+psycopg2://{var['PGUSER']}:{var['PGPASSWD']}@"
        f"{var['PGHOST']}:{var['PGPORT']}/{var['PGDB']}",
        echo=True,
    )
    return engine


def connect_to_db(function: Callable):
    """Secure connection to the database. Commit if success and rollback if exception."""

    def wrapper(values: dict = None):
        engine = get_engine()
        try:
            with engine.begin() as connection:
                result = function(connection, values)
                if result[1] != 200:
                    raise DBError(f"{result[1]=}")
        except DBError:
            ...
        return result

    return wrapper


if __name__ == "__main__":
    print(get_engine())
