## ruta: `src/workflow/notificador.py`
from src.app.api_client import ApiClient
from src.mailing.email_service import enviar_notificacion

class Notificador:

    def __init__(self, api=None):
        self.api = api or ApiClient()

    def validar_mensaje(self, msg: str) -> bool:
        return bool(msg and msg.strip())

    def enviar_mensaje(self, msg: str) -> dict:
        return {"ok": True, "msg": msg}

    def procesar(self, msg: str) -> dict:
        # Paso 1: validar
        if not self.validar_mensaje(msg):
            return {"ok": False, "error": "mensaje_vacio"}

        # Paso 2: enviar
        return self.enviar_mensaje(msg)
    
    def procesar_evento(self, email, payload):
        """
        1. Envía un correo de alerta.
        2. Envía datos a la API externa.
        3. Retorna dict con resultados de ambos.
        """
        resultado_email = enviar_notificacion(email, "Nuevo evento recibido")

        resultado_api = self.api.enviar(payload)

        return {
            "email_ok": resultado_email,
            "api_ok": resultado_api["ok"],
            "api_error": resultado_api.get("error"),
        }
    

    