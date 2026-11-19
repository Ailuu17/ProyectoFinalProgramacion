from datetime import date
from typing import Dict, List

try:
    from .principales import Moneda
except (ImportError, ValueError):
    from principales import Moneda


class Billetera:
    def __init__(self, saldos: Dict[Moneda, int] = None) -> None:
        self._saldos: Dict[Moneda, int] = dict(saldos) if saldos is not None else {}

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


class Jugador:
    def __init__(
        self,
        id: str,
        nombre: str,
        billetera: Billetera = None,
        cartas: List[str] = None,
        actividades_completadas: List[str] = None,
        sobres_comprados: Dict[str, int] = None,
        victorias_por_dia: Dict[date, int] = None,
        cartas_compradas_mercado: int = 0,
        intercambios_completados: int = 0,
        victorias_consecutivas: int = 0,
    ) -> None:
        self.id: str = id
        self.nombre: str = nombre
        self.billetera: Billetera = billetera if billetera is not None else Billetera()
        self._cartas: List[str] = list(cartas) if cartas is not None else []
        self._actividades_completadas: List[str] = list(actividades_completadas) if actividades_completadas is not None else []
        self._sobres_comprados: Dict[str, int] = dict(sobres_comprados) if sobres_comprados is not None else {}
        self._victorias_por_dia: Dict[date, int] = dict(victorias_por_dia) if victorias_por_dia is not None else {}
        self._cartas_compradas_mercado: int = cartas_compradas_mercado
        self._intercambios_completados: int = intercambios_completados
        self._victorias_consecutivas: int = victorias_consecutivas

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

    @property
    def cartas_compradas_mercado(self) -> int:
        return self._cartas_compradas_mercado

    @property
    def intercambios_completados(self) -> int:
        return self._intercambios_completados

    @property
    def victorias_consecutivas(self) -> int:
        return self._victorias_consecutivas

    def agregar_carta(self, carta_id: str) -> None:
        self._cartas.append(carta_id)

    def quitar_carta(self, carta_id: str) -> None:
        if carta_id in self._cartas:
            self._cartas.remove(carta_id)
        else:
            raise ValueError(f"El jugador no posee la carta {carta_id}.")
