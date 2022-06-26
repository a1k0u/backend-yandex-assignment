from db.connection import get_engine

from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Goods(Base):
    __tablename__ = "Goods"

    id_ = Column(String(36), primary_key=True, nullable=False)
    name_ = Column(String, nullable=False)
    type_ = Column(String(32))
    parent_id_ = Column(String(36))
    price_ = Column(Integer)
    time_ = Column(String(24), nullable=False)


if __name__ == "__main__":
    Base.metadata.create_all(get_engine())
