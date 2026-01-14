# wandb_buddy

Utilities for W&B experiment analysis.

## Installation

```bash
pip install wandb_buddy
```

Or install from source:

```bash
pip install -e .
```

## Usage

```python
import wandb_buddy as wb

# Tag-based filtering (simple)
df = wb.load_runs("your-entity", "your-project", tags=["experiment-v1"])

# Exclude certain tags
df = wb.load_runs("your-entity", "your-project", tags=["experiment-v1"], exclude_tags=["debug"])

# Raw filters (flexible)
df = wb.load_runs("your-entity", "your-project", filters={"config.lr": 0.001})

# Combined tag and raw filters
df = wb.load_runs("your-entity", "your-project", tags=["experiment-v1"], filters={"config.lr": 0.001})

# Include all run states (not just finished)
df = wb.load_runs("your-entity", "your-project", tags=["experiment-v1"], state="all")

# Custom timeout
df = wb.load_runs("your-entity", "your-project", tags=["experiment-v1"], timeout=10000)
```

The returned DataFrame contains: `name`, `id`, `state`, `created_at`, `heartbeat_at`, `tags`, `sweep_id`, plus all config and summary values from each run.

## Development

```bash
pip install -e ".[dev]"
```
