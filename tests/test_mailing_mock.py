# tests/test_mailing_mock.py
import pytest
from unittest.mock import patch
from src.mailing.sender import enviar_email


@pytest.mark.mail
@patch("src.mailing.sender.smtplib.SMTP")  # simulamos el objeto SMTP
def test_enviar_email_exitoso(mock_smtp):
    """Simula un envío exitoso sin usar un servidor real."""
    instance = mock_smtp.return_value.__enter__.return_value
    instance.sendmail.return_value = {}

    resultado = enviar_email("usuario@test.com", "Asunto", "Mensaje de prueba")

    assert resultado is True
    instance.sendmail.assert_called_once_with(
        "noreply@example.com", "usuario@test.com", "Mensaje de prueba"
    )


@pytest.mark.mail_error
def test_enviar_email_invalido():
    """Simula error al usar un correo inválido."""
    with pytest.raises(ValueError):
        enviar_email("sin_arroba.com", "Asunto", "Mensaje")
