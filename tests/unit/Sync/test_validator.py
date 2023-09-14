import pytest
from unittest.mock import MagicMock, Mock
from pycsi.Sync.Subvalidator import Subvalidator
from pycsi.Sync.Validator import Validator
from pycsi.utils.BaseSubValidator import ValidatorError
from tests.unit.conftest import AbstractTestValidator


class TestSyncValidator(AbstractTestValidator):
    _validator: Validator

    @pytest.fixture(autouse=True)
    def _setup_data(self) -> None:
        """
        test_constructor
        """
        self._first_subvalidator = MagicMock(Subvalidator)
        self._second_subvalidator = MagicMock(Subvalidator)
        self._third_subvalidator = MagicMock(Subvalidator)

    @pytest.fixture(autouse=True)
    def _setup(self, _setup_data) -> None:
        """
        test_constructor
        """
        self._validator = Validator()
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
    def test_run(
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
        self._validator.run()
        assert (
            len(self._validator.unvalidated_set) == expected_number_of_errors
        )
