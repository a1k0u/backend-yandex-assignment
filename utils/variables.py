import os
from dotenv import load_dotenv

load_dotenv()


def get_env_vars() -> dict:
    return dict(
        PGUSER=os.getenv("PGUSER"),
        PGPASSWD=os.getenv("PGPASSWD"),
        PGHOST=os.getenv("PGHOST"),
        PGPORT=os.getenv("PGPORT"),
        PGDB=os.getenv("PGDB"),
    )
