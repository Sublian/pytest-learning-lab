# ruta: tests/test_email_service_fixtures.py
import pytest
from src.mailing.email_service import enviar_notificacion

@pytest.mark.parametrize("status_code,expected", [(200, True), (500, False), (404, False)])
def test_envio_parametrizado(mocker, status_code, expected):
    fake_post = mocker.patch("src.mailing.email_service.requests.post")
    fake_post.return_value.status_code = status_code

    ok = enviar_notificacion("param@test.com", "Hola")
    assert ok == expected
