# Documento de Predicciones y Validación de Funciones Clave (PREDICCIONES.md)

**Proyecto:** Mercado de Cartas Mitológicas (Proyecto B)  
**Asignatura:** Programación Científica y Técnica 2026
**Fecha de Entrega:** Jueves 19 de Noviembre de 2026  
**Integrantes:**  Lara Canío, Julieta Fernández, Sabrina Pereira y Aileen Waller

---

## 1. Introducción y Metodología de Validación

Para dar estricto cumplimiento a la consigna oficial, el equipo definió una metodología de **predicción previa** antes de disparar la ejecución de cada función clave del sistema. Esta práctica garantiza que los desarrolladores comprendan a cabalidad las precondiciones, postcondiciones, tipos de retorno y efectos colaterales esperados, evitando la programación por ensayo y error.

A continuación se detallan las **25 funciones y operaciones clave** del sistema (asociadas a las 25 pruebas unitarias implementadas en `tests/test_mercado.py` y descriptas en `documentos/tests.txt`), documentando la predicción previa formulada por el grupo, el resultado real obtenido en la ejecución y la comparación que convalida que el comportamiento cumple con lo esperado.

---

## 2. Registro de Predicciones por Función Clave

### Predicción 01: Integridad y Carga del Catálogo
- **Función Clave:** `crear_catalogo_completo()` y consultas al catálogo `Catalogo.buscar(codigo)`.
- **Precondición / Entrada:** Catálogo inicializado con todas las plantillas del archivo de criaturas mitológicas.
- **Predicción Previa:** Esperábamos que la función instanciara exactamente 227 plantillas de criaturas únicas, sin colisiones de códigos alfanuméricos (`len(codigos) == 227`), y que todos los tipos estuvieran normalizados con inicial mayúscula (`tipo[0].isupper()`).
- **Resultado Real Obtenido:** Se crearon exactamente 227 objetos `PlantillaCriatura`. Códigos iniciales como `CDRA` y legendarios como `LAPE` se recuperaron con atributos correctos. Cero duplicados.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_criaturas_cargadas_correctamente` (Regla 1).

---

### Predicción 02: Invariante Financiero de No Negatividad
- **Función Clave:** `Billetera.retirar(moneda, monto)` y `Billetera.depositar(moneda, monto)`.
- **Precondición / Entrada:** Billetera con saldo inicial de 100 Aureos. Se intenta retirar 150 Aureos; luego se intenta depositar -10 Aureos.
- **Predicción Previa:** Esperábamos que el intento de sobregiro (retirar 150 teniendo 100) lanzara inmediatamente una excepción `ValueError` y que el saldo se mantuviera intacto en 100. Asimismo, esperábamos que el depósito negativo fuera rechazado con `ValueError`.
- **Resultado Real Obtenido:** Ambas operaciones fallaron lanzando `ValueError("Saldo insuficiente")` y `ValueError("Monto inválido")`. El saldo final verificado en la billetera fue exactamente 100.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_invariante_saldo_no_negativo` (Regla 2).

---

### Predicción 03: Generación Secuencial de Identificadores de Cartas
- **Función Clave:** `PlantillaCriatura.crear_carta(juego=juego)` coordinado por `Juego._contadores`.
- **Precondición / Entrada:** Instancia de `Juego` limpia. Se invocan consecutivamente dos creaciones de cartas físicas para la plantilla Dragonzuelo (`CDRA`).
- **Predicción Previa:** Esperábamos que la primera carta recibiera el identificador `"CDRA-1"` con contador 1, y la segunda `"CDRA-2"` con contador 2, quedando registrado en la lista de contadores del juego el total de 2 cartas emitidas de esa especie.
- **Resultado Real Obtenido:** `c1.id` devolvió `"CDRA-1"`, `c2.id` devolvió `"CDRA-2"`, y `juego.contadores` reflejó `{"codigo": "CDRA", "cantidad": 2}`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_invariante_contador_plantilla_produce_ids_unicos` (Regla 3).

---

### Predicción 04: Azar Determinista en Apertura de Sobres
- **Función Clave:** `TipoSobre.abrir(catalogo, tirar=funcion_azar_pura)`.
- **Precondición / Entrada:** Un sobre con distribución de probabilidades y una función determinista inyectada `tirar_secuencial` que devuelve valores predefinidos sin recurrir al reloj del sistema ni a generadores aleatorios no controlados.
- **Predicción Previa:** Esperábamos que al ejecutar la apertura dos veces con la misma función determinista inyectada, ambas llamadas produjeran exactamente las mismas cartas, en el mismo orden y con las mismas rarezas.
- **Resultado Real Obtenido:** Las listas de cartas resultantes de ambas aperturas fueron idénticas en plantillas y rarezas resultantes.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_azar_determinista_apertura_sobre` (Regla 4).

---

### Predicción 05: Atomicidad Transaccional al Comprar Sobres
- **Función Clave:** `Juego.comprar_sobre(jugador_id, sobre_id)`.
- **Precondición / Entrada:** Jugador con 100 Aureos. Se intenta comprar un sobre que cuesta 50 Aureos, pero forzando a que la apertura falle (simulando catálogo vacío o error interno en apertura).
- **Predicción Previa:** Esperábamos que si la apertura fallaba a mitad de camino, el dinero del jugador NO fuera debitado y el sobre NO fuera registrado en `sobres_comprados` (primero abrir, luego cobrar).
- **Resultado Real Obtenido:** La operación levantó el error correspondiente; el saldo del jugador permaneció intacto en 100 Aureos y `sobres_comprados` continuó en 0.
- **Comparación:** **Cumple con lo esperado.** (Corrige el error real de la IA detectado por Alfonso).
- **Test que lo valida:** `TestMercadoCartasUML.test_comprar_sobre_y_carta` (Regla 5).

---

### Predicción 06: Conservación de Cartas en Intercambios (Sin Duplicación)
- **Función Clave:** `Juego.intercambiar(jugador_a, cartas_a, jugador_b, cartas_b)`.
- **Precondición / Entrada:** Jugador 1 posee carta `C1`, Jugador 2 posee carta `C2`. Ambos aceptan el intercambio.
- **Predicción Previa:** Esperábamos que la masa total de cartas en el sistema se conservara exactamente igual (2 cartas en total), que `C1` saliera del inventario de J1 y pasara a J2, y que `C2` saliera de J2 y pasara a J1.
- **Resultado Real Obtenido:** J1 terminó con `[C2]`, J2 terminó con `[C1]`. Ninguna carta se duplicó ni desapareció.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_invariante_intercambio_cartas_sin_duplicacion` (Regla 6).

---

### Predicción 07: Inocuidad de Intercambios Inválidos
- **Función Clave:** `Juego.intercambiar(...)` con parámetros erróneos o cartas inexistentes.
- **Precondición / Entrada:** J1 intenta ofrecer una carta que no le pertenece o J2 no da su consentimiento explícito (`aceptado_b = False`).
- **Predicción Previa:** Esperábamos que la transacción abortara de inmediato lanzando `ValueError` y que los inventarios de ambos participantes permanecieran inalterados sin efectos secundarios residuales.
- **Resultado Real Obtenido:** Se arrojó `ValueError("Uno o ambos jugadores no aceptaron el intercambio")`. Los inventarios mantuvieron sus cartas originales intactas.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_invariante_intercambio_invalido_sin_rastros` (Regla 7).

---

### Predicción 08: Vigencia Temporal de Sobres de Evento
- **Función Clave:** `Mercado.sobres_disponibles(eventos, fecha)`.
- **Precondición / Entrada:** Evento "Noche Eterna" vigente del 20/10/2026 al 20/11/2026. Se consulta disponibilidad el 01/11/2026 (dentro) y el 25/11/2026 (fuera).
- **Predicción Previa:** Esperábamos que el 01/11 devolviera 4 sobres (3 estándar + 1 de evento) y el 25/11 devolviera únicamente los 3 sobres estándar.
- **Resultado Real Obtenido:** Para la fecha dentro del rango la lista incluyó el sobre "Noche Eterna"; para la fecha posterior al evento, solo devolvió los tres sobres estables.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_sobres_disponibles_segun_vigencia_evento` (Regla 8).

---

### Predicción 09: Conversión de Divisas Condicionada a Eventos
- **Función Clave:** `Mercado.cambiar_moneda(cantidad_comunes)` y `Juego.convertir_moneda(...)`.
- **Precondición / Entrada:** Tasa de cambio oficial de 5 Aureos por 1 Jack. Se intenta cambiar 10 Aureos durante el evento; luego se intenta cambiar un monto no múltiplo (12 Aureos) o fuera de fecha.
- **Predicción Previa:** Esperábamos que 10 Aureos se convirtieran exactamente en 2 Jacks; y que 12 Aureos fuera rechazado con `ValueError` por no ser múltiplo de 5.
- **Resultado Real Obtenido:** 10 Aureos devolvió exactamente 2 Jacks. Al ingresar 12 Aureos se lanzó `ValueError("La cantidad debe ser múltiplo de 5")`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_convertir_moneda_vigencia_evento` (Regla 9).

---

### Predicción 10: Unicidad de Recompensa en Actividades y Misiones
- **Función Clave:** `Juego.reclamar_actividad(jugador_id, actividad_nombre)`.
- **Precondición / Entrada:** Jugador que cumple la condición de una misión. La reclama una vez; inmediatamente intenta reclamarla por segunda vez.
- **Predicción Previa:** Esperábamos que el primer reclamo acreditara la recompensa en la billetera y registrara la actividad como completada; y que el segundo reclamo lanzara `ValueError` impidiendo duplicar el cobro.
- **Resultado Real Obtenido:** Primer reclamo acreditó las monedas y sumó la actividad a `actividades_completadas`. El segundo reclamo arrojó `ValueError("La actividad ya fue completada y cobrada.")`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_actividad_mision_recompensa_unica` (Regla 10).

---

### Predicción 11: Coherencia de Clases y Atributos con el UML
- **Función Clave:** Inspección reflexiva de clases (`Moneda`, `Billetera`, `Carta`, `TipoSobre`, `SobreEstable`, `SobreVariable`, `Juego`).
- **Precondición / Entrada:** Clases instanciadas según el diagrama `UML_imagen.png`.
- **Predicción Previa:** Esperábamos que `Moneda` careciera de atributos visuales superfluos (`color`, `diseno`), que `SobreVariable` no contuviera diccionarios de SSR ni Legendaria, y que `Juego.contadores` fuera una lista de diccionarios (`list<dict>`).
- **Resultado Real Obtenido:** Todas las aserciones de introspección pasaron exitosamente. La estructura del código coincide con fidelidad absoluta con el UML.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_coincidencia_con_uml` (Regla 11).

---

### Predicción 12: Propagación Transparente de Errores en Azar Inyectado
- **Función Clave:** `TipoSobre._tirar_opcion(tirar, opciones, pesos)` invocada con una función `tirar` defectuosa.
- **Precondición / Entrada:** Se inyecta una función que deliberadamente arroja `TypeError("Bug simulado")`.
- **Predicción Previa:** Esperábamos que el error NO fuera silenciado con un bloque `try/except: pass` encubierto, sino que la excepción se propagara visiblemente hacia el llamador.
- **Resultado Real Obtenido:** La ejecución de `obtener_carta` falló visiblemente levantando `TypeError`, sin tragar el error.
- **Comparación:** **Cumple con lo esperado.** (Corrige la segunda observación crítica de Alfonso).
- **Test que lo valida:** `TestMercadoCartasUML.test_error_en_tirar_se_propaga_sin_ser_silenciado` (Regla 12).

---

### Predicción 13: Límite de Intercambio (Máximo 3 Cartas)
- **Función Clave:** `Juego.intercambiar(...)` enviando 4 cartas de un lado.
- **Precondición / Entrada:** Jugador 1 intenta transferir 4 cartas en una sola propuesta de intercambio.
- **Predicción Previa:** Esperábamos que la función rechazara la operación con `ValueError` por exceder el límite reglamentario de 3 cartas por jugador.
- **Resultado Real Obtenido:** Se levantó `ValueError("Un jugador no puede ofrecer más de 3 cartas en un intercambio.")`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_intercambio_reglas_maximo_tres_cartas_y_ambos_aceptan` (Regla 13).

---

### Predicción 14: Señalización Explícita de Funcionalidades Reservadas
- **Función Clave:** Invocación a métodos del subsistema de combate no desarrollado (`Juego.iniciar_combate()`).
- **Precondición / Entrada:** Llamada a la interfaz de combate.
- **Predicción Previa:** Esperábamos que el sistema levantara explícitamente `NotImplementedError`, documentando que el módulo de batallas fue postergado a favor del mercado de cartas.
- **Resultado Real Obtenido:** Se arrojó `NotImplementedError` con mensaje explicativo formal.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_batalla_no_implementada_documentada` (Regla 14).

---

### Predicción 15: Configuración Oficial de Precios y Sobres Estándar
- **Función Clave:** `crear_mercado_estandar()`.
- **Precondición / Entrada:** Inicialización del mercado con el catálogo completo.
- **Predicción Previa:** Esperábamos exactamente 3 sobres estables con precios oficiales: Sobre Comun (20 Aureos, 6 cartas), Sobre Especial (45 Aureos, 6 cartas), Sobre Legendario (80 Aureos, 6 cartas), y tasa de cambio de 5 a 1.
- **Resultado Real Obtenido:** Se obtuvieron exactamente los 3 sobres con sus precios y 6 cartas cada uno, más la tasa de cambio en 5.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_mercado_estandar_precios_y_sobres` (Regla 15).

---

### Predicción 16: Cantidad y Naturaleza de Actividades
- **Función Clave:** `crear_actividades()`, `crear_misiones()`, `crear_desafios()`.
- **Precondición / Entrada:** Generación de las actividades del documento oficial.
- **Predicción Previa:** Esperábamos exactamente 12 actividades en total, subdivididas en 7 misiones y 5 desafíos, todas con recompensas positivas (`recompensa > 0`).
- **Resultado Real Obtenido:** 12 actividades creadas (7 con `tipo="Misión"` y 5 con `tipo="Desafío"`, todas instancias directas de la clase `Actividad` según el diagrama UML), todas con recompensa numérica mayor a cero.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_crear_actividades_cantidad_y_tipos` (Regla 16).

---

### Predicción 17: Distribución Proporcional de Pesos en Cartas de Evento
- **Función Clave:** Función pura `calcular_pesos_cartas_evento(cartas_evento)`.
- **Precondición / Entrada:** Lista con 2 criaturas Comunes y 1 criatura Rara.
- **Predicción Previa:** Según la ponderación matemática (Comun peso 2.0, Rara peso 1.0; total relativo = 5.0), esperábamos que el 15% del sobre se distribuyera exactamente en: Comun 1 = 6.0%, Comun 2 = 6.0%, Rara = 3.0%. Además, esperábamos que si se incluía una carta SSR o Legendaria, lanzara `ValueError`.
- **Resultado Real Obtenido:** Los pesos devueltos fueron exactamente `{"TC01": 6.0, "TC02": 6.0, "TR01": 3.0}` sumando 15.0%. Al pasar una criatura SSR o Legendaria se lanzó `ValueError`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_pesos_cartas_evento` (Regla 17).

---

### Predicción 18: Condición de Misión "Comprar 5 Cartas del Mercado"
- **Función Clave:** Evaluación pura de `mision.esta_cumplida(jugador, cartas)`.
- **Precondición / Entrada:** Jugador realiza 4 compras de cartas en el mercado; luego realiza la 5ª compra.
- **Predicción Previa:** Esperábamos que con 4 compras `esta_cumplida` devolviera `False`, y tras la 5ª compra devolviera `True`.
- **Resultado Real Obtenido:** Con 4 compras devolvió `False`. Tras la 5ª compra devolvió `True` y `cartas_compradas_mercado == 5`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_mision_comprar_cartas_mercado` (Regla 18).

---

### Predicción 19: Condición de Misión "Conseguir al Leviatán"
- **Función Clave:** `mision.esta_cumplida(jugador, cartas)` para la criatura legendaria `LLEV`.
- **Precondición / Entrada:** Jugador sin la carta; luego se agrega al inventario una carta con plantilla de código `"LLEV"`.
- **Predicción Previa:** Esperábamos que antes de poseer la carta devolviera `False`, y una vez agregada al inventario devolviera `True`.
- **Resultado Real Obtenido:** `esta_cumplida` evaluó `False` inicialmente y `True` inmediatamente tras recibir la carta del Leviatán.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_mision_conseguir_leviatan` (Regla 19).

---

### Predicción 20: Desafío de Victorias Consecutivas
- **Función Clave:** `Juego.registrar_victoria(jugador_id, fecha)` y evaluación del desafío de 3 victorias.
- **Precondición / Entrada:** Jugador registra 2 victorias seguidas; luego registra la 3ª victoria.
- **Predicción Previa:** Esperábamos que con 2 victorias el desafío no estuviera cumplido, y al registrar la 3ª consecutiva se cumpliera (`victorias_consecutivas == 3`).
- **Resultado Real Obtenido:** Con 2 victorias devolvió `False`. Tras la 3ª victoria devolvió `True`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_desafio_victorias_consecutivas` (Regla 20).

---

### Predicción 21: Reinicio de Racha tras Derrota
- **Función Clave:** `Juego.registrar_derrota(jugador_id)`.
- **Precondición / Entrada:** Jugador con 2 victorias consecutivas acumuladas registra una derrota en combate.
- **Predicción Previa:** Esperábamos que el contador `victorias_consecutivas` se reseteara estrictamente a 0, y que una victoria posterior iniciara la cuenta en 1.
- **Resultado Real Obtenido:** Tras invocar `registrar_derrota`, el contador pasó inmediatamente a 0. La siguiente victoria colocó el contador en 1.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_registrar_derrota_reinicia_consecutivas` (Regla 21).

---

### Predicción 22: Nombres Oficiales de Monedas y Sobres
- **Función Clave:** Verificación de constantes de negocio en `mercado_cartas.economia`.
- **Precondición / Entrada:** Módulo de economía cargado.
- **Predicción Previa:** Esperábamos que la moneda común se llamara `"Aureos"`, la de evento `"Jacks"`, y el sobre y evento oficial `"Noche Eterna"`. Además, que el sobre de evento tuviera 3 cartas y precio de 20 Jacks.
- **Resultado Real Obtenido:** Todas las constantes coincidieron exactamente con los nombres oficiales requeridos.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_nombres_oficiales_evento_y_monedas` (Regla 22).

---

### Predicción 23: Probabilidades del Sobre de Evento (*Noche Eterna*)
- **Función Clave:** `crear_sobre_evento()` y `crear_evento_noche_eterna()`.
- **Precondición / Entrada:** Creación del sobre y evento de temporada.
- **Predicción Previa:** Esperábamos que el sobre tuviera probabilidades: Comun 40%, Rara 30%, Super Rara 15%, Cartas del evento 15%; con cero presencia de SSR o Legendaria. Y que las cartas exclusivas fueran Chupacabritas (6%), Espíritu oscuro (6%) y Wendigo (3%).
- **Resultado Real Obtenido:** El diccionario de probabilidades reflejó 40%, 30%, 15% y 15%; no se encontraron claves de SSR ni Legendaria. Los pesos del evento asignaron exactamente 6.0 a `CCHU`, 6.0 a `CESO` y 3.0 a `RWEN`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_sobre_evento_probabilidades_y_cartas_exclusivas` (Regla 23).

---

### Predicción 24: Exclusividad y Bloqueo de Cartas de Evento
- **Función Clave:** `SobreEstable.abrir(catalogo)` en sobres regulares.
- **Precondición / Entrada:** Múltiples aperturas de sobres estándar (Sobre Comun, Sobre Especial, Sobre Legendario).
- **Predicción Previa:** Esperábamos que ninguna apertura de sobres estándar produjera jamás a Chupacabritas (`CCHU`), Espíritu oscuro (`CESO`) ni Wendigo (`RWEN`), manteniéndose como exclusivas absolutas del evento.
- **Resultado Real Obtenido:** Se iteró sobre todas las cartas obtenidas y ninguna coincidió con los códigos de `CODIGOS_CARTAS_EVENTO_EXCLUSIVAS`.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_cartas_exclusivas_no_obtenibles_en_sobres_regulares` (Regla 24).

---

### Predicción 25: Composición Exacta del Mercado de 25 Cartas
- **Función Clave:** `crear_ofertas_mercado(catalogo)`.
- **Precondición / Entrada:** Generación del catálogo de ofertas directas del mercado.
- **Predicción Previa:** Esperábamos exactamente 25 cartas disponibles: 15 Comunes a 10 Aureos, 7 Raras a 25 Aureos (incluyendo a Diablo de Jersey `RDJE`) y 3 Super Raras a 40 Aureos. Esperábamos que Wendigo, Chupacabritas y Espíritu oscuro NO estuvieran a la venta.
- **Resultado Real Obtenido:** `len(mercado.ofertas) == 25`. Diablo de Jersey estuvo presente a 25 Aureos; Wendigo, Chupacabritas y Espíritu oscuro quedaron excluidos de las ofertas directas.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_mercado_ofertas_oficiales_25_cartas` (Regla 25).

---

### Predicción 26: Misiones de Abrir Sobres, Intercambio y Colección
- **Función Clave:** `mision.esta_cumplida(jugador, cartas)` para las misiones de interacción.
- **Precondición / Entrada:** Jugador compra y abre 2 sobres; completa 1 intercambio; y acumula 15 cartas en su colección.
- **Predicción Previa:** Esperábamos que cada misión evaluara `False` antes de alcanzar el umbral, y `True` inmediatamente al registrar 2 sobres comprados, 1 intercambio completado y 15 cartas en inventario, respectivamente.
- **Resultado Real Obtenido:** Las tres misiones evaluaron `True` exactamente al alcanzar las cantidades objetivo estipuladas.
- **Comparación:** **Cumple con lo esperado.**
- **Test que lo valida:** `TestMercadoCartasUML.test_economia_misiones_abrir_sobres_intercambio_y_coleccion` (Regla 26).

---

## 3. Resumen de la Comparación y Conclusión

| Métrica de Validación | Valor Registrado |
|---|---|
| Total de Funciones Clave Predichas | 26 |
| Total de Pruebas Unitarias Ejecutadas | 26 |
| Pruebas que Cumplieron la Predicción Inicial | 26 (100%) |
| Fallos o Desviaciones No Esperadas | 0 |
| Tiempo Total de Ejecución de la Suite | 0.013 segundos |

**Conclusión:**  
La comparación sistemática entre las predicciones documentadas previamente y los resultados reales arrojados por el intérprete de Python demuestra que el sistema respeta de manera determinista todos los invariantes financieros, lúdicos y estructurales especificados en el diseño.
