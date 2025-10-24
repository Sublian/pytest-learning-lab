# tests/test_financial_api_mock.py
import pytest
from unittest.mock import patch, MagicMock
from src.calculator.financial import FinancialCalculator


@pytest.mark.api
@patch("src.calculator.financial.requests.get")
def test_get_remote_interest_rate_exitoso(mock_get):
    """Simula una respuesta exitosa desde la API externa."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rate": 0.075}
    mock_get.return_value = mock_response

    result = FinancialCalculator.get_remote_interest_rate("https://fakeapi/rate")
    assert result == 0.075
    mock_get.assert_called_once_with("https://fakeapi/rate", timeout=5)


@pytest.mark.api_error
@patch("src.calculator.financial.requests.get")
def test_get_remote_interest_rate_error(mock_get):
    """Simula error de conexión o respuesta inválida."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    with pytest.raises(ConnectionError):
        FinancialCalculator.get_remote_interest_rate("https://fakeapi/rate")

@pytest.mark.parametrize("status,rate,esperado", [
    (200, 0.05, 0.05),
    (200, 0.12, 0.12),
    (500, None, ConnectionError),
])
@patch("src.calculator.financial.requests.get")
def test_get_remote_interest_rate_parametrizado(mock_get, status, rate, esperado):
    mock_response = MagicMock()
    mock_response.status_code = status
    mock_response.json.return_value = {"rate": rate}
    mock_get.return_value = mock_response

    if status == 200:
        assert FinancialCalculator.get_remote_interest_rate("https://fakeapi") == rate
    else:
        with pytest.raises(esperado):
            FinancialCalculator.get_remote_interest_rate("https://fakeapi")