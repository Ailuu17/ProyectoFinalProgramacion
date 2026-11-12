from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

try:
    from .principales import Moneda
except (ImportError, ValueError):
    from principales import Moneda


@dataclass
class Billetera:
    _saldos: Dict[Moneda, int] = field(default_factory=dict)

    @property
    def saldos(self) -> Dict[Moneda, int]:
        return dict(self._saldos)

    def saldo(self, moneda: Moneda) -> int:
        return self._saldos.get(moneda, 0)

    def depositar(self, moneda: Moneda, monto: int) -> None:
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        self._saldos[moneda] = self.saldo(moneda) + monto

    def retirar(self, moneda: Moneda, monto: int) -> None:
        if monto < 0:
            raise ValueError("El monto no puede ser negativo.")
        if self.saldo(moneda) < monto:
            raise ValueError(f"Saldo insuficiente en {moneda.nombre}.")
        self._saldos[moneda] = self.saldo(moneda) - monto


@dataclass
class Jugador:
    id: str
    nombre: str
    billetera: Billetera = field(default_factory=Billetera)
    _cartas: List[str] = field(default_factory=list)
    _actividades_completadas: List[str] = field(default_factory=list)
    _sobres_comprados: Dict[str, int] = field(default_factory=dict)
    _victorias_por_dia: Dict[date, int] = field(default_factory=dict)

    @property
    def cartas(self) -> List[str]:
        return list(self._cartas)

    @property
    def actividades_completadas(self) -> List[str]:
        return list(self._actividades_completadas)

    @property
    def sobres_comprados(self) -> Dict[str, int]:
        return dict(self._sobres_comprados)

    @property
    def victorias_por_dia(self) -> Dict[date, int]:
        return dict(self._victorias_por_dia)

    def agregar_carta(self, carta_id: str) -> None:
        self._cartas.append(carta_id)

    def quitar_carta(self, carta_id: str) -> None:
        if carta_id in self._cartas:
            self._cartas.remove(carta_id)
        else:
            raise ValueError(f"El jugador no posee la carta {carta_id}.")
