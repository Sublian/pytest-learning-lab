
# 🧠 Día 17 — Resumen: Spy vs Mock en Pytest

## 🎯 Objetivo del Día
Comprender con claridad cuándo usar **spy** y cuándo usar **mock**, especialmente al probar flujos donde intervienen funciones externas como servicios de email o API.

---

# 👁️ Mock vs Spy — Diferencias Fundamentales

| Característica | **Mock** | **Spy** |
|----------------|----------|---------|
| Observa llamadas reales | ❌ No | ✅ Sí |
| Ejecuta el código original | ❌ No | ✔️ Sí |
| Se usa para aislar dependencias externas | ✔️ | ⚠️ Algunas veces |
| Permite validar parámetros usados | ✔️ | ✔️ |
| Permite capturar el valor retornado real | ❌ | ✔️ `spy.spy_return` |
| Corta efectos secundarios | ✔️ | ❌ A menos que se mockee internamente |
| Recomendado para | Integraciones externas | Seguimiento de funciones internas |

---

## 🔍 Concepto Clave

### Un Spy **no reemplaza** la función, solo la observa  
→ Si la función tiene efectos reales (email, HTTP), estos ocurrirán a menos que se mockeen internamente.

### Un Mock **reemplaza completamente** la función  
→ No ejecuta lógica real, no genera efectos secundarios.

---

## 🧪 Ideas Clave del Día

✔ Los **Mocks** se usan para:  
- Aislar dependencias externas  
- Simular respuestas  
- Evitar side effects  

✔ Los **Spies** se usan para:  
- Asegurarte de que una función se llamó  
- Ver argumentos reales  
- Capturar el valor retornado real  

---

## 📘 Ejemplos

### Cuándo usar Mock
```python
mock_api = mocker.Mock()
mock_api.enviar.return_value = {"ok": True}
```

---

## 🧩 Conclusión

Hoy consolidaste:
- Por qué un spy puede romper pruebas si la función tiene efectos reales
- Cómo aislar correctamente dependencias usando mock
- Cómo combinar spy + mock para obtener pruebas más ricas
- Cómo interpretar errores como NameResolutionError
- Dominio clave para test avanzado y diseño orientado a testabilidad.

Dominar la diferencia entre spies y mocks marca un salto grande hacia:

- testing avanzado,
- test-driven refactoring,
- pruebas de integración limpias,
- diseño orientado a testabilidad.