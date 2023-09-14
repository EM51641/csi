from unittest.mock import AsyncMock, MagicMock, Mock
import pytest
from pycsi.Async.Subvalidator import AsyncSubvalidator
from pycsi.Async.Validator import AsyncValidator
from pycsi.Sync.Subvalidator import Subvalidator
from pycsi.utils.BaseSubValidator import ValidatorError
from tests.unit.conftest import AbstractTestValidator


class TestAsyncValidator(AbstractTestValidator):
    _validator: AsyncValidator

    @pytest.fixture(autouse=True)
    def _setup_data(self) -> None:
        """
        test_constructor
        """
        self._first_subvalidator = AsyncMock(AsyncSubvalidator)
        self._second_subvalidator = AsyncMock(AsyncSubvalidator)
        self._third_subvalidator = MagicMock(Subvalidator)

    @pytest.fixture(autouse=True)
    def _setup(self, _setup_data) -> None:
        """
        test_constructor
        """
        self._validator = AsyncValidator()
        self._validator.add(self._first_subvalidator)
        self._validator.add(self._second_subvalidator)
        self._validator.add(self._third_subvalidator)

    def test_add(self) -> None:
        assert len(self._validator.callable_list) == 3

    def test_clear(self) -> None:
        self._validator.clear()
        assert len(self._validator.callable_list) == 0

    @pytest.mark.parametrize(
        [
            "first_error",
            "second_error",
            "third_error",
            "expected_number_of_errors",
        ],
        (
            (None, None, None, 0),
            (None, None, Mock(ValidatorError), 1),
            (None, Mock(ValidatorError), Mock(ValidatorError), 2),
            (
                Mock(ValidatorError),
                Mock(ValidatorError),
                Mock(ValidatorError),
                3,
            ),
        ),
    )
    @pytest.mark.asyncio
    async def test_run(
        self,
        first_error: bool,
        second_error: bool,
        third_error: bool,
        expected_number_of_errors: int,
    ) -> None:
        """
        test run method
        """
        self._first_subvalidator.run.return_value = first_error
        self._second_subvalidator.run.return_value = second_error
        self._third_subvalidator.run.return_value = third_error
        await self._validator.run()
        assert (
            len(self._validator.unvalidated_set) == expected_number_of_errors
        )
