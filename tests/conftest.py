# tests/conftest.py  (este archivo se usa para fixtures globales)
import pytest
from calculator.math_ops import MathOperations

@pytest.fixture(scope="module")
def math_ops_module():
    """
    Fixture que se crea una vez por módulo de tests y se reutiliza.
    Ideal si la inicialización fuera costosa.
    """
    return MathOperations


@pytest.fixture(autouse=True)
def limpia_estado_global():
    # setup: por ejemplo, borra variables globales del módulo
    yield
    # teardown: opcional