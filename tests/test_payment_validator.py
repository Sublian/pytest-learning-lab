# tests/test_payment_validator.py

from src.payments.payment_validator import PaymentValidator

def test_payment_validator_dynamic_side_effect(mocker):

    fake_api = mocker.Mock()

    def fake_check_payment(monto):

        if monto < 100:
            return {"status": "approved"}

        if monto <= 500:
            return {"status": "review"}

        return {"status": "rejected"}

    fake_api.check_payment.side_effect = fake_check_payment

    validator = PaymentValidator(fake_api)
    
    print()
    print(validator.validar_pago(50))    # approved
    print(validator.validar_pago(200))   # manual_review    
    print(validator.validar_pago(1000))  # rejected

    assert validator.validar_pago(50) == "approved"
    assert validator.validar_pago(200) == "manual_review"
    assert validator.validar_pago(1000) == "rejected"