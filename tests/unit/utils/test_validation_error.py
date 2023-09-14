from __future__ import annotations
import pytest
from typing import TYPE_CHECKING
from unittest.mock import Mock
from pycsi.utils.BaseSubValidator import ValidatorError

if TYPE_CHECKING:
    from typing import Any


class TestValidatorError:
    @pytest.fixture(autouse=True)
    def _setup(self) -> None:
        self._validator_error = ValidatorError(
            condition="test_condition",
            error_message="test_error_message",
        )

    def test_constructor(self) -> None:
        assert self._validator_error.condition == "test_condition"
        assert self._validator_error.error_message == "test_error_message"

    @pytest.mark.parametrize(
        ["object", "expected_result"],
        [
            (ValidatorError("test_condition", "test_error_message"), True),
            (ValidatorError("test_condition", "test_error_messages"), False),
            (ValidatorError("test_condition_", "test_error_message"), False),
            ("string_object", False),
            (
                Mock(
                    condition="test_condition",
                    error_message="test_error_message",
                ),
                False,
            ),
        ],
    )
    def test_equality(self, object: Any, expected_result: bool) -> None:
        assert (self._validator_error == object) is expected_result

    def test_str(self) -> None:
        assert (
            str(self._validator_error)
            == "ValidatorError(condition='test_condition', error_message='test_error_message')"
        )

    def test_repr(self) -> None:
        assert (
            repr(self._validator_error)
            == "ValidatorError(condition='test_condition', error_message='test_error_message')"
        )
