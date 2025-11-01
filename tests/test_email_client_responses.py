import pytest
import requests
from src.mailing.email_client import EmailClient

def test_reintento_por_http_error(mocker):
    """Debe reintentar si el servidor responde con error 500."""
    mock_post = mocker.patch("requests.post")

    # Simula respuestas HTTP con distintos status_code
    mock_response_500 = mocker.MagicMock(status_code=500)
    mock_response_200 = mocker.MagicMock(status_code=200)

    # Falla primero, luego éxito
    mock_post.side_effect = [mock_response_500, mock_response_200]

    client = EmailClient(delay=0)
    resultado = client.enviar_con_reintento("user@test.com", "Mensaje", reintentos=2)

    assert resultado is True
    assert mock_post.call_count == 2



def make_response(status_code, text=""):
    resp = requests.Response()
    resp.status_code = status_code
    resp._content = text.encode("utf-8")
    return resp


def test_reintento_por_error_http_y_excepcion(mocker):
    """Simula errores mixtos (excepción + status_code 500 + éxito)."""
    mock_post = mocker.patch("requests.post")
    mock_post.side_effect = [
        requests.ConnectionError("Timeout"),
        make_response(500, "Internal Server Error"),
        make_response(200, "OK")
    ]

    client = EmailClient(delay=0)
    resultado = client.enviar_con_reintento("user@test.com", "Mensaje", reintentos=3)

    assert resultado is True
    assert mock_post.call_count == 3
