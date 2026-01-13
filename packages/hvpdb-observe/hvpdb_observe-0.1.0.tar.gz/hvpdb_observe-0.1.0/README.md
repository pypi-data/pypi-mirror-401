# HVPDB Observe Plugin

Observability, metrics, and monitoring integration for **HVPDB**.

This is an official plugin for [HVPDB (High Velocity Python Database)](https://github.com/8w6s/hvpdb).

## Installation

```bash
pip install hvpdb-observe
```

## Usage

```python
from hvpdb_observe import MetricsCollector

# Enable metrics
collector = MetricsCollector(db)
print(collector.get_stats())
```
