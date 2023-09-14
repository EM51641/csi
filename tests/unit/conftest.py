from __future__ import annotations
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
    from pycsi.utils.BaseValidator import BaseValidator
    from pycsi.utils.BaseSubValidator import BaseSubvalidator
    from unittest.mock import MagicMock, AsyncMock


class AbstractTestSubvalidator:
    _subvalidator: BaseSubvalidator
    _callable: MagicMock | AsyncMock

    @pytest.fixture(autouse=True)
    def _setup_data(self) -> None:
        self._name = "test_subvalidator"
        self._message_if_fails = "test_subvalidator failed"
        self._args = (1, 2, 3)
        self._kwargs = {"height": 200, "weight": 80, "age": 40}

    def test_constructor(self) -> None:
        """
        test_constructor
        """

        assert self._subvalidator.name == self._name
        assert self._subvalidator.message_if_fails == self._message_if_fails
        assert self._subvalidator.callable == self._callable
        assert self._subvalidator.args == self._args
        assert self._subvalidator.kwargs == {
            "height": 200,
            "weight": 80,
            "age": 40,
        }


class AbstractTestValidator:
    _validator: BaseValidator

    def test_constructor(self) -> None:
        """
        test_constructor
        """
        assert self._validator.unvalidated_set == set()
