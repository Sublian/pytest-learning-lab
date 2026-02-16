# tests/test_workflow_parametrizado.py
import pytest
from src.workflow.notificador import Notificador

@pytest.mark.parametrize(
    "email_ok, api_response, esperado",
    [
        (True,  {"ok": True},                 {"email_ok": True,  "api_ok": True,  "api_error": None}),
        (False, {"ok": True},                 {"email_ok": False, "api_ok": True,  "api_error": None}),
        (True,  {"ok": False, "error": 500},  {"email_ok": True,  "api_ok": False, "api_error": 500}),
        (True,  {"ok": False, "error": "timeout"}, {"email_ok": True, "api_ok": False, "api_error": "timeout"}),
    ]
)
def test_should_process_event_and_return_combined_result(
    mocker,
    api_factory,
    email_ok,
    api_response,
    esperado
):
    # Mock del correo
    mocker.patch(
        # "src.mailing.email_service.enviar_notificacion",  FALLO. Siempre se mockea DONDE SE USA, no donde se define
        "src.workflow.notificador.enviar_notificacion",
        return_value=email_ok
    )

    # API falsa configurable
    api = api_factory(api_response)

    wf = Notificador(api=api)

    r = wf.procesar_evento("test@test.com", {"id": 1})

    assert r == esperado
