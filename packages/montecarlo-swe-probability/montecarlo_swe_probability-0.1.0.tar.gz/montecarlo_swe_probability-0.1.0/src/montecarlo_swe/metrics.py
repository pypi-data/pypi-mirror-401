"""Calculate throughput and cycle time metrics from work item data."""

from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta

from .data_loader import WorkItem


@dataclass
class ThroughputMetrics:
    """Daily throughput metrics derived from work items."""

    daily_throughput: list[int]  # Items completed per day (including zeros)
    working_days_throughput: list[int]  # Items completed per working day (non-weekend)
    date_range: tuple[date, date]
    total_items: int
    total_days: int
    total_working_days: int

    @property
    def average_daily_throughput(self) -> float:
        """Average items completed per calendar day."""
        if not self.daily_throughput:
            return 0.0
        return sum(self.daily_throughput) / len(self.daily_throughput)

    @property
    def average_working_day_throughput(self) -> float:
        """Average items completed per working day."""
        if not self.working_days_throughput:
            return 0.0
        return sum(self.working_days_throughput) / len(self.working_days_throughput)


@dataclass
class CycleTimeMetrics:
    """Cycle time metrics derived from work items."""

    cycle_times: list[int]  # Cycle time in days for each item
    min_days: int
    max_days: int
    average_days: float
    median_days: float
    percentile_85: float
    percentile_95: float


def is_weekend(d: date) -> bool:
    """Check if a date falls on a weekend (Saturday=5, Sunday=6)."""
    return d.weekday() >= 5


def calculate_throughput(
    items: list[WorkItem],
    exclude_weekends: bool = True,
) -> ThroughputMetrics:
    """Calculate throughput metrics from work items.

    Throughput is measured as items completed per day, derived from end_dates.

    Args:
        items: List of work items (should be sorted by end_date)
        exclude_weekends: Whether to exclude weekends from working days throughput

    Returns:
        ThroughputMetrics with daily and working day throughput values
    """
    if not items:
        raise ValueError("Cannot calculate throughput from empty item list")

    # Get date range
    min_date = min(item.end_date for item in items)
    max_date = max(item.end_date for item in items)

    # Count items completed on each date
    completion_counts = Counter(item.end_date for item in items)

    # Build daily throughput list (including zero days)
    daily_throughput: list[int] = []
    working_days_throughput: list[int] = []

    current_date = min_date
    while current_date <= max_date:
        count = completion_counts.get(current_date, 0)
        daily_throughput.append(count)

        if not is_weekend(current_date):
            working_days_throughput.append(count)

        current_date += timedelta(days=1)

    return ThroughputMetrics(
        daily_throughput=daily_throughput,
        working_days_throughput=working_days_throughput,
        date_range=(min_date, max_date),
        total_items=len(items),
        total_days=len(daily_throughput),
        total_working_days=len(working_days_throughput),
    )


def calculate_cycle_time(items: list[WorkItem]) -> CycleTimeMetrics:
    """Calculate cycle time metrics from work items.

    Cycle time is the duration from start_date to end_date (inclusive).

    Args:
        items: List of work items

    Returns:
        CycleTimeMetrics with various cycle time statistics
    """
    if not items:
        raise ValueError("Cannot calculate cycle time from empty item list")

    cycle_times = sorted(item.cycle_time_days for item in items)
    n = len(cycle_times)

    def percentile(p: float) -> float:
        """Calculate the p-th percentile."""
        k = (n - 1) * (p / 100)
        f = int(k)
        c = f + 1 if f + 1 < n else f
        return cycle_times[f] + (k - f) * (cycle_times[c] - cycle_times[f])

    return CycleTimeMetrics(
        cycle_times=cycle_times,
        min_days=cycle_times[0],
        max_days=cycle_times[-1],
        average_days=sum(cycle_times) / n,
        median_days=percentile(50),
        percentile_85=percentile(85),
        percentile_95=percentile(95),
    )


def get_working_days_count(start_date: date, end_date: date) -> int:
    """Count working days (Mon-Fri) between two dates, inclusive."""
    if end_date < start_date:
        return 0

    count = 0
    current = start_date
    while current <= end_date:
        if not is_weekend(current):
            count += 1
        current += timedelta(days=1)
    return count


def add_working_days(start_date: date, working_days: int) -> date:
    """Add a number of working days to a start date."""
    if working_days <= 0:
        return start_date

    current = start_date
    days_added = 0

    while days_added < working_days:
        current += timedelta(days=1)
        if not is_weekend(current):
            days_added += 1

    return current
