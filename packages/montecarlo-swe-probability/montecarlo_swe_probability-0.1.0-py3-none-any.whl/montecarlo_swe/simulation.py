"""Monte Carlo simulation engine for forecasting."""

from dataclasses import dataclass
from datetime import date
from typing import Literal

import numpy as np

from .metrics import ThroughputMetrics, add_working_days, get_working_days_count


@dataclass
class SimulationConfig:
    """Configuration for Monte Carlo simulation."""

    num_simulations: int = 10_000
    confidence_levels: tuple[int, ...] = (50, 85, 95)
    exclude_weekends: bool = True
    random_seed: int | None = None


@dataclass
class DateForecastResult:
    """Result of a date forecast simulation."""

    items_to_complete: int
    start_date: date
    simulations_run: int
    days_distribution: list[int]  # Number of days for each simulation
    percentiles: dict[int, int]  # Confidence level -> days
    forecast_dates: dict[int, date]  # Confidence level -> date
    exclude_weekends: bool

    @property
    def min_days(self) -> int:
        return min(self.days_distribution)

    @property
    def max_days(self) -> int:
        return max(self.days_distribution)

    @property
    def average_days(self) -> float:
        return sum(self.days_distribution) / len(self.days_distribution)


@dataclass
class ScopeForecastResult:
    """Result of a scope forecast simulation."""

    target_date: date
    start_date: date
    working_days_available: int
    simulations_run: int
    items_distribution: list[int]  # Number of items for each simulation
    percentiles: dict[int, int]  # Confidence level -> items
    exclude_weekends: bool

    @property
    def min_items(self) -> int:
        return min(self.items_distribution)

    @property
    def max_items(self) -> int:
        return max(self.items_distribution)

    @property
    def average_items(self) -> float:
        return sum(self.items_distribution) / len(self.items_distribution)


def forecast_date(
    throughput: ThroughputMetrics,
    items_remaining: int,
    start_date: date | None = None,
    config: SimulationConfig | None = None,
) -> DateForecastResult:
    """Forecast when a given number of items will be completed.

    Uses Monte Carlo simulation by sampling from historical throughput data.

    Args:
        throughput: Historical throughput metrics
        items_remaining: Number of items to complete
        start_date: Date to start forecast from (defaults to today)
        config: Simulation configuration

    Returns:
        DateForecastResult with percentile forecasts
    """
    if config is None:
        config = SimulationConfig()

    if start_date is None:
        start_date = date.today()

    if items_remaining <= 0:
        raise ValueError("items_remaining must be positive")

    # Use working days throughput if excluding weekends
    if config.exclude_weekends:
        throughput_data = throughput.working_days_throughput
    else:
        throughput_data = throughput.daily_throughput

    if not throughput_data:
        raise ValueError("No throughput data available")

    # Convert to numpy array for efficient sampling
    throughput_array = np.array(throughput_data, dtype=np.float64)

    # Set random seed if specified
    rng = np.random.default_rng(config.random_seed)

    days_results: list[int] = []

    for _ in range(config.num_simulations):
        total_items = 0
        days = 0

        # Sample throughput values until we reach the target
        while total_items < items_remaining:
            # Sample a random throughput value from historical data
            sampled_throughput = rng.choice(throughput_array)
            total_items += sampled_throughput
            days += 1

        days_results.append(days)

    # Sort for percentile calculation
    days_results.sort()

    # Calculate percentiles
    percentiles: dict[int, int] = {}
    forecast_dates: dict[int, date] = {}

    for level in config.confidence_levels:
        idx = int(len(days_results) * level / 100)
        idx = min(idx, len(days_results) - 1)  # Clamp to valid index
        days = days_results[idx]
        percentiles[level] = days

        if config.exclude_weekends:
            forecast_dates[level] = add_working_days(start_date, days)
        else:
            from datetime import timedelta

            forecast_dates[level] = start_date + timedelta(days=days)

    return DateForecastResult(
        items_to_complete=items_remaining,
        start_date=start_date,
        simulations_run=config.num_simulations,
        days_distribution=days_results,
        percentiles=percentiles,
        forecast_dates=forecast_dates,
        exclude_weekends=config.exclude_weekends,
    )


def forecast_scope(
    throughput: ThroughputMetrics,
    target_date: date,
    start_date: date | None = None,
    config: SimulationConfig | None = None,
) -> ScopeForecastResult:
    """Forecast how many items can be completed by a target date.

    Uses Monte Carlo simulation by sampling from historical throughput data.

    Args:
        throughput: Historical throughput metrics
        target_date: Date by which items should be completed
        start_date: Date to start forecast from (defaults to today)
        config: Simulation configuration

    Returns:
        ScopeForecastResult with percentile forecasts
    """
    if config is None:
        config = SimulationConfig()

    if start_date is None:
        start_date = date.today()

    if target_date <= start_date:
        raise ValueError("target_date must be after start_date")

    # Calculate available days
    if config.exclude_weekends:
        available_days = get_working_days_count(start_date, target_date) - 1
        throughput_data = throughput.working_days_throughput
    else:
        available_days = (target_date - start_date).days
        throughput_data = throughput.daily_throughput

    if available_days <= 0:
        raise ValueError("No working days available between start and target date")

    if not throughput_data:
        raise ValueError("No throughput data available")

    # Convert to numpy array
    throughput_array = np.array(throughput_data, dtype=np.float64)

    # Set random seed if specified
    rng = np.random.default_rng(config.random_seed)

    items_results: list[int] = []

    for _ in range(config.num_simulations):
        # Sample throughput for each available day
        sampled_throughputs = rng.choice(throughput_array, size=available_days)
        total_items = int(np.sum(sampled_throughputs))
        items_results.append(total_items)

    # Sort for percentile calculation
    items_results.sort()

    # Calculate percentiles (note: for scope, lower percentiles = more conservative)
    percentiles: dict[int, int] = {}

    for level in config.confidence_levels:
        # For scope forecasting, we want "at least X items with Y% confidence"
        # So 85% confidence means 85% of simulations achieved at least this many items
        # We use (100 - level) to get the lower bound
        idx = int(len(items_results) * (100 - level) / 100)
        idx = max(0, min(idx, len(items_results) - 1))
        percentiles[level] = items_results[idx]

    return ScopeForecastResult(
        target_date=target_date,
        start_date=start_date,
        working_days_available=available_days,
        simulations_run=config.num_simulations,
        items_distribution=items_results,
        percentiles=percentiles,
        exclude_weekends=config.exclude_weekends,
    )
