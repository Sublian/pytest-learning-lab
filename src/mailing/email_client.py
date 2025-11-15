# src/mailing/email_client.py

import time
from src.mailing import email_service


class EmailClient:
    """Cliente que envía notificaciones con reintentos."""

    def __init__(self, delay: float = 0.0):
        self.delay = delay

    def enviar_con_reintento(self, email: str, mensaje: str, reintentos: int = 3) -> bool:
        for intento in range(1, reintentos + 1):

            resultado = email_service.enviar_notificacion(email, mensaje)

            if resultado is True:
                return True

            if intento < reintentos:
                time.sleep(self.delay)

        return False
