# src/payments/payment_api_client.py

class PaymentAPIClient:

    def __init__(self, api):
        self.api = api

    def cobrar(self, monto):

        try:
            r = self.api.charge(monto)

            return {
                "success": r.get("ok", False),
                "error": r.get("error")
            }

        except TimeoutError:
            return {
                "success": False,
                "error": "timeout"
            }

        except ConnectionError:
            return {
                "success": False,
                "error": "connection"
            }