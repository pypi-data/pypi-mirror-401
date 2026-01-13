"""Performance metrics export functionality."""

import json
from pathlib import Path

from .models import PerformanceMetrics


class MetricsExporter:
    """Export performance metrics to various formats."""

    @staticmethod
    def export_to_json(metrics: list[PerformanceMetrics], file_path: Path) -> None:
        """
        Export metrics to a JSON file.

        Args:
            metrics: List of PerformanceMetrics objects
            file_path: Path to the output file
        """
        try:
            metrics_data = [
                {
                    "operation_name": metric.operation_name,
                    "execution_time": metric.execution_time,
                    "start_time": metric.start_time,
                    "end_time": metric.end_time,
                    "success": metric.success,
                    "additional_data": metric.additional_data,
                }
                for metric in metrics
            ]

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(metrics_data, f, indent=2, ensure_ascii=False)
        except (OSError, TypeError) as e:
            # Handle file I/O errors and JSON serialization errors
            raise Exception(f"Failed to export metrics to {file_path}: {e}")
