from __future__ import annotations

from typing import Optional, Sequence


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
