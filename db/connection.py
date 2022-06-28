"""
Creates engine to database by sqlalchemy and saves it by lru_cache,
and here's you can find a decorator for functions,
which work with database. This decorator creates connection
and after success executes commits changes or rollback if programme got exceptions.
"""

from functools import lru_cache
from typing import Callable

from sqlalchemy import create_engine
from flask import jsonify
import sqlalchemy.engine

from objects.variables import get_env_vars
from objects.exceptions import DatabaseError


@lru_cache
def get_engine() -> sqlalchemy.engine.Engine:
    """
    Creates a sqlalchemy Engine for database.
    All necessary information gets from environmental
    variables. If engine has been already created,
    lru_cache will return it.
    """

    var = get_env_vars()
    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{var['PGUSER']}:"
        f"{var['PGPASSWD']}@"
        f"{var['PGHOST']}:"
        f"{var['PGPORT']}/"
        f"{var['PGDB']}"
    )

    return engine


def __serialize_data(response: tuple):
    return jsonify(response[0]), *response[1:]


def connect_to_db(function: Callable) -> Callable:
    """
    Secure connection to the database.
    Commits change in DB if success and rollbacks if exception.

    Gets function for DB and creates connection for it.
    Returns response in serialized form by flask.jsonify and
    code like a 'HTTP status code'.
    """

    def wrapper(values: dict = None):
        engine = get_engine()
        try:
            with engine.begin() as connection:
                result = function(connection, values)
                if result[1] != 200:
                    raise DatabaseError(f"Expected HTTP status code 200, got {result[1]=}.")
        except DatabaseError:
            ...

        return __serialize_data(result)

    return wrapper


if __name__ == "__main__":
    print(get_engine().connect())
