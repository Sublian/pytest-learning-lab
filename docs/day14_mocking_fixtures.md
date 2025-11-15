# 🧩 Día 14 (Versión Extendida)

Pytest + Mocking Avanzado + Fixtures Dinámicas**

## 📘 Conceptos Clave
### 1️⃣ ¿Por qué usar mocking junto a fixtures?

Hasta ahora has usado mocks directamente en los tests, pero a veces necesitas que el mismo mock se aplique a varios tests o cambie de forma dinámica según el contexto.

➡️ Solución: usar fixtures que configuran mocks automáticamente.

### 2️⃣ pytest-mock y su fixture mocker

pytest-mock añade una fixture especial llamada mocker que simplifica el uso de unittest.mock.
Permite:
- Simular funciones o métodos.
- Espiar llamadas (call_count, called_with).
- Restaurar automáticamente el estado original.

```python
def test_mock_example(mocker):
    fake_get = mocker.patch("requests.get")
    fake_get.return_value.status_code = 200

    from src.network import get_status
    assert get_status("https://test.com") == 200
```

### 3️⃣ Mocking con Fixtures Reutilizables

Puedes encapsular tus mocks dentro de fixtures reutilizables.
Por ejemplo, una API falsa que siempre devuelve datos controlados:

```python
# ruta: tests/conftest.py
import pytest

@pytest.fixture
def mock_api_response(mocker):
    fake_post = mocker.patch("src.mailing.email_service.requests.post")
    fake_post.return_value.status_code = 200
    return fake_post
```

Luego, cualquier test que use esta fixture tendrá el mismo comportamiento controlado:

```python
# ruta: tests/test_email_client.py
def test_envio_email(mock_api_response):
    from src.mailing.email_service import enviar_notificacion
    assert enviar_notificacion("user@test.com", "Hola") is True
```

### 4️⃣ Mocking Condicional o Parametrizado

A veces necesitas simular distintos resultados (éxito, fallo, excepción).

```python
@pytest.fixture(params=[200, 500, 404])
def mock_api_variable(mocker, request):
    fake_post = mocker.patch("src.mailing.email_service.requests.post")
    fake_post.return_value.status_code = request.param
    return fake_post

def test_envio_variable(mock_api_variable):
    from src.mailing.email_service import enviar_notificacion
    ok = enviar_notificacion("user@test.com", "msg")
    assert isinstance(ok, bool)
```

Así, pytest ejecutará el test tres veces (una por cada código HTTP simulado).

## 🧪 Ejecuta las pruebas
```python
uv run pytest -v -s
```


📌 Usa -s para ver si algún print() interno del cliente indica los intentos.
Todos los tests deberían pasar correctamente mostrando los mocks activos.

## 🧠 Qué estás aprendiendo realmente

- Cómo inyectar mocks mediante fixtures para no repetir código.
- Cómo parametrizar mocks para probar múltiples comportamientos.
- Cómo combinar fixtures + mocker para entornos realistas y limpios.
- Cómo reutilizar dependencias simuladas en toda tu suite de tests.

---

## 🎯 OBJETIVO EXTENDIDO

Para dominar las pruebas profesionales, hoy aprenderás:

✔ Cómo combinar mocks con fixtures para aislar dependencias
✔ Cómo simular errores reales, tiempos de espera, excepciones, llamadas secuenciales
✔ Cómo usar side_effect para simular comportamientos avanzados
✔ Cómo parametrizar servicios externos completos
✔ Cómo validar que tu cliente maneje correctamente:
- API caída
- Códigos HTTP inesperados
- Timeouts
- Reintentos
- Errores intermitentes
- Limitación de rate
- Respuestas corruptas

## 🧩 1. Mocking Avanzado: side_effect

**side_effect** permite simular comportamientos no estáticos, por ejemplo:

🔥 1) lanzar una excepción

🔥 2) devolver valores distintos cada vez

🔥 3) mezclar valores + excepciones

🔥 4) simular retrasos

```python
fake_get.side_effect = [200, 500, Exception("API caída")]
```

## 🧩 2. Simular Errores de Red (Timeout, conexión caída)

Tu función usa requests.post().

### 💡 ¿Qué estamos simulando?
- La API no responde
- requests lanza Timeout
- El cliente debe manejar la excepción, no crashear

### 🧩 3. Simular Errores Intermitentes

Esto es MUY real en producción (API down, rate limiting, etc.)

Simulamos:
1. error
2. error
3. éxito

## Mejores prácticas en proyectos reales
✔ Simula errores reales: timeout, 404, 500

✔ Usa side_effect para escenarios complejos

✔ Nunca hagas llamadas reales dentro de tests unitarios

✔ Usa fixtures para evitar repetir código

✔ Parametriza para cubrir más casos sin duplicar tests

✔ Spy para validar cuántos intentos hiciste

✔ Usa mocks “minimalistas”, sólo lo necesario

✔ No abuses del mocking (false sense of security)


## 📘 Buenas prácticas definitivas con mocker

|Buenas prácticas |	Ejemplo|
|-----------|-----------|
| Parchea donde se usa	| mocker.patch("app.modulo.funcion")|
| Crea mocks explícitos	| fake = mocker.Mock()|
| Usa side_effect para errores	| timeouts, 500s, retries|
| NO mezclar lógica real con mocks	| nada real debe ejecutarse|
| Mantén cada test aislado	| no dependas de orden entre tests|

## 🎁 Plantilla ideal para pruebas con mocker

```python
def test_mi_funcion(mocker):
    # 1. Preparar fake
    fake_respuesta = {"status": "ok"}

    # 2. Parchear dependencias externas
    mocker.patch("app.mi_modulo.dependencia", return_value=fake_respuesta)

    # 3. Ejecutar
    from app.mi_modulo import mi_funcion
    r = mi_funcion()

    # 4. Verificar
    assert r["status"] == "ok"
```