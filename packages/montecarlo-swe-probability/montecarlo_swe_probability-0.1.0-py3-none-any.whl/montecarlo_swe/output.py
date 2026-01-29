"""Output formatting for forecast results."""

import json
from datetime import date
from typing import Any

from .simulation import DateForecastResult, ScopeForecastResult


def format_date_forecast_text(
    result: DateForecastResult,
    historical_item_count: int,
    historical_date_range: tuple[date, date],
    show_histogram: bool = True,
    histogram_buckets: int = 10,
) -> str:
    """Format date forecast result as human-readable text."""
    lines = []

    lines.append("")
    lines.append("Monte Carlo Forecast - Date Prediction")
    lines.append("=" * 40)
    lines.append(f"Items remaining: {result.items_to_complete}")
    lines.append(f"Forecast start: {result.start_date}")
    lines.append(f"Simulations: {result.simulations_run:,}")
    lines.append(
        f"Historical data: {historical_item_count} items "
        f"({historical_date_range[0]} to {historical_date_range[1]})"
    )
    if result.exclude_weekends:
        lines.append("Mode: Working days only (excludes weekends)")
    lines.append("")

    lines.append("Forecast Results:")
    for level in sorted(result.percentiles.keys()):
        days = result.percentiles[level]
        forecast_date = result.forecast_dates[level]
        day_type = "working days" if result.exclude_weekends else "days"
        lines.append(f"  {level}% confidence: {forecast_date} ({days} {day_type})")

    if show_histogram:
        lines.append("")
        lines.append("Distribution:")
        lines.append(_format_histogram(result.days_distribution, histogram_buckets))

    return "\n".join(lines)


def format_scope_forecast_text(
    result: ScopeForecastResult,
    historical_item_count: int,
    historical_date_range: tuple[date, date],
    show_histogram: bool = True,
    histogram_buckets: int = 10,
) -> str:
    """Format scope forecast result as human-readable text."""
    lines = []

    lines.append("")
    lines.append("Monte Carlo Forecast - Scope Prediction")
    lines.append("=" * 40)
    lines.append(f"Target date: {result.target_date}")
    lines.append(f"Forecast start: {result.start_date}")
    day_type = "working days" if result.exclude_weekends else "days"
    lines.append(f"Available time: {result.working_days_available} {day_type}")
    lines.append(f"Simulations: {result.simulations_run:,}")
    lines.append(
        f"Historical data: {historical_item_count} items "
        f"({historical_date_range[0]} to {historical_date_range[1]})"
    )
    if result.exclude_weekends:
        lines.append("Mode: Working days only (excludes weekends)")
    lines.append("")

    lines.append("Forecast Results (items completable):")
    for level in sorted(result.percentiles.keys()):
        items = result.percentiles[level]
        lines.append(f"  {level}% confidence: at least {items} items")

    if show_histogram:
        lines.append("")
        lines.append("Distribution:")
        lines.append(_format_histogram(result.items_distribution, histogram_buckets))

    return "\n".join(lines)


def _format_histogram(values: list[int], num_buckets: int = 10) -> str:
    """Create an ASCII histogram from a list of values."""
    if not values:
        return "  (no data)"

    min_val = min(values)
    max_val = max(values)

    if min_val == max_val:
        return f"  All simulations: {min_val}"

    # Create buckets
    bucket_size = (max_val - min_val) / num_buckets
    buckets: list[int] = [0] * num_buckets

    for val in values:
        bucket_idx = int((val - min_val) / bucket_size)
        bucket_idx = min(bucket_idx, num_buckets - 1)  # Handle edge case for max value
        buckets[bucket_idx] += 1

    # Find max count for scaling
    max_count = max(buckets)
    bar_width = 20

    lines = []
    for i, count in enumerate(buckets):
        bucket_start = min_val + (i * bucket_size)
        bucket_end = min_val + ((i + 1) * bucket_size)

        # Scale bar
        bar_len = int((count / max_count) * bar_width) if max_count > 0 else 0
        bar = "█" * bar_len + "░" * (bar_width - bar_len)

        # Calculate percentage
        pct = (count / len(values)) * 100

        lines.append(f"  {bucket_start:5.0f}-{bucket_end:5.0f} │{bar}│ {pct:4.1f}%")

    return "\n".join(lines)


def format_date_forecast_json(
    result: DateForecastResult,
    historical_item_count: int,
    historical_date_range: tuple[date, date],
) -> str:
    """Format date forecast result as JSON."""
    data = {
        "forecast_type": "date",
        "input": {
            "items_remaining": result.items_to_complete,
            "start_date": result.start_date.isoformat(),
            "exclude_weekends": result.exclude_weekends,
        },
        "historical_data": {
            "item_count": historical_item_count,
            "date_range": {
                "start": historical_date_range[0].isoformat(),
                "end": historical_date_range[1].isoformat(),
            },
        },
        "simulation": {
            "runs": result.simulations_run,
        },
        "results": {
            "percentiles": {
                str(level): {
                    "days": days,
                    "date": result.forecast_dates[level].isoformat(),
                }
                for level, days in result.percentiles.items()
            },
            "statistics": {
                "min_days": result.min_days,
                "max_days": result.max_days,
                "average_days": round(result.average_days, 2),
            },
        },
    }
    return json.dumps(data, indent=2)


def format_scope_forecast_json(
    result: ScopeForecastResult,
    historical_item_count: int,
    historical_date_range: tuple[date, date],
) -> str:
    """Format scope forecast result as JSON."""
    data = {
        "forecast_type": "scope",
        "input": {
            "target_date": result.target_date.isoformat(),
            "start_date": result.start_date.isoformat(),
            "working_days_available": result.working_days_available,
            "exclude_weekends": result.exclude_weekends,
        },
        "historical_data": {
            "item_count": historical_item_count,
            "date_range": {
                "start": historical_date_range[0].isoformat(),
                "end": historical_date_range[1].isoformat(),
            },
        },
        "simulation": {
            "runs": result.simulations_run,
        },
        "results": {
            "percentiles": {
                str(level): items for level, items in result.percentiles.items()
            },
            "statistics": {
                "min_items": result.min_items,
                "max_items": result.max_items,
                "average_items": round(result.average_items, 2),
            },
        },
    }
    return json.dumps(data, indent=2)


def format_validation_text(validation_result: dict[str, Any]) -> str:
    """Format CSV validation result as text."""
    lines = []

    if validation_result["valid"]:
        lines.append("")
        lines.append("CSV Validation: PASSED")
        lines.append("=" * 30)
        lines.append(f"Items found: {validation_result['item_count']}")
        lines.append(
            f"Date range: {validation_result['date_range']['start']} "
            f"to {validation_result['date_range']['end']}"
        )
        lines.append("")
        lines.append("Cycle Time Statistics:")
        ct = validation_result["cycle_time"]
        lines.append(f"  Min: {ct['min']} days")
        lines.append(f"  Max: {ct['max']} days")
        lines.append(f"  Avg: {ct['avg']:.1f} days")
    else:
        lines.append("")
        lines.append("CSV Validation: FAILED")
        lines.append("=" * 30)
        for error in validation_result["errors"]:
            lines.append(f"  Error: {error}")

    return "\n".join(lines)


def format_validation_json(validation_result: dict[str, Any]) -> str:
    """Format CSV validation result as JSON."""
    return json.dumps(validation_result, indent=2)


def format_config_text(config_dict: dict[str, Any], config_path: str | None) -> str:
    """Format configuration as text."""
    lines = []
    lines.append("")
    lines.append("Current Configuration")
    lines.append("=" * 30)

    if config_path:
        lines.append(f"Config file: {config_path}")
    else:
        lines.append("Config file: (using defaults)")

    lines.append("")

    for section, values in config_dict.items():
        lines.append(f"[{section}]")
        for key, value in values.items():
            if value is None:
                lines.append(f"  {key} = (not set)")
            else:
                lines.append(f"  {key} = {value}")
        lines.append("")

    return "\n".join(lines)
