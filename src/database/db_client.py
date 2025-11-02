
class DatabaseClient:
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        self.connected = False

    def connect(self):
        """Simula una conexión a la base de datos."""
        if "fail" in self.connection_url:
            raise ConnectionError("Error de conexión a la base de datos.")
        self.connected = True
        return True

    def disconnect(self):
        """Simula el cierre de conexión."""
        self.connected = False
        return True

    def fetch_data(self, table_name: str):
        """Simula obtención de datos."""
        if not self.connected:
            raise RuntimeError("No hay conexión activa.")
        return [f"row_from_{table_name}_1", f"row_from_{table_name}_2"]
