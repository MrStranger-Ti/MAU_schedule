import pytest
from freezegun import freeze_time

from schedule.parser import PeriodManager
from schedule.parser.ext.period_manager import convert_to_iso_8601


def test_convert_to_iso_8601():
    testing_data = "25.01.2025"
    expected_data = "2025-01-25"
    assert convert_to_iso_8601(testing_data) == expected_data


class TestPeriodManger:
    testing_period = "20.01.2025-26.01.2025"

    def test_validate_success(self, mocker):
        spy = mocker.spy(PeriodManager, "validate")
        period_manager = PeriodManager(period=self.testing_period)

        assert spy.assert_called_once
        assert period_manager.period == self.testing_period

    @pytest.mark.parametrize(
        "invalid_period",
        ["invalid period", "27.1.2025-02.2.2025", "2025-01-27-2025.02.02"],
    )
    def test_validate_fail(self, invalid_period, mocker):
        spy = mocker.spy(PeriodManager, "validate")
        period_manager = PeriodManager(period=invalid_period)

        spy.assert_called_once
        assert period_manager.period != invalid_period

    @freeze_time("2025-01-25")
    def test_get_current_period(self, mocker):
        expected_period = self.testing_period

        get_current_period_spy = mocker.spy(
            PeriodManager,
            "_PeriodManager__get_current_period",
        )
        period_manager = PeriodManager()

        get_current_period_spy.assert_called_once()
        assert period_manager.period == expected_period

    def test_start(self):
        expected_start = "2025-01-20"
        period_manager = PeriodManager(period=self.testing_period)
        assert period_manager.start == expected_start

    def test_end(self):
        expected_end = "2025-01-26"
        period_manager = PeriodManager(period=self.testing_period)
        assert period_manager.end == expected_end
