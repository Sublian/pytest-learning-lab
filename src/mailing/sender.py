# src/mailing/sender.py
import smtplib

def enviar_email(destinatario, asunto, mensaje):
    """Envía un correo usando SMTP (simulación)."""
    if not destinatario or "@" not in destinatario:
        raise ValueError("Dirección de correo no válida")

    # Simulación de envío real
    with smtplib.SMTP("smtp.example.com") as server:
        server.sendmail("noreply@example.com", destinatario, mensaje)
    return True
