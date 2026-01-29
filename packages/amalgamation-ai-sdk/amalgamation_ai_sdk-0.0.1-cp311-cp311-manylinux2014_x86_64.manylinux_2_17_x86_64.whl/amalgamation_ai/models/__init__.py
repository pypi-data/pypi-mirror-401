"""Data models for AmalgamationAI SDK."""

from .blueprint import BlueprintGenerationResponse, GenerationResult, GenerationStatus
from .common import ErrorResponse, StatusEnum
from .execution import ExecutionResult, ExecutionStatus

__all__ = [
    "StatusEnum",
    "ErrorResponse",
    "GenerationResult",
    "GenerationStatus",
    "ExecutionResult",
    "ExecutionStatus",
    # Backward compatibility
    "BlueprintGenerationResponse",  # Deprecated, use GenerationResult
]
