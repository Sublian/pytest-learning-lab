import pytest
from calculator.financial import FinancialCalculator

# test parametrizado sin errores
@pytest.mark.parametrize(
    "principal, rate, time, expected",
    [
        (1000, 0.05, 2, 1102.5),
        (500, 0.10, 1, 550.0),
    ],
)
def test_compound_interest_ok(principal, rate, time, expected):
    result = FinancialCalculator.compound_interest(principal, rate, time)
    assert round(result, 2) == expected

# test parametrizado para los errores
@pytest.mark.parametrize(
    "principal, rate, time",
    [
        (-100, 0.05, 2),
        (1000, -0.05, 2),
    ],
)
def test_compound_interest_error(principal, rate, time):
    with pytest.raises(ValueError):
        FinancialCalculator.compound_interest(principal, rate, time)
