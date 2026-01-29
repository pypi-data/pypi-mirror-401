# db.py

from dotenv import load_dotenv, find_dotenv
import os
import pyodbc

# find .env by walking up parent dirs
dotenv_path = find_dotenv(usecwd=True)

if dotenv_path:
    load_dotenv(dotenv_path=dotenv_path, override=False)

DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"

def get_connection(dbkey: str='APP', driver:str=DEFAULT_DRIVER) -> pyodbc.Connection:
    """
    Open a SQL Server connection using env variables prefixed with `dbkey`.

    Expected env vars (in `.env.example` with dbkey='APP'):

    <dbkey>DB_SERVER=
    <dbkey>DB_NAME=
    <dbkey>DB_USER=
    <dbkey>DB_PASS=
    """

    prefix = f"{dbkey}DB_"

    # fail-fast
    server = os.getenv(prefix + "SERVER") 
    database = os.getenv(prefix + "NAME")
    username = os.getenv(prefix + "USER")
    password = os.getenv(prefix + "PASS")

    if not all([server, database, username, password]):
        raise RuntimeError(f"Missing environment variables for {dbkey}")

    connection_string = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )

    return pyodbc.connect(connection_string)
