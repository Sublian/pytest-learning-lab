import pytest
from src.calculator.math_ops import MathOperations

@pytest.fixture
def datos_numericos():
    """Fixture que devuelve un set de datos base."""
    return [(2, 3), (10, 5), (0, 1), (2,2)]

@pytest.mark.parametrize("operacion", ["add", "subtract", "multiply", 'divide'])
def test_operaciones_parametrizadas(operacion, datos_numericos):
    """Ejecuta distintas operaciones sobre los mismos datos."""
    for a, b in datos_numericos:
        if operacion == "add":
            resultado = MathOperations.add(a, b)
            assert resultado == a + b
        elif operacion == "subtract":
            resultado = MathOperations.subtract(a, b)
            assert resultado == a - b
        elif operacion == "multiply":
            resultado = MathOperations.multiply(a, b)
            assert resultado == a * b
        elif operacion =='divide':
            resultado = MathOperations.divide(a, b)
            assert resultado == a / b
