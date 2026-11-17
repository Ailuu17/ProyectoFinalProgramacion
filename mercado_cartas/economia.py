"""Configuración oficial de la economía, sobres y actividades del juego."""
from datetime import date
from typing import Dict, List, Optional, Sequence
try:
    from .principales import (
        Actividad,
        Desafio,
        Evento,
        Mision,
        Moneda,
        PlantillaCriatura,
        SobreEstable,
        SobreVariable,
    )
    from .catalogo import Catalogo, Mercado
    from .criaturas import CRIATURAS, PLANTILLAS_CRIATURAS
except (ImportError, ValueError):
    from principales import (
        Actividad,
        Desafio,
        Evento,
        Mision,
        Moneda,
        PlantillaCriatura,
        SobreEstable,
        SobreVariable,
    )
    from catalogo import Catalogo, Mercado
    from criaturas import CRIATURAS, PLANTILLAS_CRIATURAS

# ----------------------------------------------------------------------
# Nombres oficiales de monedas, sobres y eventos
# ----------------------------------------------------------------------
NOMBRE_MONEDA_COMUN = "Aureos"
NOMBRE_MONEDA_EVENTO = "Jacks"
NOMBRE_SOBRE_EVENTO = "Noche Eterna"
NOMBRE_EVENTO_VIGENTE = "Noche Eterna"

# ----------------------------------------------------------------------
# Monedas estándar
# ----------------------------------------------------------------------
MONEDA_COMUN = Moneda(NOMBRE_MONEDA_COMUN)
MONEDA_EVENTO = Moneda(NOMBRE_MONEDA_EVENTO, evento=NOMBRE_EVENTO_VIGENTE)

# ----------------------------------------------------------------------
# Cantidad de cartas por tipo de sobre
# ----------------------------------------------------------------------
CANTIDAD_CARTAS_SOBRE_ESTANDAR = 6
CANTIDAD_CARTAS_SOBRE_EVENTO = 3

# ----------------------------------------------------------------------
# Precios de sobres (en monedas normales salvo el sobre de evento)
# ----------------------------------------------------------------------
PRECIO_SOBRE_COMUN = 20
PRECIO_SOBRE_ESPECIAL = 45
PRECIO_SOBRE_LEGENDARIO = 80
PRECIO_SOBRE_EVENTO = 20  # monedas de evento

# ----------------------------------------------------------------------
# Precios de cartas en el mercado (monedas normales)
# ----------------------------------------------------------------------
PRECIO_CARTA_COMUN = 10
PRECIO_CARTA_RARA = 25
PRECIO_CARTA_SUPER_RARA = 40

# ----------------------------------------------------------------------
# Tasa de cambio de monedas (5 normales por 1 de evento)
# ----------------------------------------------------------------------
TASA_CAMBIO_NORMAL_A_EVENTO = 5

# ----------------------------------------------------------------------
# Probabilidades de los sobres
# ----------------------------------------------------------------------
PROBABILIDADES_SOBRE_COMUN: Dict[str, float] = {
    "Común": 74.0,
    "Rara": 20.0,
    "Súper Rara": 5.0,
    "Súper Súper Rara": 0.9,
    "Legendaria": 0.1,
}

PROBABILIDADES_SOBRE_ESPECIAL: Dict[str, float] = {
    "Común": 45.0,
    "Rara": 35.0,
    "Súper Rara": 15.0,
    "Súper Súper Rara": 4.0,
    "Legendaria": 1.0,
}

PROBABILIDADES_SOBRE_LEGENDARIO: Dict[str, float] = {
    "Común": 20.0,
    "Rara": 35.0,
    "Súper Rara": 30.0,
    "Súper Súper Rara": 10.0,
    "Legendaria": 5.0,
}

PROBABILIDADES_SOBRE_EVENTO: Dict[str, float] = {
    "Común": 40.0,
    "Rara": 30.0,
    "Súper Rara": 15.0,
    "Cartas del evento": 15.0,
}


def calcular_pesos_cartas_evento(
    cartas_evento: Sequence[PlantillaCriatura],
) -> Dict[str, float]:
    """Reparte el 15% del sobre de evento entre sus cartas exclusivas según rareza.
    El sobre de evento no maneja cartas SSR ni Legendarias.
    
    Para el evento vigente (Noche Eterna):
    - Común: peso relativo 2.0 (ej. 6% cada una si son 2 Comunes)
    - Rara: peso relativo 1.0 (ej. 3% si es 1 Rara)
    - Súper Rara: peso relativo 0.5
    """
    if not cartas_evento:
        return {}
    for c in cartas_evento:
        r = c.rareza.lower()
        if r in ("ssr", "súper súper rara", "super super rara", "legendaria", "legendario", "l"):
            raise ValueError(
                f"El sobre de evento no maneja cartas SSR o Legendarias: {c.nombre} ({c.rareza})"
            )
    peso_rareza = {
        "común": 2.0,
        "comun": 2.0,
        "rara": 1.0,
        "raro": 1.0,
        "súper rara": 0.5,
        "super rara": 0.5,
        "sr": 0.5,
    }
    total_rel = sum(peso_rareza.get(c.rareza.lower(), 1.0) for c in cartas_evento)
    pesos: Dict[str, float] = {}
    for c in cartas_evento:
        rel = peso_rareza.get(c.rareza.lower(), 1.0)
        pesos[c.codigo] = round(15.0 * (rel / total_rel), 2)
    return pesos


def crear_sobres_estandar(
    moneda_comun: Optional[Moneda] = None,
    cantidad_cartas: int = CANTIDAD_CARTAS_SOBRE_ESTANDAR,
) -> List[SobreEstable]:
    """Crea los tres sobres estables oficiales del juego (cada uno contiene 6 cartas)."""
    moneda = moneda_comun or MONEDA_COMUN
    sobre_comun = SobreEstable(
        nombre="Sobre común",
        cantidad_cartas=cantidad_cartas,
        precio=PRECIO_SOBRE_COMUN,
        moneda=moneda,
        azar_rareza=dict(PROBABILIDADES_SOBRE_COMUN),
    )
    sobre_especial = SobreEstable(
        nombre="Sobre especial",
        cantidad_cartas=cantidad_cartas,
        precio=PRECIO_SOBRE_ESPECIAL,
        moneda=moneda,
        azar_rareza=dict(PROBABILIDADES_SOBRE_ESPECIAL),
    )
    sobre_legendario = SobreEstable(
        nombre="Sobre legendario",
        cantidad_cartas=cantidad_cartas,
        precio=PRECIO_SOBRE_LEGENDARIO,
        moneda=moneda,
        azar_rareza=dict(PROBABILIDADES_SOBRE_LEGENDARIO),
    )
    return [sobre_comun, sobre_especial, sobre_legendario]


def crear_sobre_evento(
    moneda_evento: Optional[Moneda] = None,
    cartas_evento: Sequence[PlantillaCriatura] = (),
    nombre: str = NOMBRE_SOBRE_EVENTO,
    cantidad_cartas: int = CANTIDAD_CARTAS_SOBRE_EVENTO,
) -> SobreVariable:
    """Crea el sobre de evento (por defecto 'Noche Eterna', contiene 3 cartas) con probabilidad
    40% C, 30% R, 15% SR y 15% cartas de evento (no maneja SSR ni L).
    """
    for c in cartas_evento:
        r = c.rareza.lower()
        if r in ("ssr", "súper súper rara", "super super rara", "legendaria", "legendario", "l"):
            raise ValueError(
                f"El sobre de evento no maneja cartas SSR o Legendarias: {c.nombre} ({c.rareza})"
            )
    moneda = moneda_evento or MONEDA_EVENTO
    return SobreVariable(
        nombre=nombre,
        cantidad_cartas=cantidad_cartas,
        precio=PRECIO_SOBRE_EVENTO,
        moneda=moneda,
        azar_rareza=dict(PROBABILIDADES_SOBRE_EVENTO),
    )


def crear_evento_noche_eterna(
    cartas_evento: Sequence[PlantillaCriatura],
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    cantidad_cartas: int = CANTIDAD_CARTAS_SOBRE_EVENTO,
) -> Evento:
    """Crea el evento oficial vigente Noche Eterna con la moneda Jacks y el sobre Noche Eterna (3 cartas)."""
    f_inicio = fecha_inicio or date(2026, 10, 20)
    f_fin = fecha_fin or date(2026, 11, 20)
    sobre = crear_sobre_evento(
        moneda_evento=MONEDA_EVENTO,
        cartas_evento=cartas_evento,
        nombre=NOMBRE_SOBRE_EVENTO,
        cantidad_cartas=cantidad_cartas,
    )
    pesos = calcular_pesos_cartas_evento(cartas_evento)
    return Evento(
        nombre=NOMBRE_EVENTO_VIGENTE,
        fecha_inicio=f_inicio,
        fecha_fin=f_fin,
        moneda=MONEDA_EVENTO,
        sobre=sobre,
        pesos_cartas=pesos,
    )


# Alias de compatibilidad hacia atrás
crear_evento_halloween = crear_evento_noche_eterna


def crear_ofertas_mercado(catalogo: Optional[Catalogo] = None) -> Dict[str, int]:
    """Genera las ofertas de mercado asignando precios por rareza:
    - Común: 10 monedas
    - Rara: 25 monedas
    - Súper Rara: 40 monedas
    (SSR y Legendarias no se venden directamente en el mercado).
    """
    plantillas = catalogo.plantillas.values() if catalogo else CRIATURAS
    ofertas: Dict[str, int] = {}
    for p in plantillas:
        r = p.rareza.lower()
        if r in ("común", "comun"):
            ofertas[p.codigo] = PRECIO_CARTA_COMUN
        elif r in ("rara", "raro"):
            ofertas[p.codigo] = PRECIO_CARTA_RARA
        elif r in ("súper rara", "super rara", "sr"):
            ofertas[p.codigo] = PRECIO_CARTA_SUPER_RARA
    return ofertas


def crear_mercado_estandar(
    catalogo: Optional[Catalogo] = None,
    moneda_comun: Optional[Moneda] = None,
) -> Mercado:
    """Crea el mercado estándar con los 3 sobres oficiales, ofertas de cartas y cambio 5 a 1."""
    sobres = crear_sobres_estandar(moneda_comun=moneda_comun)
    ofertas = crear_ofertas_mercado(catalogo=catalogo)
    return Mercado(
        ofertas=ofertas,
        sobres=sobres,
        tasa_cambio=TASA_CAMBIO_NORMAL_A_EVENTO,
    )


# ----------------------------------------------------------------------
# Actividades oficiales (Documentos/Actividades.docx)
# ----------------------------------------------------------------------
def crear_misiones() -> List[Mision]:
    """Crea las 7 misiones oficiales del documento Actividades."""
    return [
        Mision(
            nombre="Conseguir al Leviatán",
            recompensa=100,
            tipo="Misión",
            condicion=lambda j, cartas: any(
                c.plantilla.codigo == "LLEV" or c.plantilla.nombre.lower() == "leviatán"
                for c in cartas
            ),
        ),
        Mision(
            nombre="Comprar 10 sobres comunes",
            recompensa=20,
            tipo="Misión",
            condicion=lambda j, cartas: j.sobres_comprados.get("Sobre común", 0) >= 10,
        ),
        Mision(
            nombre="Comprar 5 cartas del mercado",
            recompensa=5,
            tipo="Misión",
            condicion=lambda j, cartas: j.cartas_compradas_mercado >= 5,
        ),
        Mision(
            nombre="Comprar 15 cartas del mercado",
            recompensa=15,
            tipo="Misión",
            condicion=lambda j, cartas: j.cartas_compradas_mercado >= 15,
        ),
        Mision(
            nombre="Comprar 25 cartas del mercado",
            recompensa=25,
            tipo="Misión",
            condicion=lambda j, cartas: j.cartas_compradas_mercado >= 25,
        ),
        Mision(
            nombre="Conseguir 10 sobres especiales",
            recompensa=45,
            tipo="Misión",
            condicion=lambda j, cartas: j.sobres_comprados.get("Sobre especial", 0) >= 10,
        ),
        Mision(
            nombre="Conseguir 10 sobres legendarios",
            recompensa=80,
            tipo="Misión",
            condicion=lambda j, cartas: j.sobres_comprados.get("Sobre legendario", 0) >= 10,
        ),
    ]


def crear_desafios() -> List[Desafio]:
    """Crea los 5 desafíos oficiales del documento Actividades."""
    return [
        Desafio(
            nombre="Ganar 5 combates en un día",
            recompensa=20,
            tipo="Desafío",
            condicion=lambda j, cartas: any(v >= 5 for v in j.victorias_por_dia.values()),
        ),
        Desafio(
            nombre="Ganar 10 combates en un día",
            recompensa=40,
            tipo="Desafío",
            condicion=lambda j, cartas: any(v >= 10 for v in j.victorias_por_dia.values()),
        ),
        Desafio(
            nombre="Ganar 3 combates consecutivos",
            recompensa=10,
            tipo="Desafío",
            condicion=lambda j, cartas: j.victorias_consecutivas >= 3,
        ),
        Desafio(
            nombre="Ganar 6 combates consecutivos",
            recompensa=20,
            tipo="Desafío",
            condicion=lambda j, cartas: j.victorias_consecutivas >= 6,
        ),
        Desafio(
            nombre="Ganar 9 combates consecutivos",
            recompensa=30,
            tipo="Desafío",
            condicion=lambda j, cartas: j.victorias_consecutivas >= 9,
        ),
    ]


def crear_actividades() -> List[Actividad]:
    """Devuelve las 12 actividades (7 misiones + 5 desafíos) combinadas."""
    return list(crear_misiones()) + list(crear_desafios())
