from src.app.processor import procesar_envio

def test_processor_validacion_falla(mocker):
    mocker.patch("src.app.processor.validar", return_value=False)

    r = procesar_envio({"email": "x"})
    assert r == {"ok": False, "motivo": "validacion_fallida"}


def test_processor_envio_exitoso(mocker):
    mocker.patch("src.app.processor.validar", return_value=True)

    fake_api = mocker.Mock()
    fake_api.enviar.return_value = {
        "success": True,
        "data": {"id": 1}
    }

    mocker.patch("src.app.processor.ApiClient", return_value=fake_api)

    r = procesar_envio({"email": "a@mail.com", "mensaje": "hola"})

    assert r["ok"] is True
    assert r["resultado"]["id"] == 1


def test_processor_falla_api(mocker):
    mocker.patch("src.app.processor.validar", return_value=True)

    fake_api = mocker.Mock()
    fake_api.enviar.return_value = {
        "success": False,
        "error": 500
    }

    mocker.patch("src.app.processor.ApiClient", return_value=fake_api)

    r = procesar_envio({"email": "a@mail.com", "mensaje": "hola"})

    assert r["ok"] is False
    assert r["motivo"] == 500

# Extra 
def test_processor_reintentos_en_api(mocker):
    mocker.patch("src.app.processor.validar", return_value=True)

    fake_api = mocker.Mock()
    fake_api.enviar.side_effect = [
        {"success": False, "error": "timeout"},
        {"success": False, "error": 500},
        {"success": True, "data": {"ok": True}}
    ]

    mocker.patch("src.app.processor.ApiClient", return_value=fake_api)

    results = []

    for _ in range(3):
        results.append(procesar_envio({"email": "a@mail.com", "mensaje": "hola"}))

    assert results[0]["motivo"] == "timeout"
    assert results[1]["motivo"] == 500
    assert results[2]["ok"] is True

