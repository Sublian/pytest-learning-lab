import pytest
from src.calculator.financial import FinancialCalculator

@pytest.mark.rapidas
def test_interes_compuesto_simple():
    assert FinancialCalculator.compound_interest(1000, 0.1, 2) == 1210.0

@pytest.mark.lentas
def test_pago_prestamo_complejo():
    pago = FinancialCalculator.calculate_loan_payment(5000, 5, 10)
    assert round(pago, 2) == 53.03

@pytest.mark.error_handling
def test_interest_compuesto_simple_fallido():
    with pytest.raises(ValueError): 
        FinancialCalculator.compound_interest(1000, 0.1, -10)
        
@pytest.mark.error_handling
def test_pago_prestamo_complejo_fallido():
    with pytest.raises(ValueError): 
        FinancialCalculator.calculate_loan_payment(0, 5, 10)