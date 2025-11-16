# src/app/api_client.py

import requests

class ApiClient:
    BASE_URL = "https://fake-api.com"

    def enviar(self, payload):
        try:
            r = requests.post(f"{self.BASE_URL}/send", json=payload, timeout=2)
        except Exception as e:
            # Caso: error de red, timeout, etc
            return {"ok": False, "error": str(e)}

        # Caso: status code no exitoso
        if r.status_code != 200:
            return {"ok": False, "error": r.status_code}

        # Caso: llamado exitoso
        return {"ok": True, "data": r.json()}
