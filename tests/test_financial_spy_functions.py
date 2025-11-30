# tests/test_financial_spy_functions.py
import pytest
from src.calculator.financial import FinancialCalculator

def test_spy_compound_interest(mocker):
    spy = mocker.spy(FinancialCalculator, "compound_interest")

    resultado = FinancialCalculator.compound_interest(1000, 0.05, 2)

    assert spy.call_count == 1
    spy_args = spy.call_args[0]
    spy_return = spy.spy_return
    
    assert spy_args == (1000, 0.05, 2)
    # assert resultado == 1102.5
    assert resultado == spy_return


def test_spy_calculate_loan_payment(mocker):
    spy = mocker.spy(FinancialCalculator, "calculate_loan_payment")

    pago = FinancialCalculator.calculate_loan_payment(10000, 12, 1)
    
    spy_return = spy.spy_return
    
    assert spy.call_count == 1
    # assert pago > 0
    assert pago == spy_return
    assert spy_return > 0
