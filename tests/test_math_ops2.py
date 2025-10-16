import pytest
from src.calculator.math_ops import MathOperations

# Parametrización basica
@pytest.mark.parametrize(
    "a, b, resultado",
    [
        (2, 3, 5),
        (10, -5, 5),
        (0, 0, 0),
        (10, 0, 10),
        (-3, -7, -10),
    ],
)
def test_add_parametrizado(a, b, resultado):
    assert MathOperations.add(a, b) == resultado

@pytest.mark.parametrize(
    "a, b, resultado",
    [
        (8, 3, 5),
        (10, 5, 5),
        (0, 0, 0),
        (10, 0, 10),
        (17, 7, 10),
    ],
)
def test_subtract_parametrizado(a, b, resultado):
    assert MathOperations.subtract(a,b) ==resultado

# Parametrización de excepciones
@pytest.mark.parametrize(
    "a, b, error",
    [
        (5, 0, ValueError),
        ("a", 3, TypeError),
    ],
)
def test_dividir_excepciones(a, b, error):
    with pytest.raises(error):
        MathOperations.divide(a, b)

# Parametrización con fixtures
@pytest.fixture
def base_data():
    return [1, 2, 3, 4]

@pytest.mark.parametrize("factor", [1, 2, 3,4,5,6,7])
def test_multiplicacion_parametrizada(base_data, factor):
    resultado = [x * factor for x in base_data]
    assert all(isinstance(r, int) for r in resultado)

def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        MathOperations.divide(10, 0)