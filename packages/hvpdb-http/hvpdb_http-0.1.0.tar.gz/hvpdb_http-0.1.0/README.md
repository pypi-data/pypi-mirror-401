# HVPDB HTTP Plugin

Lightweight HTTP/REST API gateway for **HVPDB**.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-http
```

## Usage

```python
from hvpdb_http import run_server

# Expose database over HTTP
run_server(db_path="./mydb.hvp", port=3000)
```
