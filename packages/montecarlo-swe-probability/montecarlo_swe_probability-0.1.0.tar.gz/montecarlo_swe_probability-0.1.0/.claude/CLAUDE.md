# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

**montecarlo-swe-probability** (`mcswe`) is a Python CLI tool that uses Monte Carlo simulation to forecast delivery dates and scope for software engineering teams based on historical throughput data.

## Key Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_simulation.py -v

# Run CLI commands
mcswe --help
mcswe validate examples/sample_data.csv
mcswe forecast date --items 20 --data examples/sample_data.csv
mcswe forecast scope --target-date 2026-03-01 --data examples/sample_data.csv
mcswe config show
```

## Architecture

```
src/montecarlo_swe/
├── cli.py          # Click CLI entry point (main command group)
├── simulation.py   # Monte Carlo engine (forecast_date, forecast_scope)
├── data_loader.py  # CSV parsing & validation (load_csv, WorkItem)
├── metrics.py      # Throughput & cycle time calculations
├── output.py       # Text, JSON, histogram formatters
└── config.py       # TOML config loading (~/.config/montecarlo-swe/config.toml)
```

## Core Concepts

- **Throughput**: Items completed per day, derived from `end_date` in historical data
- **Date Forecasting**: Given X items, when will they be done? (samples throughput until target reached)
- **Scope Forecasting**: Given a target date, how many items can be completed? (samples throughput for available days)
- **Confidence Levels**: Results reported at percentiles (default: 50%, 85%, 95%)

## Data Format

CSV with required columns `start_date` and `end_date` (YYYY-MM-DD format):

```csv
item_id,start_date,end_date
PROJ-101,2024-01-05,2024-01-08
PROJ-102,2024-01-06,2024-01-10
```

## Dependencies

- Python 3.11+
- click (CLI framework)
- numpy (random sampling, array operations)
- pytest (testing)

## Testing

44 unit tests covering data loading, metrics calculation, and simulation logic. Tests use `pytest` with fixtures defined in test files. All tests should pass before merging changes.

## Configuration

TOML config file at `~/.config/montecarlo-swe/config.toml` supports:
- `num_simulations`: Number of Monte Carlo runs (default: 10000)
- `confidence_levels`: Percentiles to report (default: [50, 85, 95])
- `exclude_weekends`: Skip weekends in calculations (default: true)
- `sample_size_limit`: Use only last N data points
- `date_from`/`date_to`: Filter historical data by date range
