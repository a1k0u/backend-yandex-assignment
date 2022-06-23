import os
from collections import namedtuple

import sqlalchemy.engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

load_dotenv()


def get_env() -> namedtuple:
    """Loads database variables"""
    Variables = namedtuple(
        "Variables", ["PGUSER", "PGPASSWD", "PGHOST", "PGPORT", "PGDB"]
    )

    return Variables(
        PGUSER=os.getenv("PGUSER"),
        PGPASSWD=os.getenv("PGPASSWD"),
        PGHOST=os.getenv("PGHOST"),
        PGPORT=os.getenv("PGPORT"),
        PGDB=os.getenv("PGDB"),
    )


def __db_exist(engine) -> None:
    if not database_exists(engine.url):
        create_database(engine.url)


def get_engine() -> sqlalchemy.engine.Engine:
    """"""
    var = get_env()
    url = (
        f"postgresql+psycopg2://{var.PGUSER}:{var.PGPASSWD}@{var.PGPORT}:{var.PGPORT}/{var.PGDB}"
    )
    engine = create_engine(url, echo=True)
    __db_exist(engine)

    return engine


def get_session():
    """"""
    ...


if __name__ == "__main__":
    get_engine()
