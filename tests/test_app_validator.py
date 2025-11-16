from src.app.validator import validar

def test_validator_acepta_payload_correcto():
    payload = {"email": "test@mail.com", "mensaje": "hola"}
    assert validar(payload) is True

def test_validator_rechaza_sin_email():
    assert validar({"mensaje": "hola"}) is False

def test_validator_rechaza_email_invalido():
    assert validar({"email": "no-valido", "mensaje": "hola"}) is False
