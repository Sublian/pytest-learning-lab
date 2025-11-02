
import pytest
from src.database.db_client import DatabaseClient


# 🔹 Fixture dinámica: el parámetro "db_url" cambia en cada test parametrizado
@pytest.fixture
def db_client(request):
    """Crea una conexión a la base de datos o simula un fallo controlado."""
    db_url = getattr(request, "param", "sqlite://default")
    client = DatabaseClient(db_url)
    
    try:
        client.connect()
    except ConnectionError:
        # Si el URL contiene "fail", dejamos que el test maneje el error
        pass

    yield client
    client.disconnect()

@pytest.mark.parametrize(
    "db_client",
    ["sqlite://localhost"],
    indirect=True
)
def test_obtener_datos_parametrizados(db_client, tabla_usuario):
    filas = db_client.fetch_data(tabla_usuario)
    assert len(filas) == 2
    assert "row_from_usuarios_1" in filas[0]

# 🔹 Fixture global con autouse=True para inicialización del entorno
@pytest.fixture(autouse=True, scope="function")
def log_test_start():
    print("\n➡️ Iniciando prueba...")
    yield
    print("✅ Finalizando prueba.")


# 🔹 Tests parametrizados que usan la fixture dinámica
@pytest.mark.parametrize(
    "db_client",
    ["sqlite://localhost", "postgres://localhost"],
    indirect=True
)
def test_conexion_exitosa(db_client):
    assert db_client.connected is True


@pytest.mark.parametrize(
    "db_client",
    ["fail://localhost"],
    indirect=True
)
def test_conexion_fallida(db_client):
    with pytest.raises(ConnectionError):
        db_client.connect()


# 🔹 Test que usa una fixture anidada
@pytest.fixture
def tabla_usuario():
    return "usuarios"


def test_obtener_datos(db_client, tabla_usuario):
    filas = db_client.fetch_data(tabla_usuario)
    assert len(filas) == 2
    assert "row_from_usuarios_1" in filas[0]
