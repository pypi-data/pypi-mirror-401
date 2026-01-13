"""
Collection of McpError instances.

Useful for collecting multiple validation errors before returning a response.

Example:
    >>> from mcp_error_codes import ErrorBag, McpError
    >>>
    >>> errors = ErrorBag()
    >>>
    >>> if not input.get("email"):
    ...     errors.add_validation("email", "Required")
    >>> if not input.get("name"):
    ...     errors.add_validation("name", "Required")
    >>>
    >>> if errors.has_errors():
    ...     return errors.to_dict()
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any, TypedDict

from .error_code import ErrorCategory
from .mcp_error import McpError


class ErrorBagDict(TypedDict, total=False):
    """Dictionary representation of an error bag."""

    success: bool
    error: str
    code: str
    error_count: int
    errors: list[dict[str, Any]]


class ErrorBag:
    """Collection of McpError instances."""

    def __init__(self) -> None:
        """Create an empty error bag."""
        self._errors: list[McpError] = []

    @classmethod
    def from_list(cls, errors: list[McpError]) -> ErrorBag:
        """Create an error bag from a list of errors."""
        bag = cls()
        for error in errors:
            bag.add(error)
        return bag

    def add(self, error: McpError) -> ErrorBag:
        """Add an error to the bag."""
        self._errors.append(error)
        return self

    def add_validation(self, field: str, reason: str) -> ErrorBag:
        """Add a validation error to the bag (convenience method)."""
        return self.add(McpError.validation(field, reason))

    def merge(self, other: ErrorBag) -> ErrorBag:
        """Merge another error bag into this one."""
        for error in other._errors:
            self._errors.append(error)
        return self

    def has_errors(self) -> bool:
        """Check if the bag has any errors."""
        return len(self._errors) > 0

    def is_empty(self) -> bool:
        """Check if the bag is empty."""
        return len(self._errors) == 0

    def count(self) -> int:
        """Return the number of errors."""
        return len(self._errors)

    def all(self) -> list[McpError]:
        """Return all errors."""
        return list(self._errors)

    def first(self) -> McpError | None:
        """Return the first error, or None if empty."""
        return self._errors[0] if self._errors else None

    def for_field(self, field: str) -> list[McpError]:
        """Return errors for a specific field (validation errors only)."""
        return [e for e in self._errors if e.get_details().get("field") == field]

    def by_category(self, category: ErrorCategory) -> list[McpError]:
        """Return errors by category."""
        return [e for e in self._errors if e.get_category() == category]

    def clear(self) -> ErrorBag:
        """Clear all errors."""
        self._errors = []
        return self

    def __iter__(self) -> Iterator[McpError]:
        """Make the bag iterable."""
        return iter(self._errors)

    def __len__(self) -> int:
        """Return the number of errors."""
        return len(self._errors)

    # =========================================================================
    # Conversion Methods
    # =========================================================================

    def get_summary_message(self) -> str:
        """Get a summary message for all errors."""
        count = len(self._errors)

        if count == 0:
            return "No errors"

        if count == 1:
            return self._errors[0].get_message()

        # Group by category for smarter summary
        categories: dict[str, int] = {}
        for error in self._errors:
            cat = error.get_category()
            categories[cat] = categories.get(cat, 0) + 1

        if len(categories) == 1 and "validation" in categories:
            return f"{count} validation errors occurred."

        return f"{count} errors occurred."

    def to_dict(self) -> ErrorBagDict:
        """Convert to dictionary format."""
        if not self._errors:
            return {
                "success": True,
                "errors": [],
            }

        # Use first error as primary
        primary = self._errors[0]
        result: ErrorBagDict = {
            "success": False,
            "error": self.get_summary_message(),
            "code": primary.get_code(),
            "error_count": len(self._errors),
            "errors": [],
        }

        # Collect all error details
        for error in self._errors:
            result["errors"].append(
                {
                    "message": error.get_raw_message(),
                    "code": error.get_code(),
                    "details": error.get_details(),
                }
            )

        return result

    def to_call_tool_result(self) -> Any:
        """
        Convert to MCP CallToolResult (requires mcp package).

        Raises:
            ImportError: If mcp package is not installed.
        """
        try:
            from mcp.types import CallToolResult, TextContent  # pragma: no cover
        except ImportError:
            raise ImportError(
                "mcp package is required for to_call_tool_result(). "
                "Install with: pip install mcp"
            ) from None

        if not self._errors:  # pragma: no cover
            return CallToolResult(  # pragma: no cover
                content=[TextContent(type="text", text="No errors")],  # pragma: no cover
                isError=False,  # pragma: no cover
                structuredContent={"success": True},  # pragma: no cover
            )  # pragma: no cover

        return CallToolResult(  # pragma: no cover
            content=[TextContent(type="text", text=self.get_summary_message())],  # pragma: no cover
            isError=True,  # pragma: no cover
            structuredContent=self.to_dict(),  # pragma: no cover
        )  # pragma: no cover

    def to_json_rpc_error(self) -> dict[str, Any]:
        """
        Convert to JSON-RPC Error (uses first error).

        Raises:
            ValueError: If bag is empty.
        """
        if not self._errors:
            raise ValueError("Cannot convert empty ErrorBag to JsonRpcError")

        primary = self._errors[0]
        data = self.to_dict()
        # Remove success and error from data
        data.pop("success", None)
        data.pop("error", None)

        return {
            "code": primary.get_json_rpc_code(),
            "message": self.get_summary_message(),
            "data": data,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())
