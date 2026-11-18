# Documento de Ética, Legislación y Responsabilidad del Sistema

**Proyecto:** Mercado de Cartas Mitológicas (Proyecto B)  
**Asignatura:** Programación Científica y Técnica 2026
**Fecha de Entrega:** Jueves 19 de Noviembre de 2026  
**Integrantes:**  Lara Canío, Julieta Fernández, Sabrina Pereira y Aileen Waller

---

## 1. Datos que Maneja la Aplicación

El sistema fue diseñado bajo el principio de **minimización de datos** (*Privacy by Design*), el cuál busca minimizar los datos personales, identificativos o sensibles que se recolectan:

1. **Identificadores de usuario y perfiles:** Implementamos seudónimos como identificadores (`id: "j1"`, `id: "j2"`), alias públicos elegidos por el usuario (`nombre: "Ash"`, `nombre: "Misty"`) y avatares visuales.
2. **Estado económico y billetera:** Usamos monedas de ficción (definidas como int; `Aureos` como moneda base y `Jacks` como moneda estacional de evento), guardados en la entidad `Billetera` bajo invariantes matemáticos estrictos de no negatividad (`saldo >= 0`).
3. **Inventario e instancias de cartas:** Registro de cartas coleccionadas vinculadas a identificadores únicos, inmutables y secuenciales (`{codigo}-{contador}`, ej. `CDRA-1`), junto con su estado de posesión.
4. **Métricas de actividad lúdica:** Registros no sensibles de interacción dentro del juego: sobres comprados, cartas adquiridas en el mercado, actividades y misiones reclamadas, y rachas de victorias/derrotas de combate.

**Privacidad absoluta:** La aplicación **no recolecta, almacena ni transmite** datos personales sensibles. No solicita nombres reales, correos electrónicos, contraseñas, documentos de identidad, números de tarjetas de crédito ni datos de geolocalización o telemetría. Además, toda la información vive en memoria volátil de ejecución o en el navegador local, garantizando privacidad total por diseño. 
En una implementación futura probablemente se requiera un email para asociar al jugador y una contraseña para que cada usuario esté protegido, pero en esta implementación inicial no sucede.

---

## 2. Riesgo Ético Concreto y Cambio de Diseño que lo Mitiga

### Riesgo Ético Identificado: Vulnerabilidad de Menores de Edad por métricas del azar
La industria de los videojuegos ha incorporado cada vez más sistemas de cajas de recompensa aleatoria (*loot boxes*) monetizadas con dinero real. Diversos estudios de psicología del comportamiento y bioética demuestran que al hacerlo se activan respuestas neurológicas idénticas a los juegos de azar tradicionales (ludopatía). Cuando tales dinámicas están al alcance de menores de edad (un público clave en juegos de criaturas coleccionables como el nuestro), el riesgo de inducir patrones de consumo compulsivo, adicción y distorsión del valor del dinero es muy alto.

### Decisiones de Diseño Implementadas para su Mitigación:
1. **Aislamiento Total del Dinero Real (Economía de Circuito Cerrado):**
   - El sistema opera únicamente con monedas ficticias (`Aureos` y `Jacks`).
   - Está prohibida desde la arquitectura del programa cualquier vía de ingreso de divisas reales o de conversión de cartas y monedas a dinero real (*cash-out*).
2. **Transparencia Matemática Radical de Probabilidades:**
   - En cumplimiento ético de las normativas de protección al consumidor, las probabilidades que maneja nuestro azar de cada rareza en todos los sobres están explícitamente publicadas en la sección de información de cada sobre y son inmutables:
     - *Sobre Comun:* Comun 74%, Rara 20%, Super Rara 5%, Super Super Rara 0.9%, Legendaria 0.1%.
     - *Sobre Especial:* Comun 45%, Rara 35%, Super Rara 15%, Super Super Rara 4%, Legendaria 1%.
     - *Sobre Legendario:* Comun 20%, Rara 35%, Super Rara 30%, Super Super Rara 10%, Legendaria 5%.
     - Las categorías superiores a estas no se pueden asquirir directamente del mercado.
   - No existen algoritmos de probabilidad adaptativa oculta ni "manipulación de retención" (técnicas de *dark patterns* o *pity mechanics* opacas).
3. **Acceso Directo y Precios Justos en el Mercado:**
   - Para evitar la frustración y la dependencia exclusiva del azar, el mercado ofrece una selección fija de 25 cartas con precios estables por rareza (10 Aureos Comun, 25 Aureos Rara, 40 Aureos Super Rara), permitiendo a los jugadores obtener criaturas específicas sin recurrir al azar y poder comenzar su juego con ellas.

---

## 3. Marco Legal y Licencias Citados Tras su Lectura

1. **Protección de Datos Personales — Ley Nº 18.331 (República Oriental del Uruguay):**
   - *Artículo 7 (Principio de Finalidad y Proporcionalidad):* Establece que los datos no pueden ser usados para fines distintos de aquellos para los que fueron recabados. El diseño del juego cumple con lo solicitado al prescindir de datos personales identificables.
   - *Artículo 8 (Seguridad de Datos):* Se garantiza la integridad de los datos en memoria mediante encapsulamiento estricto de clases, imposibilitando la alteración no autorizada de saldos o transferencias sin consentimiento mutuo. Como mencionamos antes, nuestras monedas se encapsulan en la clase "billetera" y los datos de la sesión son volátiles en esta versión 1.0.
2. **Regulación de Loterías y Juegos de Azar — Ley Nº 19.535 y Marco de la Dirección Nacional de Loterías y Quinielas (DNLQ):**
   - El ordenamiento jurídico uruguayo reserva la explotación de juegos de azar con apuestas en dinero al Estado. Al mantener una economía 100% ficticia, sin costo económico real de entrada ni posibilidad de convertir los activos digitales en dinero real, el sistema se cataloga formalmente como software de entretenimiento lúdico, quedando fuera de la figura de juego de azar ilegal o apuesta clandestina.
3. **Propiedad Intelectual, Obras Derivadas y Licencias de Arte:**
   - **Dominio Público Cultural:** Los conceptos mitológicos, nombres y leyendas tradicionales (Sirena, Dragón, Kraken, Basilisco, etc.) pertenecen al patrimonio cultural universal y son de libre aprovechamiento lúdico.
   - **Autoría Humana Original (Ley Nº 9.739 y Ley Nº 17.616 de Derechos de Autor de Uruguay):** La concepción creativa, diseño visual y composición de los personajes nacieron del trabajo manual de una integrante del equipo, quien dibujó a lápiz sobre papel los bocetos originales de todas las criaturas, monedas y sobres que luego fueron digitalizados.
   - **Digitalización Asistida por IA y Términos de Servicio (ToS):** Los dibujos físicos fueron digitalizados y renderizados a color mediante herramientas de IA generativa (*sketch-to-image* / procesamiento gráfico), actuando la IA como herramienta técnica sobre el trabajo humano.Cumpliendo los Términos de Servicio de las herramientas empleadas y la doctrina de propiedad intelectual, el creador del input original retiene la titularidad sobre la obra derivada resultante.
   - **Licencia Pública de Distribución:** El catálogo gráfico resultante se comparte bajo licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 Internacional (CC BY-NC-SA 4.0)**, transparentando la autoría humana del arte base y su renderizado tecnológico sin fines comerciales.

---

## 4. Registro y Gobernanza del Uso de Inteligencia Artificial

Cumpliendo con los criterios de evaluación del curso, el uso de Inteligencia Artificial (asistente Antigravity / Claude) se rigió bajo supervisión y validación humana continua:

- **Tareas en las que se utilizó la IA:**
  - Digitalización y renderizado de arte analógico: Procesamiento, colorizado y texturizado digital asistido a partir de las ilustraciones originales dibujadas a lápiz sobre papel por la integrante anteriormente mencionada.
  - Estructuración inicial y normalización de las 227 plantillas de criaturas desde el documento de diseño base (`Personajes_mitologicos_juego.docx`).
  - Asistencia en la formulación algebraica de probabilidades proporcionales y justas para el sobre de evento.
  - Generación de la batería exhaustiva de pruebas unitarias (`unittest`) para verificar invariantes transaccionales.
  - Maquetación y estilos del frontend web responsive (`HTML5`, `CSS3` y componentes `JS`).
- **Criterio de Rechazo y Corrección de Errores de la IA:**
  - *Error real de la IA detectado:* La IA inicialmente propuso importar `from __future__ import annotations` y sugirió dependencias externas no autorizadas; ambas fueron rechazadas de inmediato para utilización estricta a la biblioteca estándar de Python y mantener total transparencia.
  - *Error conceptual de la IA en la economía del evento:* La IA intercambió erróneamente las cartas raras entre el evento y el mercado; nosotras detectamos la inconsistencia con la especificación de diseño y pudimos corregir el catálogo, asignando Wendigo (`RWEN`, Rara) como la carta exclusiva del sobre de evento *Noche Eterna* y Diablo de Jersey (`RDJE`) en el mercado de 25 cartas.
  - *Regla ortográfica de normalización:* La IA alternaba el uso de tildes ("Común" y "Comun", "Súper Rara" y "Super Rara"); al notarlo, establecimos la normalización obligatoria sin tildes ("Comun", "Super Rara") en todo el sistema.
- **Aprendizaje obtenido:** La IA acelera la escritura de código repetitivo y tests, pero el modelado conceptual, la coherencia de invariantes, la ética del juego y la toma de decisiones arquitectónicas exigen pensamiento crítico y juicio humano permanente.
