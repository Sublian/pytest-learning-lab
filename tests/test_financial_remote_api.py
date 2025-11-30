import pytest
from src.calculator.financial import FinancialCalculator

class FakeResponse:
    def __init__(self, status, json_data):
        self.status_code = status
        self._json = json_data

    def json(self):
        return self._json


def test_get_remote_interest_rate_ok(mocker):
    mock_get = mocker.patch(
        "src.calculator.financial.requests.get",
        return_value=FakeResponse(200, {"rate": "4.5"})
    )

    rate = FinancialCalculator.get_remote_interest_rate("http://api.test")
    assert rate == 4.5
    mock_get.assert_called_once()


def test_get_remote_interest_rate_falla_status(mocker):
    mocker.patch(
        "src.calculator.financial.requests.get",
        return_value=FakeResponse(500, {})
    )

    with pytest.raises(ConnectionError):
        FinancialCalculator.get_remote_interest_rate("http://api.test")
