from utils.models import Product
from utils.exceptions import DBError
from typing import Callable
from pathlib import Path

import sqlite3
from sqlite3 import Error


def create_connection():
    try:
        connection = sqlite3.connect(Path("/home/a1k0u/Documents/Python/backend-yandex-assignment/db.sqlite"))
    except Error:
        connection = None
    return connection


def create_tables(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goods (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        parent_id TEXT,
        price INTEGER,
        time TEXT NOT NULL)
        """
    )

    return None


def insert_item(cursor, product: Product):
    cursor.execute(f"""
        INSERT INTO 
            goods (id, name, type, parent_id, price, time)
        VALUES 
            ('{product.uuid}',
             '{product.name}',
             '{product.group}',
             '{product.parent_id}',
             '{product.price}',
             '{product.date}'
             )
    """)

    return None


def update_item(cursor, product: Product):
    cursor.execute(f"""
        UPDATE 
            goods 
        SET 
            name='{product.name}',
            type='{product.group}',
            parent_id='{product.parent_id}',
            price='{product.price}',
            time='{product.date}'
        WHERE 
            id='{product.uuid}'
    """)

    return None


def check_item(cursor, product: Product):
    cursor.execute(f"""
        SELECT 
            id,
            type
        FROM
            goods
        WHERE 
            id='{product.uuid}'
    """)

    return cursor.fetchall()


def delete_item(cursor, uuid):
    cursor.execute(f"""
        DELETE FROM
            goods
        WHERE
            id='{uuid}'
    """)

    return None


def find_by_parent_id(cursor, uuid):
    cursor.execute(f"""
        SELECT
            id,
            type
        FROM
            goods
        WHERE 
            parent_id='{uuid}'
    """)

    return cursor.fetchall()


def db_request(request: Callable, *args):
    connection = create_connection()
    if connection is None:
        raise DBError
    cursor = connection.cursor()
    result = request(cursor, *args)
    cursor.close()

    return result


if __name__ == "__main__":
    db_request(create_tables)
