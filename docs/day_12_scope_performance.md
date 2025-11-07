## 🧪 Día 12: Testing con Scope y Performance Fixtures

**Objetivo:**  
Comprender cómo optimizar y controlar el rendimiento de las pruebas usando el parámetro `scope` de las fixtures (`function`, `class`, `module`, `session`) y la opción `--durations` para medir los tiempos de ejecución.

---

### 📘 Conceptos Clave

#### 🔹 1. Qué es el `scope` en las fixtures
Cada fixture puede definirse con un alcance diferente que determina **cuándo se crea y destruye**:

| Scope | Se ejecuta... | Ideal para... |
|--------|----------------|----------------|
| `function` | Antes y después de **cada test** | Casos rápidos y aislados |
| `class` | Una vez por **clase de tests** | Tests que comparten datos comunes |
| `module` | Una vez por **archivo de test** | Conexiones de DB o recursos costosos |
| `session` | Una vez por **toda la ejecución** | Configuraciones globales o caches |

---

#### 🔹 2. Medir rendimiento con `--durations`

Ejecuta:
```bash
uv run pytest -v --durations=0
