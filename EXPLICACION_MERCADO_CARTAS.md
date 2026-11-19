# Explicación Detallada del Paquete `mercado_cartas`

Este documento detalla la responsabilidad, estructura y funcionamiento de cada uno de los archivos de código Python que componen el paquete **`mercado_cartas`**.

---

## 1. Visión General de la Arquitectura

El paquete `mercado_cartas` implementa el modelo de dominio completo del juego de cartas coleccionables de seres mitológicos. Está programado con **clases tradicionales de Python** (con constructores explícitos `__init__`, sin uso de `dataclasses`) y respeta al 100% el diagrama de clases **UML** oficial del proyecto y las correcciones de la cátedra.

El paquete se compone de **7 módulos principales**:

```
mercado_cartas/
├── __init__.py          # Fachada del paquete y exportaciones públicas
├── principales.py       # Modelos centrales del dominio, azar y clases base
├── catalogo.py          # Gestión de catálogo de plantillas y lógica del mercado
├── criaturas.py         # Definición e instanciación de las 227 criaturas mitológicas
├── jugador.py           # Gestión del perfil del jugador y billetera multimoneda
├── juego.py             # Motor y coordinador transaccional central de la partida
└── economia.py          # Configuración de precios, probabilidades, sobres y actividades
```

---

## 2. Detalle Archivo por Archivo

---

### `principales.py` — Entidades Fundamentales del Dominio

**Propósito:** Define las clases base e invariantes estructurales sobre las cuales opera todo el sistema de juego, implementadas como clases convencionales de Python.

#### Clases y Componentes Clave:
1. **`_tirar_opcion(tirar, opciones, pesos)`**:
   - Función central para la resolución del azar.
   - Si se pasa una función de azar (`tirar`), la invoca directamente mediante `tirar(opciones, pesos)`. Si no se inyecta ninguna función, recurre a `random.choices` o `random.choice` de la librería estándar de Python.
   - Cualquier error o bug en una función inyectada se propaga de inmediato sin ser ocultado por bloques `try/except`.

2. **`Moneda`**:
   - Clase tradicional con constructor `__init__(self, nombre: str, evento: str = "")`.
   - Implementa `__hash__` y `__eq__` para poder ser utilizada de forma segura como clave en diccionarios (como en la `Billetera`).
   - Cumple fielmente con el UML (únicamente atributos `nombre` y `evento`).

3. **`CODIGOS_CARTAS_EVENTO_EXCLUSIVAS`**:
   - Conjunto inmutable (`Set[str]`) con los códigos de las cartas exclusivas del evento vigente (`{"CCHU", "CESO", "RWEN"}`: Chupacabritas, Espíritu oscuro y Wendigo).
   - Garantiza que estas cartas no aparezcan en sobres estándar ni en las ofertas regulares del mercado.

4. **`PlantillaCriatura`**:
   - Representa la ficha o modelo canónico de una criatura (`codigo`, `nombre`, `tipo`, `rareza`, `vida`, `ataque`, `defensa`, `habilidad`, `descripcion_habilidad`, `usos_habilidad`).
   - En su `__init__` normaliza la rareza (por ejemplo `"Comun"` sin tildes).
   - **Método `crear_carta(juego=None)`**: Genera una instancia física `Carta` con un identificador secuencial único (`{codigo}-{numero}`). Si se asocia a una instancia de `Juego`, el contador se gestiona de forma aislada por partida.

5. **`Carta`**:
   - Representa el ejemplar individual y físico que posee un jugador en su inventario.
   - Atributos: `id: str` (único e irrepetible) y `plantilla: PlantillaCriatura`.

6. **`TipoSobre`**:
   - Clase base tradicional para los sobres de cartas.
   - Atributos inicializados en `__init__`: `nombre`, `cantidad_cartas`, `precio`, `moneda`, `azar_rareza`, pools de criaturas (`azar_criatura_c`, `_r`, `_sr`).
   - Define el método `abrir(catalogo, evento, tirar, juego) -> List[Carta]`.

7. **`SobreEstable`**:
   - Subclase de `TipoSobre` para sobres convencionales (Común, Especial, Legendario).
   - Administra además `azar_criatura_ssr` y `azar_criatura_l`.
   - Filtra las cartas exclusivas de evento para no distribuirlas en sobres estándar.

8. **`SobreVariable`**:
   - Subclase de `TipoSobre` diseñada para sobres de eventos estacionales.
   - Valida en su `__init__` que el sobre no contenga rarezas SSR ni Legendarias.
   - Aplica el esquema oficial: 40% Común, 30% Rara, 15% Súper Rara y 15% Cartas exclusivas del evento.

9. **`Evento`**:
   - Modela un evento por tiempo limitado con `nombre`, `fecha_inicio`, `fecha_fin`, `moneda`, `sobre` y `pesos_cartas`.
   - Método `carta_para(numero)` para selección determinista según ponderaciones.

10. **`Actividad`**:
    - Modela objetivos y recompensas del juego con `nombre: str`, `tipo: str = "Actividad"`, `recompensa: int = 0` y `condicion: Any = None`.
    - Método `esta_cumplida(jugador, cartas) -> bool`: Evalúa de forma pura y funcional si el jugador cumple los requisitos de la actividad.
    - **Alineación con el UML:** Todo se modela en `Actividad` distinguiéndose por el atributo `tipo` (`"Misión"` o `"Desafío"`), sin subclases innecesarias.

---

### `catalogo.py` — Gestión de Fichas y Mercado

**Propósito:** Proporciona colecciones para la búsqueda e indexación de criaturas y encapsula la tienda del mercado.

#### Clases Clave:
1. **`Catalogo`**:
   - Contenedor de todas las plantillas disponibles (`plantillas: Dict[str, PlantillaCriatura]`).
   - **`buscar(codigo)`**: Obtiene una plantilla por su código identificador o lanza `ValueError` si no existe.
   - **`de_rareza(rareza)`**: Filtra plantillas por rareza normalizada.
   - **`de_tipo(tipo)`**: Filtra plantillas por familia elemental o mitológica.

2. **`Mercado`**:
   - Modela la tienda donde los jugadores compran sobres, adquieren cartas sueltas o convierten divisas.
   - Atributos: `ofertas: Dict[str, int]`, `sobres: List[SobreEstable]`, `tasa_cambio: int = 1` (o 5 según configuración económica).
   - **`precio_de(codigo)`**: Consulta el costo de una carta individual ofertada.
   - **`cambiar_moneda(cantidad_comunes)`**: Calcula la conversión a moneda de evento exigiendo que la cantidad sea un múltiplo exacto de `tasa_cambio` (5 comunes por 1 de evento).
   - **`evento_vigente(eventos, fecha)`**: Determina si en una fecha determinada existe un evento activo comparando rangos de fechas.
   - **`sobres_disponibles(eventos, fecha)`**: Devuelve los sobres estándar más el sobre exclusivo del evento únicamente si la fecha cae dentro de su vigencia.

---

### `criaturas.py` — Base de Datos de Criaturas Mitológicas

**Propósito:** Define formalmente en código las **227 criaturas mitológicas** del documento oficial del proyecto.

#### Componentes Clave:
- Cada criatura está instanciada como un objeto `PlantillaCriatura` con sus estadísticas oficiales.
- Se exportan individualmente criaturas de uso frecuente (`dragonzuelo`, `sirena`, `chupacabritas`, `espiritu_oscuro`, `diablo_de_jersey`, `wendigo`, etc.).
- `CRIATURAS`: Tupla inmutable que contiene las 227 instancias.
- `PLANTILLAS_CRIATURAS`: Diccionario mapeando `codigo -> PlantillaCriatura`.
- `crear_catalogo_completo()`: Factoría que retorna una instancia de `Catalogo` poblada con las 227 criaturas.

---

### `jugador.py` — Billetera y Perfil del Jugador

**Propósito:** Modela el estado individual del usuario: sus finanzas multimoneda, su inventario de cartas y sus métricas de progreso.

#### Clases Clave:
1. **`Billetera`**:
   - Administra el saldo por cada tipo de `Moneda` en un diccionario privado `_saldos`.
   - **`saldo(moneda)`**: Devuelve el balance actual.
   - **`depositar(moneda, monto)`**: Acredita fondos validando montos no negativos.
   - **`retirar(moneda, monto)`**: Debita fondos garantizando que el saldo no quede en negativo.

2. **`Jugador`**:
   - Representa al participante en el juego con `id`, `nombre` y `billetera`.
   - Propiedades de solo lectura y métodos de actualización para:
     - `cartas`: Inventario de cartas del jugador.
     - `actividades_completadas`: Registro de misiones cobradas.
     - `sobres_comprados`: Estadísticas de compra por tipo de sobre.
     - `victorias_por_dia`: Registro de victorias diarias.
     - `victorias_consecutivas`: Racha de victorias seguidas.
     - `cartas_compradas_mercado` e `intercambios_completados`.
   - Métodos `agregar_carta(carta_id)` y `quitar_carta(carta_id)`.

---

### `juego.py` — Motor y Coordinador Transaccional

**Propósito:** Orquestador principal (fachada) del sistema que garantiza operaciones seguras y atómicas.

#### Métodos y Reglas Clave:
1. **Contadores de Cartas por Partida**:
   - Administra `_contadores` en la instancia del juego para que cada partida numere sus cartas de manera independiente sin colisiones globales.
2. **`comprar_sobre(jugador_id, sobre, fecha)`**:
   - Valida disponibilidad y saldo.
   - Abre el sobre y entrega las cartas **primero**.
   - Solo si la apertura y entrega fueron exitosas, debita el dinero y registra la compra (evitando que el jugador pierda saldo si la apertura falla).
3. **`comprar_carta(jugador_id, codigo)`**:
   - Valida saldo, crea la carta, la asigna al jugador y cobra la tarifa oficial.
4. **`intercambiar(jugador_a_id, cartas_a_ids, jugador_b_id, cartas_b_ids, aceptado_a, aceptado_b)`**:
   - Máximo 3 cartas por participante.
   - Requiere mutuo acuerdo de ambas partes.
   - Valida que las cartas pertenezcan a los participantes y realiza la transferencia de forma atómica.
5. **`convertir_moneda(jugador_id, cantidad_comunes, fecha)`**:
   - Requiere evento vigente en la fecha y aplica la tasa de cambio del mercado.
6. **`completar_actividad(jugador_id, actividad)`**:
   - Verifica que la actividad no haya sido cobrada antes y evalúa `actividad.esta_cumplida(jugador, cartas)`. Si se cumple, deposita la recompensa.
7. **`registrar_victoria` / `registrar_derrota`**:
   - Actualiza victorias diarias y mantiene o resetea a cero la racha consecutiva.
8. **`batallar(jugador_a_id, jugador_b_id)`**:
   - Lanza `NotImplementedError` documentando que el combate se reserva para versiones futuras.

---

### `economia.py` — Configuración Oficial y Factorías de Negocio

**Propósito:** Centraliza los parámetros económicos, probabilidades matemáticas de los sobres, listas oficiales de mercado y actividades del juego.

#### Constantes y Factorías:
1. **Nombres y Monedas Oficiales**:
   - Moneda común: `"Aureos"`.
   - Moneda de evento: `"Jacks"`.
   - Evento y sobre de evento: `"Noche Eterna"`.
2. **Capacidad de Cartas**:
   - Sobres estándar: **6 cartas**.
   - Sobre de evento: **3 cartas**.
3. **Precios Oficiales**:
   - Sobres estándar: Común (20 Aureos), Especial (45 Aureos), Legendario (80 Aureos).
   - Sobre de evento: 20 Jacks.
   - Cartas sueltas en el mercado: Común (10 Aureos), Rara (25 Aureos), Súper Rara (40 Aureos).
   - Tasa de cambio: 5 Aureos por cada 1 Jack.
4. **Probabilidades Matemáticas**:
   - Sobre Común: 74% C, 20% R, 5% SR, 0.9% SSR, 0.1% L.
   - Sobre Especial: 45% C, 35% R, 15% SR, 4% SSR, 1% L.
   - Sobre Legendario: 20% C, 35% R, 30% SR, 10% SSR, 5% L.
   - Sobre de Evento: 40% C, 30% R, 15% SR, 15% Cartas de evento.
5. **Función `calcular_pesos_cartas_evento(cartas_evento)`**:
   - Distribuye proporcionalmente el 15% entre sus cartas exclusivas (6% Chupacabritas, 6% Espíritu oscuro, 3% Wendigo). Lanza `ValueError` ante SSR o Legendarias.
6. **Ofertas del Mercado (`CODIGOS_CARTAS_MERCADO`)**:
   - 25 cartas oficiales (15 Comunes, 7 Raras y 3 Súper Raras), incluyendo al Diablo de Jersey en el mercado.
7. **Actividades Oficiales**:
   - 7 Misiones y 5 Desafíos instanciados mediante `Actividad(..., tipo="Misión")` y `Actividad(..., tipo="Desafío")`.

---

### `__init__.py` — Fachada y Punto de Acceso del Módulo

**Propósito:** Define una interfaz pública limpia y organizada a través de la lista **`__all__`**, permitiendo importaciones limpias con `from mercado_cartas import ...` y garantizando que solo se expongan las entidades y funciones válidas del proyecto.
