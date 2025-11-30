# tests/test_email_service_mock.py

import pytest
from src.mailing.email_service import enviar_notificacion

class FakeResponse:
    def __init__(self, status_code=200, json_data=None, fail_json=False):
        self.status_code = status_code
        self._json = json_data or {}
        self.fail_json = fail_json

    def json(self):
        if self.fail_json:
            raise ValueError("JSON corrupto")
        return self._json


def test_envio_exitoso(mocker):
    mocker.patch(
        "src.mailing.email_service.requests.post",
        return_value=FakeResponse(200, {"ok": True})
    )

    assert enviar_notificacion("a@a.com", "msg") is True


def test_envio_status_malo(mocker):
    mocker.patch(
        "src.mailing.email_service.requests.post",
        return_value=FakeResponse(500)
    )
    assert enviar_notificacion("a@a.com", "msg") is False


def test_envio_json_corrupto(mocker):
    mocker.patch(
        "src.mailing.email_service.requests.post",
        return_value=FakeResponse(200, fail_json=True)
    )

    # aunque falle el JSON, retorna True
    assert enviar_notificacion("a@a.com", "msg") is True
