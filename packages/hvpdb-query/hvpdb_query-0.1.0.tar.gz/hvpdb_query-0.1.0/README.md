# HVPDB Query Plugin

Polyglot query engine supporting SQL-like and MongoDB-like syntax for **HVPDB**.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-query
```

## Usage

```python
from hvpdb_query import execute_query

# Run SQL
result = execute_query(db, "SELECT * FROM users WHERE role='admin'")
```
