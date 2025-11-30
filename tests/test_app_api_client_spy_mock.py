# tests/test_app_api_client_spy_mock.py
import pytest
from src.app.api_client import ApiClient

class FakeResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data or {}

    def json(self):
        return self._json


def test_enviar_con_mock_y_spy(mocker):
    client = ApiClient()

    # --- MOCK requests.post ---
    mock_post = mocker.patch(
        "src.app.api_client.requests.post",
        return_value=FakeResponse(200, {"resultado": "ok"})
    )
    print(f"\nMock de requests.post creado: {mock_post}")

    # --- SPY sobre enviar ---
    spy = mocker.spy(client, "enviar")
    print(f"\nSpy creado: {spy}")

    payload = {"a": 1}
    respuesta = client.enviar(payload)
    print(f"\nRespuesta recibida: {respuesta}")

    # Validaciones del mock
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"] == payload

    # Validaciones del spy
    assert spy.call_count == 1
    assert spy.spy_return == {"ok": True, "data": {"resultado": "ok"}}

    assert respuesta["ok"] is True
