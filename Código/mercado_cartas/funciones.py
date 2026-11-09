from __future__ import annotations

from datetime import date
from typing import Iterable, List, Optional, Sequence

from .azar import Azar
from .catalogo import Catalogo, Mercado
from .principales import Actividad, Carta, Evento, TipoSobre
from .jugador import Jugador


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
    def precio_actual(codigo: str, mercado: "Mercado", fecha: date) -> int:
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
