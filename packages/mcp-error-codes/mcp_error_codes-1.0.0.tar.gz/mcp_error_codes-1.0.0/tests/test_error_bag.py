"""Tests for ErrorBag collection."""

import json

import pytest

from mcp_error_codes import ErrorBag, McpError


class TestConstruction:
    def test_creates_empty_bag(self) -> None:
        bag = ErrorBag()
        assert bag.is_empty() is True
        assert bag.count() == 0

    def test_creates_from_list(self) -> None:
        errors = [
            McpError.validation("email", "Invalid"),
            McpError.validation("name", "Required"),
        ]
        bag = ErrorBag.from_list(errors)
        assert bag.count() == 2


class TestAddingErrors:
    def test_adds_single_error(self) -> None:
        bag = ErrorBag()
        bag.add(McpError.validation("email", "Invalid"))
        assert bag.count() == 1

    def test_adds_validation_via_convenience(self) -> None:
        bag = ErrorBag()
        bag.add_validation("email", "Invalid format")
        assert bag.count() == 1
        assert bag.first() is not None
        assert bag.first().get_code() == "VALIDATION_ERROR"

    def test_supports_chaining(self) -> None:
        bag = ErrorBag().add(McpError.validation("a", "x")).add_validation("b", "y")
        assert bag.count() == 2

    def test_merges_another_bag(self) -> None:
        bag1 = ErrorBag().add_validation("a", "x")
        bag2 = ErrorBag().add_validation("b", "y")
        bag1.merge(bag2)
        assert bag1.count() == 2


class TestQueryingErrors:
    def test_has_errors_true_when_not_empty(self) -> None:
        bag = ErrorBag().add_validation("x", "y")
        assert bag.has_errors() is True

    def test_has_errors_false_when_empty(self) -> None:
        bag = ErrorBag()
        assert bag.has_errors() is False

    def test_is_empty_true_when_empty(self) -> None:
        bag = ErrorBag()
        assert bag.is_empty() is True

    def test_first_returns_first_error(self) -> None:
        bag = ErrorBag().add_validation("first", "x").add_validation("second", "y")
        first = bag.first()
        assert first is not None
        assert first.get_details()["field"] == "first"

    def test_first_returns_none_when_empty(self) -> None:
        bag = ErrorBag()
        assert bag.first() is None

    def test_all_returns_copy(self) -> None:
        bag = ErrorBag().add_validation("x", "y")
        all_errors = bag.all()
        assert len(all_errors) == 1
        all_errors.append(McpError.internal("test"))
        assert bag.count() == 1  # Original unchanged

    def test_for_field_filters(self) -> None:
        bag = (
            ErrorBag()
            .add_validation("email", "Invalid")
            .add_validation("email", "Too long")
            .add_validation("name", "Required")
        )

        email_errors = bag.for_field("email")
        assert len(email_errors) == 2

    def test_by_category_filters(self) -> None:
        bag = (
            ErrorBag()
            .add(McpError.validation("x", "y"))
            .add(McpError.not_found("User"))
            .add(McpError.validation("z", "w"))
        )

        validation_errors = bag.by_category("validation")
        assert len(validation_errors) == 2

        resource_errors = bag.by_category("resource")
        assert len(resource_errors) == 1


class TestClearing:
    def test_clear_removes_all(self) -> None:
        bag = ErrorBag().add_validation("a", "x").add_validation("b", "y")
        bag.clear()
        assert bag.is_empty() is True

    def test_clear_returns_self(self) -> None:
        bag = ErrorBag().add_validation("a", "x")
        result = bag.clear()
        assert result is bag


class TestIteration:
    def test_is_iterable(self) -> None:
        bag = ErrorBag().add_validation("a", "x").add_validation("b", "y")

        fields = []
        for error in bag:
            fields.append(error.get_details()["field"])
        assert fields == ["a", "b"]

    def test_works_with_list_conversion(self) -> None:
        bag = ErrorBag().add_validation("a", "x").add_validation("b", "y")
        errors = list(bag)
        assert len(errors) == 2

    def test_len(self) -> None:
        bag = ErrorBag().add_validation("a", "x").add_validation("b", "y")
        assert len(bag) == 2


class TestSummaryMessage:
    def test_returns_no_errors_when_empty(self) -> None:
        bag = ErrorBag()
        assert bag.get_summary_message() == "No errors"

    def test_returns_single_error_message(self) -> None:
        bag = ErrorBag().add(McpError.not_found("User"))
        assert bag.get_summary_message() == "User not found."

    def test_returns_validation_count(self) -> None:
        bag = (
            ErrorBag()
            .add_validation("a", "x")
            .add_validation("b", "y")
            .add_validation("c", "z")
        )
        assert bag.get_summary_message() == "3 validation errors occurred."

    def test_returns_generic_count_for_mixed(self) -> None:
        bag = ErrorBag().add(McpError.validation("a", "x")).add(McpError.not_found("User"))
        assert bag.get_summary_message() == "2 errors occurred."


class TestConversionMethods:
    def test_to_dict_success_when_empty(self) -> None:
        bag = ErrorBag()
        d = bag.to_dict()
        assert d["success"] is True
        assert d["errors"] == []

    def test_to_dict_with_errors(self) -> None:
        bag = ErrorBag().add_validation("email", "Invalid").add_validation("name", "Required")

        d = bag.to_dict()
        assert d["success"] is False
        assert d["code"] == "VALIDATION_ERROR"
        assert d["error_count"] == 2
        assert len(d["errors"]) == 2
        assert d["errors"][0]["code"] == "VALIDATION_ERROR"

    def test_to_json_rpc_error(self) -> None:
        bag = ErrorBag().add_validation("email", "Invalid")

        rpc = bag.to_json_rpc_error()
        assert rpc["code"] == -32602
        assert "email" in rpc["message"]
        assert rpc["data"]["code"] == "VALIDATION_ERROR"

    def test_to_json_rpc_error_raises_when_empty(self) -> None:
        bag = ErrorBag()
        with pytest.raises(ValueError, match="empty ErrorBag"):
            bag.to_json_rpc_error()

    def test_to_json(self) -> None:
        bag = ErrorBag().add_validation("x", "y")
        j = bag.to_json()
        parsed = json.loads(j)
        assert parsed["success"] is False

    def test_to_call_tool_result_raises_without_mcp(self) -> None:
        bag = ErrorBag().add_validation("x", "y")
        with pytest.raises(ImportError, match="mcp package"):
            bag.to_call_tool_result()

    def test_empty_bag_to_call_tool_result_raises_without_mcp(self) -> None:
        bag = ErrorBag()
        with pytest.raises(ImportError, match="mcp package"):
            bag.to_call_tool_result()
