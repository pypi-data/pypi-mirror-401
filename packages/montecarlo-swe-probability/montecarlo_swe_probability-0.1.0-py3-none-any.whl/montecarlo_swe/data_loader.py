"""CSV data loading and validation for historical work item data."""

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterator


@dataclass
class WorkItem:
    """Represents a single work item with start and end dates."""

    item_id: str | None
    start_date: date
    end_date: date
    item_type: str | None = None

    @property
    def cycle_time_days(self) -> int:
        """Calculate cycle time in calendar days (inclusive)."""
        return (self.end_date - self.start_date).days + 1


class DataLoadError(Exception):
    """Raised when data loading or validation fails."""

    pass


def parse_date(date_str: str, row_num: int, column: str) -> date:
    """Parse a date string in various formats.

    Supports: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY
    """
    date_str = date_str.strip()

    formats = [
        "%Y-%m-%d",  # ISO format: 2024-01-15
        "%m/%d/%Y",  # US format: 01/15/2024
        "%d/%m/%Y",  # EU format: 15/01/2024
        "%Y/%m/%d",  # Alternative: 2024/01/15
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise DataLoadError(
        f"Row {row_num}: Cannot parse {column} '{date_str}'. "
        f"Expected format: YYYY-MM-DD (e.g., 2024-01-15)"
    )


def validate_work_item(item: WorkItem, row_num: int) -> None:
    """Validate a work item for logical consistency."""
    if item.end_date < item.start_date:
        raise DataLoadError(
            f"Row {row_num}: end_date ({item.end_date}) is before "
            f"start_date ({item.start_date})"
        )


def load_csv(
    file_path: str | Path,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[WorkItem]:
    """Load work items from a CSV file.

    Args:
        file_path: Path to the CSV file
        date_from: Optional filter - only include items completed on or after this date
        date_to: Optional filter - only include items completed on or before this date

    Returns:
        List of WorkItem objects sorted by end_date

    Raises:
        DataLoadError: If the file cannot be read or contains invalid data
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise DataLoadError(f"File not found: {file_path}")

    if not file_path.suffix.lower() == ".csv":
        raise DataLoadError(f"Expected CSV file, got: {file_path.suffix}")

    items: list[WorkItem] = []

    try:
        with open(file_path, newline="", encoding="utf-8") as f:
            # Detect delimiter
            sample = f.read(1024)
            f.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel  # Default to comma-separated

            reader = csv.DictReader(f, dialect=dialect)

            # Validate required columns
            if reader.fieldnames is None:
                raise DataLoadError("CSV file appears to be empty")

            fieldnames_lower = [fn.lower().strip() for fn in reader.fieldnames]

            if "start_date" not in fieldnames_lower:
                raise DataLoadError(
                    f"Missing required column 'start_date'. "
                    f"Found columns: {', '.join(reader.fieldnames)}"
                )
            if "end_date" not in fieldnames_lower:
                raise DataLoadError(
                    f"Missing required column 'end_date'. "
                    f"Found columns: {', '.join(reader.fieldnames)}"
                )

            # Map actual column names (case-insensitive)
            column_map = {fn.lower().strip(): fn for fn in reader.fieldnames}

            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                # Get dates (required)
                start_str = row.get(column_map.get("start_date", ""), "").strip()
                end_str = row.get(column_map.get("end_date", ""), "").strip()

                if not start_str:
                    raise DataLoadError(f"Row {row_num}: Missing start_date")
                if not end_str:
                    raise DataLoadError(f"Row {row_num}: Missing end_date")

                start_date = parse_date(start_str, row_num, "start_date")
                end_date = parse_date(end_str, row_num, "end_date")

                # Get optional fields
                item_id = row.get(column_map.get("item_id", ""), "").strip() or None
                item_type = row.get(column_map.get("item_type", ""), "").strip() or None

                item = WorkItem(
                    item_id=item_id,
                    start_date=start_date,
                    end_date=end_date,
                    item_type=item_type,
                )

                validate_work_item(item, row_num)

                # Apply date filters
                if date_from and item.end_date < date_from:
                    continue
                if date_to and item.end_date > date_to:
                    continue

                items.append(item)

    except UnicodeDecodeError as e:
        raise DataLoadError(f"File encoding error: {e}. Try saving as UTF-8.")
    except csv.Error as e:
        raise DataLoadError(f"CSV parsing error: {e}")

    if not items:
        if date_from or date_to:
            raise DataLoadError(
                "No work items found within the specified date range. "
                "Check your date filters."
            )
        raise DataLoadError("CSV file contains no valid work items")

    # Sort by end_date
    items.sort(key=lambda x: x.end_date)

    return items


def validate_csv(file_path: str | Path) -> dict:
    """Validate a CSV file and return summary statistics.

    Returns:
        Dictionary with validation results and statistics
    """
    try:
        items = load_csv(file_path)

        cycle_times = [item.cycle_time_days for item in items]
        date_range_start = min(item.end_date for item in items)
        date_range_end = max(item.end_date for item in items)

        return {
            "valid": True,
            "item_count": len(items),
            "date_range": {
                "start": date_range_start.isoformat(),
                "end": date_range_end.isoformat(),
            },
            "cycle_time": {
                "min": min(cycle_times),
                "max": max(cycle_times),
                "avg": sum(cycle_times) / len(cycle_times),
            },
            "errors": [],
        }
    except DataLoadError as e:
        return {
            "valid": False,
            "item_count": 0,
            "errors": [str(e)],
        }
