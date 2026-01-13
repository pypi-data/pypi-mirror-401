# HVPDB Perms Plugin

Advanced permission management and Role-Based Access Control (RBAC) for **HVPDB**.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-perms
```

## Usage

```python
from hvpdb_perms import PermissionManager

pm = PermissionManager(db)
pm.grant_role("alice", "admin")
```
