from app.validator import validar
from app.api_client import ApiClient

def procesar_envio(payload):
    if not validar(payload):
        return {"ok": False, "motivo": "validacion_fallida"}

    api = ApiClient()
    respuesta = api.enviar(payload)

    if respuesta["success"]:
        return {"ok": True, "resultado": respuesta["data"]}
    else:
        return {"ok": False, "motivo": respuesta["error"]}
