"""
Centralized error codes for MCP server responses.

Use these constants instead of hardcoded strings to ensure consistency
across MCP servers and enable client-side error handling.
"""

from typing import Literal

# =============================================================================
# Access Control Errors
# =============================================================================

INSUFFICIENT_SCOPE: Literal["INSUFFICIENT_SCOPE"] = "INSUFFICIENT_SCOPE"
"""Write operations not allowed (read-only mode or scope restriction)."""

ADMIN_REQUIRED: Literal["ADMIN_REQUIRED"] = "ADMIN_REQUIRED"
"""Operation requires admin scope."""

ACCESS_DENIED: Literal["ACCESS_DENIED"] = "ACCESS_DENIED"
"""Generic access denied."""

RATE_LIMIT_EXCEEDED: Literal["RATE_LIMIT_EXCEEDED"] = "RATE_LIMIT_EXCEEDED"
"""Rate limit exceeded."""

READ_ONLY_MODE: Literal["READ_ONLY_MODE"] = "READ_ONLY_MODE"
"""Site/system is in read-only mode."""

# =============================================================================
# Resource Errors
# =============================================================================

NOT_FOUND: Literal["NOT_FOUND"] = "NOT_FOUND"
"""Requested entity/resource not found."""

ALREADY_EXISTS: Literal["ALREADY_EXISTS"] = "ALREADY_EXISTS"
"""Entity already exists (duplicate)."""

ENTITY_IN_USE: Literal["ENTITY_IN_USE"] = "ENTITY_IN_USE"
"""Entity is in use and cannot be deleted/modified."""

ENTITY_PROTECTED: Literal["ENTITY_PROTECTED"] = "ENTITY_PROTECTED"
"""Entity is protected and cannot be modified."""

MISSING_DEPENDENCY: Literal["MISSING_DEPENDENCY"] = "MISSING_DEPENDENCY"
"""Required dependency (module, service) is missing."""

# =============================================================================
# Validation Errors
# =============================================================================

VALIDATION_ERROR: Literal["VALIDATION_ERROR"] = "VALIDATION_ERROR"
"""Input validation failed."""

INVALID_NAME: Literal["INVALID_NAME"] = "INVALID_NAME"
"""Invalid machine name format."""

INVALID_FILE_TYPE: Literal["INVALID_FILE_TYPE"] = "INVALID_FILE_TYPE"
"""Invalid file type."""

PAYLOAD_TOO_LARGE: Literal["PAYLOAD_TOO_LARGE"] = "PAYLOAD_TOO_LARGE"
"""Payload exceeds size limit."""

MISSING_REQUIRED: Literal["MISSING_REQUIRED"] = "MISSING_REQUIRED"
"""Required parameter missing."""

# =============================================================================
# Operation Errors
# =============================================================================

INTERNAL_ERROR: Literal["INTERNAL_ERROR"] = "INTERNAL_ERROR"
"""Internal server error."""

OPERATION_FAILED: Literal["OPERATION_FAILED"] = "OPERATION_FAILED"
"""Operation failed."""

TIMEOUT: Literal["TIMEOUT"] = "TIMEOUT"
"""Operation timed out."""

CONFIRMATION_REQUIRED: Literal["CONFIRMATION_REQUIRED"] = "CONFIRMATION_REQUIRED"
"""User confirmation required before destructive operation."""

INVALID_TOOL: Literal["INVALID_TOOL"] = "INVALID_TOOL"
"""Tool not found or invalid."""

EXECUTION_FAILED: Literal["EXECUTION_FAILED"] = "EXECUTION_FAILED"
"""Tool execution failed."""

INSTANTIATION_FAILED: Literal["INSTANTIATION_FAILED"] = "INSTANTIATION_FAILED"
"""Tool instantiation failed."""

# =============================================================================
# Domain-Specific Errors
# =============================================================================

TEMPLATE_NOT_FOUND: Literal["TEMPLATE_NOT_FOUND"] = "TEMPLATE_NOT_FOUND"
"""Template not found."""

CRON_FAILED: Literal["CRON_FAILED"] = "CRON_FAILED"
"""Cron job failed."""

MIGRATION_FAILED: Literal["MIGRATION_FAILED"] = "MIGRATION_FAILED"
"""Migration failed."""

RECIPE_FAILED: Literal["RECIPE_FAILED"] = "RECIPE_FAILED"
"""Recipe application failed."""

CONFIG_ERROR: Literal["CONFIG_ERROR"] = "CONFIG_ERROR"
"""Configuration import/export failed."""

MEDIA_ERROR: Literal["MEDIA_ERROR"] = "MEDIA_ERROR"
"""Media processing failed."""

SERVICE_UNAVAILABLE: Literal["SERVICE_UNAVAILABLE"] = "SERVICE_UNAVAILABLE"
"""External service unavailable."""

# =============================================================================
# Type Definitions
# =============================================================================

ErrorCodeValue = Literal[
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
]

ErrorCategory = Literal["access", "resource", "validation", "operation", "domain"]

# =============================================================================
# All Error Codes
# =============================================================================

ALL_ERROR_CODES: dict[str, str] = {
    "INSUFFICIENT_SCOPE": INSUFFICIENT_SCOPE,
    "ADMIN_REQUIRED": ADMIN_REQUIRED,
    "ACCESS_DENIED": ACCESS_DENIED,
    "RATE_LIMIT_EXCEEDED": RATE_LIMIT_EXCEEDED,
    "READ_ONLY_MODE": READ_ONLY_MODE,
    "NOT_FOUND": NOT_FOUND,
    "ALREADY_EXISTS": ALREADY_EXISTS,
    "ENTITY_IN_USE": ENTITY_IN_USE,
    "ENTITY_PROTECTED": ENTITY_PROTECTED,
    "MISSING_DEPENDENCY": MISSING_DEPENDENCY,
    "VALIDATION_ERROR": VALIDATION_ERROR,
    "INVALID_NAME": INVALID_NAME,
    "INVALID_FILE_TYPE": INVALID_FILE_TYPE,
    "PAYLOAD_TOO_LARGE": PAYLOAD_TOO_LARGE,
    "MISSING_REQUIRED": MISSING_REQUIRED,
    "INTERNAL_ERROR": INTERNAL_ERROR,
    "OPERATION_FAILED": OPERATION_FAILED,
    "TIMEOUT": TIMEOUT,
    "CONFIRMATION_REQUIRED": CONFIRMATION_REQUIRED,
    "INVALID_TOOL": INVALID_TOOL,
    "EXECUTION_FAILED": EXECUTION_FAILED,
    "INSTANTIATION_FAILED": INSTANTIATION_FAILED,
    "TEMPLATE_NOT_FOUND": TEMPLATE_NOT_FOUND,
    "CRON_FAILED": CRON_FAILED,
    "MIGRATION_FAILED": MIGRATION_FAILED,
    "RECIPE_FAILED": RECIPE_FAILED,
    "CONFIG_ERROR": CONFIG_ERROR,
    "MEDIA_ERROR": MEDIA_ERROR,
    "SERVICE_UNAVAILABLE": SERVICE_UNAVAILABLE,
}


# =============================================================================
# ErrorCode Class
# =============================================================================


class ErrorCode:
    """
    Error code namespace combining constants and helpers.

    Example:
        >>> from mcp_error_codes import ErrorCode
        >>>
        >>> # Use constants
        >>> code = ErrorCode.NOT_FOUND
        >>>
        >>> # Use helpers
        >>> ErrorCode.is_valid("NOT_FOUND")  # True
        >>> ErrorCode.get_category(ErrorCode.NOT_FOUND)  # "resource"
        >>> ErrorCode.get_http_status(ErrorCode.NOT_FOUND)  # 404
    """

    # Constants
    INSUFFICIENT_SCOPE = INSUFFICIENT_SCOPE
    ADMIN_REQUIRED = ADMIN_REQUIRED
    ACCESS_DENIED = ACCESS_DENIED
    RATE_LIMIT_EXCEEDED = RATE_LIMIT_EXCEEDED
    READ_ONLY_MODE = READ_ONLY_MODE
    NOT_FOUND = NOT_FOUND
    ALREADY_EXISTS = ALREADY_EXISTS
    ENTITY_IN_USE = ENTITY_IN_USE
    ENTITY_PROTECTED = ENTITY_PROTECTED
    MISSING_DEPENDENCY = MISSING_DEPENDENCY
    VALIDATION_ERROR = VALIDATION_ERROR
    INVALID_NAME = INVALID_NAME
    INVALID_FILE_TYPE = INVALID_FILE_TYPE
    PAYLOAD_TOO_LARGE = PAYLOAD_TOO_LARGE
    MISSING_REQUIRED = MISSING_REQUIRED
    INTERNAL_ERROR = INTERNAL_ERROR
    OPERATION_FAILED = OPERATION_FAILED
    TIMEOUT = TIMEOUT
    CONFIRMATION_REQUIRED = CONFIRMATION_REQUIRED
    INVALID_TOOL = INVALID_TOOL
    EXECUTION_FAILED = EXECUTION_FAILED
    INSTANTIATION_FAILED = INSTANTIATION_FAILED
    TEMPLATE_NOT_FOUND = TEMPLATE_NOT_FOUND
    CRON_FAILED = CRON_FAILED
    MIGRATION_FAILED = MIGRATION_FAILED
    RECIPE_FAILED = RECIPE_FAILED
    CONFIG_ERROR = CONFIG_ERROR
    MEDIA_ERROR = MEDIA_ERROR
    SERVICE_UNAVAILABLE = SERVICE_UNAVAILABLE

    @staticmethod
    def all() -> dict[str, str]:
        """Get all defined error codes."""
        return dict(ALL_ERROR_CODES)

    @staticmethod
    def is_valid(code: str) -> bool:
        """Check if a code is a valid error code."""
        return code in ALL_ERROR_CODES.values()

    @staticmethod
    def get_category(code: str) -> ErrorCategory:
        """Get error category from code."""
        if code in (
            INSUFFICIENT_SCOPE,
            ADMIN_REQUIRED,
            ACCESS_DENIED,
            RATE_LIMIT_EXCEEDED,
            READ_ONLY_MODE,
        ):
            return "access"

        if code in (
            NOT_FOUND,
            ALREADY_EXISTS,
            ENTITY_IN_USE,
            ENTITY_PROTECTED,
            MISSING_DEPENDENCY,
        ):
            return "resource"

        if code in (
            VALIDATION_ERROR,
            INVALID_NAME,
            INVALID_FILE_TYPE,
            PAYLOAD_TOO_LARGE,
            MISSING_REQUIRED,
        ):
            return "validation"

        if code in (
            INTERNAL_ERROR,
            OPERATION_FAILED,
            TIMEOUT,
            CONFIRMATION_REQUIRED,
            INVALID_TOOL,
            EXECUTION_FAILED,
            INSTANTIATION_FAILED,
        ):
            return "operation"

        return "domain"

    @staticmethod
    def is_recoverable(code: str) -> bool:
        """Check if the error is recoverable (client can retry)."""
        return code in (
            RATE_LIMIT_EXCEEDED,
            TIMEOUT,
            SERVICE_UNAVAILABLE,
            INTERNAL_ERROR,
        )

    @staticmethod
    def get_http_status(code: str) -> int:
        """Get suggested HTTP status code for an error."""
        if code in (INSUFFICIENT_SCOPE, ADMIN_REQUIRED, ACCESS_DENIED, READ_ONLY_MODE):
            return 403

        if code == RATE_LIMIT_EXCEEDED:
            return 429

        if code in (NOT_FOUND, TEMPLATE_NOT_FOUND):
            return 404

        if code in (ALREADY_EXISTS, ENTITY_IN_USE, ENTITY_PROTECTED):
            return 409

        if code in (VALIDATION_ERROR, INVALID_NAME, INVALID_FILE_TYPE, MISSING_REQUIRED, INVALID_TOOL):
            return 400

        if code == PAYLOAD_TOO_LARGE:
            return 413

        if code == TIMEOUT:
            return 408

        if code == SERVICE_UNAVAILABLE:
            return 503

        return 500

    @staticmethod
    def get_json_rpc_code(code: str) -> int:
        """
        Get JSON-RPC 2.0 error code for an error.

        JSON-RPC standard codes:
        - -32700: Parse error
        - -32600: Invalid Request
        - -32601: Method not found
        - -32602: Invalid params
        - -32603: Internal error
        - -32000 to -32099: Server-defined errors
        """
        # Map to standard JSON-RPC codes where applicable
        if code in (VALIDATION_ERROR, INVALID_NAME, INVALID_FILE_TYPE, MISSING_REQUIRED):
            return -32602  # Invalid params

        if code == INVALID_TOOL:
            return -32601  # Method not found

        if code in (INTERNAL_ERROR, EXECUTION_FAILED, INSTANTIATION_FAILED):
            return -32603  # Internal error

        # Server-defined errors (-32000 to -32099)
        if code in (ACCESS_DENIED, INSUFFICIENT_SCOPE, ADMIN_REQUIRED):
            return -32001  # Access denied

        if code in (NOT_FOUND, TEMPLATE_NOT_FOUND):
            return -32002  # Not found

        if code == RATE_LIMIT_EXCEEDED:
            return -32003  # Rate limited

        if code == READ_ONLY_MODE:
            return -32004  # Read-only

        if code in (ALREADY_EXISTS, ENTITY_IN_USE, ENTITY_PROTECTED):
            return -32005  # Conflict

        if code == MISSING_DEPENDENCY:
            return -32006  # Missing dependency

        if code == TIMEOUT:
            return -32007  # Timeout

        if code == SERVICE_UNAVAILABLE:
            return -32008  # Service unavailable

        if code == PAYLOAD_TOO_LARGE:
            return -32009  # Payload too large

        if code == CONFIRMATION_REQUIRED:
            return -32010  # Confirmation required

        if code in (OPERATION_FAILED, CRON_FAILED, MIGRATION_FAILED, RECIPE_FAILED, CONFIG_ERROR, MEDIA_ERROR):
            return -32011  # Operation failed

        return -32000  # Generic server error
