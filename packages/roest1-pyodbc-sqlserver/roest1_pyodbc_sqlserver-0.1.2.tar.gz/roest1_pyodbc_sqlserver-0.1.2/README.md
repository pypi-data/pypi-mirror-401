# pyodbc-sqlserver

Lightweight, opinionated helpers for connecting to Microsoft SQL Server using
[`pyodbc`](https://github.com/mkleehammer/pyodbc).

Designed for **internal company use** where:

- SQL Server auth is handled via environment variables
- Multiple databases may be accessed from the same app
- You want zero ORM, zero magic, just clean connections

---

## Features

- Simple SQL Server connection factory
- Environment-variable–based configuration
- Supports multiple databases via prefixes (`APPDB_`, `REPORTDB_`, etc.)
- Thin wrapper on top of `pyodbc` (no abstraction leakage)

---

## Installation

### (Optional) Create environment - Conda

```bash
conda create -n envname python=3.10 -y
conda activate envname
```

### Install Dependencies

```bash
conda install -c conda-forge pyodbc unixodbc -y
```

### From local source (recommended for internal use)

```bash
pip install -e .
```

Or from a private Git repo:

SSH:

```bash
pip install git+ssh://git@github.com/roest1/pyodbc-sqlserver.git
```

HTTP:

```bash
pip install git+https://github.com/roest1/pyodbc-sqlserver.git
```

---

## Environment Configuration / Variable Loading

This package will automatically load a `.env` file from the current working
directory **if one exists**.

- Existing environment variables are **not overridden**
- If no `.env` file is present, no action is taken

This behavior is intended to simplify local development. In production
environments (Docker, CI, servers), environment variables should be provided
by the runtime environment.

### Single database

```env
DB_SERVER=sqlserver.company.local
DB_NAME=MyDatabase
DB_USER=app_user
DB_PASS=secret
```

### Multiple databases (recommended)

Use prefixes to distinguish connections:

```env
APPDB_SERVER=sqlserver.company.local
APPDB_NAME=ApplicationDB
APPDB_USER=app_user
APPDB_PASS=secret

REPORTDB_SERVER=sqlserver.company.local
REPORTDB_NAME=ReportingDB
REPORTDB_USER=report_user
REPORTDB_PASS=secret
```

---

## Usage

```python
from pyodbc_sqlserver.db import get_connection

# Default (no prefix)
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    print(cursor.fetchone())

# Prefixed database
with get_connection("APP") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dbo.Users")
    print(cursor.fetchone())
```

---

## System Requirements

This package depends on system-level ODBC libraries.

### Linux

```bash
sudo apt install unixodbc unixodbc-dev
```

### Conda

```bash
conda install -c conda-forge unixodbc
```

## Driver Notes

By default this package uses:

```
ODBC Driver 18 for SQL Server
```

Ensure it is installed on the host system.

Linux:

```bash
msodbcsql18
```

Windows:

- Install via Microsoft ODBC driver installer

---

## Why this exists

This package intentionally does **not**:

- Provide ORM features
- Manage migrations
- Wrap cursors or results

It exists to standardize how our internal Python services connect to SQL Server
without copy/pasting connection logic everywhere.

---

## License

MIT
