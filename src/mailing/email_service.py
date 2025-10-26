# src/mailing/email_service.py
import requests

def enviar_notificacion(email: str, mensaje: str) -> bool:
    """Envía un mensaje usando una API externa simulada."""
    url = "https://api.fake-mailer.com/send"
    data = {"email": email, "mensaje": mensaje}
    response = requests.post(url, json=data)
    return response.status_code == 200




