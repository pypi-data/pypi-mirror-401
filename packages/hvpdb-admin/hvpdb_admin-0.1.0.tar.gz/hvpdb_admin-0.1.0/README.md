# HVPDB Admin Plugin

Administration dashboard and management interface for **HVPDB**.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-admin
```

## Usage

```python
from hvpdb_admin import AdminServer

# Start the admin dashboard
server = AdminServer(db_path="./mydb.hvp")
server.start(port=8080)
```
