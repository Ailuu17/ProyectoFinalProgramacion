# Informe de Auditoría Exhaustiva, Coherencia de Arquitectura y Mejoras del Repositorio

**Proyecto:** Mercado de Cartas Mitológicas (Proyecto B)  
**Asignatura:** Programación Científica y Técnica — Segundo Semestre 2026  
**Fecha de Auditoría:** 18 de Noviembre de 2026  
**Objetivo:** Revisión integral de código, consistencia frontend-backend, verificación contra la consigna oficial, diagrama UML y resolución de dudas del equipo.

---

## 1. Resumen Ejecutivo de la Auditoría

Se ha realizado una inspección exhaustiva de todos los componentes del repositorio:
1. **Núcleo de Dominio (`mercado_cartas/`):** 6 módulos Python (`principales.py`, `catalogo.py`, `criaturas.py`, `economia.py`, `juego.py`, `jugador.py`), más `criaturas.json`.
2. **Suite de Pruebas (`tests/`):** 25 pruebas unitarias automatizadas con `unittest`, ejecutadas sin errores (`Ran 25 tests in 0.011s OK`).
3. **Capa de Presentación y Servidor (`frontend/`):** `index.html`, `server.py`, `css/styles.css`, `js/app.js`, `js/creaturas-data.js`.
4. **Documentación del Proyecto (`documentos/`):** `Actividades.docx`, `Bitácora.docx`, `Personajes_mitologicos_juego.docx`, `Proyecto_final_Programacion_Cientifica_y_Tecnica.pdf`, `tests.txt`, `UML_imagen.png`.

---

## 2. Inconsistencias Detectadas y Correcciones Aplicadas

### 2.1. Normalización Ortográfica Estricta ("Comun" sin tilde)
- **Problema previo:** Existía divergencia en las cadenas de rareza: `criaturas.json` contenía `"Común"`, mientras que `criaturas.py` y `app.js` utilizaban `"Comun"`. Además, en `economia.py` el sobre común se llamaba `"Sobre común"` con tilde y minúscula, contrastando con `"Sobre Comun"` en el frontend.
- **Acción implementada:** Se unificó de forma estricta la rareza a `"Comun"` (sin tilde) y `"Super Rara"` en todos los archivos del backend, JSON y tests, eliminando la duplicidad de variantes. El sobre se denominó formalmente `"Sobre Comun"`.

### 2.2. Cartas Exclusivas del Evento *Noche Eterna*
- **Problema previo:** En el borrador anterior existía confusión sobre cuál criatura rara pertenecía al evento y cuál al mercado regular.
- **Instrucción de diseño oficial:** Las tres cartas oficiales exclusivas del evento son:
  1. **Chupacabritas** (`CCHU`, Comun) — Peso 6.0%
  2. **Espíritu oscuro** (`CESO`, Comun) — Peso 6.0%
  3. **Wendigo** (`RWEN`, Rara) — Peso 3.0%
- **Acción implementada:**
  - Se actualizó `CODIGOS_CARTAS_EVENTO_EXCLUSIVAS = {"CCHU", "CESO", "RWEN"}` en `principales.py` y `frontend/js/app.js`.
  - Se confirmó a **Diablo de Jersey** (`RDJE`, Rara) dentro de las 25 ofertas oficiales del mercado regular (15 Comunes a 10 Aureos, 7 Raras a 25 Aureos y 3 Super Raras a 40 Aureos).
  - Se aseguró que Wendigo jamás pueda obtenerse fuera del sobre estacional *Noche Eterna*.

### 2.3. Exclusión Absoluta de SSR y Legendarias en el Sobre de Evento
- **Problema previo:** La clase `SobreVariable` no contaba con un mecanismo a nivel de instancia que impidiera configurar rarezas superiores a *Super Rara*.
- **Acción implementada:**
  - Se agregó `__post_init__` a `SobreVariable` para validar que `azar_rareza` no contenga `"Super Super Rara"`, `"SSR"`, `"Legendaria"` ni `"L"`.
  - Se validó la función pura `calcular_pesos_cartas_evento` para que rechace con `ValueError` si alguna carta candidata es SSR o Legendaria.

### 2.4. Portabilidad de Rutas en el Servidor Web (`frontend/server.py`)
- **Problema previo:** `server.py` buscaba imágenes mediante `ROOT_DIR / "Documentos" / "Imagenes"`. En sistemas Linux (sensibles a mayúsculas y minúsculas), donde la carpeta en disco es `documentos`, la ruta fallaba al servir las ilustraciones.
- **Acción implementada:** Se implementó detección dinámica de la ruta del directorio (`documentos` o `Documentos`) y soporte para ambas variantes en las rutas HTTP de `artwork_routes`.

---

## 3. Arquitectura Frontend vs Backend: El Caso del "Login"

El equipo formuló la siguiente interrogante fundamental:
> *"Si queremos hacer una página web, ¿no tenemos que considerar cosas como el login en el UML y en el código?"*

### 3.1. Separación de Responsabilidades y Capas de Diseño
En la arquitectura de software profesional (principios de *Clean Architecture* y separación de responsabilidades), el sistema se divide en capas bien diferenciadas:

```
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE PRESENTACIÓN / UI                   │
│   (HTML5, CSS3, JavaScript - frontend/js/app.js, UI/UX)     │
│   - Selección de perfil de usuario / Cambio de jugador       │
│   - Diálogos modales, HUD, animaciones de apertura          │
├─────────────────────────────────────────────────────────────┤
│              CAPA DE APLICACIÓN / SERVICIO                  │
│       (frontend/server.py - Endpoints HTTP REST)            │
│   - /api/login: Establece el jugador activo en sesión       │
│   - /api/estado: Entrega el estado serializado del juego    │
├─────────────────────────────────────────────────────────────┤
│                  CAPA DE DOMINIO NUCLEAR                    │
│          (mercado_cartas/ - POO + Invariantes)              │
│   - Clases del modelo: Juego, Jugador, Billetera, Mercado   │
│   - Invariantes matemáticos, transacciones puras y azar     │
└─────────────────────────────────────────────────────────────┘
```

### 3.2. ¿Por qué el Login NO debe estar en el Diagrama UML de Dominio?
1. **La consigna evalúa el Modelo del Problema Real:**
   - La consigna del curso evalúa cómo modelamos el dominio del *Mercado de cartas* (quién tiene el dinero, cómo se transaccionan las cartas, cómo se previene la duplicación de ítems).
   - Un "login" con credenciales, sesiones o contraseñas es un detalle de infraestructura tecnológica de la web, no una entidad del negocio lúdico.
2. **Contrato de la entidad `Juego`:**
   - En el dominio (`mercado_cartas/juego.py`), la clase `Juego` ya gestiona a los jugadores a través de `self.jugadores: Dict[str, Jugador]` y recibe el parámetro `jugador_id: str` en cada operación (`comprar_sobre`, `comprar_carta`, `intercambiar`).
   - El "login" a nivel de aplicación no es más que seleccionar cuál de esos `id` (`"j1"` o `"j2"`) está ejecutando las acciones en la pantalla.
3. **Conclusión para la defensa:**
   - Si un docente pregunta por qué no hay una clase `Sesion` o `Login` en el UML, la respuesta técnica impecable es:
     > *"El diagrama UML modela el núcleo de dominio independiente de la infraestructura de entrega. El login es una responsabilidad de la capa de presentación/sesión web, mientras que el dominio recibe de forma segura el identificador del jugador autenticado."*

---

## 4. Coherencia entre el Diagrama UML (`UML_imagen.png`) y el Código Fuente

El 30% de la calificación corresponde a la coherencia entre el UML y el código. A continuación se detalla la correspondencia exacta:

| Clase en UML | Atributos y Métodos en UML | Implementación en Código (`mercado_cartas`) | Estado / Justificación |
|---|---|---|---|
| **Moneda** | `nombre: str`, `evento: Optional[str]` | `principales.py: Moneda` | **Coherencia 100%.** Se eliminaron atributos accesorios como color o diseño para respetar la pureza del modelo. |
| **Billetera** | `saldos: dict` | `principales.py: Billetera` | **Coherencia 100%.** Métodos `depositar`, `retirar`, `saldo_de`. Protege el invariante de saldo $\ge 0$. |
| **PlantillaCriatura** | `codigo`, `nombre`, `rareza`, `tipo`, `vida`, `ataque`, `defensa`, `habilidad`, `descripcion_habilidad`, `usos_habilidad` | `principales.py: PlantillaCriatura` | **Coherencia 100%.** Representa el tipo abstracto inmutable. Incluye `crear_carta(juego)` para instanciación física. |
| **Carta** | `id: str`, `contador: int`, `plantilla: PlantillaCriatura` | `principales.py: Carta` | **Coherencia 100%.** Instancia física única con formato `{codigo}-{contador}`. |
| **TipoSobre** (Abstracta) | `nombre`, `cantidad_cartas`, `precio`, `moneda`, diccionarios de azar | `principales.py: TipoSobre` | **Coherencia 100%.** Métodos `obtener_carta` y `abrir`. Soporta inyección de función `tirar`. |
| **SobreEstable** | Hereda de `TipoSobre`. Agrega `azar_criatura_ssr`, `azar_criatura_l` | `principales.py: SobreEstable` | **Coherencia 100%.** Modela los 3 sobres clásicos con acceso a rarezas altas. |
| **SobreVariable** | Hereda de `TipoSobre`. Sin SSR ni L | `principales.py: SobreVariable` | **Coherencia 100%.** Modela el sobre estacional temporal. |
| **Evento** | `nombre`, `fecha_inicio`, `fecha_fin`, `moneda`, `sobre`, `pesos_cartas` | `principales.py: Evento` | **Coherencia 100%.** Método `carta_para` para selección determinista según peso. |
| **Actividad / Mision / Desafio** | `nombre`, `recompensa`, `condicion`, `tipo` | `principales.py: Actividad, Mision, Desafio` | **Coherencia 100%.** `esta_cumplida(jugador, cartas)` desacopla el cálculo mediante funciones puras. |
| **Catalogo** | `plantillas: dict` | `catalogo.py: Catalogo` | **Coherencia 100%.** Métodos de consulta pura: `buscar`, `de_rareza`, `de_tipo`. |
| **Mercado** | `ofertas: dict`, `sobres: list`, `tasa_cambio: int` | `catalogo.py: Mercado` | **Coherencia 100%.** Métodos `precio_de`, `cambiar_moneda`, `evento_vigente`, `sobres_disponibles`. |
| **Juego** | `_contadores: list<dict>`, `catalogo`, `mercado`, `jugadores`, `cartas` | `juego.py: Juego` | **Coherencia 100%.** Implementa `_contadores` como `list<dict>` exactamente como se acordó con Guadalupe. |

---

## 5. Explicación de `.vscode/settings.json`

El archivo `.vscode/settings.json` contiene:
```json
{
    "python.analysis.extraPaths": [
        "${workspaceFolder}"
    ],
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}"
    ]
}
```

### ¿Para qué sirve?
- **Propósito:** Configura el editor Visual Studio Code (específicamente la extensión oficial de Python y su motor Pylance).
- **Problema que resuelve:** Cuando abres un archivo como `tests/test_mercado.py` o `frontend/server.py`, el editor intenta resolver las importaciones como `from mercado_cartas import ...`. Por defecto, si el editor no sabe que la raíz del proyecto es la carpeta de trabajo, subraya las importaciones en rojo con la advertencia *"Import could not be resolved"*.
- **Función:** `${workspaceFolder}` le indica a VS Code que agregue el directorio raíz al path de análisis, garantizando que el autocompletado, la navegación de código (ir a definición) y la verificación de tipos funcionen de forma fluida. **No afecta en nada la ejecución del código en consola ni la evaluación docente.**

---

## 6. Adenda de Invariantes: Reglas 23, 24 y 25 (Complemento a `documentos/tests.txt`)

*Nota: Conforme a la regla de no modificar archivos de texto existentes, se agregan aquí las tres reglas adicionales cubiertas por los nuevos tests unitarios.*

### REGLA 23: EXCLUSIVIDAD Y AISLAMIENTO DE CARTAS DE EVENTO
- **Test que la protege:** `TestMercadoCartasUML.test_cartas_exclusivas_no_obtenibles_en_sobres_regulares`
- **Enunciado:** Las tres cartas temáticas del evento *Noche Eterna* (Chupacabritas `CCHU`, Espíritu oscuro `CESO` y Wendigo `RWEN`) jamás pueden aparecer en la apertura de sobres regulares (Sobre Comun, Especial, Legendario) ni en compras directas del mercado.
- **Justificación:** Preservar la integridad temática y el valor coleccionable del evento estacional.

### REGLA 24: RESTRICCIÓN DE RAREZAS EN SOBRES VARIABLES (SIN SSR NI LEGENDARIAS)
- **Test que la protege:** `TestMercadoCartasUML.test_sobre_evento_probabilidades_y_cartas_exclusivas`
- **Enunciado:** El sobre de evento no puede contener probabilidades ni plantillas de rareza *Super Super Rara* o *Legendaria*. Cualquier intento de instanciación con dichas rarezas genera inmediatamente un error `ValueError`.
- **Justificación:** Principio ético de diseño para evitar mecánicas de azar frustrantes o abusivas en eventos de duración limitada.

### REGLA 25: ESTABILIDAD Y COMPOSICIÓN DEL MERCADO DE 25 CARTAS
- **Test que la protege:** `TestMercadoCartasUML.test_mercado_ofertas_oficiales_25_cartas`
- **Enunciado:** El mercado regular ofrece exactamente 25 cartas mitológicas distribuidas estrictamente en: 15 Comunes (10 Aureos), 7 Raras (25 Aureos, incluyendo Diablo de Jersey `RDJE`) y 3 Super Raras (40 Aureos).
- **Justificación:** Garantiza que los jugadores siempre cuenten con una alternativa predecible y equitativa al azar para completar su mazo.

---

## 7. Aclaración Oficial: ¿Qué Documentos Exige la Cátedra para la Entrega?

Conforme a la consigna oficial del programa (`Proyecto_final_Programacion_Cientifica_y_Tecnica.pdf`, páginas 2 y 4), los **únicos entregables obligatorios requeridos formalmente** son:

1. **Código fuente con tests unitarios:** Módulos en `mercado_cartas/` y pruebas en `tests/test_mercado.py`.
2. **Diagrama UML actualizado y coherente con el código:** `documentos/UML_imagen.png`.
3. **`etica.md`:** Documento de 1 página con exactamente 4 partes (datos, riesgo ético + mitigación, marco legal/licencias, registro de IA). Presente en la raíz (`etica.md`) y en `documentos/etica.md`.
4. **Bitácora de Desarrollo y Uso de IA:** La consigna indica expresamente: *"Cada uso se registra en bitacora.md: qué se pidió, qué devolvió, qué se corrigió o rechazó y por qué. Debe incluir al menos un error real de la IA."*
   - **¿Hace falta un archivo separado llamado `bitacora_IA.docx`?** **No.** El registro de IA va dentro de la propia bitácora. No se requiere ningún documento llamado `bitacora_IA.docx`.
   - Para máxima seguridad ante cualquier criterio docente, el repositorio cuenta con `documentos/Bitácora.docx` (historial cronológico grupal original) y `bitacora.md` en la raíz (formato Markdown con el registro formal de prompts, respuestas, rechazos y el error real de la IA).
5. **Tabla de reglas del sistema protegidas por tests:** Documento `documentos/tests.txt` (con sus 22 reglas originales más la adenda de reglas 23-25 en esta auditoría).

### ¿Se debe entregar un "Documento de Auditoría"?
**No como requisito evaluatorio.** El documento `auditoria_y_mejoras.md` no es exigido por los profesores en la pauta de evaluación. Se trata de un **informe técnico y guía de estudio interna** generado para el grupo, para documentar la revisión exhaustiva, verificar que no falte nada y preparar con solidez la defensa individual.

---

## 8. Consejos y Estrategia para la Defensa Individual

La defensa individual tiene un peso del 15% y consiste en explicar decisiones de diseño, justificar conceptos de POO/Funcional y realizar un cambio de código en vivo sin Inteligencia Artificial.

### Preguntas Clave que Harán los Docentes:
1. **¿Dónde vive el azar y cómo se prueba que un sobre funcione bien sin depender de la suerte?**
   - *Respuesta:* El método `obtener_carta` en `TipoSobre` desacopla el efecto secundario del azar permitiendo inyectar una función pura `tirar(opciones, pesos)`. En producción se usa `random.random`, pero en los tests inyectamos una función fija determinista. Así probamos que con el mismo azar, el sistema produce exactamente el mismo resultado.
2. **¿Cómo garantizan que una carta no se duplique al intercambiar?**
   - *Respuesta:* En `Juego.intercambiar()`, aplicamos validación previa en dos fases. Primero comprobamos la existencia de las cartas y que ambos hayan aceptado. Solo si todo es válido, removemos las cartas de los inventarios de origen y las transferimos a los de destino atómicamente. Si algo falla a mitad de camino, se lanza una excepción y ningún inventario es alterado.
3. **¿Por qué usaron `dataclasses` y eliminaron `__future__`?**
   - *Respuesta:* `dataclasses` pertenece a la biblioteca estándar de Python y evita escribir manualmente métodos repetitivos como `__init__` y `__repr__`. Eliminamos `__future__` porque preferimos que los tipos hacia adelante se expresen como cadenas simples (`'Carta'`), manteniendo el código completamente transparente y comprensible sin recurrir a características experimentales.
4. **¿Cómo se calculan las probabilidades en el sobre de evento?**
   - *Respuesta:* El sobre asigna 40% a Comun, 30% a Rara, 15% a Super Rara y 15% a las cartas exclusivas del evento. Ese 15% se reparte proporcionalmente con la función pura `calcular_pesos_cartas_evento`: las Comunes tienen peso relativo 2.0 y las Raras peso 1.0. Para 2 Comunes y 1 Rara, el total relativo es 5, lo que da exactamente 6% para Chupacabritas, 6% para Espíritu oscuro y 3% para Wendigo.
