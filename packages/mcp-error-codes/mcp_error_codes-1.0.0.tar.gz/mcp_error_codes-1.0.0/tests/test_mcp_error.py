"""Tests for McpError fluent builder."""

import json

import pytest

from mcp_error_codes import McpError


class TestAccessErrors:
    def test_access_denied(self) -> None:
        error = McpError.access_denied()
        assert error.get_code() == "ACCESS_DENIED"
        assert error.get_message() == "Access denied."
        assert error.get_category() == "access"

    def test_access_denied_with_resource(self) -> None:
        error = McpError.access_denied("admin panel")
        assert error.get_message() == "Access denied to admin panel."

    def test_insufficient_scope(self) -> None:
        error = McpError.insufficient_scope("write")
        assert error.get_code() == "INSUFFICIENT_SCOPE"
        assert error.get_message() == "Operation requires 'write' scope."

    def test_admin_required(self) -> None:
        error = McpError.admin_required()
        assert error.get_code() == "ADMIN_REQUIRED"
        assert error.get_message() == "This operation requires admin privileges."

    def test_rate_limited(self) -> None:
        error = McpError.rate_limited()
        assert error.get_code() == "RATE_LIMIT_EXCEEDED"
        assert error.get_message() == "Rate limit exceeded."

    def test_rate_limited_with_retry_after(self) -> None:
        error = McpError.rate_limited(60)
        assert error.get_retry_after() == 60
        assert error.get_details()["retry_after"] == 60


class TestResourceErrors:
    def test_not_found(self) -> None:
        error = McpError.not_found("User")
        assert error.get_code() == "NOT_FOUND"
        assert error.get_message() == "User not found."
        assert error.get_details()["entity_type"] == "User"

    def test_not_found_with_identifier(self) -> None:
        error = McpError.not_found("User", 123)
        assert error.get_message() == "User '123' not found."

    def test_already_exists(self) -> None:
        error = McpError.already_exists("User", "john@example.com")
        assert error.get_code() == "ALREADY_EXISTS"
        assert error.get_message() == "User 'john@example.com' already exists."

    def test_entity_in_use(self) -> None:
        error = McpError.entity_in_use("Role", "editor")
        assert error.get_code() == "ENTITY_IN_USE"
        assert "Role 'editor' is in use" in error.get_message()

    def test_entity_in_use_with_used_by(self) -> None:
        error = McpError.entity_in_use("Role", "editor", "5 users")
        assert "by 5 users" in error.get_message()

    def test_entity_protected(self) -> None:
        error = McpError.entity_protected("User", "admin")
        assert error.get_code() == "ENTITY_PROTECTED"
        assert "protected" in error.get_message()


class TestValidationErrors:
    def test_validation(self) -> None:
        error = McpError.validation("email", "Invalid format")
        assert error.get_code() == "VALIDATION_ERROR"
        assert "email" in error.get_message()
        assert "Invalid format" in error.get_message()
        assert error.get_details()["field"] == "email"
        assert error.get_details()["reason"] == "Invalid format"

    def test_missing_required(self) -> None:
        error = McpError.missing_required("name")
        assert error.get_code() == "MISSING_REQUIRED"
        assert "name" in error.get_message()
        assert error.get_details()["field"] == "name"


class TestOperationErrors:
    def test_internal(self) -> None:
        error = McpError.internal("Database connection failed")
        assert error.get_code() == "INTERNAL_ERROR"
        assert error.get_message() == "Database connection failed"

    def test_operation_failed(self) -> None:
        error = McpError.operation_failed("save")
        assert error.get_code() == "OPERATION_FAILED"
        assert "save" in error.get_message()

    def test_operation_failed_with_reason(self) -> None:
        error = McpError.operation_failed("save", "disk full")
        assert "disk full" in error.get_message()

    def test_timeout(self) -> None:
        error = McpError.timeout()
        assert error.get_code() == "TIMEOUT"
        assert error.get_message() == "Operation timed out."

    def test_timeout_with_operation(self) -> None:
        error = McpError.timeout("database query")
        assert "database query" in error.get_message()

    def test_service_unavailable(self) -> None:
        error = McpError.service_unavailable()
        assert error.get_code() == "SERVICE_UNAVAILABLE"

    def test_service_unavailable_with_service(self) -> None:
        error = McpError.service_unavailable("payment gateway")
        assert "payment gateway" in error.get_message()

    def test_invalid_tool(self) -> None:
        error = McpError.invalid_tool("unknown_tool")
        assert error.get_code() == "INVALID_TOOL"
        assert error.get_details()["tool"] == "unknown_tool"

    def test_invalid_tool_with_reason(self) -> None:
        error = McpError.invalid_tool("broken_tool", "missing handler")
        assert "missing handler" in error.get_message()

    def test_execution_failed(self) -> None:
        error = McpError.execution_failed("my_tool", "null pointer")
        assert error.get_code() == "EXECUTION_FAILED"
        assert error.get_details()["tool"] == "my_tool"

    def test_confirmation_required(self) -> None:
        error = McpError.confirmation_required("delete_all")
        assert error.get_code() == "CONFIRMATION_REQUIRED"
        assert "confirm=true" in error.get_message()


class TestGenericFactory:
    def test_from_code(self) -> None:
        error = McpError.from_code("CUSTOM_ERROR", "Custom message")
        assert error.get_code() == "CUSTOM_ERROR"
        assert error.get_message() == "Custom message"


class TestBuilderMethods:
    def test_with_suggestion(self) -> None:
        error = McpError.not_found("User", 123).with_suggestion("Check the user ID")
        assert "Check the user ID" in error.get_message()
        assert error.get_details()["suggestion"] == "Check the user ID"

    def test_with_context(self) -> None:
        error = McpError.validation("email", "Invalid").with_context(
            {"provided": "not-an-email", "expected": "email format"}
        )
        assert error.get_details()["provided"] == "not-an-email"
        assert error.get_details()["expected"] == "email format"

    def test_with_detail(self) -> None:
        error = McpError.internal("Error").with_detail("trace_id", "abc123")
        assert error.get_details()["trace_id"] == "abc123"

    def test_retry_after(self) -> None:
        error = McpError.internal("Busy").retry_after(30)
        assert error.get_retry_after() == 30

    def test_chained_methods(self) -> None:
        error = (
            McpError.validation("email", "Invalid")
            .with_suggestion("Use valid email")
            .with_context({"input": "bad"})
            .with_detail("validator", "email")
        )
        assert error.get_details()["suggestion"] == "Use valid email"
        assert error.get_details()["input"] == "bad"
        assert error.get_details()["validator"] == "email"


class TestGetters:
    def test_get_raw_message(self) -> None:
        error = McpError.not_found("User").with_suggestion("Try again")
        assert error.get_raw_message() == "User not found."
        assert "Try again" in error.get_message()

    def test_get_http_status(self) -> None:
        assert McpError.not_found("X").get_http_status() == 404
        assert McpError.access_denied().get_http_status() == 403
        assert McpError.validation("x", "y").get_http_status() == 400

    def test_get_json_rpc_code(self) -> None:
        assert McpError.not_found("X").get_json_rpc_code() == -32002
        assert McpError.validation("x", "y").get_json_rpc_code() == -32602


class TestConversionMethods:
    def test_to_dict(self) -> None:
        error = McpError.not_found("User", 123)
        d = error.to_dict()

        assert d["success"] is False
        assert d["error"] == "User '123' not found."
        assert d["code"] == "NOT_FOUND"
        assert d["category"] == "resource"
        assert d["details"]["entity_type"] == "User"

    def test_to_dict_omits_empty_details(self) -> None:
        error = McpError.from_code("TEST", "Test")
        d = error.to_dict()
        assert "details" not in d

    def test_to_json_rpc_error(self) -> None:
        error = McpError.not_found("User")
        rpc = error.to_json_rpc_error()

        assert rpc["code"] == -32002
        assert rpc["message"] == "User not found."
        assert rpc["data"]["code"] == "NOT_FOUND"
        assert rpc["data"]["category"] == "resource"

    def test_to_json_rpc_error_omits_empty_details(self) -> None:
        error = McpError.from_code("TEST", "Test")
        rpc = error.to_json_rpc_error()
        assert "details" not in rpc["data"]

    def test_str(self) -> None:
        error = McpError.not_found("User")
        assert str(error) == "[NOT_FOUND] User not found."

    def test_repr(self) -> None:
        error = McpError.not_found("User")
        assert "McpError" in repr(error)
        assert "NOT_FOUND" in repr(error)

    def test_to_json(self) -> None:
        error = McpError.not_found("User")
        j = error.to_json()
        parsed = json.loads(j)
        assert parsed["code"] == "NOT_FOUND"

    def test_to_call_tool_result_raises_without_mcp(self) -> None:
        error = McpError.not_found("User")
        with pytest.raises(ImportError, match="mcp package"):
            error.to_call_tool_result()
