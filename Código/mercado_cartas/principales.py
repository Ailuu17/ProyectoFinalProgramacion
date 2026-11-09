from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable, Dict, List, Optional, Sequence


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
        total = sum(self.pesos_cartas.values())
        valor = numero % total
        acumulado = 0
        for codigo, peso in self.pesos_cartas.items():
            acumulado += peso
            if valor < acumulado:
                return self.sobre.probabilidades and codigo in self.sobre.probabilidades and self.sobre.probabilidades and codigo or codigo
        return next(iter(self.pesos_cartas.keys()))


@dataclass(frozen=True)
class Actividad:
    nombre: str
    recompensa: int
    condicion: Callable[["Jugador", Sequence["Carta"]], bool]

    def esta_cumplida(self, jugador: "Jugador", cartas: Sequence[Carta]) -> bool:
        return bool(self.condicion(jugador, cartas))
