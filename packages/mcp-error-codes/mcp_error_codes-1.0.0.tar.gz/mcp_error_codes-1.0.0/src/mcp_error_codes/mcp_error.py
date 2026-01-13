"""
Fluent error builder for MCP responses.

Example:
    >>> from mcp_error_codes import McpError
    >>>
    >>> # Simple errors
    >>> error = McpError.not_found("user", 123)
    >>> error.get_message()
    "user '123' not found."
    >>>
    >>> # With additional context
    >>> detailed = (
    ...     McpError.validation("email", "Invalid format")
    ...     .with_suggestion("Use a valid email like user@example.com")
    ...     .with_context({"provided": "not-an-email"})
    ... )
"""

from __future__ import annotations

import json
from typing import Any, TypedDict

from .error_code import (
    ACCESS_DENIED,
    ADMIN_REQUIRED,
    ALREADY_EXISTS,
    CONFIRMATION_REQUIRED,
    ENTITY_IN_USE,
    ENTITY_PROTECTED,
    EXECUTION_FAILED,
    INSUFFICIENT_SCOPE,
    INTERNAL_ERROR,
    INVALID_TOOL,
    MISSING_REQUIRED,
    NOT_FOUND,
    OPERATION_FAILED,
    RATE_LIMIT_EXCEEDED,
    SERVICE_UNAVAILABLE,
    TIMEOUT,
    VALIDATION_ERROR,
    ErrorCategory,
    ErrorCode,
)


class ErrorDetails(TypedDict, total=False):
    """Error details structure."""

    field: str
    reason: str
    suggestion: str


class ErrorDict(TypedDict, total=False):
    """Dictionary representation of an error."""

    success: bool
    error: str
    code: str
    category: ErrorCategory
    details: dict[str, Any]


class JsonRpcError(TypedDict):
    """JSON-RPC error structure."""

    code: int
    message: str
    data: dict[str, Any]


class McpError:
    """Fluent MCP error builder."""

    def __init__(self, code: str, message: str) -> None:
        self._code = code
        self._message = message
        self._details: dict[str, Any] = {}
        self._suggestion: str | None = None
        self._retry_after_seconds: int | None = None

    # =========================================================================
    # Factory Methods - Access Errors
    # =========================================================================

    @classmethod
    def access_denied(cls, resource: str | None = None) -> McpError:
        """Create an access denied error."""
        if resource:
            msg = f"Access denied to {resource}."
        else:
            msg = "Access denied."
        return cls(ACCESS_DENIED, msg)

    @classmethod
    def insufficient_scope(cls, required_scope: str) -> McpError:
        """Create an insufficient scope error."""
        return cls(INSUFFICIENT_SCOPE, f"Operation requires '{required_scope}' scope.")

    @classmethod
    def admin_required(cls) -> McpError:
        """Create an admin required error."""
        return cls(ADMIN_REQUIRED, "This operation requires admin privileges.")

    @classmethod
    def rate_limited(cls, retry_after: int | None = None) -> McpError:
        """Create a rate limit exceeded error."""
        error = cls(RATE_LIMIT_EXCEEDED, "Rate limit exceeded.")
        if retry_after is not None:
            error._retry_after_seconds = retry_after
            error._details["retry_after"] = retry_after
        return error

    # =========================================================================
    # Factory Methods - Resource Errors
    # =========================================================================

    @classmethod
    def not_found(cls, entity_type: str, identifier: str | int | None = None) -> McpError:
        """Create a not found error."""
        if identifier is not None:
            msg = f"{entity_type} '{identifier}' not found."
        else:
            msg = f"{entity_type} not found."
        return cls(NOT_FOUND, msg).with_detail("entity_type", entity_type)

    @classmethod
    def already_exists(cls, entity_type: str, identifier: str) -> McpError:
        """Create an already exists error."""
        return cls(ALREADY_EXISTS, f"{entity_type} '{identifier}' already exists.").with_detail(
            "entity_type", entity_type
        )

    @classmethod
    def entity_in_use(
        cls, entity_type: str, identifier: str, used_by: str | None = None
    ) -> McpError:
        """Create an entity in use error."""
        msg = f"{entity_type} '{identifier}' is in use"
        if used_by:
            msg += f" by {used_by}"
        msg += " and cannot be modified."
        return cls(ENTITY_IN_USE, msg).with_detail("entity_type", entity_type)

    @classmethod
    def entity_protected(cls, entity_type: str, identifier: str) -> McpError:
        """Create an entity protected error."""
        return cls(
            ENTITY_PROTECTED,
            f"{entity_type} '{identifier}' is protected and cannot be modified.",
        ).with_detail("entity_type", entity_type)

    # =========================================================================
    # Factory Methods - Validation Errors
    # =========================================================================

    @classmethod
    def validation(cls, field: str, reason: str) -> McpError:
        """Create a validation error."""
        return (
            cls(VALIDATION_ERROR, f"Validation failed for '{field}': {reason}")
            .with_detail("field", field)
            .with_detail("reason", reason)
        )

    @classmethod
    def missing_required(cls, field: str) -> McpError:
        """Create a missing required field error."""
        return cls(MISSING_REQUIRED, f"Required field '{field}' is missing.").with_detail(
            "field", field
        )

    # =========================================================================
    # Factory Methods - Operation Errors
    # =========================================================================

    @classmethod
    def internal(cls, message: str) -> McpError:
        """Create an internal error."""
        return cls(INTERNAL_ERROR, message)

    @classmethod
    def operation_failed(cls, operation: str, reason: str | None = None) -> McpError:
        """Create an operation failed error."""
        msg = f"Operation '{operation}' failed"
        if reason:
            msg += f": {reason}"
        msg += "."
        return cls(OPERATION_FAILED, msg).with_detail("operation", operation)

    @classmethod
    def timeout(cls, operation: str | None = None) -> McpError:
        """Create a timeout error."""
        if operation:
            msg = f"Operation '{operation}' timed out."
        else:
            msg = "Operation timed out."
        return cls(TIMEOUT, msg)

    @classmethod
    def service_unavailable(cls, service: str | None = None) -> McpError:
        """Create a service unavailable error."""
        if service:
            msg = f"Service '{service}' is currently unavailable."
        else:
            msg = "Service is currently unavailable."
        return cls(SERVICE_UNAVAILABLE, msg)

    @classmethod
    def invalid_tool(cls, tool_name: str, reason: str | None = None) -> McpError:
        """Create an invalid tool error."""
        msg = f"Tool '{tool_name}' is invalid"
        if reason:
            msg += f": {reason}"
        msg += "."
        return cls(INVALID_TOOL, msg).with_detail("tool", tool_name)

    @classmethod
    def execution_failed(cls, tool_name: str, reason: str) -> McpError:
        """Create an execution failed error."""
        return cls(EXECUTION_FAILED, f"Tool '{tool_name}' execution failed: {reason}").with_detail(
            "tool", tool_name
        )

    @classmethod
    def confirmation_required(cls, action: str) -> McpError:
        """Create a confirmation required error."""
        return cls(
            CONFIRMATION_REQUIRED,
            f"Action '{action}' requires confirmation. Set confirm=true to proceed.",
        ).with_detail("action", action)

    # =========================================================================
    # Factory Methods - Generic
    # =========================================================================

    @classmethod
    def from_code(cls, code: str, message: str) -> McpError:
        """Create an error from any code and message."""
        return cls(code, message)

    # =========================================================================
    # Builder Methods
    # =========================================================================

    def with_suggestion(self, suggestion: str) -> McpError:
        """Add a suggestion for resolving the error."""
        self._suggestion = suggestion
        self._details["suggestion"] = suggestion
        return self

    def with_context(self, context: dict[str, Any]) -> McpError:
        """Add context information."""
        self._details.update(context)
        return self

    def with_detail(self, key: str, value: Any) -> McpError:
        """Add a single detail."""
        self._details[key] = value
        return self

    def retry_after(self, seconds: int) -> McpError:
        """Set retry-after hint (for rate limiting)."""
        self._retry_after_seconds = seconds
        self._details["retry_after"] = seconds
        return self

    # =========================================================================
    # Getters
    # =========================================================================

    def get_code(self) -> str:
        """Get the error code."""
        return self._code

    def get_raw_message(self) -> str:
        """Get the raw message without formatting."""
        return self._message

    def get_message(self) -> str:
        """Get the formatted message (includes suggestion if set)."""
        if self._suggestion:
            return f"{self._message} {self._suggestion}"
        return self._message

    def get_category(self) -> ErrorCategory:
        """Get the error category."""
        return ErrorCode.get_category(self._code)

    def get_details(self) -> dict[str, Any]:
        """Get the error details."""
        return dict(self._details)

    def get_http_status(self) -> int:
        """Get the HTTP status code."""
        return ErrorCode.get_http_status(self._code)

    def get_json_rpc_code(self) -> int:
        """Get the JSON-RPC error code."""
        return ErrorCode.get_json_rpc_code(self._code)

    def get_retry_after(self) -> int | None:
        """Get the retry-after value in seconds."""
        return self._retry_after_seconds

    # =========================================================================
    # Conversion Methods
    # =========================================================================

    def to_dict(self) -> ErrorDict:
        """Convert to a dictionary."""
        result: ErrorDict = {
            "success": False,
            "error": self.get_message(),
            "code": self._code,
            "category": self.get_category(),
        }

        if self._details:
            result["details"] = self.get_details()

        return result

    def to_json_rpc_error(self) -> JsonRpcError:
        """Convert to JSON-RPC error format."""
        data: dict[str, Any] = {
            "code": self._code,
            "category": self.get_category(),
        }

        if self._details:
            data["details"] = self.get_details()

        return {
            "code": self.get_json_rpc_code(),
            "message": self.get_message(),
            "data": data,
        }

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

        return CallToolResult(  # pragma: no cover
            content=[TextContent(type="text", text=self.get_message())],  # pragma: no cover
            isError=True,  # pragma: no cover
            structuredContent=self.to_dict(),  # pragma: no cover
        )  # pragma: no cover

    def __str__(self) -> str:
        """Convert to string for logging."""
        return f"[{self._code}] {self.get_message()}"

    def __repr__(self) -> str:
        """Return repr string."""
        return f"McpError(code={self._code!r}, message={self._message!r})"

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict())
