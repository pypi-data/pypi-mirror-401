"""
Structured logging implementation for WL Commands.

This file maintains backward compatibility while delegating to the modularized
structured_logging package.
"""

# Import the modularized StructuredLogger from the structured_logging package
# Import datetime for backward compatibility with tests
import datetime as _datetime

from .structured_logging.core import StructuredLogger

# Re-export for backward compatibility
__all__ = ["StructuredLogger"]

# For backward compatibility, expose datetime
datetime = _datetime
