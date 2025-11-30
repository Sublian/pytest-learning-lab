## ruta: `src/workflow/notificador.py`


class Notificador:

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
    

    