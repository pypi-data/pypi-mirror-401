# db_reader.py 

from .db import get_connection
from typing import Iterable, Optional

def fetch_all(sql: str, params: Optional[Iterable] = None, dbkey:str='APP'):
    """
    Execute a SELECT query and return rows as tuples.
    """
    with get_connection(dbkey=dbkey) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchall()


def fetch_dicts(sql: str, params: Optional[Iterable] = None, dbkey:str='APP'):
    """
    Execute a SELECT query and return rows as dicts.
    """
    with get_connection(dbkey) as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params or [])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def query(sql: str, dbkey:str='APP'): 
    """
    print to console
    """
    rows = fetch_all(sql,dbkey=dbkey)
    for row in rows:
        print(row)
