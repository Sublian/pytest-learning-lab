# 🧪 Pytest Learning Lab

This repository documents my learning journey with **pytest**, automation, and testing best practices using Python.

## 🚀 Project Overview
This lab includes:
- Test-driven examples using `pytest`
- Parametrization and fixtures
- Exception handling and advanced test scenarios
- Code profiling and optimization techniques

## 📂 Structure
```bash
pytest-uv-project/
├── src/ # Core code
├── tests/ # Unit and integration tests
└── pyproject.toml # uv project configuration

```

## 🧰 Tools
- Python 3.11+
- [pytest](https://docs.pytest.org)
- [uv](https://github.com/astral-sh/uv)
- GitHub Actions (future integration)


---

### ⚙️ Inicialización del entorno con UV

```bash
# Activar el entorno virtual
uv venv

# Instalar pytest y plugins
uv pip install pytest pytest-cov pytest-mock
```
## Ejecutar los tests completos:
>uv run pytest -v

## Ejecutar los tests por marcador:
>uv run pytest -m error_handling -v
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
```

**📘 Reflexión del día**
Hoy entendí que pytest no solo sirve para validar resultados, sino también para diseñar tests más expresivos y reutilizables.
Con cada refactor, el testing se siente menos como una tarea extra y más como una herramienta de calidad y aprendizaje continuo.

---

## 🧩 Día 5 — Pytest + UV: Parametrización Avanzada y Markers
### 🎯 Objetivos del día

> En este día aprendimos a combinar **fixtures, parametrización y markers personalizados**,  
> tres pilares para estructurar pruebas profesionales y reutilizables en Python.  
> Además, exploramos la ejecución selectiva y el manejo de casos de error.

## 🛠️ Solución a los Warnings de Markers 
### (Agrega tus marcas personalizadas en el archivo pyproject.toml)

``` python
[tool.pytest.ini_options]
markers = [
    "rapidas: pruebas rápidas",
    "lentas: pruebas con operaciones costosas",
    "error_handling: validación de manejo de errores"
]
```

### 🧭 Resumen rápido día 5
| Concepto | Qué hace | Cuándo usarlo |
|-----------|-----------|----------------|
| @pytest.mark.parametrize | Ejecuta múltiples escenarios con un mismo test | Varias combinaciones de entrada  | 
| Fixtures combinadas | Reutiliza datos o configuraciones | Escenarios repetitivos | 
| Markers personalizados | Agrupa y filtra pruebas | Ejecución selectiva (rápidas, lentas, errores) | 
| conftest.py | Centraliza fixtures globales | Configuración común de tests | 

---


## 🧩 Día 6 — Pruebas con Mocks: Simulando Dependencias Externas
### 🎯 Objetivo del Día

>Aprender a aislar el código que depende de servicios externos (APIs, correo, archivos, BD, etc.)
>utilizando herramientas de mocking que ofrece pytest + unittest.mock.
>“El mocking no es mentirle al código —
>es enseñarle a pensar por sí mismo en un entorno controlado,
>es construir un entorno seguro donde el código puede fallar sin consecuencias.”

---
### ⚙️ Instalación de dependencias

Antes de ejecutar los ejemplos, instala la librería `requests` en tu entorno virtual manejado por **uv**:

```bash
# Activar entorno virtual si no está activo
uv venv

# Instalar requests dentro del entorno
uv pip install requests
```

### 🧠 Explicación Detallada del Mock
|Elemento |	Qué hace |	Ejemplo|
|-----------|-----------|----------------|
|@patch("src.calculator.financial.requests.get") |	Sustituye la función real requests.get por un mock temporal |	Evita llamadas reales a internet|
|MagicMock() |	Crea un objeto flexible que puede simular cualquier atributo o método |	mock_response.json.return_value = {...}|
|assert_called_once_with() |	Verifica que la función se haya llamado correctamente |	Previene llamadas duplicadas o erróneas|
|pytest.raises(ConnectionError) |	Comprueba el flujo de error esperado |	Asegura que la app responde correctamente a fallos externos|

### 🧭 Resumen del Día 6 — Parte 2
| Concepto | Descripción | Beneficio |
|-----------|-----------|----------------|
|Mock de requests |	Sustituye llamadas reales a la red |	Tests sin conexión|
|MagicMock |	Crea objetos con comportamiento controlado |	Simula APIs o archivos|
|Parametrización con mocks |	Prueba múltiples escenarios rápidamente |	Mayor cobertura|
|Combinación con markers |	Clasifica tests por tipo (API, errores, etc.) |	Organización profesional|

## 🧭 Pytest + UV — Mini Guía Visual (Día 6)

> 💡 Esta guía resume los comandos y patrones más útiles de **pytest** cuando se combina con **uv**.  
> Ideal como referencia rápida durante el desarrollo o debugging de tests.


### 🧭 En resumen
|Objetivo |	Comando|
|-----------|-----------|
|Ejecutar todos los tests |	uv run pytest|
|Ejecutar un archivo |	uv run pytest tests/test_math_ops.py|
|Ejecutar una función específica |	uv run pytest tests/test_math_ops.py::test_sumatoria_basica|
|Ejecutar por marker |	uv run pytest -m api|
|Ejecutar con varios markers |	uv run pytest -m "api or error_handling"|
|Ejecutar con filtro de nombre |	uv run pytest -k interest|

---

## 🧩 Día 7 — Mocking y Pruebas con `requests` en Pytest + UVs

> 🎯 Objetivo: aprender a simular comportamientos externos (APIs, archivos, bases de datos)  
> sin depender de servicios reales, usando **mocking** para mantener las pruebas rápidas, seguras y determinísticas.

### 🔹 ¿Qué es el *Mocking*?
El **mocking** (simulación) permite reemplazar dependencias externas por **objetos falsos**  
que imitan su comportamiento esperado durante las pruebas.
Se usa para probar la lógica del código sin depender de factores externos como:

- 🔗 APIs externas que pueden fallar o ser lentas  
- 💾 Archivos o bases de datos con acceso restringido  
- 🌐 Conexiones HTTP no disponibles en el entorno de test  

### ⚙️ Instalación del soporte para Mocking
Ya que trabajamos con `uv`, instalaremos `pytest-mock` y `requests` así:

```bash
uv add pytest-mock requests
```

Esto permite usar la fixture mocker, incluida con pytest-mock, para simular objetos o funciones.

🧠 Conclusión del Día 7
|Concepto |	Qué Aprendiste|
|-----------|-----------|
|mocker.patch() | Reemplazar funciones o módulos externos|
|return_value | 	Simular valores de retorno|
|assert_called_with() | 	Verificar argumentos usados en la llamada|
|Parametrización + Mock | 	Probar varios escenarios de API en una sola función|
|Fixture de Mock | 	Reutilizar simulaciones en múltiples tests|

### 🧩 Aprender a hacer mocking no solo ahorra tiempo, sino que también permite testear lo imposible: lo que aún no existe o no se puede conectar.

---