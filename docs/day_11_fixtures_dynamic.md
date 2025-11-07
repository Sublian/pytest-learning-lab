---

## 🧪 Día 11 — Fixtures dinámicas y uso de autouse

En este día aprendí a usar **fixtures dinámicas y automáticas** en Pytest.  
Implementé un cliente de base de datos simulado con una fixture que cambia según el
parámetro del test (`request.param`) y una fixture con `autouse=True` para iniciar y cerrar
recursos de manera automática antes y después de cada prueba.

🔍 **Conceptos clave:**
- `request.param` para valores dinámicos.
- `autouse=True` para ejecutar fixtures globales sin declararlas.
- Encadenamiento de fixtures (`db_client`, `tabla_usuario`).
- Control del ciclo de vida con `yield`.

💡 Este día refuerza la comprensión del manejo de contexto y la limpieza de recursos,
pilares para pruebas limpias y reproducibles.

---
## Día 11 — Mini reto

🎯 Objetivo

Reforzar el uso de fixtures dinámicas parametrizadas (request.param) y su integración con recursos reales (como bases de datos temporales), manejando correctamente los escenarios de error y limpieza.

📘 **Descripción del Reto**
- Creamos un módulo temp_db.py que simula una base de datos SQLite temporal, junto con su fixture temp_db, capaz de:
- Conectarse dinámicamente a rutas distintas (pasadas por parámetro).
- Manejar errores simulados cuando la ruta contiene "fail://...".
- Crear directorios automáticamente si no existen.
- Insertar datos de prueba y realizar limpieza final.

Este ejercicio refuerza conceptos de setup/teardown, parametrización y manejo de errores controlados en entornos de testing.

