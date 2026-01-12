# src/payments/payment_service.py

class PaymentService:

    def __init__(self, api):
        self.api = api

    def procesar_pago(self, amount):
        result = self.api.charge(amount)

        return {
            "success": result.get("ok"),
            "error": result.get("error")
        }
