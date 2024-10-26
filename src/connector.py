import psycopg2
from psycopg2 import connect
from psycopg2.extras import NamedTupleCursor
from typing import Optional, List
from config_reader import config


def db_connection() -> Optional["psycopg2.connection"]:
    return connect(
        host=config.db_host.get_secret_value(),
        port=config.db_port,
        dbname=config.db_name.get_secret_value(),
        user=config.db_user.get_secret_value(),
        password=config.db_pass.get_secret_value()
    )

def select(query: str) -> List[tuple]:
    with db_connection() as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
        
def insert(query: str) -> None:
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
