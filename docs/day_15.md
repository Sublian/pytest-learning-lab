# 🧪 Día 15 — Dominando el Aislamiento de Módulos con `mocker`  
## 📌 Y el caso real del fallo en la función `enviar()`

Bienvenido al **Día 15**.  
Hoy consolidamos un punto fundamental en pruebas profesionales:  
**el aislamiento correcto de dependencias y cómo un pequeño detalle puede romper una prueba perfectamente diseñada.**

---

# 🎯 Objetivo del día

- Comprender por qué **el uso correcto de `mocker.patch()`** define el éxito de las pruebas.
- Ver cómo **las pruebas revelan contratos ocultos** en tu código.
- Analizar un caso real de fallo en tu función `enviar()` y cómo lo solucionaste.
- Crear buenas prácticas para asegurar que tus pruebas sean **determinísticas, robustas y predecibles**.

---

# 🚧 1. La importancia de ejecutar correctamente las pruebas

Cuando ejecutamos:
```python
uv run pytest -s -v
```

lo que buscamos es:

1. **Fiabilidad**: cada prueba debe dar siempre la misma respuesta.  
2. **Aislamiento**: las pruebas no deben depender del entorno real (red, API externa, etc).  
3. **Contratos claros**: cuando una prueba falla, revela un comportamiento no definido del sistema.  
4. **Rapidez**: las pruebas mockeadas deben ejecutarse en milisegundos.

Un sistema de pruebas bien diseñado te permite:

- Refactorizar sin miedo  
- Cambiar implementaciones internas sin romper la API  
- Detectar inconsistencias en la lógica  
- Protegerte contra bugs regresivos  

**Esto es ingeniería de software real.**

---

# 🧩 2. Caso real: el fallo en tu función `enviar()`

Tus pruebas estaban correctas.  
Tu implementación original **no seguía el contrato que las pruebas esperaban**.

## 🚨 Escenario de fallos

Estas pruebas eran correctas:

- `test_envio_exitoso`
- `test_envio_falla_status_code`
- `test_envio_timeout`

Pero tu función `enviar()` no cumplía con las expectativas esperadas en cada flujo.

### ❌ Problema 1: No se manejaban excepciones
Esto provocó que:

```python
side_effect=Exception("timeout")
```

hiciera fallar la prueba con un error real:

```python
Exception: timeout
```

❌ Problema 2: El error de status code no devolvía "error"

test_envio_falla_status_code esperaba:

```python
assert r["error"] == 500
```

pero tu función devolvía:

```python
{"ok": False}
```

Esto produjo:

```python
KeyError: 'error'
```

❌ Problema 3: Ajustar un caso rompía otro

Cuando corregías un flujo, otro se rompía porque la lógica no era uniforme.

### La versión final corregida de enviar()

La solución correcta, estable y coherente fue:

```python
def enviar(self, payload):
    try:
        r = requests.post(f"{self.BASE_URL}/send", json=payload, timeout=2)

    except Exception as e:
        # Flujo de error por excepción -> timeout, network error, etc.
        return {"ok": False, "error": str(e)}

    if r.status_code != 200:
        # Flujo de error por status code -> error controlado
        return {"ok": False, "error": r.status_code}

    return {"ok": True, "data": r.json()}
```

Esta versión pasa:

✔ test_envio_exitoso

✔ test_envio_falla_status_code

✔ test_envio_timeout


Y sigue un contrato claro:

|Caso |	Retorno |
|-----------|-----------|
| Éxito	| {"ok": True, "data": ...} |
| Código 400–500 |	{"ok": False, "error": status_code} |
| Excepción |	{"ok": False, "error": "mensaje"} |

## 🧠 Lección aprendida: las pruebas revelan los contratos del sistema

Tus pruebas no estaban mal.
Tu función era la que incumplía varios contratos implícitos que las pruebas estaban definiendo.

Esto es valioso porque:

- Las pruebas actúan como documentación viviente
- Las pruebas fuerzan el diseño correcto
- Las pruebas descubren inconsistencias de lógica
- Las pruebas protegen tu código frente a regresiones

No hay mejor indicador de calidad que un test que falla por la razón correcta.

## 🎉 Conclusión del Día 15

Hoy aprendiste algo muy valioso:

> Las pruebas no solo detectan bugs… revelan el diseño correcto del sistema.

Ver fallar un test no es un problema.
Es una oportunidad para mejorar el contrato, la estabilidad y la claridad del código.

Tu función terminó mejor que como empezó, **gracias a las pruebas.**