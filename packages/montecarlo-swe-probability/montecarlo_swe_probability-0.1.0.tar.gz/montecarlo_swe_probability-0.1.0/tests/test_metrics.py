"""Tests for metrics module."""

from datetime import date

import pytest

from montecarlo_swe.data_loader import WorkItem
from montecarlo_swe.metrics import (
    add_working_days,
    calculate_cycle_time,
    calculate_throughput,
    get_working_days_count,
    is_weekend,
)


class TestIsWeekend:
    def test_weekday(self):
        # Monday 2024-01-15
        assert is_weekend(date(2024, 1, 15)) is False

    def test_saturday(self):
        # Saturday 2024-01-13
        assert is_weekend(date(2024, 1, 13)) is True

    def test_sunday(self):
        # Sunday 2024-01-14
        assert is_weekend(date(2024, 1, 14)) is True


class TestGetWorkingDaysCount:
    def test_full_week(self):
        # Monday to Friday
        start = date(2024, 1, 15)  # Monday
        end = date(2024, 1, 19)  # Friday
        assert get_working_days_count(start, end) == 5

    def test_includes_weekend(self):
        # Monday to next Monday (7 days, 6 working days)
        start = date(2024, 1, 15)  # Monday
        end = date(2024, 1, 22)  # Next Monday
        assert get_working_days_count(start, end) == 6

    def test_same_day(self):
        d = date(2024, 1, 15)  # Monday
        assert get_working_days_count(d, d) == 1

    def test_weekend_only(self):
        start = date(2024, 1, 13)  # Saturday
        end = date(2024, 1, 14)  # Sunday
        assert get_working_days_count(start, end) == 0


class TestAddWorkingDays:
    def test_add_five_days_no_weekend(self):
        start = date(2024, 1, 15)  # Monday
        result = add_working_days(start, 5)
        assert result == date(2024, 1, 22)  # Next Monday (skips weekend)

    def test_add_zero_days(self):
        start = date(2024, 1, 15)
        result = add_working_days(start, 0)
        assert result == start

    def test_add_one_day(self):
        start = date(2024, 1, 15)  # Monday
        result = add_working_days(start, 1)
        assert result == date(2024, 1, 16)  # Tuesday


class TestCalculateThroughput:
    def test_basic_throughput(self):
        items = [
            WorkItem("1", date(2024, 1, 15), date(2024, 1, 15)),
            WorkItem("2", date(2024, 1, 15), date(2024, 1, 16)),
            WorkItem("3", date(2024, 1, 16), date(2024, 1, 16)),
        ]

        result = calculate_throughput(items, exclude_weekends=False)

        assert result.total_items == 3
        assert result.date_range == (date(2024, 1, 15), date(2024, 1, 16))
        # Throughput is based on end_date: 1 item ends on 1/15, 2 items end on 1/16
        assert result.daily_throughput == [1, 2]

    def test_throughput_with_gap_days(self):
        items = [
            WorkItem("1", date(2024, 1, 15), date(2024, 1, 15)),
            WorkItem("2", date(2024, 1, 17), date(2024, 1, 17)),
        ]

        result = calculate_throughput(items, exclude_weekends=False)

        # Should include zero for 1/16
        assert result.daily_throughput == [1, 0, 1]

    def test_empty_items_raises(self):
        with pytest.raises(ValueError):
            calculate_throughput([])

    def test_working_days_excludes_weekends(self):
        # Items completed on Fri, Sat, Sun, Mon
        items = [
            WorkItem("1", date(2024, 1, 12), date(2024, 1, 12)),  # Friday
            WorkItem("2", date(2024, 1, 13), date(2024, 1, 13)),  # Saturday
            WorkItem("3", date(2024, 1, 14), date(2024, 1, 14)),  # Sunday
            WorkItem("4", date(2024, 1, 15), date(2024, 1, 15)),  # Monday
        ]

        result = calculate_throughput(items, exclude_weekends=True)

        # Working days throughput should only include Fri (1) and Mon (1)
        assert result.working_days_throughput == [1, 1]
        # Daily throughput includes all days
        assert result.daily_throughput == [1, 1, 1, 1]


class TestCalculateCycleTime:
    def test_basic_cycle_time(self):
        items = [
            WorkItem("1", date(2024, 1, 1), date(2024, 1, 3)),  # 3 days
            WorkItem("2", date(2024, 1, 1), date(2024, 1, 5)),  # 5 days
            WorkItem("3", date(2024, 1, 1), date(2024, 1, 2)),  # 2 days
        ]

        result = calculate_cycle_time(items)

        assert result.min_days == 2
        assert result.max_days == 5
        assert result.average_days == pytest.approx(10 / 3, rel=0.01)
        assert result.cycle_times == [2, 3, 5]  # Sorted

    def test_empty_items_raises(self):
        with pytest.raises(ValueError):
            calculate_cycle_time([])

    def test_percentiles(self):
        # Create 100 items with cycle times 1-100 days
        from datetime import timedelta

        base_date = date(2024, 1, 1)
        items = [
            WorkItem(str(i), base_date, base_date + timedelta(days=i))
            for i in range(100)
        ]

        result = calculate_cycle_time(items)

        # Median should be around 50-51
        assert 49 <= result.median_days <= 52
        # 85th percentile should be around 85
        assert 84 <= result.percentile_85 <= 87
        # 95th percentile should be around 95
        assert 94 <= result.percentile_95 <= 97
