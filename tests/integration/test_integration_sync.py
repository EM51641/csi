import pytest
from pycsi.Sync.Subvalidator import Subvalidator
from pycsi.Sync.Validator import Validator
from pycsi.utils.BaseSubValidator import ValidatorError
from tests.integration.conftest import (
    is_all_positive,
    is_divisible_by_three,
    is_quotient_positive,
)


class TestIntegrationSyncValidator:
    @pytest.fixture(autouse=True)
    def _setup_subvalidator(self):
        self._first_subvalidator = Subvalidator(
            "First condition",
            "Number is not divisible by 3",
            is_divisible_by_three,
            x=3,
        )

        self._second_subvalidator = Subvalidator(
            "Second condition",
            "Not every number is positive",
            is_all_positive,
            numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, -10],
        )

        self._third_subvalidator = Subvalidator(
            "Third condition",
            "Quotient is not positive",
            is_quotient_positive,
            x=10,
            y=2,
        )

    @pytest.fixture(autouse=True)
    def _setup(self, _setup_subvalidator):
        self._validator = Validator()
        self._validator.add(self._first_subvalidator)
        self._validator.add(self._second_subvalidator)
        self._validator.add(self._third_subvalidator)

    def test_constructor(self) -> None:
        assert len(self._validator.callable_list) == 3

    def test_clear(self) -> None:
        self._validator.clear()
        assert len(self._validator.callable_list) == 0

    def test_run(self) -> None:
        self._validator.run()
        comparable_set = set(
            [
                ValidatorError(
                    condition="Second condition",
                    error_message="Not every number is positive",
                )
            ]
        )
        assert comparable_set == self._validator.unvalidated_set
