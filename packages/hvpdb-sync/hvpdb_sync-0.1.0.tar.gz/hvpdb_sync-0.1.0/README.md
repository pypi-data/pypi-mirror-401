# HVPDB Sync Plugin

Synchronization and replication tools for distributed **HVPDB** instances.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-sync
```

## Usage

```python
from hvpdb_sync import SyncManager

# Sync local DB with remote peer
syncer = SyncManager(local_db=db)
syncer.pull_from("http://remote-node:3000")
```
