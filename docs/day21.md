
# Pytest Learning Lab
## Día 21 — Uso avanzado de `side_effect`

### 🎯 Objetivo
Aprender a utilizar `side_effect` en mocks para simular comportamientos más realistas de dependencias externas como APIs, bases de datos o servicios externos.

---

## Concepto clave

En pruebas unitarias, muchas veces dependemos de servicios externos.

Ejemplo:

- APIs
- Servicios de correo
- Pasarelas de pago
- Microservicios

No queremos llamar estos servicios en nuestras pruebas.

Para eso usamos **mocks**.

`pytest-mock` permite modificar el comportamiento de un mock usando:

- `return_value`
- `side_effect`

---

# 1️⃣ return_value (comportamiento fijo)

El mock siempre devuelve el mismo valor.

```python
fake_api.check_payment.return_value = {"status": "approved"}
```

Cada llamada devuelve exactamente lo mismo.

Esto funciona bien cuando el comportamiento no cambia.

---

# 2️⃣ side_effect para simular errores

También podemos usarlo para lanzar excepciones.

```python
fake_api.check_payment.side_effect = TimeoutError
```

Esto permite probar cómo reacciona nuestro código ante fallos externos.

---

# 3️⃣ side_effect dinámico (concepto central del día 21)

Aquí está el concepto más importante.

side_effect puede recibir una función.

Esto permite que el mock cambie su comportamiento dependiendo de los argumentos.

```python
def fake_check_payment(amount):

    if amount < 100:
        return {"status": "approved"}

    if amount <= 500:
        return {"status": "review"}

    return {"status": "rejected"}

fake_api.check_payment.side_effect = fake_check_payment
```

Ahora el mock se comporta como una API real.

---

# 4️⃣ side_effect secuencial

También podemos simular respuestas en secuencia.

```python
fake_api.check_payment.side_effect = [
    {"status": "approved"},
    {"status": "review"},
    {"status": "rejected"},
]
```

Cada llamada devuelve el siguiente valor.

Esto es útil para simular:

- retries

- estados progresivos

- workflows

### Comparación rápida

Técnica    |	Uso
|-|-|
return_value    |	respuesta fija
side_effect = Exception	    | simular fallos
side_effect = list	    | respuestas secuenciales
side_effect = function	    | comportamiento dinámico

---

# Qué aprendimos realmente

En el Día 21 dominamos:

- mocks simples

- mocks con valores fijos

- mocks que simulan errores

- mocks que cambian comportamiento dinámicamente

Esto representa nivel intermedio de testing con pytest.