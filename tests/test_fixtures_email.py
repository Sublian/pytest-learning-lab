# tests/test_fixtures_email.py
import pytest
from mailing.mail import validar_email

# -------------------------
# FIXTURES SIMPLES
# -------------------------
@pytest.fixture
def email_valido():
    """Fixture que devuelve un email válido de ejemplo."""
    return "usuario@dominio.com"

@pytest.fixture
def email_invalido():
    """Fixture que devuelve un email inválido (sin @)."""
    return "usuariodominio.com"


# -------------------------
# FIXTURES MULTIPLE
# -------------------------
# 🔧 Fixture: prepara una lista de correos válidos
@pytest.fixture
def correos_validos():
    """Devuelve una lista de correos válidos para las pruebas."""
    return [
        "usuario@gmail.com",
        "test@example.org",
        "contact@empresa.pe",
    ]
    
# 🔧 Fixture: prepara una lista de correos inválidos
@pytest.fixture
def correos_invalidos():
    """Devuelve una lista de correos con errores de formato."""
    return [
        "",
        "usuario_sinarroba.com",
        "test@com",
        "a@b",
    ]

# -------------------------
# FIXTURE HIBRIDO
# -------------------------
@pytest.fixture
def correos_mixtos():
    """
    Devuelve una lista de tuplas (email, resultado_esperado).
    True = debe pasar la validación
    False = debe lanzar ValueError
    """
    return [
        ("usuario@gmail.com", True),
        ("", False),
        ("contacto@empresa.com", True),
        ("test_sin_arroba.com", False),
        ("valid@example.pe", True),
        ("bad@", False),
    ]
# -------------------------
# TESTS
# -------------------------
def test_email_valido(email_valido):
    """Comprueba que el email válido pasa la validación."""
    assert validar_email(email_valido) is True

def test_email_invalido(email_invalido):
    """Comprueba que el email inválido produce ValueError."""
    with pytest.raises(ValueError):
        validar_email(email_invalido)

# ✅ Test usando la primera fixture
def test_correos_validos(correos_validos):
    """Verifica que todos los correos válidos pasen la validación."""
    for correo in correos_validos:
        assert validar_email(correo) is True

# ❌ Test usando la segunda fixture
def test_correos_invalidos(correos_invalidos):
    """Verifica que todos los correos inválidos generen excepción."""
    for correo in correos_invalidos:
        with pytest.raises(ValueError):
            validar_email(correo)
            
def test_correos_mixtos(correos_mixtos):
    """
    Verifica que cada correo se comporte como se espera.
    Si el resultado esperado es True → debe pasar.
    Si es False → debe lanzar ValueError.
    """
    for correo, esperado in correos_mixtos:
        if esperado:
            # Caso esperado correcto
            assert validar_email(correo) is True
        else:
            # Caso esperado incorrecto → debe fallar
            with pytest.raises(ValueError):
                validar_email(correo)
            