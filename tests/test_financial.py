"""Tests para operaciones financieras."""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator.financial import FinancialCalculator

@pytest.fixture
def financial_calc():
    return FinancialCalculator()

def test_compound_interest_basic(financial_calc):
    """Test interés compuesto básico."""
    result = financial_calc.compound_interest(1000, 0.05, 2)
    expected = 1000 * (1.05) ** 2
    assert result == expected

def test_compound_interest_negative_values(financial_calc):
    """Test interés compuesto con valores negativos."""
    with pytest.raises(ValueError):
        financial_calc.compound_interest(-1000, 0.05, 2)

def test_loan_payment_calculation(financial_calc):
    """Test cálculo de pago de préstamo."""
    payment = financial_calc.calculate_loan_payment(100000, 5.0, 30)
    assert isinstance(payment, float)
    assert payment > 0

def test_loan_payment_zero_interest(financial_calc):
    """Test préstamo sin interés."""
    payment = financial_calc.calculate_loan_payment(12000, 0, 1)
    # 12000 / 12 meses = 1000 exactamente
    assert payment == 1000.0 # 12000 / 12 meses
    
def test_loan_payment_zero_interest_rounding(financial_calc):
    """Test que verifica el redondeo correcto."""
    payment = financial_calc.calculate_loan_payment(10000, 0, 2)
    # 10000 / 24 meses = 416.666... → debería redondear a 416.67
    assert payment == 416.67    