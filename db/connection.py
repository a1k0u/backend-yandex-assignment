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
from utils.logger import log_db, log_route


@lru_cache
def get_engine() -> sqlalchemy.engine.Engine:
    """
    Creates a sqlalchemy Engine for database.
    All necessary information gets from environmental
    variables. If engine has been already created,
    lru_cache will return it.
    """

    var = get_env_vars()
    log_db.debug("Got environmental variables for database.")

    engine = create_engine(
        f"postgresql+psycopg2://"
        f"{var['PGUSER']}:"
        f"{var['PGPASSWD']}@"
        f"{var['PGHOST']}:"
        f"{var['PGPORT']}/"
        f"{var['PGDB']}"
    )
    log_db.debug("Engine for db was created.")

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
                log_db.debug("Got connection to db.")

                result = function(connection, values)

                log_db.debug("Got results from database.")

                if result[1] != 200:
                    raise DatabaseError("DB error.")
        except DatabaseError:
            log_db.warning(f"Expected HTTP status code 200, got {result[1]=}.")

        response = __serialize_data(result)
        log_route.debug("Data was serialized.")

        return response

    return wrapper


if __name__ == "__main__":
    print(get_engine().connect())
