"""
AegisLog SDK - Fire-and-Forget Evidence Logging

EU AI Act Article 12 compliant evidence collection for AI systems.
"""

from .client import (
    AegisLog,
    AegisLogAsync,
    PolicyContext,
    DataProvenance,
    HumanIntervention,
    ModelContext,
    SessionContext,
    PerformanceMetrics,
    Receipt,
    VerificationResult,
)
from .exceptions import AegisLogError, AegisLogAPIError, AegisLogValidationError
from .auto_logger import (
    wrap_openai,
    wrap_anthropic,
    auto_log,
    AegisLogConfig,
    LoggingContext,
)

__version__ = "3.0.0"  # Added P0 compliance schema fields
__all__ = [
    # Core clients
    "AegisLog",
    "AegisLogAsync",
    # Auto-logging wrappers
    "wrap_openai",
    "wrap_anthropic",
    "auto_log",
    "AegisLogConfig",
    "LoggingContext",
    # Compliance schema objects
    "PolicyContext",
    "DataProvenance",
    "HumanIntervention",
    "ModelContext",
    "SessionContext",
    "PerformanceMetrics",
    # Response types
    "Receipt",
    "VerificationResult",
    # Exceptions
    "AegisLogError",
    "AegisLogAPIError",
    "AegisLogValidationError",
]
