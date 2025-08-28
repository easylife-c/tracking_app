import os
import sqlite3
from typing import Optional
from flask import g

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'lostfound.db')


def get_db() -> sqlite3.Connection:
    if 'db_conn' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db_conn = conn
    return g.db_conn  # type: ignore[return-value]


def close_db(_: Optional[BaseException] = None) -> None:
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()


def init_db() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lost_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            return_location TEXT NOT NULL,
            image_filename TEXT,
            status TEXT NOT NULL DEFAULT 'REPORTED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_lost_items_status_created
        ON lost_items (status, created_at DESC);
        """
    )
    conn.commit()
    conn.close()