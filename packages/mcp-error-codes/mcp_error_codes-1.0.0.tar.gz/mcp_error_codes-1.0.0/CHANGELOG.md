# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-09

### Added
- Initial release with full feature parity with PHP and TypeScript packages
- `ErrorCode` class with 28 predefined error codes
- Error categories: access, resource, validation, operation, domain
- `get_category()` for semantic error classification
- `get_http_status()` for HTTP status code mapping
- `get_json_rpc_code()` for JSON-RPC 2.0 error code mapping
- `is_valid()` and `is_recoverable()` helper methods
- `McpError` fluent builder class
  - Factory methods: `not_found()`, `access_denied()`, `validation()`, `rate_limited()`, etc.
  - Builder methods: `with_suggestion()`, `with_context()`, `with_detail()`, `retry_after()`
  - Conversion: `to_dict()`, `to_json_rpc_error()`, `to_call_tool_result()`
- `ErrorBag` collection class for multiple errors
  - `add()`, `add_validation()`, `merge()` for building collections
  - `for_field()`, `by_category()` for filtering
  - Implements `Iterable[McpError]`
- Full type hints with strict mypy compliance
- 100% test coverage
