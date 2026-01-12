# tests/test_payment_workflow.py

import pytest
from src.payments.payment_service import PaymentService

@pytest.mark.parametrize(
    "api_response, esperado",
    [
        ({"ok": True}, {"success": True, "error": None}),
        ({"ok": True, "extra": "data"}, {"success": True, "error": None}),
        ({"ok": False}, {"success": False, "error": None}),
        ({"ok": False, "error": "insuficiente"}, {"success": False, "error": "insuficiente"}),
        ({"ok": False, "error": "fecha de vencimiento no puede ser igual a fecha de creacion"}, 
            {"success": False, "error": "fecha de vencimiento no puede ser igual a fecha de creacion"}),
        ({"ok": False, "error": "fondos"}, {"success": False, "error": "fondos"}),
        ({"ok": False, "error": "igv"},    {"success": False, "error": "igv"}),
        ({"ok": False, "error": "timeout"}, {"success": False, "error": "timeout"}),
        ({"ok": False, "error": "desconocido"}, {"success": False, "error": "desconocido"}),
    ]
)
def test_procesar_pago_parametrizado(
    payment_api_factory,
    api_response,
    esperado
):
    api = payment_api_factory(api_response)
    service = PaymentService(api)

    r = service.procesar_pago(100)

    assert r == esperado
