"""Performance monitoring data models."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PerformanceMetrics:
    """Performance metrics for a single operation."""

    operation_name: str
    execution_time: float
    start_time: float
    end_time: float
    success: bool
    additional_data: dict[str, Any] = field(default_factory=dict)
