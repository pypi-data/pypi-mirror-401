"""Performance monitoring utilities for WL Commands.

This module serves as the entry point for the modularized performance monitoring functionality.
主要功能委托给专门的模块以获得更好的组织结构。
"""

from .performance.decorators import (
    clear_metrics,
    end_operation,
    export_metrics,
    get_metrics,
    get_performance_monitor,
    monitor_operation,
    monitor_performance,
    start_operation,
)
from .performance.models import PerformanceMetrics
from .performance.monitor import PerformanceMonitor

# Backward compatibility: re-export all the main components
__all__ = [
    "PerformanceMetrics",
    "PerformanceMonitor",
    "monitor_performance",
    "get_performance_monitor",
    "start_operation",
    "end_operation",
    "monitor_operation",
    "get_metrics",
    "clear_metrics",
    "export_metrics",
]
