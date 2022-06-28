"""
There are models for sqlalchemy in this file.
If you start this script, all tables will create in DB,
which gets by get_engine in connection.py.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from db.connection import get_engine

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
    date = Column(String(24), nullable=False)  # TODO: transform info date (ISO).


if __name__ == "__main__":
    Base.metadata.create_all(get_engine())
