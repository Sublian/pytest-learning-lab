# test/test_app_api_client.py
from src.app.api_client import ApiClient

def test_envio_exitoso(mocker):
    fake_resp = mocker.Mock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = {"id": 1, "status": "ok"}

    mocker.patch("src.app.api_client.requests.post", return_value=fake_resp)

    api = ApiClient()
    r = api.enviar({"x": 1})

    assert r["ok"] is True
    assert r["data"]["status"] == "ok"


def test_envio_falla_status_code(mocker):
    fake_resp = mocker.Mock()
    fake_resp.status_code = 500

    mocker.patch("src.app.api_client.requests.post", return_value=fake_resp)

    api = ApiClient()
    r = api.enviar({"x": 1})

    assert r["ok"] is False
    assert r["error"] == 500


def test_envio_timeout(mocker):
    mocker.patch(
        "src.app.api_client.requests.post",
        side_effect=Exception("timeout")
    )

    api = ApiClient()
    r = api.enviar({"x": 1})

    assert r["ok"] is False
    assert r["error"] == "timeout"
    