# tests/test_scope_demo.py

import time
import pytest

@pytest.fixture(scope="module")
def recurso_pesado():
    print("\n🔧 Inicializando recurso pesado...")
    time.sleep(1)
    yield
    print("\n🧹 Liberando recurso pesado...")

def test_a(recurso_pesado):
    time.sleep(0.1)
    assert True

def test_b(recurso_pesado):
    time.sleep(0.1)
    assert True
