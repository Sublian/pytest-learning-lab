# tests/test_email_client_fixtures

def test_envio_exitoso(client, mock_post, make_response):
    mock_post.return_value = make_response(200, "OK")
    resultado = client.enviar_con_reintento("ok@test.com", "Mensaje")
    assert resultado is True

def test_fallo_y_reintento(client, mock_post, make_response):
    mock_post.side_effect = [
        make_response(500, "Error"),
        make_response(500, "Error"),
        make_response(200, "OK")
    ]
    resultado = client.enviar_con_reintento("fail@test.com", "Mensaje", reintentos=3)
    assert resultado is True
    assert mock_post.call_count == 3

def test_falla_total_tras_tres_intentos(client, mocker, make_response):
    mock_post = mocker.patch("requests.post")
    mock_post.side_effect = [
        make_response(500),
        make_response(500),
        make_response(500)
    ]
    # client = EmailClient(delay=0)
    assert client.enviar_con_reintento("fail@test.com", "Error") is False
    assert mock_post.call_count == 3
