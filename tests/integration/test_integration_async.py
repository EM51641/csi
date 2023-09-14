import pytest
from pycsi.Async.Subvalidator import AsyncSubvalidator
from pycsi.Async.Validator import AsyncValidator
from pycsi.Sync.Subvalidator import Subvalidator
from pycsi.utils.BaseSubValidator import ValidatorError
from tests.integration.conftest import (
    async_is_divisible_by_three,
    async_is_all_positive,
    is_quotient_positive,
)


class TestIntegrationAsyncValidator:
    @pytest.fixture(autouse=True)
    def _setup_subvalidator(self):
        self._first_subvalidator = AsyncSubvalidator(
            "First condition",
            "Number is not divisible by 3",
            async_is_divisible_by_three,
            x=10,
        )

        self._second_subvalidator = AsyncSubvalidator(
            "Second condition",
            "Not every number is positive",
            async_is_all_positive,
            numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )

        self._third_subvalidator = Subvalidator(
            "Third condition",
            "Quotient is not positive",
            is_quotient_positive,
            x=10,
            y=-2,
        )

    @pytest.fixture(autouse=True)
    def _setup(self, _setup_subvalidator):
        self._validator = AsyncValidator()
        self._validator.add(self._first_subvalidator)
        self._validator.add(self._second_subvalidator)
        self._validator.add(self._third_subvalidator)

    def test_constructor(self) -> None:
        assert len(self._validator.callable_list) == 3

    def test_clear(self) -> None:
        self._validator.clear()
        assert len(self._validator.callable_list) == 0

    @pytest.mark.asyncio
    async def test_run(self) -> None:
        await self._validator.run()
        assert len(self._validator.unvalidated_set) == 2
        comparable_set = set(
            [
                ValidatorError(
                    condition="First condition",
                    error_message="Number is not divisible by 3",
                ),
                ValidatorError(
                    condition="Third condition",
                    error_message="Quotient is not positive",
                ),
            ]
        )
        assert self._validator.unvalidated_set == comparable_set
