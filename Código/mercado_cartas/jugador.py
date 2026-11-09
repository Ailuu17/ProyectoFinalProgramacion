from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from .principales import Carta, Moneda


@dataclass
class Billetera:
    _saldos: Dict[Moneda, int] = field(default_factory=dict)

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

    def agregar_carta(self, carta_id: str) -> None:
        if carta_id not in self._cartas:
            self._cartas.append(carta_id)

    def quitar_carta(self, carta_id: str) -> None:
        if carta_id in self._cartas:
            self._cartas.remove(carta_id)
