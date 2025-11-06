# tests/conftest.py  (este archivo se usa para fixtures globales)
import pytest
import requests
from calculator.math_ops import MathOperations
import time
import random

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
    
@pytest.fixture(scope='session')
def entorno_global():
    print("\n🌍 Configurando entorno global de tests")
    yield
    print("\n🧹 Limpiando entorno global de tests")
    
# mailing    
@pytest.fixture
def mock_post(mocker):
    """Fixture para simular requests.post"""    
    return mocker.patch("requests.post")

@pytest.fixture
def client():
    """Fixture que devuelve un EmailClient con delay minimo"""
    from src.mailing.email_client import EmailClient
    return EmailClient(delay=0)

@pytest.fixture
def make_response():
    """Crea un objeto requests.Response configurable."""
    def _factory(status_code, text=""):
        resp = requests.Response()
        resp.status_code = status_code
        resp._content = text.encode('utf-8')
        return resp
    return _factory


@pytest.fixture(scope="session")
def api_client():
    print("\n🌐 Creando cliente API (una sola vez)")
    return {"base_url": "https://fake.api.local"}


@pytest.fixture(scope="session")
def init_db():
    """Simula una conexión a base de datos compartida por toda la sesión."""
    print("\n[SETUP] Creando base de datos global...")
    db = {"connected": True, "users": []}
    yield db
    print("\n[TEARDOWN] Cerrando base de datos global...")
    db["connected"] = False


@pytest.fixture(scope="function")
def user_data(init_db):
    """Crea un usuario temporal por test."""
    user = {
        "id": random.randint(1000, 9999),
        "name": f"user_{int(time.time())}"
    }
    print(f"[SETUP] Creando usuario temporal: {user['name']}")
    init_db["users"].append(user)
    yield user
    print(f"[TEARDOWN] Eliminando usuario: {user['name']}")
    init_db["users"].remove(user)