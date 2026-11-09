from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Dict, Iterable, List, Optional, Sequence


@dataclass(frozen=True)
class Moneda:
    nombre: str
    color: str
    diseno: str


@dataclass(frozen=True)
class PlantillaCriatura:
    codigo: str
    nombre: str
    rareza: str
    tipo: str
    vida: int
    ataque: int
    defensa: int
    habilidad: str
    descripcion_habilidad: str


@dataclass(frozen=True)
class Carta:
    id: str
    plantilla: PlantillaCriatura


@dataclass(frozen=True)
class TipoSobre:
    nombre: str
    cantidad_cartas: int
    probabilidades: Dict[str, float]
    precio: int
    moneda: Moneda

    def categoria_para(self, numero: int) -> str:
        if numero <= 0:
            return "base"
        if numero <= 3:
            return "comun"
        return "rara"

    def abrir(
        self,
        catalogo: "Catalogo",
        evento: Optional["Evento"],
        tirar: Callable[[], str],
    ) -> List[Carta]:
        cartas: List[Carta] = []
        for index in range(self.cantidad_cartas):
            codigo = tirar()
            plantilla = catalogo.buscar(codigo)
            cartas.append(Carta(id=f"{plantilla.codigo}-{index}", plantilla=plantilla))
        return cartas


@dataclass(frozen=True)
class Evento:
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    moneda: Moneda
    sobre: TipoSobre
    pesos_cartas: Dict[str, int]

    def carta_para(self, numero: int) -> PlantillaCriatura:
        if not self.pesos_cartas:
            raise ValueError("El evento no tiene cartas definidas.")
        valor = numero % sum(self.pesos_cartas.values())
        acumulado = 0
        for codigo, peso in self.pesos_cartas.items():
            acumulado += peso
            if valor < acumulado:
                return self.sobre.probabilidades and codigo in self.sobre.probabilidades and codigo or codigo
        return next(iter(self.pesos_cartas))


@dataclass
class Catalogo:
    plantillas: Dict[str, PlantillaCriatura] = field(default_factory=dict)

    def buscar(self, codigo: str) -> PlantillaCriatura:
        if codigo not in self.plantillas:
            raise ValueError(f"No existe la plantilla {codigo} en el catálogo.")
        return self.plantillas[codigo]

    def de_rareza(self, rareza: str) -> List[PlantillaCriatura]:
        return [plantilla for plantilla in self.plantillas.values() if plantilla.rareza == rareza]

    def de_tipo(self, tipo: str) -> List[PlantillaCriatura]:
        return [plantilla for plantilla in self.plantillas.values() if plantilla.tipo == tipo]


@dataclass
class Mercado:
    ofertas: Dict[str, int] = field(default_factory=dict)
    sobres: List[TipoSobre] = field(default_factory=list)
    eventos: List[Evento] = field(default_factory=list)
    tasa_cambio: int = 1

    def precio_de(self, codigo: str) -> int:
        if codigo not in self.ofertas:
            raise ValueError(f"La carta {codigo} no tiene precio en el mercado.")
        return self.ofertas[codigo]

    def evento_vigente(self, fecha: date) -> Optional[Evento]:
        for evento in self.eventos:
            if evento.fecha_inicio <= fecha <= evento.fecha_fin:
                return evento
        return None

    def sobres_disponibles(self, fecha: date) -> List[TipoSobre]:
        return [sobre for sobre in self.sobres if sobre.nombre]


@dataclass(frozen=True)
class Actividad:
    nombre: str
    recompensa: int
    condicion: Callable[["Jugador", Sequence["Carta"]], bool]

    def esta_cumplida(self, jugador: "Jugador", cartas: Sequence[Carta]) -> bool:
        return bool(self.condicion(jugador, cartas))


@dataclass
class Billetera:
    saldos: Dict[Moneda, int] = field(default_factory=dict)

    def saldo(self, moneda: Moneda) -> int:
        return self.saldos.get(moneda, 0)

    def depositar(self, moneda: Moneda, monto: int) -> None:
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        self.saldos[moneda] = self.saldo(moneda) + monto

    def retirar(self, moneda: Moneda, monto: int) -> None:
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        if self.saldo(moneda) < monto:
            raise ValueError(f"Saldo insuficiente en {moneda.nombre}.")
        self.saldos[moneda] = self.saldo(moneda) - monto


@dataclass
class Jugador:
    id: str
    nombre: str
    billetera: Billetera = field(default_factory=Billetera)
    cartas: List[str] = field(default_factory=list)
    actividades_completadas: List[str] = field(default_factory=list)
    sobres_comprados: Dict[str, int] = field(default_factory=dict)
    victorias_por_dia: Dict[date, int] = field(default_factory=dict)

    def agregar_carta(self, carta_id: str) -> None:
        if carta_id not in self.cartas:
            self.cartas.append(carta_id)

    def quitar_carta(self, carta_id: str) -> None:
        if carta_id in self.cartas:
            self.cartas.remove(carta_id)


MONEDA_COMUN = Moneda("Común", "gris", "base")
MONEDA_EVENTO = Moneda("Evento", "amarillo", "evento")


@dataclass
class Juego:
    catalogo: Catalogo
    mercado: Mercado
    actividades: List[Actividad] = field(default_factory=list)
    jugadores: Dict[str, Jugador] = field(default_factory=dict)
    cartas: Dict[str, Carta] = field(default_factory=dict)
    contadores: Dict[str, int] = field(default_factory=dict)
    historial: List[dict] = field(default_factory=list)

    def comprar_sobre(self, jugador_id: str, sobre: TipoSobre, fecha: date) -> List[Carta]:
        if jugador_id not in self.jugadores:
            raise ValueError("El jugador no existe.")
        jugador = self.jugadores[jugador_id]
        if jugador.billetera.saldo(sobre.moneda) < sobre.precio:
            raise ValueError("El jugador no tiene saldo suficiente para comprar el sobre.")
        jugador.billetera.retirar(sobre.moneda, sobre.precio)
        jugador.sobres_comprados[sobre.nombre] = jugador.sobres_comprados.get(sobre.nombre, 0) + 1

        evento = self.mercado.evento_vigente(fecha)
        opciones = tuple(sobre.probabilidades.keys())
        pesos = tuple(sobre.probabilidades.values())
        cartas: List[Carta] = []
        for index in range(sobre.cantidad_cartas):
            codigo = self._tirar_carta(opciones, pesos)
            plantilla = self.catalogo.buscar(codigo)
            carta = Carta(id=f"{plantilla.codigo}-{index}", plantilla=plantilla)
            cartas.append(carta)
            jugador.agregar_carta(carta.id)
            self.cartas[carta.id] = carta

        self.historial.append({"tipo": "comprar_sobre", "jugador": jugador_id, "sobre": sobre.nombre, "fecha": fecha})
        return cartas

    def comprar_carta(self, jugador_id: str, codigo: str) -> str:
        if jugador_id not in self.jugadores:
            raise ValueError("El jugador no existe.")
        jugador = self.jugadores[jugador_id]
        precio = self.mercado.precio_de(codigo)
        moneda = MONEDA_COMUN
        if jugador.billetera.saldo(moneda) < precio:
            raise ValueError("El jugador no tiene saldo suficiente para comprar la carta.")
        jugador.billetera.retirar(moneda, precio)
        jugador.agregar_carta(codigo)
        self.historial.append({"tipo": "comprar_carta", "jugador": jugador_id, "codigo": codigo})
        return codigo

    @staticmethod
    def _tirar_carta(opciones: Sequence[str], pesos: Sequence[float]) -> str:
        import random
        total = sum(float(p) for p in pesos)
        valor = random.random() * total
        acumulado = 0.0
        for opcion, peso in zip(opciones, pesos):
            acumulado += float(peso)
            if valor <= acumulado:
                return opcion
        return opciones[-1]

    def intercambiar(
        self,
        jugador_a_id: str,
        cartas_a_ids: Sequence[str],
        jugador_b_id: str,
        cartas_b_ids: Sequence[str],
    ) -> None:
        jugador_a = self.jugadores[jugador_a_id]
        jugador_b = self.jugadores[jugador_b_id]
        for carta_id in cartas_a_ids:
            if carta_id not in jugador_a.cartas:
                raise ValueError(f"El jugador {jugador_a_id} no posee la carta {carta_id}.")
        for carta_id in cartas_b_ids:
            if carta_id not in jugador_b.cartas:
                raise ValueError(f"El jugador {jugador_b_id} no posee la carta {carta_id}.")
        for carta_id in cartas_a_ids:
            jugador_a.quitar_carta(carta_id)
            jugador_b.agregar_carta(carta_id)
        for carta_id in cartas_b_ids:
            jugador_b.quitar_carta(carta_id)
            jugador_a.agregar_carta(carta_id)
        self.historial.append({"tipo": "intercambiar", "jugador_a": jugador_a_id, "jugador_b": jugador_b_id})

    def convertir_moneda(self, jugador_id: str, cantidad_comunes: int, fecha: date) -> None:
        if cantidad_comunes < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        jugador = self.jugadores[jugador_id]
        if jugador.billetera.saldo(MONEDA_COMUN) < cantidad_comunes:
            raise ValueError("No hay suficientes monedas comunes.")
        jugador.billetera.retirar(MONEDA_COMUN, cantidad_comunes)
        jugador.billetera.depositar(MONEDA_EVENTO, cantidad_comunes)
        self.historial.append({"tipo": "convertir_moneda", "jugador": jugador_id, "cantidad": cantidad_comunes, "fecha": fecha})

    def completar_actividad(self, jugador_id: str, actividad: Actividad) -> None:
        jugador = self.jugadores[jugador_id]
        if actividad.nombre in jugador.actividades_completadas:
            raise ValueError("La actividad ya fue completada.")
        cartas = [self.cartas[carta_id] for carta_id in jugador.cartas if carta_id in self.cartas]
        if not actividad.esta_cumplida(jugador, cartas):
            raise ValueError("La actividad aún no se cumple.")
        jugador.actividades_completadas.append(actividad.nombre)
        jugador.billetera.depositar(MONEDA_COMUN, actividad.recompensa)
        self.historial.append({"tipo": "completar_actividad", "jugador": jugador_id, "actividad": actividad.nombre})

    def registrar_victoria(self, jugador_id: str, fecha: date) -> None:
        jugador = self.jugadores[jugador_id]
        jugador.victorias_por_dia[fecha] = jugador.victorias_por_dia.get(fecha, 0) + 1
        self.historial.append({"tipo": "registrar_victoria", "jugador": jugador_id, "fecha": fecha})

    def cartas_de(self, jugador_id: str, filtro: Optional[Callable[[Carta], bool]] = None) -> List[Carta]:
        jugador = self.jugadores[jugador_id]
        cartas = [self.cartas[carta_id] for carta_id in jugador.cartas if carta_id in self.cartas]
        if filtro is not None:
            return [carta for carta in cartas if filtro(carta)]
        return cartas

    def coleccion_de(self, jugador_id: str) -> Dict[str, int]:
        jugador = self.jugadores[jugador_id]
        coleccion: Dict[str, int] = {}
        for carta_id in jugador.cartas:
            coleccion[carta_id] = coleccion.get(carta_id, 0) + 1
        return coleccion


class Azar:
    def elegir(self, opciones: Sequence[str], pesos: Optional[Sequence[float]] = None):
        if not opciones:
            raise ValueError("Debe haber al menos una opción disponible.")
        if pesos is None:
            return opciones[0]
        total = sum(float(p) for p in pesos)
        if total <= 0:
            raise ValueError("La suma de pesos debe ser positiva.")
        import random
        valor = random.random() * total
        acumulado = 0.0
        for opcion, peso in zip(opciones, pesos):
            acumulado += float(peso)
            if valor <= acumulado:
                return opcion
        return opciones[-1]


class AzarConSemilla(Azar):
    def __init__(self, semilla: Optional[int] = None):
        import random
        self._rng = random.Random(semilla)

    def elegir(self, opciones: Sequence[str], pesos: Optional[Sequence[float]] = None):
        if not opciones:
            raise ValueError("Debe haber al menos una opción disponible.")
        if pesos is None:
            return self._rng.choice(list(opciones))
        total = sum(float(p) for p in pesos)
        if total <= 0:
            raise ValueError("La suma de pesos debe ser positiva.")
        valor = self._rng.random() * total
        acumulado = 0.0
        for opcion, peso in zip(opciones, pesos):
            acumulado += float(peso)
            if valor <= acumulado:
                return opcion
        return opciones[-1]


class AzarFalso(Azar):
    def elegir(self, opciones: Sequence[str], pesos: Optional[Sequence[float]] = None):
        if not opciones:
            raise ValueError("Debe haber al menos una opción disponible.")
        return opciones[0]


class FuncionesPuras:
    @staticmethod
    def abrir_sobre(sobre: TipoSobre, catalogo: Catalogo, evento: Optional[Evento], azar: Azar) -> List[Carta]:
        cartas: List[Carta] = []
        opciones = tuple(sobre.probabilidades.keys())
        pesos = tuple(sobre.probabilidades.values())
        for index in range(sobre.cantidad_cartas):
            codigo = azar.elegir(opciones, pesos)
            plantilla = catalogo.buscar(codigo)
            cartas.append(Carta(id=f"{plantilla.codigo}-{index}", plantilla=plantilla))
        return cartas

    @staticmethod
    def precio_actual(codigo: str, mercado: Mercado, fecha: date) -> int:
        return mercado.precio_de(codigo)

    @staticmethod
    def evento_vigente(eventos: Iterable[Evento], fecha: date) -> Optional[Evento]:
        for evento in eventos:
            if evento.fecha_inicio <= fecha <= evento.fecha_fin:
                return evento
        return None

    @staticmethod
    def cumple(actividad: Actividad, jugador: Jugador, cartas: Sequence[Carta]) -> bool:
        return actividad.esta_cumplida(jugador, cartas)
