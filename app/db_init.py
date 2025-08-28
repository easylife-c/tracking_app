import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'lostfound.db')

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS lost_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_name TEXT NOT NULL,
    class_name TEXT NOT NULL,
    return_location TEXT NOT NULL,
    image_filename TEXT,
    status TEXT NOT NULL DEFAULT 'REPORTED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lost_items_status_created
ON lost_items (status, created_at DESC);
"""


def main() -> None:
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"Initialized database at {DB_PATH}")


if __name__ == '__main__':
    main()