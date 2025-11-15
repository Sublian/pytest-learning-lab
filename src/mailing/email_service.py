# src/mailing/email_service.py

import requests

API_URL = "https://api.fake-mailer.com/send"


def enviar_notificacion(email: str, mensaje: str) -> bool:
    """Envía un correo usando una API externa.
    Retorna True si el envío fue exitoso, False si falló.
    """

    payload = {
        "email": email,
        "mensaje": mensaje
    }

    try:
        resp = requests.post(API_URL, json=payload)
    except Exception as e:
        print(f"\n[ERROR] No se pudo enviar: {e}")
        return False

    # Solo éxito si status 200
    if resp.status_code != 200:
        return False

    # Intentamos leer JSON, pero si está corrupto igual consideramos True
    try:
        resp.json()
    except Exception:
        print("\n[WARN] JSON corrupto. Continuando como si fuera válido.")
        return True

    return True
