# 🧩 Día 13 — Pytest Fixtures Avanzadas + Reutilización y Scopes

## 🎯 Objetivo del día
Aprender a usar **fixtures avanzadas** en `pytest` para:
- Compartir datos o recursos entre varios tests.
- Controlar su ciclo de vida con `scope` (`function`, `class`, `module`, `session`).
- Encadenar fixtures y aprovechar su modularidad.
- Aplicar *autouse fixtures* y *fixtures parametrizadas*.

---

## 🧠 Conceptos Clave

### 1️⃣ ¿Qué es una *fixture*?
Una *fixture* es una función que prepara un entorno o dato necesario para un test.

```python
# ruta: tests/conftest.py
import pytest

@pytest.fixture
def sample_user():
    return {"name": "Luis", "role": "admin"}
```

## Alcance o scope de las fixtures

El scope define cuándo se crea y destruye la fixture:

|Scope |	Crea/destruye la fixture por...	| Uso típico|
|-----------|-----------|-----------|
|function |	cada test	| datos aislados|
|class |	una vez por clase	| recursos compartidos entre tests de una clase|
|module |	una vez por archivo de test	| conexiones o datos comunes|
|session |	una vez por ejecución completa	| base de datos, clientes globales|

## ✅ Aprendizaje Clave del Día 13

- Las fixtures son la base para escribir tests reutilizables y mantenibles.
- Comprender los scopes te permite optimizar el tiempo de ejecución de las pruebas.
- A partir de aquí, podrás combinar fixtures, mocks y parametrización en entornos más grandes (como Django o APIs con Celery y Docker).