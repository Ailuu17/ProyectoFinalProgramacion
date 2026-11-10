from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional, Sequence, Union

from .principales import Evento, PlantillaCriatura, SobreEstable, TipoSobre


@dataclass
class Catalogo:
    plantillas: Dict[str, PlantillaCriatura] = field(default_factory=dict)

    def buscar(self, codigo: str) -> PlantillaCriatura:
        if codigo not in self.plantillas:
            raise ValueError(f"No existe la plantilla {codigo} en el catálogo.")
        return self.plantillas[codigo]

    def de_rareza(self, rareza: str) -> List[PlantillaCriatura]:
        return [
            plantilla
            for plantilla in self.plantillas.values()
            if plantilla.rareza.lower() == rareza.lower()
        ]

    def de_tipo(self, tipo: str) -> List[PlantillaCriatura]:
        return [
            plantilla
            for plantilla in self.plantillas.values()
            if plantilla.tipo.lower() == tipo.lower()
        ]


@dataclass
class Mercado:
    ofertas: Dict[str, int] = field(default_factory=dict)
    sobres: List[SobreEstable] = field(default_factory=list)
    tasa_cambio: int = 1

    def precio_de(self, codigo: str) -> int:
        if codigo not in self.ofertas:
            raise ValueError(f"La carta {codigo} no tiene precio en el mercado.")
        return self.ofertas[codigo]

    def cambiar_moneda(self, cantidad_comunes: int) -> int:
        if cantidad_comunes < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        return int(cantidad_comunes * self.tasa_cambio)

    def evento_vigente(
        self,
        eventos_o_fecha: Union[Sequence[Evento], date],
        fecha: Optional[date] = None,
    ) -> Optional[Evento]:
        if isinstance(eventos_o_fecha, date) and fecha is None:
            fecha_busqueda = eventos_o_fecha
            lista_eventos = getattr(self, "eventos", [])
        else:
            lista_eventos = eventos_o_fecha  # type: ignore
            fecha_busqueda = fecha  # type: ignore

        if fecha_busqueda is None:
            return None

        for evento in lista_eventos:
            if evento.fecha_inicio <= fecha_busqueda <= evento.fecha_fin:
                return evento
        return None

    def sobres_disponibles(
        self,
        eventos_o_fecha: Union[Sequence[Evento], date],
        fecha: Optional[date] = None,
    ) -> List[TipoSobre]:
        if isinstance(eventos_o_fecha, date) and fecha is None:
            fecha_busqueda = eventos_o_fecha
            lista_eventos = getattr(self, "eventos", [])
        else:
            lista_eventos = eventos_o_fecha  # type: ignore
            fecha_busqueda = fecha  # type: ignore

        disponibles: List[TipoSobre] = list(self.sobres)
        if fecha_busqueda is not None:
            vigente = self.evento_vigente(lista_eventos, fecha_busqueda)
            if vigente is not None and vigente.sobre is not None:
                if vigente.sobre not in disponibles:
                    disponibles.append(vigente.sobre)
        return disponibles
