# tests/test_fixture_tmpfile.py
import pytest
from mailing.mail import validar_email

def leer_emails_desde_archivo(path):
    """Función auxiliar (solo en test) para leer emails línea por línea"""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

@pytest.fixture
def archivo_emails(tmp_path):
    """
    Crea un archivo temporal con emails mixtos.
    tmp_path es una fixture integrada de pytest.
    """
    p = tmp_path / "emails.txt"
    contenido = "\n".join([
        "uno@dominio.com",
        "invalid-email.com",
        "",
        "dos@ejemplo.org"
    ])
    p.write_text(contenido, encoding="utf-8")
    return p  # devuelve un pathlib.Path

def test_validar_emails_desde_archivo(archivo_emails):
    emails = leer_emails_desde_archivo(archivo_emails)
    assert len(emails) == 3  # la línea vacía se ignora por la función
    resultados = []
    for e in emails:
        try:
            validar_email(e)
            resultados.append((e, True))
        except ValueError:
            resultados.append((e, False))
    print(f"Resultados: {resultados}")
    assert resultados[0][1] is True   # uno@dominio.com
    assert resultados[1][1] is False  # invalid-email.com
    assert resultados[2][1] is True   # dos@ejemplo.org
