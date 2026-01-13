# HVPDB Backup Plugin

Advanced backup, restore, and snapshot capabilities for **HVPDB**.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-backup
```

## Usage

```python
from hvpdb_backup import BackupManager

# Create a hot backup
manager = BackupManager(db_path="./mydb.hvp")
manager.create_snapshot(output_path="./backups/snap_v1.hvp")
```
