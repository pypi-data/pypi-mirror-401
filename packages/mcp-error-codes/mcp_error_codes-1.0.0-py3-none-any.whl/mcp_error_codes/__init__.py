"""
mcp-error-codes: Standardized MCP error codes with semantic categories.

Example:
    >>> from mcp_error_codes import ErrorCode, McpError, ErrorBag
    >>>
    >>> # Using error codes directly
    >>> if user is None:
    ...     return {"success": False, "code": ErrorCode.NOT_FOUND}
    >>>
    >>> # Using fluent builder
    >>> error = McpError.not_found("user", 123)
    >>> error.get_message()
    "user '123' not found."
    >>>
    >>> # Collecting validation errors
    >>> errors = ErrorBag()
    >>> errors.add_validation("email", "Invalid format")
    >>> errors.add_validation("age", "Must be positive")
    >>> if errors.has_errors():
    ...     return errors.to_dict()
"""

from .error_code import (
    # Constants
    INSUFFICIENT_SCOPE,
    ADMIN_REQUIRED,
    ACCESS_DENIED,
    RATE_LIMIT_EXCEEDED,
    READ_ONLY_MODE,
    NOT_FOUND,
    ALREADY_EXISTS,
    ENTITY_IN_USE,
    ENTITY_PROTECTED,
    MISSING_DEPENDENCY,
    VALIDATION_ERROR,
    INVALID_NAME,
    INVALID_FILE_TYPE,
    PAYLOAD_TOO_LARGE,
    MISSING_REQUIRED,
    INTERNAL_ERROR,
    OPERATION_FAILED,
    TIMEOUT,
    CONFIRMATION_REQUIRED,
    INVALID_TOOL,
    EXECUTION_FAILED,
    INSTANTIATION_FAILED,
    TEMPLATE_NOT_FOUND,
    CRON_FAILED,
    MIGRATION_FAILED,
    RECIPE_FAILED,
    CONFIG_ERROR,
    MEDIA_ERROR,
    SERVICE_UNAVAILABLE,
    # Types
    ErrorCodeValue,
    ErrorCategory,
    # Class
    ErrorCode,
)
from .mcp_error import McpError, ErrorDetails, ErrorDict, JsonRpcError
from .error_bag import ErrorBag, ErrorBagDict

__version__ = "1.0.0"

__all__ = [
    # Version
    "__version__",
    # Error code constants
    "INSUFFICIENT_SCOPE",
    "ADMIN_REQUIRED",
    "ACCESS_DENIED",
    "RATE_LIMIT_EXCEEDED",
    "READ_ONLY_MODE",
    "NOT_FOUND",
    "ALREADY_EXISTS",
    "ENTITY_IN_USE",
    "ENTITY_PROTECTED",
    "MISSING_DEPENDENCY",
    "VALIDATION_ERROR",
    "INVALID_NAME",
    "INVALID_FILE_TYPE",
    "PAYLOAD_TOO_LARGE",
    "MISSING_REQUIRED",
    "INTERNAL_ERROR",
    "OPERATION_FAILED",
    "TIMEOUT",
    "CONFIRMATION_REQUIRED",
    "INVALID_TOOL",
    "EXECUTION_FAILED",
    "INSTANTIATION_FAILED",
    "TEMPLATE_NOT_FOUND",
    "CRON_FAILED",
    "MIGRATION_FAILED",
    "RECIPE_FAILED",
    "CONFIG_ERROR",
    "MEDIA_ERROR",
    "SERVICE_UNAVAILABLE",
    # Types
    "ErrorCodeValue",
    "ErrorCategory",
    # Classes
    "ErrorCode",
    "McpError",
    "ErrorBag",
    # Type aliases
    "ErrorDetails",
    "ErrorDict",
    "JsonRpcError",
    "ErrorBagDict",
]
