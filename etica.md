# Documento de Ética, Legislación y Responsabilidad del Sistema

**Proyecto:** Mercado de Cartas Mitológicas (Proyecto B)  
**Asignatura:** Programación Científica y Técnica — 2026  
**Equipo:** Estudiantes del Proyecto Final  
**Fecha:** Noviembre de 2026  

---

## 1. Datos que Maneja la Aplicación

El sistema gestiona de forma intencional y exclusiva un conjunto mínimo de datos lúdicos y transaccionales bajo el principio de **minimización de datos** (*Privacy by Design*):

1. **Identificadores de usuario y perfiles:** Identificadores alfanuméricos seudónimos (`id: "j1"`, `id: "j2"`), alias públicos elegidos por el usuario (`nombre: "Ash"`, `nombre: "Misty"`) y avatares visuales.
2. **Estado económico y billetera:** Balances numéricos enteros de monedas de ficción (`Aureos` como moneda base y `Jacks` como moneda estacional de evento), encapsulados en la entidad `Billetera` bajo invariantes matemáticos estrictos de no negatividad (`saldo >= 0`).
3. **Inventario e instancias de cartas:** Registro de cartas físicas coleccionadas vinculadas a identificadores únicos inmutables y secuenciales (`{codigo}-{contador}`, ej. `CDRA-1`), junto con su estado de posesión.
4. **Métricas de actividad lúdica:** Registros no sensibles de interacción dentro del juego: sobres comprados, cartas adquiridas en el mercado, actividades y misiones reclamadas, y rachas de victorias/derrotas de combate.

**Privacidad absoluta:** La aplicación **no recolecta, no almacena ni transmite** datos personales sensibles: no solicita nombres reales, correos electrónicos, contraseñas, documentos de identidad, números de tarjetas de crédito ni datos de geolocalización o telemetría. Toda la información vive en memoria volátil de ejecución o en el navegador local, garantizando privacidad total por diseño.

---

## 2. Riesgo Ético Concreto y Cambio de Diseño que lo Mitiga

### Riesgo Ético Identificado: Mecánicas de Azar Depredadoras (*Loot Boxes*) y Vulnerabilidad de Menores de Edad
La industria de los videojuegos ha incorporado de forma recurrente sistemas de cajas de recompensa aleatoria (*loot boxes*) monetizadas con dinero real. Diversos estudios de psicología del comportamiento y bioética demuestran que estas mecánicas activan respuestas neurológicas idénticas a los juegos de azar tradicionales (ludopatía). Cuando tales dinámicas se dirigen o están al alcance de menores de edad (un público clave en juegos de criaturas coleccionables), el riesgo de inducir patrones de consumo compulsivo, adicción conductual y distorsión del valor del dinero es crítico.

### Decisiones de Diseño Implementadas para su Mitigación:
1. **Aislamiento Total del Dinero Real (Economía de Circuito Cerrado):**
   - El sistema opera únicamente con monedas ficticias (`Aureos` y `Jacks`).
   - Está prohibida arquitectónicamente cualquier vía de ingreso de divisas reales o de conversión/liquidación de cartas y monedas por dinero real (*cash-out*).
2. **Transparencia Matemática Radical de Probabilidades:**
   - En cumplimiento ético con normativas internacionales de protección al consumidor, las probabilidades de aparición de cada rareza en todos los sobres están explícitamente publicadas y son inmutables:
     - *Sobre Comun:* Comun 74%, Rara 20%, Super Rara 5%, Super Super Rara 0.9%, Legendaria 0.1%.
     - *Sobre Especial:* Comun 45%, Rara 35%, Super Rara 15%, Super Super Rara 4%, Legendaria 1%.
     - *Sobre Legendario:* Comun 20%, Rara 35%, Super Rara 30%, Super Super Rara 10%, Legendaria 5%.
   - No existen algoritmos de probabilidad adaptativa oculta ni "manipulación de retención" (técnicas de *dark patterns* o *pity mechanics* opacas).
3. **Acceso Directo y Precios Justos en el Mercado:**
   - Para evitar la frustración y la dependencia exclusiva del azar, el mercado ofrece una selección fija de 25 cartas con precios estables por rareza (10 Aureos Comun, 25 Aureos Rara, 40 Aureos Super Rara), permitiendo a los jugadores obtener criaturas específicas sin recurrir al azar.
4. **Diseño Équitable del Sobre de Evento:**
   - El sobre estacional "Noche Eterna" mitiga la explotación por escasez artificial: excluye intencionalmente rarezas extremas inalcanzables (0% SSR y 0% Legendaria) y distribuye un 15% garantizado entre las tres criaturas icónicas del evento (Chupacabritas 6%, Espíritu oscuro 6%, Wendigo 3%).

---

## 3. Marco Legal y Licencias Citados Tras su Lectura

1. **Protección de Datos Personales — Ley Nº 18.331 (República Oriental del Uruguay):**
   - *Artículo 7 (Principio de Finalidad y Proporcionalidad):* Establece que los datos no pueden ser usados para fines distintos de aquellos para los que fueron recabados y deben limitarse a lo estrictamente necesario. El diseño del juego cumple a cabalidad al prescindir de datos personales identificables.
   - *Artículo 8 (Seguridad de Datos):* Se garantiza la integridad de los datos en memoria mediante encapsulamiento estricto de clases, imposibilitando la alteración no autorizada de saldos o transferencias sin consentimiento mutuo.
2. **Regulación de Loterías y Juegos de Azar — Ley Nº 19.535 y Marco de la Dirección Nacional de Loterías y Quinielas (DNLQ):**
   - El ordenamiento jurídico uruguayo reserva la explotación de juegos de azar con apuestas en dinero al Estado. Al mantener una economía 100% ficticia, sin costo económico real de entrada ni posibilidad de redención económica de los activos digitales, el sistema se cataloga formalmente como software de entretenimiento lúdico, quedando fuera de la figura de juego de azar ilegal o apuesta clandestina.
3. **Propiedad Intelectual y Licencias de Contenido:**
   - **Dominio Público Cultural:** Los conceptos mitológicos, nombres y leyendas populares tradicionales (Sirena, Dragón, Kraken, Basilisco, Diablo de Jersey, etc.) pertenecen al patrimonio cultural colectivo universal y son de libre uso.
   - **Ilustraciones Propias:** Los recursos artísticos digitales incluidos en `documentos/Imagenes/` han sido elaborados por el equipo y se licencian bajo la licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**, permitiendo su estudio y reutilización académica sin fines comerciales.

---

## 4. Registro y Gobernanza del Uso de Inteligencia Artificial

De conformidad con los criterios de evaluación del curso, el uso de Inteligencia Artificial (asistente Antigravity / Gemini) se rigió bajo supervisión y validación humana continua:

- **Tareas en las que se utilizó la IA:**
  - Estructuración inicial y normalización de las 227 plantillas de criaturas desde el documento de diseño base (`Personajes_mitologicos_juego.docx`).
  - Asistencia en la formulación algebraica de probabilidades proporcionales para el sobre de evento.
  - Generación de la batería exhaustiva de pruebas unitarias (`unittest`) para verificar invariantes transaccionales.
  - Maquetación y estilos del frontend web responsive (`HTML5`, `CSS3` y componentes `JS`).
- **Criterio de Rechazo y Corrección de Errores de la IA:**
  - *Error real de la IA detectado:* La IA inicialmente propuso importar `from __future__ import annotations` y sugirió dependencias externas no autorizadas; ambas fueron rechazadas de inmediato para ceñirse estrictamente a la biblioteca estándar de Python y mantener total transparencia.
  - *Error conceptual de la IA en la economía del evento:* La IA intercambió erróneamente las cartas raras entre el evento y el mercado; el equipo humano detectó la inconsistencia con la especificación de diseño y corrigió el catálogo, asignando Wendigo (`RWEN`, Rara) como la carta exclusiva del sobre de evento *Noche Eterna* y Diablo de Jersey (`RDJE`) en el mercado de 25 cartas.
  - *Regla ortográfica de normalización:* La IA alternaba el uso de tildes ("Común" y "Comun", "Súper Rara" y "Super Rara"); el equipo estableció la normalización unívoca obligatoria sin tildes ("Comun", "Super Rara") en todo el sistema.
- **Aprendizaje obtenido:** La IA acelera la escritura de código repetitivo y tests, pero el modelado conceptual, la coherencia de invariantes, la ética del juego y la toma de decisiones arquitectónicas exigen pensamiento crítico y juicio humano permanente.
