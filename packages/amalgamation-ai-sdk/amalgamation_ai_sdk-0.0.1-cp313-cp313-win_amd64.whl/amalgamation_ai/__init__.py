"""AmalgamationAI Python SDK.

Official Python SDK for AmalgamationAI - AI Vision Blueprint Platform.

Usage:
    >>> import asyncio
    >>> from amalgamation_ai import AmalgamationAISDK
    >>>
    >>> async def main():
    ...     async with AmalgamationAISDK(api_key="aai_...") as client:
    ...         result = await client.generate_blueprint(
    ...             prompt="Count people in image",
    ...             images=["photo.jpg"]
    ...         )
    ...         print(result.blueprint)  # allow-print
    >>>
    >>> asyncio.run(main())

Simplified usage with run() helper:
    >>> from amalgamation_ai import AmalgamationAISDK, run
    >>>
    >>> async def task():
    ...     async with AmalgamationAISDK(api_key="...") as client:
    ...         return await client.generate_blueprint(prompt="...")
    >>>
    >>> result = run(task())
"""

# Helper function: simplify sync execution
import asyncio
from typing import Coroutine, TypeVar

from .__version__ import __version__
from .client import AmalgamationAISDK
from .exceptions import (
    AmalgamationAIError,
    APIError,
    AuthenticationError,
    TimeoutError,
    ValidationError,
)

T = TypeVar("T")


def run(coro: Coroutine[None, None, T]) -> T:
    """Run async function in sync code (helper function).

    Args:
        coro (Coroutine[None, None, T]): The coroutine to run.

    Returns:
        T (Any): The result of the coroutine.

    Examples:
        >>> from amalgamation_ai import AmalgamationAISDK, run
        >>>
        >>> async def task():
        ...     async with AmalgamationAISDK(api_key="...") as client:
        ...         return await client.generate_blueprint(prompt="...")
        >>>
        >>> result = run(task())
    """
    return asyncio.run(coro)


__all__ = [
    "__version__",
    "AmalgamationAISDK",
    "run",
    # Exceptions
    "AmalgamationAIError",
    "AuthenticationError",
    "ValidationError",
    "TimeoutError",
    "APIError",
]
