import psycopg2
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
from typing import Optional


def db_connection() -> Optional["psycopg2.connection"]:
    return connect("host=localhost dbname=habits user=postgres password=secret")


def select(query: str) -> dict:
    with db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(query)
            return cur.fetchone()
        
def insert(query: str) -> None:
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
