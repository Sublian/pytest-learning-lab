
# 📘 Día 19 – Lección 2

“Cuándo NO parametrizar y cuándo dividir tests”

Esta lección no es técnica, es criterial.
Aquí se empieza a notar la diferencia entre “sé usar pytest” y “sé diseñar tests”.

---

## 🎯 Objetivo de esta segunda lección

Aprender a leer una matriz de casos y decidir:

- ❌ cuándo la parametrización empieza a esconder reglas

- ✅ cuándo dividir tests mejora claridad

- 🧠 cómo pensar como revisor / maintainer, no solo como autor

---

## 🧠 Punto de partida (tu estado actual)

Tú hiciste esto 👇 (resumido):

```
@pytest.mark.parametrize(
    "api_response, esperado",
    [
        ({"ok": True}, {...}),
        ({"ok": False, "error": "fondos"}, {...}),
        ({"ok": False, "error": "timeout"}, {...}),
        ...
    ]
)
def test_procesar_pago_parametrizado(...):
    ...
```

✔ Correcto

✔ Funciona

✔ Cubre muchos casos

Pero ahora hiciste algo mejor 👇

👉 lo duplicaste conscientemente en tests más específicos.

Y eso es justo lo que vamos a formalizar.

---

## 🔍 Concepto clave del Día 19 (nivel intermedio)

❗ Parametrizar ≠ simplificar

Parametrizar:

- reduce líneas

- pero puede aumentar carga cognitiva

La pregunta correcta NO es:

> “¿Puedo parametrizar esto?”

La pregunta correcta ES:

> “¿Estoy probando una sola regla o varias?”

---

## 🧪 Análisis de tus tests actuales

1️⃣ test_procesar_pago_parametrizado

Este test responde a:

- ¿El servicio traduce correctamente la respuesta de la API?

👉 Es un test de contrato

👉 Está bien que sea amplio

👉 Puede convivir con otros tests

✔ Se queda

2️⃣ test_pago_exitoso

```
def test_pago_exitoso(...):
    ...
```

Este test responde a:

- ¿Qué significa éxito para el negocio?

👉 Regla clara

👉 Nombre claro

👉 Fallo claro

✔ Muy bien diseñado

3️⃣ test_pago_error_negocio

```
@pytest.mark.parametrize("error", [...])
def test_pago_error_negocio(...):
```

Este test responde a:

- ¿Cómo maneja errores esperados del negocio?

👉 Aquí la parametrización sí suma

- misma regla

- diferentes datos

✔ Uso correcto de parametrización

4️⃣ test_pago_error_tecnico

```
def test_pago_error_tecnico(...):
```

Este test responde a:

- ¿Qué pasa cuando la API falla de forma inesperada?

👉 Conceptualmente distinto

👉 Merece su propio espacio

✔ Separación correcta

---

## 📌 Regla de oro del Día 19 (escríbela mentalmente)

> Un test debe responder una sola pregunta.
> Si el nombre necesita “y”, probablemente son dos tests.

---

## 🧠 Comparación visual

## ❌ Antes (un solo test)

¿Funciona?

¿Falla?

¿Por qué falla?

¿Quién falla?

¿Es técnico?

¿Es negocio?


Todo en uno 😵‍💫

## ✅ Después (tu estado actual)

Test |	Pregunta
| ------------- |:-------------:|
test_procesar_pago_parametrizado |	¿Contrato general OK?
test_pago_exitoso | 	¿Qué es éxito?
test_pago_error_negocio	| ¿Errores esperados?
test_pago_error_tecnico	| ¿Errores inesperados?

👉 Esto ya es diseño de pruebas, no solo pytest.

---

## 🧪 Ejercicio mental (sin escribir código)

Dado este caso nuevo:

> “Si el monto es 0, el pago no debe enviarse a la API”

Pregúntate:

- ¿parametrizo?

- ¿nuevo test?

- ¿nuevo archivo?

👉 Respuesta correcta:

- nuevo test

- nueva regla

- no parametrizar con errores de API

---

## ✅ Criterios de éxito del Día 19 (completados)

✔ Tests pasan

✔ Tests dicen qué falló

✔ Tests cuentan historias

✔ Parametrización usada con criterio

✔ Código más largo pero más claro

🔥 <b>Nivel intermedio desbloqueado</b>