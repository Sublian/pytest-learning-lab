# mail.py
def validar_email(email: str) -> bool:
    """
    Valida si el email tiene el carácter '@'.
    Devuelve True si es válido; lanza ValueError si no.
    """
    if not email:
        raise ValueError("El correo no puede estar vacío")
    if "@" not in email or "." not in email:
        raise ValueError("Formato de correo inválido")
    if len(email) < 6:
        raise ValueError("Correo demasiado corto")
    return True
