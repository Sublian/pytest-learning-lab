# 📘 Mini Resumen – Día 20
### Tests como documentación viva

Hoy trabajamos en un cambio de mentalidad importante:
dejamos de enfocarnos solo en que los tests pasen y empezamos a enfocarnos en qué historia cuentan.

## 🎯 Lo aprendido

- Un test debe responder una sola pregunta.

- Parametrizar no siempre simplifica; a veces oculta reglas.

- Separar tests por:

    - contrato

    - éxito

    - error de negocio

    - error técnico

- El naming importa:
`test_should_<resultado>_when_<condicion>`

- Si dos tests fallan por un pequeño cambio, puede haber:

- sobreacoplamiento

- contrato demasiado rígido

- redundancia estructural

## 🧠 Cambio de nivel

Antes:

>“Tengo tests que cubren casos.”

Ahora:

>“Sé qué decisión protege cada test.”

Ese es el verdadero avance del Día 20.