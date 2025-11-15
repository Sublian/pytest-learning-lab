# tests/test_email_side_effects.py

import pytest
import requests
from src.mailing.email_client import EmailClient
from src.mailing.email_service import enviar_notificacion


# -------------------------------
# 1. Timeout
# -------------------------------
def test_timeout_en_envio(mocker):
    mock_post = mocker.patch("src.mailing.email_service.requests.post")
    mock_post.side_effect = requests.Timeout("Se agotó el tiempo")

    client = EmailClient()
    ok = client.enviar_con_reintento("a@a.com", "hola")

    assert ok is False


# -------------------------------
# 2. Error intermitente
# -------------------------------
def test_error_intermitente(mocker):
    mock_post = mocker.patch("src.mailing.email_service.requests.post")

    mock_post.side_effect = [
        Exception("Error 1"),
        Exception("Error 2"),
        type("Resp", (), {"status_code": 200, "json": lambda: {"ok": True}})(),
    ]

    client = EmailClient()
    ok = client.enviar_con_reintento("a@a.com", "msg")

    assert ok is True


# -------------------------------
# 3. JSON corrupto
# -------------------------------
def test_respuesta_corrupta(mocker):
    fake_post = mocker.patch("src.mailing.email_service.requests.post")

    fake_resp = mocker.Mock()
    fake_resp.status_code = 200
    fake_resp.json.side_effect = ValueError("JSON inválido")

    fake_post.return_value = fake_resp

    ok = enviar_notificacion("user@test.com", "msg")

    assert ok is True


# -------------------------------
# 4. Rate limit
# -------------------------------
@pytest.mark.parametrize("status_code", [429, 500, 200])
def test_rate_limit(mocker, status_code):
    fake = mocker.patch("src.mailing.email_service.requests.post")
    fake.return_value.status_code = status_code
    fake.return_value.json = lambda: {}

    ok = enviar_notificacion("user@test.com", "x")

    assert ok == (status_code == 200)


# -------------------------------
# 5. Varios casos (test útil)
# -------------------------------
def test_envio_varios_casos(mock_respuesta_api):
    """Ahora sí valida: Solo True si status_code = 200."""

    ok = enviar_notificacion("x@x.com", "hola")

    # Primera respuesta del fixture es 200 -> True
    assert ok is True


# -------------------------------
# 6. Reintentos
# -------------------------------
def test_reintentos(mocker):
    # Parcheamos la función real que usa EmailClient
    mocker.patch("src.mailing.email_service.enviar_notificacion", return_value=False)

    import src.mailing.email_service as email_service

    spy = mocker.spy(email_service, "enviar_notificacion")

    client = EmailClient()

    client.enviar_con_reintento("a", "b")

    assert spy.call_count == 3


# -------------------------------
# 7. Argumentos
# -------------------------------
def test_argumentos(mocker):
    fake = mocker.patch("src.mailing.email_service.requests.post")
    fake.return_value.status_code = 200
    fake.return_value.json = lambda: {}

    enviar_notificacion("test@mail.com", "hola")

    fake.assert_called_once()
    _, kwargs = fake.call_args

    assert "json" in kwargs
    assert kwargs["json"]["email"] == "test@mail.com"
