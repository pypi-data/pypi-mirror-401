"""Tests for ErrorCode constants and helpers."""

import pytest

from mcp_error_codes import (
    ACCESS_DENIED,
    ADMIN_REQUIRED,
    ALREADY_EXISTS,
    CONFIG_ERROR,
    CONFIRMATION_REQUIRED,
    CRON_FAILED,
    ENTITY_IN_USE,
    ENTITY_PROTECTED,
    EXECUTION_FAILED,
    INSTANTIATION_FAILED,
    INSUFFICIENT_SCOPE,
    INTERNAL_ERROR,
    INVALID_FILE_TYPE,
    INVALID_NAME,
    INVALID_TOOL,
    MEDIA_ERROR,
    MIGRATION_FAILED,
    MISSING_DEPENDENCY,
    MISSING_REQUIRED,
    NOT_FOUND,
    OPERATION_FAILED,
    PAYLOAD_TOO_LARGE,
    RATE_LIMIT_EXCEEDED,
    READ_ONLY_MODE,
    RECIPE_FAILED,
    SERVICE_UNAVAILABLE,
    TEMPLATE_NOT_FOUND,
    TIMEOUT,
    VALIDATION_ERROR,
    ErrorCode,
)


class TestAll:
    def test_returns_all_error_codes(self) -> None:
        codes = ErrorCode.all()
        assert isinstance(codes, dict)
        assert len(codes) > 20
        assert codes["NOT_FOUND"] == "NOT_FOUND"
        assert codes["VALIDATION_ERROR"] == "VALIDATION_ERROR"

    def test_returns_copy(self) -> None:
        codes1 = ErrorCode.all()
        codes2 = ErrorCode.all()
        assert codes1 is not codes2
        assert codes1 == codes2


class TestIsValid:
    def test_returns_true_for_defined_codes(self) -> None:
        assert ErrorCode.is_valid(NOT_FOUND) is True
        assert ErrorCode.is_valid(VALIDATION_ERROR) is True
        assert ErrorCode.is_valid(INTERNAL_ERROR) is True

    def test_returns_false_for_unknown_codes(self) -> None:
        assert ErrorCode.is_valid("UNKNOWN_CODE") is False
        assert ErrorCode.is_valid("") is False
        assert ErrorCode.is_valid("not_found") is False


class TestGetCategory:
    def test_returns_access_for_access_codes(self) -> None:
        assert ErrorCode.get_category(INSUFFICIENT_SCOPE) == "access"
        assert ErrorCode.get_category(ADMIN_REQUIRED) == "access"
        assert ErrorCode.get_category(ACCESS_DENIED) == "access"
        assert ErrorCode.get_category(RATE_LIMIT_EXCEEDED) == "access"
        assert ErrorCode.get_category(READ_ONLY_MODE) == "access"

    def test_returns_resource_for_resource_codes(self) -> None:
        assert ErrorCode.get_category(NOT_FOUND) == "resource"
        assert ErrorCode.get_category(ALREADY_EXISTS) == "resource"
        assert ErrorCode.get_category(ENTITY_IN_USE) == "resource"
        assert ErrorCode.get_category(ENTITY_PROTECTED) == "resource"
        assert ErrorCode.get_category(MISSING_DEPENDENCY) == "resource"

    def test_returns_validation_for_validation_codes(self) -> None:
        assert ErrorCode.get_category(VALIDATION_ERROR) == "validation"
        assert ErrorCode.get_category(INVALID_NAME) == "validation"
        assert ErrorCode.get_category(INVALID_FILE_TYPE) == "validation"
        assert ErrorCode.get_category(PAYLOAD_TOO_LARGE) == "validation"
        assert ErrorCode.get_category(MISSING_REQUIRED) == "validation"

    def test_returns_operation_for_operation_codes(self) -> None:
        assert ErrorCode.get_category(INTERNAL_ERROR) == "operation"
        assert ErrorCode.get_category(OPERATION_FAILED) == "operation"
        assert ErrorCode.get_category(TIMEOUT) == "operation"
        assert ErrorCode.get_category(CONFIRMATION_REQUIRED) == "operation"
        assert ErrorCode.get_category(INVALID_TOOL) == "operation"
        assert ErrorCode.get_category(EXECUTION_FAILED) == "operation"
        assert ErrorCode.get_category(INSTANTIATION_FAILED) == "operation"

    def test_returns_domain_for_domain_codes(self) -> None:
        assert ErrorCode.get_category(CRON_FAILED) == "domain"
        assert ErrorCode.get_category(TEMPLATE_NOT_FOUND) == "domain"
        assert ErrorCode.get_category(MIGRATION_FAILED) == "domain"
        assert ErrorCode.get_category("UNKNOWN_CODE") == "domain"


class TestIsRecoverable:
    def test_returns_true_for_retryable_codes(self) -> None:
        assert ErrorCode.is_recoverable(RATE_LIMIT_EXCEEDED) is True
        assert ErrorCode.is_recoverable(TIMEOUT) is True
        assert ErrorCode.is_recoverable(SERVICE_UNAVAILABLE) is True
        assert ErrorCode.is_recoverable(INTERNAL_ERROR) is True

    def test_returns_false_for_permanent_codes(self) -> None:
        assert ErrorCode.is_recoverable(NOT_FOUND) is False
        assert ErrorCode.is_recoverable(VALIDATION_ERROR) is False
        assert ErrorCode.is_recoverable(ACCESS_DENIED) is False
        assert ErrorCode.is_recoverable(ALREADY_EXISTS) is False


class TestGetHttpStatus:
    def test_returns_403_for_access_codes(self) -> None:
        assert ErrorCode.get_http_status(INSUFFICIENT_SCOPE) == 403
        assert ErrorCode.get_http_status(ADMIN_REQUIRED) == 403
        assert ErrorCode.get_http_status(ACCESS_DENIED) == 403
        assert ErrorCode.get_http_status(READ_ONLY_MODE) == 403

    def test_returns_404_for_not_found(self) -> None:
        assert ErrorCode.get_http_status(NOT_FOUND) == 404
        assert ErrorCode.get_http_status(TEMPLATE_NOT_FOUND) == 404

    def test_returns_409_for_conflicts(self) -> None:
        assert ErrorCode.get_http_status(ALREADY_EXISTS) == 409
        assert ErrorCode.get_http_status(ENTITY_IN_USE) == 409
        assert ErrorCode.get_http_status(ENTITY_PROTECTED) == 409

    def test_returns_400_for_validation(self) -> None:
        assert ErrorCode.get_http_status(VALIDATION_ERROR) == 400
        assert ErrorCode.get_http_status(INVALID_NAME) == 400
        assert ErrorCode.get_http_status(INVALID_FILE_TYPE) == 400
        assert ErrorCode.get_http_status(MISSING_REQUIRED) == 400
        assert ErrorCode.get_http_status(INVALID_TOOL) == 400

    def test_returns_special_codes(self) -> None:
        assert ErrorCode.get_http_status(RATE_LIMIT_EXCEEDED) == 429
        assert ErrorCode.get_http_status(PAYLOAD_TOO_LARGE) == 413
        assert ErrorCode.get_http_status(TIMEOUT) == 408
        assert ErrorCode.get_http_status(SERVICE_UNAVAILABLE) == 503

    def test_returns_500_for_unknown(self) -> None:
        assert ErrorCode.get_http_status(INTERNAL_ERROR) == 500
        assert ErrorCode.get_http_status(CRON_FAILED) == 500
        assert ErrorCode.get_http_status("UNKNOWN_CODE") == 500


class TestGetJsonRpcCode:
    def test_returns_validation_code(self) -> None:
        assert ErrorCode.get_json_rpc_code(VALIDATION_ERROR) == -32602
        assert ErrorCode.get_json_rpc_code(INVALID_NAME) == -32602
        assert ErrorCode.get_json_rpc_code(INVALID_FILE_TYPE) == -32602
        assert ErrorCode.get_json_rpc_code(MISSING_REQUIRED) == -32602

    def test_returns_method_not_found(self) -> None:
        assert ErrorCode.get_json_rpc_code(INVALID_TOOL) == -32601

    def test_returns_internal_error(self) -> None:
        assert ErrorCode.get_json_rpc_code(INTERNAL_ERROR) == -32603
        assert ErrorCode.get_json_rpc_code(EXECUTION_FAILED) == -32603
        assert ErrorCode.get_json_rpc_code(INSTANTIATION_FAILED) == -32603

    def test_returns_server_defined_codes(self) -> None:
        assert ErrorCode.get_json_rpc_code(ACCESS_DENIED) == -32001
        assert ErrorCode.get_json_rpc_code(INSUFFICIENT_SCOPE) == -32001
        assert ErrorCode.get_json_rpc_code(ADMIN_REQUIRED) == -32001
        assert ErrorCode.get_json_rpc_code(NOT_FOUND) == -32002
        assert ErrorCode.get_json_rpc_code(TEMPLATE_NOT_FOUND) == -32002
        assert ErrorCode.get_json_rpc_code(RATE_LIMIT_EXCEEDED) == -32003
        assert ErrorCode.get_json_rpc_code(READ_ONLY_MODE) == -32004
        assert ErrorCode.get_json_rpc_code(ALREADY_EXISTS) == -32005
        assert ErrorCode.get_json_rpc_code(ENTITY_IN_USE) == -32005
        assert ErrorCode.get_json_rpc_code(ENTITY_PROTECTED) == -32005
        assert ErrorCode.get_json_rpc_code(MISSING_DEPENDENCY) == -32006
        assert ErrorCode.get_json_rpc_code(TIMEOUT) == -32007
        assert ErrorCode.get_json_rpc_code(SERVICE_UNAVAILABLE) == -32008
        assert ErrorCode.get_json_rpc_code(PAYLOAD_TOO_LARGE) == -32009
        assert ErrorCode.get_json_rpc_code(CONFIRMATION_REQUIRED) == -32010
        assert ErrorCode.get_json_rpc_code(OPERATION_FAILED) == -32011
        assert ErrorCode.get_json_rpc_code(CRON_FAILED) == -32011
        assert ErrorCode.get_json_rpc_code(MIGRATION_FAILED) == -32011
        assert ErrorCode.get_json_rpc_code(RECIPE_FAILED) == -32011
        assert ErrorCode.get_json_rpc_code(CONFIG_ERROR) == -32011
        assert ErrorCode.get_json_rpc_code(MEDIA_ERROR) == -32011

    def test_returns_generic_for_unknown(self) -> None:
        assert ErrorCode.get_json_rpc_code("UNKNOWN_CODE") == -32000


class TestErrorCodeClass:
    def test_exposes_constants(self) -> None:
        assert ErrorCode.NOT_FOUND == "NOT_FOUND"
        assert ErrorCode.VALIDATION_ERROR == "VALIDATION_ERROR"
        assert ErrorCode.ACCESS_DENIED == "ACCESS_DENIED"
