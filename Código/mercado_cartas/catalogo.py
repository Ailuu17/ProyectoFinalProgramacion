from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

from .principales import Evento, Moneda, PlantillaCriatura, TasaCambio, TipoSobre


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
    tasa_cambio: TasaCambio = field(
        default_factory=lambda: TasaCambio(
            moneda_origen=Moneda("Común", "gris", "base"),
            moneda_destino=Moneda("Evento", "amarillo", "evento"),
            factor=5,
        )
    )

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
        return list(self.sobres)
