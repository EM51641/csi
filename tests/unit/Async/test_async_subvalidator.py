import pytest
from unittest.mock import AsyncMock
from pycsi.Async.Subvalidator import AsyncSubvalidator
from pycsi.utils.BaseSubValidator import ValidatorError
from tests.unit.conftest import AbstractTestSubvalidator


class TestAsyncSubvalidator(AbstractTestSubvalidator):
    _subvalidator: AsyncSubvalidator

    @pytest.fixture(autouse=True)
    def _setup_callable(self):
        """
        Setup callable
        """
        self._callable = AsyncMock()

    @pytest.fixture(autouse=True)
    def _setup(self, _setup_data, _setup_callable):
        """
        Setup Subvalidator
        """
        self._subvalidator = AsyncSubvalidator(
            self._name,
            self._message_if_fails,
            self._callable,
            *self._args,
            **self._kwargs,
        )

    @pytest.mark.asyncio
    async def test_run_no_error(self):
        """
        Test run() method without error
        """
        self._callable.return_value = True
        error = await self._subvalidator.run()
        assert error is None

    @pytest.mark.asyncio
    async def test_run_error(self) -> None:
        """
        Test run() method with error
        """
        self._callable.return_value = False
        error = await self._subvalidator.run()

        assert error == ValidatorError(
            condition="test_subvalidator",
            error_message="test_subvalidator failed",
        )
