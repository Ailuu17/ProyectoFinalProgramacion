# Bitácora de Desarrollo y Registro de Gobernanza de Inteligencia Artificial

**Proyecto:** Mercado de Cartas Mitológicas (Proyecto B)  
**Asignatura:** Programación Científica y Técnica — Segundo Semestre 2026  
**Fecha de Entrega:** Jueves 19 de Noviembre de 2026  
**Equipo:** Proyecto Final  
**Documento Fuente:** Registro formal en cumplimiento con la consigna oficial del curso (complementario al histórico grupal en `documentos/Bitácora.docx`).  

---

## 1. Cronología General de Desarrollo del Proyecto

### Martes 20/10 — Lanzamiento del Proyecto
- **Actividad:** Presentación de la consigna oficial por parte de la docente Guadalupe. Conformación de equipos de trabajo.
- **Acuerdos:** Repaso de los tres proyectos propuestos (Ruta viva, Mercado de cartas y Radio infinita). Análisis inicial de fortalezas del equipo en Programación Orientada a Objetos y funciones puras.

### Jueves 22/10 — Planificación de Hitos
- **Actividad:** Definición de la fecha de entrega y defensa individual (Jueves 19 de Noviembre).
- **Decisión:** Compromiso de evaluar durante el fin de semana el proyecto a seleccionar y sus ejes de variación.

### Martes 27/10 — Selección de Proyecto y Modelado Inicial
- **Decisión unánime:** Selección de **Proyecto B: Mercado de Cartas**.
- **Temática:** Animales y criaturas mitológicas de distintas culturas.
- **Diseño del catálogo base:** División de las criaturas en 5 niveles de rareza: *Comun*, *Rara*, *Super Rara*, *Super Super Rara* y *Legendaria*.
- **Diseño de sobres:** Tres sobres estándar con 6 cartas cada uno:
  - *Sobre Comun:* 74% Comun, 20% Rara, 5% Super Rara, 0.9% Super Super Rara, 0.1% Legendaria. Precio: 20 monedas comunes (*Aureos*).
  - *Sobre Especial:* 45% Comun, 35% Rara, 15% Super Rara, 4% Super Super Rara, 1% Legendaria. Precio: 45 Aureos.
  - *Sobre Legendario:* 20% Comun, 35% Rara, 30% Super Rara, 10% Super Super Rara, 5% Legendaria. Precio: 80 Aureos.
- **Mecánica de eventos estacionales (diferencial):** Dos eventos por año con duración aproximada de un mes. Sobres de 3 cartas con probabilidades especiales (40% Comun, 30% Rara, 15% Super Rara y 15% entre 3 criaturas exclusivas del evento). Moneda temática propia intercambiable en el mercado.
- **Mercado directo:** Catálogo de 25 cartas disponibles para compra directa (15 Comunes a 10 monedas, 7 Raras a 25 monedas, 3 Super Raras a 40 monedas). Tasa de cambio de 5 monedas comunes por 1 moneda de evento.

### Jueves 29/10 — Atributos y Primer Bosquejo UML
- **Actividad:** Definición de atributos de combate para cada criatura: vida, ataque, defensa y habilidad especial con usos limitados por combate.
- **Modelado:** Creación del primer borrador del diagrama UML de clases para identificar responsabilidades y límites entre entidades.

### Martes 03/11 — Digitalización Visual y Códigos Primarios
- **Actividad:** Asignación de códigos alfanuméricos de 4 caracteres a las 227 criaturas mitológicas.
- **Arte:** Inicio de bocetos e ilustraciones de los personajes mitológicos.
- **Evolución del UML:** Incorporación de las entidades `Moneda`, `Billetera`, `Mercado`, `TipoSobre` y el mecanismo de inyección de azar determinista.

### Jueves 05/11 — Consulta Docente (Alfonso)
- **Actividad:** Presentación a Alfonso de los avances en el diagrama UML y de los primeros prototipos de código.
- **Retroalimentación:** Énfasis en asegurar que el UML sea coherente con el código y que las invariantes de negocio estén completamente protegidas por pruebas.

### Martes 10/11 — Intercambio Arquitectónico (Guadalupe)
- **Actividad:** Sesión de discusión de 1 hora con la docente Guadalupe sobre la estructura del UML.
- **Conclusión consensuada:** Se acordó priorizar un UML funcional, limpio y coherente con el código real, respetando el encapsulamiento de datos y modelando explícitamente `_contadores: list<dict>` en la clase `Juego` para la generación de identificadores únicos de cartas físicas.
- **Carga de datos:** Integración de la lista completa de criaturas mitológicas en el código y carga inicial de tests con el asistente Antigravity.

### Jueves 12/11 — Cierre de Hito 2 y Preparación de Refactor
- **Actividad:** Finalización formal de la versión avanzada del UML y validación con Alfonso.
- **Coordinación:** Organización del cambio de requisito asignado por el docente y continuación de digitalización de ilustraciones.

### Lunes 16/11 — Integración de Arte, Economía y Frontend
- **Arte digital:** Subida de las ilustraciones completas de los personajes a `documentos/Imagenes/Personajes/`, monedas a `documentos/Imagenes/Monedas/` y sobres a `documentos/Imagenes/Sobres/`.
- **Economía y Actividades:** Nombramiento oficial de las monedas (*Aureos* y *Jacks*), sobre y evento vigente (*Noche Eterna*). Creación de las 7 misiones y 5 desafíos oficiales del documento `Actividades.docx`.
- **Alcance del proyecto:** Se documenta la decisión de aplazar el sistema de batallas activas para concentrar todos los esfuerzos en las funcionalidades nucleares del mercado de cartas (apertura determinista de sobres, compra/venta en mercado, gestión de billeteras e intercambio atómico entre jugadores).
- **Frontend:** Creación de la interfaz web en la carpeta `frontend/` y servidor local `server.py`.

### Martes 17/11 — Auditoría Técnica y Depuración de Dependencias
- **Revisión profunda:** Eliminación de dependencias complejas o no dominadas como `__future__`, reemplazando las anotaciones pospuestas por referencias de tipos encapsuladas en cadenas (`'Carta'`, `'Juego'`).
- **Validación de bibliotecas:** Consenso de mantener únicamente bibliotecas estándar de Python:
  - `typing`: Mejora la legibilidad, mantenibilidad y tipado estático sin impacto en tiempo de ejecución.
  - `pathlib`: Manipulación de rutas orientada a objetos y multiplataforma (Windows/Linux/macOS).
  - `unittest`: Marco canónico oficial para la suite de pruebas unitarias.
  - `dataclasses`: Reducción de código repetitivo (*boilerplate*) para clases de dominio con estado inmutable o claro.
- **Tokens de IA:** Agotamiento y rotación de tokens en cuentas de Antigravity para completar la suite de tests.

### Miércoles 18/11 — Auditoría Integral, Normalización y Entrega
- **Normalización ortográfica estricta:** Unificación total de rarezas a `"Comun"` y `"Super Rara"` (eliminando variantes con tilde en todo el código y JSON).
- **Corrección de cartas exclusivas de evento:** Asignación definitiva de Chupacabritas (`CCHU`, Comun, 6%), Espíritu oscuro (`CESO`, Comun, 6%) y Wendigo (`RWEN`, Rara, 3%) como las 3 cartas exclusivas del sobre *Noche Eterna*, manteniendo a Diablo de Jersey (`RDJE`, Rara) en el mercado general de 25 cartas.
- **Generación de entregables finales:** Redacción de `etica.md`, `bitacora.md` y `auditoria_y_mejoras.md`.
- **Verificación final:** Ejecución exitosa de 25 pruebas unitarias en `tests/test_mercado.py` (`Ran 25 tests in 0.014s OK`).

---

## 2. Registro Sistemático de Uso de Inteligencia Artificial (Antigravity / Gemini)

De acuerdo con el requisito explícito de la consigna oficial:
> *"Cada uso se registra en la bitácora: qué se pidió, qué devolvió, qué se corrigió o rechazó y por qué. Debe incluir al menos un error real de la IA."*

| ID | Fecha | Qué se pidió al Asistente | Qué devolvió el Asistente | Qué se corrigió o rechazó | Causa / Justificación |
|---|---|---|---|---|---|
| **IA-01** | 27/10 | Proponer distribución de cantidades de cartas y probabilidades de sobres. | Generó tabla con 222 cartas (90 C, 60 R, 36 SR, 24 SSR, 12 L) y porcentajes para 3 tipos de sobres. | Se aceptó la distribución matemática, pero se amplió el catálogo a 227 cartas para incluir variantes mitológicas adicionales. | Adecuación al universo narrativo creado por el equipo humano. |
| **IA-02** | 10/11 | Modelar el método de creación de cartas físicas en `principales.py`. | Sugirió usar `import uuid` para generar identificadores de cartas aleatorios (ej. `uuid.uuid4()`). | **Rechazado.** Se implementó el esquema de IDs secuenciales `{codigo}-{contador}` gobernado por `_contadores: list<dict>` en `Juego`. | La consigna exige identificadores deterministas, legibles y auditables; los UUID violan la secuencialidad requerida por la cátedra. |
| **IA-03** | 12/11 | Implementar la tipificación en Python 3 para resolver referencias circulares entre `Carta` y `PlantillaCriatura`. | La IA agregó automáticamente `from __future__ import annotations` al inicio de todos los módulos. | **Rechazado y Eliminado.** Se removió `__future__` y se usaron tipos como cadenas literales (`'Carta'`, `'Juego'`). | Principio de transparencia pedagógica: no utilizar módulos mágicos no dominados por el equipo y mantener compatibilidad nativa limpia. |
| **IA-04** | 16/11 | Asignar la cantidad de cartas contenidas en los sobres estándar y de evento. | La IA configuró 2 cartas en los sobres estándar y 1 carta en el sobre de evento. | **Corregido.** Se restablecieron los valores oficiales: 6 cartas por sobre estándar y 3 cartas por sobre de evento. | La IA desatendió el acuerdo grupal del 27/10 registrado en la bitácora original. |
| **IA-05** | 17/11 | Sugerir bibliotecas para el backend y frontend (ej. `flask`, `pydantic`, `pytest`). | Sugirió un ecosistema basado en `pip install flask pydantic pytest`. | **Rechazado categóricamente.** Se mantuvo 100% biblioteca estándar (`http.server`, `unittest`, `dataclasses`, `pathlib`). | Restricción inviolable de la consigna: no se permiten dependencias externas fuera de la biblioteca estándar de Python. |
| **IA-06** | 18/11 | Implementar las 3 cartas exclusivas del evento *Noche Eterna* y sus probabilidades. | **Error real de la IA:** La IA confundió las asignaciones e intentó intercambiar a Wendigo y Diablo de Jersey de ubicación, además de aceptar variantes con tildes ("Común" y "Comun"). | **Detectado y Corregido:** Se estableció a Wendigo (`RWEN`, Rara) como la 3ª exclusiva del evento junto a Chupacabritas y Espíritu oscuro, se fijó a Diablo de Jersey (`RDJE`) en el mercado de 25 cartas y se forzó la normalización sin tildes `"Comun"`. | Error de comprensión semántica de la IA respecto a las cartas exclusivas del evento y los productos del mercado. |
| **IA-07** | 18/11 | Configurar las probabilidades del sobre de evento *Noche Eterna*. | La IA intentó mantener slots para *Super Super Rara* y *Legendaria* en el sobre de evento. | **Corregido:** Se bloqueó la inclusión de SSR y Legendaria tanto en las probabilidades del sobre como en las cartas participantes, arrojando `ValueError` si se intentara. | Requisito ético y de diseño: el sobre de evento estacional no contiene SSR ni Legendarias (40% Comun, 30% Rara, 15% Super Rara, 15% Cartas de evento). |

---

## 3. Análisis de Decisiones de Diseño y Filosofía del Código

### 3.1. Separación de Efectos Secundarios y Funciones Puras (Programación Funcional)
Uno de los pilares evaluados por la cátedra es la Programación Funcional:
- **Efectos de Azar Desacoplados:** En lugar de invocar `random.choice` directamente dentro del método `obtener_carta`, el método recibe un argumento inyectable `tirar: Optional[Callable] = None`. En producción se usa `random.random`, pero en pruebas unitarias se inyecta una función determinista pura (`_tirar_determinista`). Esto permite que con los mismos datos y el mismo azar, el sistema produzca siempre de forma idéntica el mismo resultado.
- **Efectos de Reloj y Calendario:** Las validaciones de vigencia de eventos no consultan `datetime.now()` de forma encubierta, sino que reciben objetos `date` explícitos por parámetro, permitiendo testear viajes en el tiempo sin depender del reloj del sistema.
- **Funciones de Orden Superior:** Uso de lambdas y funciones de evaluación en las condiciones de misiones (`condicion: Callable[[Jugador, List[Carta]], bool]`), desacoplando la lógica de satisfacción de la estructura rígida de clases.

### 3.2. Encapsulamiento e Invariantes Críticos (POO)
- **Billetera:** Los saldos de monedas no pueden ser negativos bajo ninguna circunstancia. Cualquier intento de depósito con monto negativo o de retiro por encima del saldo levanta `ValueError` y no muta el balance.
- **Intercambio Atómico:** El método `juego.intercambiar()` aplica un protocolo de dos fases:
  1. *Fase de validación previa:* Se verifica que ambos jugadores existan, que posean las cartas ofertadas (hasta un máximo de 3 cada uno) y que ambos hayan marcado `aceptado = True`.
  2. *Fase de mutación atómica:* Si cualquier condición falla, la transacción aborta sin dejar ningún rastro ni cartas perdidas o duplicadas en el sistema.
- **Unicidad de Cartas Físicas:** Distinción ontológica entre `PlantillaCriatura` (el molde abstracto inmutable) y `Carta` (la tarjeta coleccionable concreta en el inventario de un jugador, con ID único irrepetible).

---

## 4. Reflexión y Aprendizaje Obtenido

El desarrollo del Mercado de Cartas Mitológicas demostró que la Inteligencia Artificial es un acelerador notable para tareas de soporte, redacción de tests de regresión y maquetación de interfaces visuales. Sin embargo, quedó en evidencia que la IA carece de comprensión contextual profunda sobre las reglas de negocio si no existe una supervisión humana rigurosa.

El verdadero valor de la ingeniería de software reside en la capacidad del desarrollador para:
1. Validar formalmente cada invariante del sistema.
2. Cuestionar las propuestas del modelo generativo cuando violan las restricciones del curso.
3. Defender con argumentos técnicos cada decisión de modelado en el UML y en el código fuente.
