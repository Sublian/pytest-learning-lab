# tests/test_fixture_yield.py
import pytest
from pathlib import Path

@pytest.fixture
def archivo_temporal_con_yield(tmp_path):
    file = tmp_path / "tmp.txt"
    file.write_text("content")
    # setup hecho
    yield file
    # teardown: ejemplo de limpieza adicional
    if file.exists():
        file.unlink()

def test_lee_archivo(archivo_temporal_con_yield):
    assert archivo_temporal_con_yield.read_text() == "content"
