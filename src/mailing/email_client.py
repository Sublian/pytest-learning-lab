# src/mailing/email_client.py
import time
from src.mailing.email_service import enviar_notificacion

class EmailClient:
    """Cliente que usa email_service para enviar notificaciones,
    manejando errores y simulando retrasos."""

    def __init__(self, delay: float = 0.0):
        self.delay = delay

    def enviar_con_reintento(self, email: str, mensaje: str, reintentos: int = 3) -> bool:
        """Envía una notificación con posibilidad de reintentos."""
        for intento in range(1,reintentos +1):
            try:
                resultado = enviar_notificacion(email, mensaje)
                if resultado:
                    return True
            except Exception as e:
                print(f"[INTENTO {intento}] Error: {e}")

            if intento < reintentos:
                time.sleep(self.delay)
        return False
