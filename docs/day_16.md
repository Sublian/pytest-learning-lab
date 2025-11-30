
# 🧪 Lección 16 (Refuerzo) — Mocks vs Spies & Aislamiento Profesional en Pytest

## 🎯 Objetivo de Aprendizaje
Profundizar en el uso correcto de mocks y spies, reforzando cómo aislar módulos y cómo elegir la técnica adecuada según el diseño y comportamiento esperado.

---

## 🔍 Enfoque de Implementación

### 1. **Mocks**
Son objetos totalmente simulados; reemplazan por completo a la dependencia real.

**Útil para:**
- APIs externas
- requests
- bases de datos
- correo electrónico
- integraciones con otros servicios

**Ventaja:**  
Aislamiento total, velocidad, control absoluto de la entrada/salida.

---

### 2. **Spies**
Son observadores que permiten ver cuántas veces se llamó una función, qué argumentos recibió y qué devolvió, sin necesidad de reemplazarla.

**Útil para:**
- Funciones puras
- Transformaciones de datos
- Validar composición interna de funciones
- Confirmar la secuencia de pasos en un flujo

**Ventaja:**  
Permiten probar flujos internos sin perder la lógica original.

---

## 📊 Cuadro Comparativo

| Aspecto | Mock | Spy |
|--------|------|------|
| ¿Ejecuta la lógica real? | ❌ No | ✔️ Sí (si no se sobreescribe) |
| ¿Control del entorno? | Alto | Medio |
| ¿Velocidad? | Alta | Media |
| ¿Riesgo de falsos positivos? | Alto (si el mock no representa la realidad) | Bajo |
| ¿Ideal para? | Integraciones | Transformaciones internas |
| ¿Aislamiento? | Total | Parcial |

---

# 🧪 Día 16 — Parte 2  
# Ejercicios Prácticos Avanzados de Mock y Spy

## 🎯 Objetivo de Aprendizaje
- Aplicar mock y spy en escenarios reales de APIs, cálculos financieros y servicios de correo.
- Practicar aislamiento total y parcial de módulos.
- Comprender cuándo usar spy para lógica interna y cuándo mock para dependencias externas.

---

## 📚 Conceptos a Practicar
- [ ] Mock de `requests.post` y `requests.get`
- [ ] Spy sobre métodos reales para observar flujo
- [ ] Aislamiento interno vs externo
- [ ] Simulación de excepciones y JSON corrupto
- [ ] Validación de argumentos de llamadas

---

## ✅ Criterios de Éxito
- [ ] Pruebas ejecutan correctamente
- [ ] Se mockean dependencias externas correctamente
- [ ] Se utilizan spies para validar flujos internos sin romper la ejecución
- [ ] La suite completa funciona bajo `pytest -q`

---

## 🔍 Enfoque de Implementación
1. **Aislar APIs externas con mocks**  
   (`ApiClient`, `get_remote_interest_rate`, `email_service`).

2. **Revisar el flujo interno con spies**, sin detener la ejecución real  
   (`compound_interest`, `calculate_loan_payment`, `ApiClient.enviar`).

3. **Validar argumentos, cantidad de llamadas, valores retornados**  
   usando:
   - `spy.call_args`
   - `spy.spy_return`
   - `mock.assert_called_once()`

---
## 🧪 EJERCICIO 1

✔ Mock + Spy sobre ApiClient.enviar

Objetivo. Aprender a:

- Mockear la API externa (requests.post)

- Usar spy sobre la función interna enviar para observar argumentos, llamadas y flujo.

✅ Código de prueba

<tests/test_app_api_client_spy_mock.py

## 🧪 EJERCICIO 2

✔ Mock total sobre API externa: FinancialCalculator.get_remote_interest_rate
Objetivo. Aislar completamente la llamada remota.

✅ Código de prueba

<tests/test_financial_remote_api.py

## 🧪 EJERCICIO 3

✔ Spy para validar flujo interno de funciones puras

Este ejercicio te enseña cómo spyar funciones que sí quieres ejecutar.

✅ Código de prueba

<tests/test_financial_spy_functions.py

## 🧪 EJERCICIO 4

✔ Mock avanzado sobre email_service.enviar_notificacion

Este ejercicio combina:

- mock de requests.post

- manejar status distintos

- simular JSON corrupto

✅ Código de prueba

<tests/test_email_service_mock.py

---
## 📖 Recursos
- Pytest Mock Documentation  
  https://pytest-mock.readthedocs.io/

- unittest.mock documentation  
  https://docs.python.org/3/library/unittest.mock.html

- Artículo recomendado:  
  *“Mock vs Spy — Cómo testear comportamiento real sin perder aislamiento”*



uv run pytest tests/test_workflow_spy.py -v -s