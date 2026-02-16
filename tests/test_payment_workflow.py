# tests/test_payment_workflow.py

import pytest
from src.payments.payment_service import PaymentService

# ---------------------------
# CONTRATO / TRADUCCIÓN API
# ---------------------------

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
def test_should_translate_api_response_into_payment_result(
    payment_api_factory,
    api_response,
    esperado
):
    api = payment_api_factory(api_response)
    service = PaymentService(api)

    r = service.procesar_pago(100)

    assert r == esperado


# ---------------------------
# CASOS DE ÉXITO
# ---------------------------

# Dia 19 
# Refactorizacion conceptual

# Test 1 - pagos exitosos
@pytest.mark.parametrize(
    "api_response",
    [
        {"ok": True},
        {"ok": True, "extra": "data"},
    ]
)
def test_should_return_success_when_api_response_is_ok(payment_api_factory, api_response):
    api = payment_api_factory(api_response)
    service = PaymentService(api)

    r = service.procesar_pago(100)

    assert r == {"success": True, "error": None}

# ---------------------------
# ERRORES DE NEGOCIO
# ---------------------------
# Test 2 - Errores de negocio
@pytest.mark.parametrize(
    "error",
    [
        "fondos",
        "igv",
        "insuficiente",
        "fecha de vencimiento no puede ser igual a fecha de creacion",
    ]
)
def test_should_return_business_error_when_api_returns_known_error(payment_api_factory, error):
    api = payment_api_factory({"ok": False, "error": error})
    service = PaymentService(api)

    r = service.procesar_pago(100)

    assert r == {"success": False, "error": error}


# ---------------------------
# ERRORES TÉCNICOS
# ---------------------------
# Test 3 - errores tecnicos
@pytest.mark.parametrize(
    "error",
    ["timeout", "desconocido"]
)
def test_should_return_failure_when_api_returns_technical_error(payment_api_factory, error):
    api = payment_api_factory({"ok": False, "error": error})
    service = PaymentService(api)

    r = service.procesar_pago(100)

    assert r["success"] is False
    assert r["error"] == error
