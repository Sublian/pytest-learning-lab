import pytest
from src.calculator.financial import FinancialCalculator

# --- fixture base ---
@pytest.fixture
def datos_financieros():
    """Devuelve datos comunes para pruebas de interes compuesto"""
    return [
        {'principal': 1000, 'rate': 0.05, 'time': 2, 'esperado': 1102.5},
        {'principal': 1000, 'rate': 0.05, 'time': 2, 'esperado': 1102.5},
        {'principal': 1000, 'rate': 0.05, 'time': 2, 'esperado': 1102.5},
    ]
    
# --- test con parametrizacion y marker personalizado ---
@pytest.mark.financial
@pytest.mark.parametrize('indice', [0, 1, 2])
def test_calculo_interes_parametrizado(datos_financieros, indice):
    """Verifica varios escenarios usando una sola fixture compartida."""
    data = datos_financieros[indice]
    resultado = FinancialCalculator.compound_interest(
        data['principal'], data['rate'], data['time']
    )
    assert round(resultado, 2) == data['esperado']


# --- test con parametrizacion y marker personalizado ---
@pytest.mark.financial_error
@pytest.mark.parametrize(
    "principal, rate, time",
    [
        (-1000, 0.05, 2),  # negativo
        (1000, -0.05, 2),  # tasa negativa
        (1000, 0.05, -1),  # tiempo negativo
    ],
)
def test_interes_compuesto_errores(principal, rate, time):
    """Verifica que se lancen excepciones en casos invalidos"""
    with pytest.raises(ValueError):
        FinancialCalculator.compound_interest(principal, rate, time)