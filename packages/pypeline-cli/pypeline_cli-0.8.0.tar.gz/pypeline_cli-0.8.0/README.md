# pypeline-cli

> **Build production-ready data pipelines on Snowflake or Databricks in minutes, not hours.**

[![PyPI version](https://badge.fury.io/py/pypeline-cli.svg)](https://badge.fury.io/py/pypeline-cli)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is pypeline-cli?

pypeline-cli is a CLI tool that scaffolds complete ETL pipeline projects with:

- 🏗️ **Instant project setup** — One command creates a production-ready structure
- 🔌 **Platform choice** — Snowflake (Snowpark) or Databricks (PySpark)
- 📦 **Built-in utilities** — Session management, logging, decorators, table caching
- 🧩 **Modular architecture** — Pipelines contain processors, processors contain transformations
- 📝 **Simple dependency management** — Edit a Python list, not TOML

---

## Quick Start

### 1. Install

```bash
pip install pypeline-cli
```

### 2. Create a Project

```bash
# For Snowflake
pypeline init --name my_project --platform snowflake

# For Databricks
pypeline init --name my_project --platform databricks
```

### 3. Set Up Your Environment

```bash
cd my_project
pypeline install      # Creates .venv and installs dependencies
source .venv/bin/activate
```

### 4. Create a Pipeline

```bash
pypeline create-pipeline --name sales-etl
```

### 5. Add Processors

```bash
pypeline create-processor --name extract-orders --pipeline sales-etl
pypeline create-processor --name transform-metrics --pipeline sales-etl
```

### 6. Build for Deployment

```bash
pypeline build        # Creates deployment-ready ZIP
```

That's it! You now have a complete pipeline project with logging, session management, and test scaffolding.

---

## Project Structure

After running the commands above, you'll have:

```
my_project/
├── pyproject.toml              # Project configuration
├── dependencies.py             # Edit this to add packages
├── credentials.py.example      # Connection credentials template
├── my_project/
│   ├── __init__.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── sales_etl/
│   │       ├── sales_etl_runner.py    # Main pipeline class
│   │       ├── config.py              # Table configurations
│   │       └── processors/
│   │           ├── extract_orders_processor.py
│   │           └── transform_metrics_processor.py
│   ├── schemas/
│   └── utils/
│       ├── etl.py              # Session singleton
│       ├── logger.py           # Structured logging
│       ├── decorators.py       # @time_function, @skip_if_exists
│       ├── table_cache.py      # Pre-load tables efficiently
│       └── databases.py        # Database/schema constants
└── tests/
```

---

## Commands

| Command | Description |
|---------|-------------|
| `pypeline init` | Create a new project |
| `pypeline install` | Create venv and install dependencies |
| `pypeline create-pipeline` | Add a new pipeline to your project |
| `pypeline create-processor` | Add a processor to a pipeline |
| `pypeline sync-deps` | Sync dependencies.py → pyproject.toml |
| `pypeline build` | Create deployment-ready package |

### Common Options

```bash
# Initialize with all options
pypeline init \
  --name my_project \
  --platform snowflake \      # or databricks
  --author-name "Your Name" \
  --author-email "you@email.com" \
  --license MIT \
  --no-git                    # Skip git initialization

# Create pipeline
pypeline create-pipeline --name customer-analytics

# Create processor in a pipeline
pypeline create-processor --name aggregate-sales --pipeline customer-analytics
```

---

## How It Works

### The Pipeline Pattern

pypeline uses a simple **Extract → Transform → Load** pattern:

```
Pipeline
├── __init__(): Extract - Load source tables into cache
├── run_processors(): Transform - Chain processor transformations
└── _write_to_snowflake(): Load - Write final results
```

### Processors

Each processor focuses on one transformation concern:

```python
class AggregateOrdersProcessor:
    def __init__(self, cache):
        self.orders = cache["orders"]  # Pre-loaded by pipeline
    
    def process(self) -> DataFrame:
        return self._filter_valid() \
            .pipe(self._aggregate_by_customer) \
            .pipe(self._calculate_metrics)
```

### Built-in Utilities

| Utility | Purpose |
|---------|---------|
| `ETL` | Singleton for session management |
| `Logger` | Structured, color-coded logging |
| `TableCache` | Pre-load and cache source tables |
| `@time_function` | Automatically log execution time |
| `@skip_if_exists` | Skip processing if output exists |
| `TableConfig` | Dynamic table names (yearly, monthly, stable) |

---

## Managing Dependencies

Edit `dependencies.py` instead of `pyproject.toml`:

```python
# dependencies.py
BASE_DEPENDENCIES = [
    "snowflake-snowpark-python>=1.20.0",
    "pandas>=2.0.0",
    # ... auto-generated
]

USER_DEPENDENCIES = [
    # Add your packages here
    "requests>=2.31.0",
    "python-dotenv>=1.0.0",
]

DEFAULT_DEPENDENCIES = BASE_DEPENDENCIES + USER_DEPENDENCIES
```

Then sync to pyproject.toml:

```bash
pypeline sync-deps
```

---

## Platform Differences

| Feature | Snowflake | Databricks |
|---------|-----------|------------|
| DataFrame | `snowflake.snowpark` | `pyspark.sql` |
| Session | `SnowflakeSession` | `SparkSession` |
| Catalog | Database.Schema.Table | Catalog.Schema.Table |
| Write | `.save_as_table()` | `.saveAsTable()` (Delta) |

Databricks projects also include utilities for querying Snowflake tables (cross-platform data access).

---

## Example: Complete Pipeline

Here's what a real pipeline looks like:

```python
# sales_etl_runner.py
class SalesEtlPipeline:
    def __init__(self, year: int, month: int, _write: bool = True):
        self.etl = ETL()
        self.cache = TableCache(self.etl)
        self._write = _write
        
        # Extract: Pre-load all source tables
        self.cache.preload_tables({
            "orders": TABLE_CONFIGS["orders"].get_full_path(year, month),
            "customers": TABLE_CONFIGS["customers"].get_full_path(),
        })
        
        # Initialize processors with shared cache
        self.aggregate_orders = AggregateOrdersProcessor(self.cache)
        self.enrich_customers = EnrichCustomersProcessor(self.cache)

    def run(self) -> DataFrame:
        # Transform: Chain processors
        df = self.aggregate_orders.process()
        df = self.enrich_customers.process(df)
        
        # Load: Write results
        if self._write:
            self._write_to_snowflake(df)
        return df
```

---

## Requirements

- **Python 3.12+**
- **Snowflake** or **Databricks** account (for running pipelines)

---

## Learn More

For detailed documentation on architecture, best practices, and advanced usage, see [README_DETAILED.md](README_DETAILED.md).

---

## Contributing

Contributions welcome! See our [Contributing Guide](CONTRIBUTING.md).

```bash
# Development setup
git clone https://github.com/dbrown540/pypeline-cli.git
cd pypeline-cli
pip install -e .
pytest
```

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Need Help?

- 📖 [Full Documentation](README_DETAILED.md)
- 🐛 [Report Issues](https://github.com/dbrown540/pypeline-cli/issues)
- 💬 [Discussions](https://github.com/dbrown540/pypeline-cli/discussions)
