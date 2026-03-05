class PaymentValidator:

    def __init__(self, api):
        self.api = api

    def validar_pago(self, monto):

        r = self.api.check_payment(monto)

        if r["status"] == "approved":
            return "approved"

        if r["status"] == "review":
            return "manual_review"

        return "rejected"