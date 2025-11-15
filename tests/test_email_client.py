# ruta: tests/test_email_client.py


import pytest


def test_envio_email(mock_api_response):
    from src.mailing.email_service import enviar_notificacion
    assert enviar_notificacion("user@test.com", "Hola") is True

@pytest.fixture(params=[200, 500, 404])
def mock_api_variable(mocker, request):
    fake_post = mocker.patch("src.mailing.email_service.requests.post")
    fake_post.return_value.status_code = request.param
    return fake_post


def test_envio_variable(mock_api_variable):
    from src.mailing.email_service import enviar_notificacion
    ok = enviar_notificacion("user@test.com", "msg")
    print(f"\nEstado simulado: {mock_api_variable.return_value.status_code}")
    print(f"Resultado del envío: {ok}")
    assert isinstance(ok, bool)