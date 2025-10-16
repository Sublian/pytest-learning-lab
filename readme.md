# 🧪 Pytest Learning Lab

This repository documents my learning journey with **pytest**, automation, and testing best practices using Python.

## 🚀 Project Overview
This lab includes:
- Test-driven examples using `pytest`
- Parametrization and fixtures
- Exception handling and advanced test scenarios
- Code profiling and optimization techniques

## 📂 Structure
pytest-uv-project/
│
├── src/ # Core code
├── tests/ # Unit and integration tests
└── pyproject.toml # uv project configuration


## 🧰 Tools
- Python 3.11+
- [pytest](https://docs.pytest.org)
- [uv](https://github.com/astral-sh/uv)
- GitHub Actions (future integration)

---

### 🧭 Status
✔️ Week 1: Pytest Fundamentals  
🚧 Week 2: Mocking & Fixtures  
🔜 Week 3: CI/CD & Coverage Reports

---

## 🧩 Pytest — Aprendizaje y Recordatorio Técnico

> Esta sección documenta los fundamentos clave de **pytest** aplicados en este proyecto, combinando teoría y práctica.  
> El objetivo es reforzar conceptos esenciales para crear pruebas más limpias, escalables y mantenibles en Python.

---

### 🔹 ¿Qué es una *Fixture*?

Una **fixture** es una función especial que prepara datos o recursos antes de ejecutar una prueba.  
Ayuda a eliminar código repetido y asegura que cada test empiece con un entorno limpio y controlado.

```python
import pytest

@pytest.fixture
def usuario_base():
    return {"nombre": "Luis", "rol": "admin"}

def test_usuario_tiene_rol(usuario_base):
    assert usuario_base["rol"] == "admin"
```
💡 **Nota:** Las fixtures ayudan a mantener las pruebas aisladas y predecibles.

✅ **Buenas prácticas**
- Usa nombres descriptivos para tus fixtures.
- Evita modificar los datos compartidos dentro del test.
- Reutiliza fixtures solo cuando su configuración sea estable.

---

### 🔹 tmp_path — Archivos Temporales

tmp_path es una fixture integrada en pytest que crea carpetas temporales únicas por test.
Es ideal para pruebas que requieren lectura o escritura de archivos sin ensuciar el proyecto.

```python
import pytest

def test_generar_reporte(tmp_path):
    archivo = tmp_path / "reporte.txt"
    archivo.write_text("resultado exitoso")
    contenido = archivo.read_text()
    assert "exitoso" in contenido
```

---

### 🔹 yield — Separando Setup y Teardown

Dentro de una fixture, yield define el punto de entrega del recurso al test.
El código después del yield se ejecuta siempre al terminar la prueba, incluso si falla.

```python
@pytest.fixture
def conexion_db():
    conn = conectar_db()
    yield conn
    conn.close()  # Se ejecuta al final del test, pase o falle
```

🧠 A diferencia de `unittest`, que usa `setup()` y `teardown()`, en pytest el control se logra con `yield`, simplificando la sintaxis.

---

### 🧭 Resumen rápido
| Concepto | Qué hace | Cuándo usarlo |
|-----------|-----------|----------------|
| Fixture | Prepara datos o recursos | Cuando hay código repetido |
| tmp_path | Crea archivos temporales | Pruebas con lectura/escritura |
| yield | Controla inicio y limpieza | Cuando se usan recursos externos |

---

📅 **Progreso del aprendizaje — Día 3**

Hoy avancé con las *fixtures* en pytest.  
Aprendí a usar `tmp_path`, `yield` y `scope`, entendiendo cómo ayudan a mantener los tests limpios y seguros.  
Cada día me resulta más claro cómo pytest puede hacer el proceso de testing más elegante y profesional.

---

## 🧩 Día 4 — Parametrización y Reutilización de Datos en Pytest

> Hoy exploré cómo **pytest** permite ejecutar la misma prueba con múltiples combinaciones de datos sin repetir código, utilizando **parametrización** y **fixtures parametrizadas**.  
> Este enfoque mejora la cobertura y mantiene las pruebas limpias y reutilizables.

---

### 🔹 Parametrización básica con `@pytest.mark.parametrize`

Permite definir un conjunto de datos para ejecutar el mismo test múltiples veces.

```python
import pytest
from src.calculator.math_ops import MathOperations

@pytest.mark.parametrize("a,b,resultado", [
    (2, 3, 5),
    (4, 1, 3),
    (10, -5, 5)
])
def test_add(a, b, resultado):
    assert MathOperations.add(a, b) == resultado

**📘 Reflexión del día**
Hoy entendí que pytest no solo sirve para validar resultados, sino también para diseñar tests más expresivos y reutilizables.
Con cada refactor, el testing se siente menos como una tarea extra y más como una herramienta de calidad y aprendizaje continuo.