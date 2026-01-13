# mcp-error-codes

Standardized MCP error codes with semantic categories, HTTP/JSON-RPC mapping, and fluent builders for Python.

## Installation

```bash
pip install mcp-error-codes
```

## Features

- **28 predefined error codes** covering access, resource, validation, operation, and domain errors
- **Semantic categories** for error classification
- **HTTP status code mapping** for REST APIs
- **JSON-RPC 2.0 code mapping** for MCP protocol compliance
- **Fluent error builder** (`McpError`) for creating rich error responses
- **Error collection** (`ErrorBag`) for aggregating multiple validation errors
- **Full type hints** with strict mypy compliance
- **Zero runtime dependencies**

## Quick Start

### Using Error Codes Directly

```python
from mcp_error_codes import ErrorCode, NOT_FOUND

# Use constants
if user is None:
    return {"success": False, "code": NOT_FOUND}

# Use helper methods
ErrorCode.is_valid("NOT_FOUND")           # True
ErrorCode.get_category(NOT_FOUND)         # "resource"
ErrorCode.get_http_status(NOT_FOUND)      # 404
ErrorCode.get_json_rpc_code(NOT_FOUND)    # -32002
ErrorCode.is_recoverable(NOT_FOUND)       # False
```

### Using Fluent Error Builder

```python
from mcp_error_codes import McpError

# Simple errors
error = McpError.not_found("User", 123)
print(error.get_message())  # "User '123' not found."
print(error.get_http_status())  # 404

# With suggestions and context
detailed = (
    McpError.validation("email", "Invalid format")
    .with_suggestion("Use a valid email like user@example.com")
    .with_context({"provided": "not-an-email"})
)

# Convert to different formats
detailed.to_dict()          # {"success": False, "error": "...", ...}
detailed.to_json_rpc_error()  # {"code": -32602, "message": "...", ...}
```

### Collecting Multiple Errors

```python
from mcp_error_codes import ErrorBag, McpError

errors = ErrorBag()

if not data.get("email"):
    errors.add_validation("email", "Required")
if not data.get("name"):
    errors.add_validation("name", "Required")
if data.get("age", 0) < 0:
    errors.add(McpError.validation("age", "Must be positive"))

if errors.has_errors():
    return errors.to_dict()
    # {
    #   "success": False,
    #   "error": "3 validation errors occurred.",
    #   "code": "VALIDATION_ERROR",
    #   "error_count": 3,
    #   "errors": [...]
    # }
```

## Error Codes

### Access Control

| Code | Description | HTTP | JSON-RPC |
|------|-------------|------|----------|
| `INSUFFICIENT_SCOPE` | Write operations not allowed | 403 | -32001 |
| `ADMIN_REQUIRED` | Admin privileges required | 403 | -32001 |
| `ACCESS_DENIED` | Generic access denied | 403 | -32001 |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded | 429 | -32003 |
| `READ_ONLY_MODE` | System in read-only mode | 403 | -32004 |

### Resource

| Code | Description | HTTP | JSON-RPC |
|------|-------------|------|----------|
| `NOT_FOUND` | Resource not found | 404 | -32002 |
| `ALREADY_EXISTS` | Resource already exists | 409 | -32005 |
| `ENTITY_IN_USE` | Cannot delete, entity in use | 409 | -32005 |
| `ENTITY_PROTECTED` | Entity is protected | 409 | -32005 |
| `MISSING_DEPENDENCY` | Required dependency missing | 500 | -32006 |

### Validation

| Code | Description | HTTP | JSON-RPC |
|------|-------------|------|----------|
| `VALIDATION_ERROR` | Input validation failed | 400 | -32602 |
| `INVALID_NAME` | Invalid machine name | 400 | -32602 |
| `INVALID_FILE_TYPE` | Invalid file type | 400 | -32602 |
| `PAYLOAD_TOO_LARGE` | Payload exceeds limit | 413 | -32009 |
| `MISSING_REQUIRED` | Required parameter missing | 400 | -32602 |

### Operation

| Code | Description | HTTP | JSON-RPC |
|------|-------------|------|----------|
| `INTERNAL_ERROR` | Internal server error | 500 | -32603 |
| `OPERATION_FAILED` | Operation failed | 500 | -32011 |
| `TIMEOUT` | Operation timed out | 408 | -32007 |
| `CONFIRMATION_REQUIRED` | Needs user confirmation | 500 | -32010 |
| `INVALID_TOOL` | Tool not found/invalid | 400 | -32601 |
| `EXECUTION_FAILED` | Tool execution failed | 500 | -32603 |
| `INSTANTIATION_FAILED` | Tool instantiation failed | 500 | -32603 |

## API Reference

### ErrorCode

```python
# All error code constants
ErrorCode.NOT_FOUND
ErrorCode.VALIDATION_ERROR
# ... etc

# Helper methods
ErrorCode.all() -> dict[str, str]
ErrorCode.is_valid(code: str) -> bool
ErrorCode.get_category(code: str) -> Literal["access", "resource", "validation", "operation", "domain"]
ErrorCode.is_recoverable(code: str) -> bool
ErrorCode.get_http_status(code: str) -> int
ErrorCode.get_json_rpc_code(code: str) -> int
```

### McpError

```python
# Factory methods
McpError.not_found(entity_type: str, identifier: str | int | None = None) -> McpError
McpError.access_denied(resource: str | None = None) -> McpError
McpError.validation(field: str, reason: str) -> McpError
McpError.rate_limited(retry_after: int | None = None) -> McpError
McpError.internal(message: str) -> McpError
# ... and more

# Builder methods
error.with_suggestion(suggestion: str) -> McpError
error.with_context(context: dict[str, Any]) -> McpError
error.with_detail(key: str, value: Any) -> McpError
error.retry_after(seconds: int) -> McpError

# Getters
error.get_code() -> str
error.get_message() -> str
error.get_category() -> str
error.get_http_status() -> int
error.get_json_rpc_code() -> int

# Conversion
error.to_dict() -> ErrorDict
error.to_json_rpc_error() -> JsonRpcError
error.to_call_tool_result() -> CallToolResult  # requires mcp package
```

### ErrorBag

```python
# Construction
ErrorBag()
ErrorBag.from_list(errors: list[McpError]) -> ErrorBag

# Adding errors
bag.add(error: McpError) -> ErrorBag
bag.add_validation(field: str, reason: str) -> ErrorBag
bag.merge(other: ErrorBag) -> ErrorBag

# Querying
bag.has_errors() -> bool
bag.is_empty() -> bool
bag.count() -> int
bag.all() -> list[McpError]
bag.first() -> McpError | None
bag.for_field(field: str) -> list[McpError]
bag.by_category(category: str) -> list[McpError]

# Conversion
bag.to_dict() -> ErrorBagDict
bag.to_json_rpc_error() -> dict
bag.to_call_tool_result() -> CallToolResult  # requires mcp package
```

## Cross-Language Support

This package is part of the MCP error codes ecosystem:

| Language | Package |
|----------|---------|
| Python | `mcp-error-codes` |
| TypeScript | [`@codewheel/mcp-error-codes`](https://www.npmjs.com/package/@codewheel/mcp-error-codes) |
| PHP | [`code-wheel/mcp-error-codes`](https://packagist.org/packages/code-wheel/mcp-error-codes) |

All packages maintain API parity for consistent error handling across your stack.

## License

MIT
