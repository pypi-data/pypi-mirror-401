"""Performance monitoring decorators and utilities."""

import functools
from pathlib import Path
from typing import Any, Callable

from .monitor import PerformanceMonitor


def monitor_performance(operation_name: str, **additional_data: Any):
    """
    Decorator for monitoring the performance of a function.

    Args:
        operation_name: Name of the operation to track
        **additional_data: Additional data to store with the metrics
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            monitor = get_performance_monitor()
            with monitor.monitor_operation(operation_name, **additional_data):
                return func(*args, **kwargs)

        return wrapper

    return decorator


# Global monitor instance
_performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """
    Get the global performance monitor instance.

    Returns:
        The global performance monitor instance
    """
    return _performance_monitor


def start_operation(operation_name: str) -> None:
    """
    Start timing an operation using the global monitor.

    Args:
        operation_name: Name of the operation to track
    """
    _performance_monitor.start_operation(operation_name)


def end_operation(
    operation_name: str, success: bool = True, **additional_data: Any
) -> Any:
    """
    End timing an operation and record metrics using the global monitor.

    Args:
        operation_name: Name of the operation to track
        success: Whether the operation was successful
        **additional_data: Additional data to store with the metrics

    Returns:
        PerformanceMetrics object with the recorded metrics
    """
    return _performance_monitor.end_operation(
        operation_name, success, **additional_data
    )


def monitor_operation(operation_name: str, **additional_data: Any):
    """
    Context manager for monitoring an operation using the global monitor.

    Args:
        operation_name: Name of the operation to track
        **additional_data: Additional data to store with the metrics
    """
    return _performance_monitor.monitor_operation(operation_name, **additional_data)


def get_metrics() -> list[Any]:
    """
    Get all recorded metrics from the global monitor.

    Returns:
        List of PerformanceMetrics objects
    """
    return _performance_monitor.get_metrics()


def clear_metrics() -> None:
    """Clear all recorded metrics from the global monitor."""
    _performance_monitor.clear_metrics()


def export_metrics(file_path: Path) -> None:
    """
    Export metrics to a JSON file using the global monitor.

    Args:
        file_path: Path to the output file
    """
    from .exporter import MetricsExporter

    metrics = _performance_monitor.get_metrics()
    MetricsExporter.export_to_json(metrics, file_path)
