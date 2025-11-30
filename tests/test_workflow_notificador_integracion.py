# tests/test_workflow_notificador_integracion.py

from src.workflow.notificador import Notificador
from src.app.api_client import ApiClient

def test_procesar_evento_integration(fake_api, mocker):
    # Mock del envío de correo
    mock_email = mocker.patch(
        # "src.mailing.email_service.enviar_notificacion",
        "src.workflow.notificador.enviar_notificacion",
        return_value=True
    )

    wf = Notificador(api=fake_api)
    r = wf.procesar_evento("x@x.com", {"foo": 123})
    print(f"\nResultado procesar_evento: {r}")

    # Validaciones
    mock_email.assert_called_once()

    assert r["email_ok"] is True
    assert r["api_ok"] is True
    assert r["api_error"] is None

def test_procesar_evento_email_falla(fake_api, mocker):
    # Mock del envío de correo
    mock_email = mocker.patch(
        # "src.mailing.email_service.enviar_notificacion",
        "src.workflow.notificador.enviar_notificacion",
        return_value=False
    )

    wf = Notificador(api=fake_api)
    r = wf.procesar_evento("test@x.com", {"a": 1})
    print(f"\nResultado procesar_evento: {r}")

    # Validaciones
    mock_email.assert_called_once()

    assert r["email_ok"] is False
    assert r["api_ok"] is True
    
def test_procesar_evento_spy_api(mocker):
        # Mock del envío de correo
    mocker.patch(
        # "src.mailing.email_service.enviar_notificacion", 
        "src.workflow.notificador.enviar_notificacion",
        return_value=True
        )

    api = ApiClient()
    spy = mocker.spy(api, "enviar")

    wf = Notificador(api=api)

    r = wf.procesar_evento("x@x.com", {"x": 9})
    # print(f"\nResultado procesar_evento: {r}")
    # print(f"\nSpy info: call_count={spy.call_count}, call_args={spy.call_args}, spy_return={spy.spy_return}")
    
    assert spy.call_count == 1
    assert spy.spy_return["ok"] in (True, False)
    
def test_procesar_evento_mocks_totales(mocker):
    # Mock del envío de correo
    mocker.patch(
        # "src.mailing.email_service.enviar_notificacion", 
        "src.workflow.notificador.enviar_notificacion",
        return_value=True
        )

    fake_resp = {"ok": False, "error": 500}

    mock_api = mocker.Mock()
    mock_api.enviar.return_value = fake_resp

    wf = Notificador(api=mock_api)

    r = wf.procesar_evento("xx@test", {"id": 99})
    print(f"\nResultado procesar_evento: {r}")
    
    assert r["email_ok"] is True
    assert r["api_ok"] is False
    assert r["api_error"] == 500
    