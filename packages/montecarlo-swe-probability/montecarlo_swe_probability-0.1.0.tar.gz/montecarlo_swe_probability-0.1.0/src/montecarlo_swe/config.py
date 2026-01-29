"""Configuration loading from TOML files."""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "montecarlo-swe" / "config.toml"


@dataclass
class Config:
    """Application configuration."""

    # Simulation settings
    num_simulations: int = 10_000
    confidence_levels: list[int] = field(default_factory=lambda: [50, 85, 95])
    exclude_weekends: bool = True

    # Data filtering
    sample_size_limit: int | None = None  # Use only last N items
    date_from: str | None = None  # Filter: items completed after this date
    date_to: str | None = None  # Filter: items completed before this date

    # Output settings
    show_histogram: bool = True
    histogram_buckets: int = 10

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        """Create Config from a dictionary (e.g., parsed TOML)."""
        simulation = data.get("simulation", {})
        filtering = data.get("filtering", {})
        output = data.get("output", {})

        return cls(
            num_simulations=simulation.get("num_simulations", cls.num_simulations),
            confidence_levels=simulation.get(
                "confidence_levels", cls().confidence_levels
            ),
            exclude_weekends=simulation.get("exclude_weekends", cls.exclude_weekends),
            sample_size_limit=filtering.get("sample_size_limit"),
            date_from=filtering.get("date_from"),
            date_to=filtering.get("date_to"),
            show_histogram=output.get("show_histogram", cls.show_histogram),
            histogram_buckets=output.get("histogram_buckets", cls.histogram_buckets),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert Config to a dictionary for display."""
        return {
            "simulation": {
                "num_simulations": self.num_simulations,
                "confidence_levels": self.confidence_levels,
                "exclude_weekends": self.exclude_weekends,
            },
            "filtering": {
                "sample_size_limit": self.sample_size_limit,
                "date_from": self.date_from,
                "date_to": self.date_to,
            },
            "output": {
                "show_histogram": self.show_histogram,
                "histogram_buckets": self.histogram_buckets,
            },
        }


def load_config(config_path: Path | None = None) -> Config:
    """Load configuration from a TOML file.

    Args:
        config_path: Path to config file. Uses default location if not specified.

    Returns:
        Config object with loaded or default values
    """
    if config_path is None:
        config_path = DEFAULT_CONFIG_PATH

    if not config_path.exists():
        return Config()

    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return Config.from_dict(data)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Invalid TOML in config file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading config file: {e}")


def get_default_config_template() -> str:
    """Return a template for the config file."""
    return '''# Monte Carlo SWE Probability Configuration
# Location: ~/.config/montecarlo-swe/config.toml

[simulation]
# Number of Monte Carlo simulations to run
num_simulations = 10000

# Confidence levels to report (percentiles)
confidence_levels = [50, 85, 95]

# Exclude weekends from working days calculations
exclude_weekends = true

[filtering]
# Use only the last N data points (comment out to use all)
# sample_size_limit = 100

# Only use items completed after this date (YYYY-MM-DD)
# date_from = "2024-01-01"

# Only use items completed before this date (YYYY-MM-DD)
# date_to = "2024-12-31"

[output]
# Show histogram in text output
show_histogram = true

# Number of buckets for histogram
histogram_buckets = 10
'''
