# tests/test_temp_db_fixture.py
import pytest
import os
from src.database.temp_db import TempDatabase

@pytest.mark.parametrize("temp_db", ["tmp/test1.db", "tmp/test2.db"], indirect=True)
def test_lectura_correcta(temp_db):
    rows = temp_db.fetch_data()
    assert len(rows) == 2
    assert "Alice" in rows[0][1]

@pytest.mark.parametrize("temp_db", ["fail://tmp/fail.db"], indirect=True)
def test_conexion_fallida(temp_db):
    with pytest.raises(ConnectionError):
        temp_db.connect()

@pytest.mark.parametrize("temp_db", ["tmp/test3.db"], indirect=True)
def test_cleanup(temp_db):
    path = temp_db.path
    temp_db.close()
    temp_db.cleanup()
    assert not os.path.exists(path)


@pytest.fixture
def temp_db(request):
    db_path = getattr(request, "param", "tmp/test_default.db")

    # 🔒 Detectar si es un caso simulado (no crear directorios con 'fail://')
    if db_path.startswith("fail://"):
        with pytest.raises(ConnectionError):
            TempDatabase(db_path).connect()
        # Yield dummy database (para mantener estructura de test)
        yield TempDatabase(db_path)
        return

    # ✅ Crear directorio si no es un caso simulado
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    db = TempDatabase(db_path)
    db.connect()
    db.insert_demo_data()

    yield db

    db.close()
    db.cleanup()