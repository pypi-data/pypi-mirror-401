import csv
from pathlib import Path
from typing import Union, Optional, List, Dict

from .base import BaseLoader
from ..metrics.store import MetricStore


class CSVLoader(BaseLoader):
    """Loader for CSV log files."""

    def __init__(
        self,
        step_column: Optional[str] = None,
        delimiter: str = ",",
        skip_columns: Optional[List[str]] = None,
    ):
        """Initialize CSV loader.

        Args:
            step_column: Name of the step/iteration column. Auto-detected if None.
            delimiter: CSV delimiter character.
            skip_columns: Column names to skip when loading.
        """
        self.step_column = step_column
        self.delimiter = delimiter
        self.skip_columns = set(skip_columns or [])

        # Common names for step columns
        self._step_column_names = {
            "step", "steps", "iteration", "iterations", "iter",
            "epoch", "global_step", "training_step", "batch", "update"
        }

    def can_load(self, path: Union[str, Path]) -> bool:
        """Check if path is a CSV file."""
        path = Path(path)
        return path.suffix.lower() == ".csv" and path.is_file()

    def load(self, path: Union[str, Path], store: MetricStore) -> None:
        """Load metrics from a CSV file."""
        path = Path(path)

        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)

            if reader.fieldnames is None:
                raise ValueError(f"CSV file has no headers: {path}")

            step_col = self._find_step_column(reader.fieldnames)
            metric_cols = [
                col for col in reader.fieldnames
                if col != step_col and col not in self.skip_columns
            ]

            for row in reader:
                step = self._parse_step(row.get(step_col))
                if step is None:
                    continue

                metrics = {}
                for col in metric_cols:
                    value = self._parse_value(row.get(col))
                    if value is not None:
                        metrics[col] = value

                if metrics:
                    store.log(step, **metrics)

    def _find_step_column(self, columns: List[str]) -> str:
        """Find the step column from available columns."""
        if self.step_column and self.step_column in columns:
            return self.step_column

        # Look for common step column names
        columns_lower = {c.lower(): c for c in columns}
        for name in self._step_column_names:
            if name in columns_lower:
                return columns_lower[name]

        # Default to first column
        return columns[0]

    def _parse_step(self, value: Optional[str]) -> Optional[int]:
        """Parse a step value from string."""
        if value is None or value.strip() == "":
            return None
        try:
            # Handle float step values (convert to int)
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def _parse_value(self, value: Optional[str]) -> Optional[float]:
        """Parse a metric value from string."""
        if value is None or value.strip() == "":
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
