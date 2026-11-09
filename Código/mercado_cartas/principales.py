from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Sequence

if TYPE_CHECKING:
    from .catalogo import Catalogo
    from .jugador import Jugador


@dataclass
class Moneda:
    nombre: str
    color: str
    diseno: str

    def __hash__(self) -> int:
        # A stable hash preserves value equality while currency fields are mutable.
        return hash(type(self))


@dataclass
class TasaCambio:
    moneda_origen: Moneda
    moneda_destino: Moneda
    factor: float

    def __post_init__(self) -> None:
        if self.factor <= 0:
            raise ValueError("El factor de conversión debe ser positivo.")

    def convertir(self, cantidad: int) -> int:
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        if self.factor <= 0:
            raise ValueError("El factor de conversión debe ser positivo.")
        return int(cantidad * self.factor)


@dataclass
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

    def __hash__(self) -> int:
        # Template fields are mutable, but templates are also used as dictionary keys.
        return hash(type(self))


@dataclass
class Carta:
    id: str
    plantilla: PlantillaCriatura


@dataclass
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


@dataclass
class Evento:
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    moneda: Moneda
    sobre: TipoSobre
    pesos_cartas: Dict[PlantillaCriatura, int]

    def carta_para(self, numero: int) -> PlantillaCriatura:
        if not self.pesos_cartas:
            raise ValueError("El evento no tiene cartas definidas.")
        total = sum(self.pesos_cartas.values())
        valor = numero % total
        acumulado = 0
        for plantilla, peso in self.pesos_cartas.items():
            acumulado += peso
            if valor < acumulado:
                return plantilla
        return next(iter(self.pesos_cartas.keys()))


@dataclass
class Actividad:
    nombre: str
    recompensa: int
    condicion: Callable[["Jugador", Sequence["Carta"]], bool]

    def esta_cumplida(self, jugador: "Jugador", cartas: Sequence[Carta]) -> bool:
        return bool(self.condicion(jugador, cartas))


@dataclass
class Mision(Actividad):
    pass


@dataclass
class Desafio(Actividad):
    pass
