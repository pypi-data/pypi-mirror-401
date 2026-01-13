"""Core performance monitoring functionality."""

import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable

from .models import PerformanceMetrics


class PerformanceMonitor:
    """A utility class for monitoring performance of operations."""

    def __init__(self):
        self._metrics: list[PerformanceMetrics] = []
        self._active_operations: dict[str, float] = {}

    def start_operation(self, operation_name: str) -> None:
        """
        Start timing an operation.

        Args:
            operation_name: Name of the operation to track
        """
        self._active_operations[operation_name] = time.perf_counter()

    def end_operation(
        self, operation_name: str, success: bool = True, **additional_data: Any
    ) -> PerformanceMetrics:
        """
        End timing an operation and record metrics.

        Args:
            operation_name: Name of the operation to track
            success: Whether the operation was successful
            **additional_data: Additional data to store with the metrics

        Returns:
            PerformanceMetrics object with the recorded metrics
        """
        if operation_name not in self._active_operations:
            raise ValueError(f"Operation '{operation_name}' was not started")

        start_time = self._active_operations.pop(operation_name)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        metrics = PerformanceMetrics(
            operation_name=operation_name,
            execution_time=execution_time,
            start_time=start_time,
            end_time=end_time,
            success=success,
            additional_data=additional_data,
        )

        self._metrics.append(metrics)
        return metrics

    def record_operation(
        self,
        operation_name: str,
        execution_time: float,
        success: bool = True,
        **additional_data: Any,
    ) -> PerformanceMetrics:
        """
        Record metrics for an operation without timing it.

        Args:
            operation_name: Name of the operation to track
            execution_time: Execution time in seconds
            success: Whether the operation was successful
            **additional_data: Additional data to store with the metrics

        Returns:
            PerformanceMetrics object with the recorded metrics
        """
        start_time = time.perf_counter() - execution_time
        end_time = start_time + execution_time

        metrics = PerformanceMetrics(
            operation_name=operation_name,
            execution_time=execution_time,
            start_time=start_time,
            end_time=end_time,
            success=success,
            additional_data=additional_data,
        )

        self._metrics.append(metrics)
        return metrics

    @contextmanager
    def monitor_operation(self, operation_name: str, **additional_data: Any):
        """
        Context manager for monitoring an operation.

        Args:
            operation_name: Name of the operation to track
            **additional_data: Additional data to store with the metrics
        """
        self.start_operation(operation_name)
        success = True
        try:
            yield
        except Exception:
            success = False
            raise
        finally:
            try:
                self.end_operation(operation_name, success, **additional_data)
            except ValueError:
                # Operation was not started, ignore
                pass

    def get_metrics(self) -> list[PerformanceMetrics]:
        """
        Get all recorded metrics.

        Returns:
            List of PerformanceMetrics objects
        """
        return self._metrics.copy()

    def get_average_execution_time(self, operation_name: str) -> float | None:
        """
        Get the average execution time for an operation.

        Args:
            operation_name: Name of the operation

        Returns:
            Average execution time in seconds, or None if no metrics found
        """
        times = [
            metric.execution_time
            for metric in self._metrics
            if metric.operation_name == operation_name
        ]

        if not times:
            return None

        return sum(times) / len(times)

    def clear_metrics(self) -> None:
        """Clear all recorded metrics."""
        self._metrics.clear()
        self._active_operations.clear()

    def export_metrics(self, file_path: Path) -> None:
        """
        Export metrics to a JSON file.

        Args:
            file_path: Path to the output file
        """
        from .exporter import MetricsExporter

        MetricsExporter.export_to_json(self._metrics, file_path)
