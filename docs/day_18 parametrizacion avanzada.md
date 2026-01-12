
## 🎯 Objetivo del día
Comprender **dónde y cómo aplicar mocks correctamente** para lograr **tests unitarios aislados**, evitando llamadas reales a servicios externos y falsos positivos.

---

## 🧠 Idea central (la más importante del curso hasta ahora)

> **Los mocks se aplican en el lugar donde la función ES USADA,  
no donde está definida.**

Esta regla explica más del 70% de los errores con mocks en proyectos reales.

---

## 🔍 Qué aprendimos realmente

Durante el Día 18 descubrimos que:

- Un test puede “pasar” aunque esté mal diseñado
- Ver errores reales (HTTP, logs, prints) dentro de un test **es una señal de alarma**
- Mockear el módulo incorrecto provoca que:
  - El código real se ejecute
  - Se rompa el aislamiento
  - Tengamos falsos positivos o falsos negativos

---

## ❌ Error típico detectado

```python
mocker.patch("src.mailing.email_service.enviar_notificacion")
```

Este mock NO afecta a Notificador porque:

```python
# notificador.py
from src.mailing.email_service import enviar_notificacion
Aquí Python crea una referencia local, independiente.
```

## ✅ Solución correcta

```python
# notificador.py
mocker.patch("src.workflow.notificador.enviar_notificacion")
```

Ahora el mock reemplaza exactamente lo que el código ejecuta.

---

## 🧪 Resultado práctico

Después de corregir el mock:

✅ Todos los tests pasan de forma consistente

✅ No hay llamadas reales a red

✅ El comportamiento depende solo del escenario del test

✅ El test es determinista y confiable

---

## 🚨 Falso positivo (concepto crítico)

Uno de los tests pasaba por casualidad porque:

El servicio real fallaba

El valor False coincidía con lo esperado

Esto es extremadamente peligroso en entornos reales.

## 🧠 Regla mental definitiva

Cuando escribas un mock, pregúntate:

“¿Desde qué archivo se está llamando esta función?”

Ese es el path que debes mockear.
