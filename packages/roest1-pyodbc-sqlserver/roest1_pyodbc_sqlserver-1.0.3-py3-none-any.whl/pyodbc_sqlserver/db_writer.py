# db_writer.py

from .db import get_connection
from pathlib import Path
from typing import Iterable, Optional

def execute(sql: str, params: Optional[Iterable] = None, dbkey:str='APP'):
    """
    Execute a single INSERT / UPDATE / DELETE statement.
    """
    with get_connection(dbkey) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        conn.commit()


def execute_many(sql: str, rows: Iterable[Iterable], dbkey:str='APP'):
    """
    Bulk insert/update.
    """
    with get_connection(dbkey) as conn:
        cursor = conn.cursor()
        cursor.executemany(sql, rows)
        conn.commit()


def run_sql_file(path: str | Path, dbkey: str):
    if isinstance(path, str):
        path = Path(path)
        
        path = path.resolve()

    # normalize to absolute path under project root
    # path = (ROOT / path).resolve()
    # no longer tracking ROOT var

    # print(f"\n▶ Running: {path.relative_to(ROOT)}")
    print(f"\n▶ Running: {path}")

    sql = path.read_text(encoding="utf-8").strip()
    if not sql:
        print("⚠️  Skipping empty file")
        return

    execute(sql, dbkey=dbkey)
    print("✅ Done")

