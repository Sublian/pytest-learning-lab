"""Tests para operaciones matemáticas."""
import pytest
import sys
import os

# Agregar src al path para que Python encuentre los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator.math_ops import MathOperations

def test_add_positive_numbers():
    """Test suma de números positivos."""
    math_ops = MathOperations()
    assert math_ops.add(2, 3) == 5
    assert math_ops.add(0, 0) == 0

def test_add_negative_numbers():
    """Test suma de números negativos."""
    math_ops = MathOperations()
    assert math_ops.add(-1, 1) == 0
    assert math_ops.add(-5, -3) == -8

def test_divide_by_zero():
    """Test división por cero."""
    math_ops = MathOperations()
    with pytest.raises(ValueError, match="No se puede dividir por cero"):
        math_ops.divide(10, 0)

def test_power_operations():
    """Test operaciones de potencia."""
    math_ops = MathOperations()
    assert math_ops.power(2, 3) == 8
    assert math_ops.power(5, 0) == 1
    assert math_ops.power(10, 2) == 100

def test_factorial_valid():
    """Test factorial con valores válidos."""
    math_ops = MathOperations()
    assert math_ops.factorial(0) == 1
    assert math_ops.factorial(1) == 1
    assert math_ops.factorial(5) == 120

def test_factorial_invalid():
    """Test factorial con valores inválidos."""
    math_ops = MathOperations()
    with pytest.raises(ValueError):
        math_ops.factorial(-1)
    with pytest.raises(ValueError):
        math_ops.factorial(3.5)

# Test parametrizado - múltiples casos en una sola función
@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (9, 3, 3),
    (1, 1, 1),
    (0, 5, 0),
])
def test_divide_parameterized(math_ops, a, b, expected):
    """Test parametrizado de división."""
    assert math_ops.divide(a, b) == expected

# Fixture para reutilizar la instancia
@pytest.fixture
def math_ops():
    return MathOperations()

"""
    Ejecutar Tests Expandidos
# Ejecutar todos los tests
python -m pytest tests/ -v

# Ejecutar con cobertura
python -m pytest tests/ --cov=src --cov-report=term-missing

# Ejecutar solo tests específicos
python -m pytest tests/test_math_ops.py::test_factorial_valid -v
"""

# tests/test_math_ops.py
def test_add(math_ops_module):
    assert math_ops_module.add(2,3) == 5

def test_divide(math_ops_module):
    assert math_ops_module.divide(10,2) == 5
