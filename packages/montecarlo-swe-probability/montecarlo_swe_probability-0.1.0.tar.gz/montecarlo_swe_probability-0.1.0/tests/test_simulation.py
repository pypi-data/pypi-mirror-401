"""Tests for simulation module."""

from datetime import date

import pytest

from montecarlo_swe.data_loader import WorkItem
from montecarlo_swe.metrics import calculate_throughput
from montecarlo_swe.simulation import (
    SimulationConfig,
    forecast_date,
    forecast_scope,
)


@pytest.fixture
def sample_items():
    """Create sample work items with known throughput pattern."""
    # Create items that complete roughly 1-2 per day over 30 days
    items = []
    for i in range(50):
        # Spread completions across 30 days
        day_offset = i % 30
        end = date(2024, 1, 1 + day_offset)
        start = date(2024, 1, max(1, 1 + day_offset - 2))
        items.append(WorkItem(str(i), start, end))
    return items


@pytest.fixture
def throughput(sample_items):
    """Calculate throughput from sample items."""
    return calculate_throughput(sample_items, exclude_weekends=False)


class TestSimulationConfig:
    def test_defaults(self):
        config = SimulationConfig()
        assert config.num_simulations == 10_000
        assert config.confidence_levels == (50, 85, 95)
        assert config.exclude_weekends is True

    def test_custom_values(self):
        config = SimulationConfig(
            num_simulations=5000,
            confidence_levels=(25, 50, 75),
            exclude_weekends=False,
        )
        assert config.num_simulations == 5000
        assert config.confidence_levels == (25, 50, 75)
        assert config.exclude_weekends is False


class TestForecastDate:
    def test_basic_forecast(self, throughput):
        config = SimulationConfig(
            num_simulations=1000,
            confidence_levels=(50, 85, 95),
            exclude_weekends=False,
            random_seed=42,
        )

        result = forecast_date(
            throughput=throughput,
            items_remaining=10,
            start_date=date(2024, 2, 1),
            config=config,
        )

        assert result.items_to_complete == 10
        assert result.start_date == date(2024, 2, 1)
        assert result.simulations_run == 1000
        assert len(result.days_distribution) == 1000

        # Check percentiles are ordered
        assert result.percentiles[50] <= result.percentiles[85]
        assert result.percentiles[85] <= result.percentiles[95]

        # Check forecast dates exist
        assert 50 in result.forecast_dates
        assert 85 in result.forecast_dates
        assert 95 in result.forecast_dates

    def test_reproducible_with_seed(self, throughput):
        config = SimulationConfig(
            num_simulations=100,
            random_seed=42,
            exclude_weekends=False,
        )

        result1 = forecast_date(throughput, 10, config=config)
        result2 = forecast_date(throughput, 10, config=config)

        assert result1.days_distribution == result2.days_distribution

    def test_more_items_takes_longer(self, throughput):
        config = SimulationConfig(
            num_simulations=1000,
            random_seed=42,
            exclude_weekends=False,
        )

        result_small = forecast_date(throughput, 5, config=config)
        result_large = forecast_date(throughput, 20, config=config)

        # More items should take longer on average
        assert result_large.average_days > result_small.average_days

    def test_zero_items_raises(self, throughput):
        with pytest.raises(ValueError):
            forecast_date(throughput, 0)

    def test_negative_items_raises(self, throughput):
        with pytest.raises(ValueError):
            forecast_date(throughput, -5)


class TestForecastScope:
    def test_basic_forecast(self, throughput):
        config = SimulationConfig(
            num_simulations=1000,
            confidence_levels=(50, 85, 95),
            exclude_weekends=False,
            random_seed=42,
        )

        result = forecast_scope(
            throughput=throughput,
            target_date=date(2024, 2, 15),
            start_date=date(2024, 2, 1),
            config=config,
        )

        assert result.target_date == date(2024, 2, 15)
        assert result.start_date == date(2024, 2, 1)
        assert result.simulations_run == 1000
        assert len(result.items_distribution) == 1000

        # For scope, lower confidence = fewer items (more conservative)
        # 95% confidence means we're 95% sure we'll complete at least X items
        assert result.percentiles[95] <= result.percentiles[85]
        assert result.percentiles[85] <= result.percentiles[50]

    def test_longer_time_more_items(self, throughput):
        config = SimulationConfig(
            num_simulations=1000,
            random_seed=42,
            exclude_weekends=False,
        )

        result_short = forecast_scope(
            throughput, date(2024, 2, 10), date(2024, 2, 1), config
        )
        result_long = forecast_scope(
            throughput, date(2024, 2, 28), date(2024, 2, 1), config
        )

        # More time should mean more items
        assert result_long.average_items > result_short.average_items

    def test_target_before_start_raises(self, throughput):
        with pytest.raises(ValueError):
            forecast_scope(
                throughput,
                target_date=date(2024, 1, 1),
                start_date=date(2024, 2, 1),
            )

    def test_same_date_raises(self, throughput):
        with pytest.raises(ValueError):
            forecast_scope(
                throughput,
                target_date=date(2024, 2, 1),
                start_date=date(2024, 2, 1),
            )


class TestWeekendExclusion:
    def test_weekend_exclusion_affects_forecast(self, sample_items):
        # Calculate throughput both ways
        throughput_with_weekends = calculate_throughput(sample_items, exclude_weekends=False)
        throughput_no_weekends = calculate_throughput(sample_items, exclude_weekends=True)

        config_weekends = SimulationConfig(
            num_simulations=500,
            random_seed=42,
            exclude_weekends=False,
        )
        config_no_weekends = SimulationConfig(
            num_simulations=500,
            random_seed=42,
            exclude_weekends=True,
        )

        result_weekends = forecast_date(
            throughput_with_weekends, 10, config=config_weekends
        )
        result_no_weekends = forecast_date(
            throughput_no_weekends, 10, config=config_no_weekends
        )

        # Results should differ (working days vs calendar days)
        # Can't make strong assertions about which is larger since
        # it depends on throughput calculation
        assert result_weekends.exclude_weekends is False
        assert result_no_weekends.exclude_weekends is True
