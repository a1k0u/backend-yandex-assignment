"""
There are models for sqlalchemy in this file.
If you start this script, all tables will create in DB,
which gets by get_engine in connection.py.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

from db.connection import get_engine
from utils.logger import log_db

Base = declarative_base()


class Goods(Base):
    """
    The main table, which contains all
    the necessary information about offers and categories.
    """

    __tablename__ = "Goods"

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String(32))
    parent_id = Column(String(36))
    price = Column(Integer)
    date = Column(DateTime, nullable=False)


if __name__ == "__main__":
    log_db.debug("Tables was created.")
    Base.metadata.create_all(get_engine())
