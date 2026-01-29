"""Tests for data_loader module."""

import tempfile
from datetime import date
from pathlib import Path

import pytest

from montecarlo_swe.data_loader import (
    DataLoadError,
    WorkItem,
    load_csv,
    parse_date,
    validate_csv,
)


class TestParseDate:
    def test_iso_format(self):
        assert parse_date("2024-01-15", 1, "test") == date(2024, 1, 15)

    def test_us_format(self):
        assert parse_date("01/15/2024", 1, "test") == date(2024, 1, 15)

    def test_invalid_format(self):
        with pytest.raises(DataLoadError) as exc:
            parse_date("invalid", 1, "test_col")
        assert "Cannot parse test_col" in str(exc.value)
        assert "Row 1" in str(exc.value)


class TestWorkItem:
    def test_cycle_time_calculation(self):
        item = WorkItem(
            item_id="TEST-1",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 5),
        )
        assert item.cycle_time_days == 5  # Inclusive

    def test_single_day_cycle_time(self):
        item = WorkItem(
            item_id="TEST-1",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 1),
        )
        assert item.cycle_time_days == 1


class TestLoadCsv:
    def test_load_valid_csv(self, tmp_path):
        csv_content = """item_id,start_date,end_date
TEST-1,2024-01-01,2024-01-03
TEST-2,2024-01-02,2024-01-05
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        items = load_csv(csv_file)

        assert len(items) == 2
        assert items[0].item_id == "TEST-1"
        assert items[0].start_date == date(2024, 1, 1)
        assert items[0].end_date == date(2024, 1, 3)

    def test_load_csv_sorted_by_end_date(self, tmp_path):
        csv_content = """item_id,start_date,end_date
TEST-1,2024-01-05,2024-01-10
TEST-2,2024-01-01,2024-01-03
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        items = load_csv(csv_file)

        # Should be sorted by end_date
        assert items[0].item_id == "TEST-2"
        assert items[1].item_id == "TEST-1"

    def test_missing_required_column(self, tmp_path):
        csv_content = """item_id,start_date
TEST-1,2024-01-01
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        with pytest.raises(DataLoadError) as exc:
            load_csv(csv_file)
        assert "Missing required column 'end_date'" in str(exc.value)

    def test_file_not_found(self):
        with pytest.raises(DataLoadError) as exc:
            load_csv("/nonexistent/file.csv")
        assert "File not found" in str(exc.value)

    def test_end_date_before_start_date(self, tmp_path):
        csv_content = """item_id,start_date,end_date
TEST-1,2024-01-10,2024-01-05
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        with pytest.raises(DataLoadError) as exc:
            load_csv(csv_file)
        assert "end_date" in str(exc.value)
        assert "before" in str(exc.value)

    def test_date_filter_from(self, tmp_path):
        csv_content = """item_id,start_date,end_date
TEST-1,2024-01-01,2024-01-05
TEST-2,2024-01-10,2024-01-15
TEST-3,2024-01-20,2024-01-25
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        items = load_csv(csv_file, date_from=date(2024, 1, 10))

        assert len(items) == 2
        assert items[0].item_id == "TEST-2"

    def test_date_filter_to(self, tmp_path):
        csv_content = """item_id,start_date,end_date
TEST-1,2024-01-01,2024-01-05
TEST-2,2024-01-10,2024-01-15
TEST-3,2024-01-20,2024-01-25
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        items = load_csv(csv_file, date_to=date(2024, 1, 15))

        assert len(items) == 2
        assert items[1].item_id == "TEST-2"

    def test_case_insensitive_columns(self, tmp_path):
        csv_content = """Item_ID,START_DATE,End_Date
TEST-1,2024-01-01,2024-01-03
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        items = load_csv(csv_file)

        assert len(items) == 1
        assert items[0].item_id == "TEST-1"


class TestValidateCsv:
    def test_valid_file(self, tmp_path):
        csv_content = """item_id,start_date,end_date
TEST-1,2024-01-01,2024-01-03
TEST-2,2024-01-02,2024-01-05
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        result = validate_csv(csv_file)

        assert result["valid"] is True
        assert result["item_count"] == 2
        assert result["date_range"]["start"] == "2024-01-03"
        assert result["date_range"]["end"] == "2024-01-05"

    def test_invalid_file(self, tmp_path):
        csv_content = """item_id,start_date
TEST-1,2024-01-01
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        result = validate_csv(csv_file)

        assert result["valid"] is False
        assert len(result["errors"]) > 0
