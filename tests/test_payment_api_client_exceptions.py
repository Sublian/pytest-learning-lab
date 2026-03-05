from src.payments.payment_api_client import PaymentAPIClient

# Test 1 — Timeout
def test_should_return_timeout_when_api_times_out(mocker):

    fake_api = mocker.Mock()

    fake_api.charge.side_effect = TimeoutError()

    client = PaymentAPIClient(fake_api)

    r = client.cobrar(100)

    assert r == {
        "success": False,
        "error": "timeout"
    }

# Test 2 — Error de conexión
def test_should_return_connection_error_when_api_connection_fails(mocker):

    fake_api = mocker.Mock()

    fake_api.charge.side_effect = ConnectionError()

    client = PaymentAPIClient(fake_api)

    r = client.cobrar(100)

    assert r == {
        "success": False,
        "error": "connection"
    }

# Test 3 — Respuesta correcta
def test_should_return_success_when_api_returns_ok(mocker):

    fake_api = mocker.Mock()

    fake_api.charge.return_value = {"ok": True}

    client = PaymentAPIClient(fake_api)

    r = client.cobrar(100)

    assert r == {
        "success": True,
        "error": None
    }

