
def validar(payload):
    if not isinstance(payload, dict):
        return False
    if "email" not in payload or "mensaje" not in payload:
        return False
    if not payload["email"] or "@" not in payload["email"]:
        return False
    return True
