import sqlite3
from sqlite3 import Error


def create_connection():
    try:
        connection = sqlite3.connect("database.db")
    except Error:
        connection = None
    return connection


def create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goods (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        parent_id TEXT,
        price INTEGER,
        data TEXT NOT NULL)
        """
    )

def insert_data():
    conn



if __name__ == "__main__":
    create_tables()
