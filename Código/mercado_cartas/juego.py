from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Dict, List, Optional, Sequence

from .catalogo import Catalogo, Mercado
from .principales import Actividad, Carta, TipoSobre
from .jugador import Jugador


@dataclass
class Juego:
    catalogo: Catalogo
    mercado: Mercado
    actividades: List[Actividad] = field(default_factory=list)
    _jugadores: Dict[str, Jugador] = field(default_factory=dict)
    _cartas: Dict[str, Carta] = field(default_factory=dict)
    _contadores: Dict[str, int] = field(default_factory=dict)
    _historial: List[dict] = field(default_factory=list)

    def comprar_sobre(self, jugador_id: str, sobre: TipoSobre, fecha: date) -> List[Carta]:
        if jugador_id not in self._jugadores:
            raise ValueError("El jugador no existe.")
        jugador = self._jugadores[jugador_id]
        if jugador.billetera.saldo(sobre.moneda) < sobre.precio:
            raise ValueError("El jugador no tiene saldo suficiente para comprar el sobre.")
        jugador.billetera.retirar(sobre.moneda, sobre.precio)
        jugador._sobres_comprados[sobre.nombre] = jugador._sobres_comprados.get(sobre.nombre, 0) + 1

        opciones = tuple(sobre.probabilidades.keys())
        pesos = tuple(sobre.probabilidades.values())
        import random

        cartas = sobre.abrir(
            self.catalogo,
            None,
            lambda: random.choices(opciones, weights=pesos, k=1)[0],
        )
        for carta in cartas:
            jugador.agregar_carta(carta.id)
            self._cartas[carta.id] = carta

        self._historial.append({"tipo": "comprar_sobre", "jugador": jugador_id, "sobre": sobre.nombre, "fecha": fecha})
        return cartas

    def comprar_carta(self, jugador_id: str, codigo: str) -> str:
        if jugador_id not in self._jugadores:
            raise ValueError("El jugador no existe.")
        jugador = self._jugadores[jugador_id]
        precio = self.mercado.precio_de(codigo)
        moneda = self.mercado.tasa_cambio.moneda_origen
        if jugador.billetera.saldo(moneda) < precio:
            raise ValueError("El jugador no tiene saldo suficiente para comprar la carta.")
        jugador.billetera.retirar(moneda, precio)
        jugador.agregar_carta(codigo)
        self._historial.append({"tipo": "comprar_carta", "jugador": jugador_id, "codigo": codigo})
        return codigo

    def intercambiar(
        self,
        jugador_a_id: str,
        cartas_a_ids: Sequence[str],
        jugador_b_id: str,
        cartas_b_ids: Sequence[str],
    ) -> None:
        jugador_a = self._jugadores[jugador_a_id]
        jugador_b = self._jugadores[jugador_b_id]
        for carta_id in cartas_a_ids:
            if carta_id not in jugador_a._cartas:
                raise ValueError(f"El jugador {jugador_a_id} no posee la carta {carta_id}.")
        for carta_id in cartas_b_ids:
            if carta_id not in jugador_b._cartas:
                raise ValueError(f"El jugador {jugador_b_id} no posee la carta {carta_id}.")
        for carta_id in cartas_a_ids:
            jugador_a.quitar_carta(carta_id)
            jugador_b.agregar_carta(carta_id)
        for carta_id in cartas_b_ids:
            jugador_b.quitar_carta(carta_id)
            jugador_a.agregar_carta(carta_id)
        self._historial.append({"tipo": "intercambiar", "jugador_a": jugador_a_id, "jugador_b": jugador_b_id})

    def convertir_moneda(self, jugador_id: str, cantidad_comunes: int, fecha: date) -> None:
        if cantidad_comunes < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        jugador = self._jugadores[jugador_id]
        tasa = self.mercado.tasa_cambio
        if jugador.billetera.saldo(tasa.moneda_origen) < cantidad_comunes:
            raise ValueError("No hay suficientes monedas comunes.")
        cantidad_convertida = tasa.convertir(cantidad_comunes)
        jugador.billetera.retirar(tasa.moneda_origen, cantidad_comunes)
        jugador.billetera.depositar(tasa.moneda_destino, cantidad_convertida)
        self._historial.append({"tipo": "convertir_moneda", "jugador": jugador_id, "cantidad": cantidad_comunes, "fecha": fecha})

    def completar_actividad(self, jugador_id: str, actividad: Actividad) -> None:
        jugador = self._jugadores[jugador_id]
        if actividad.nombre in jugador._actividades_completadas:
            raise ValueError("La actividad ya fue completada.")
        cartas = [self._cartas[carta_id] for carta_id in jugador._cartas if carta_id in self._cartas]
        if not actividad.esta_cumplida(jugador, cartas):
            raise ValueError("La actividad aún no se cumple.")
        jugador._actividades_completadas.append(actividad.nombre)
        jugador.billetera.depositar(self.mercado.tasa_cambio.moneda_origen, actividad.recompensa)
        self._historial.append({"tipo": "completar_actividad", "jugador": jugador_id, "actividad": actividad.nombre})

    def registrar_victoria(self, jugador_id: str, fecha: date) -> None:
        jugador = self._jugadores[jugador_id]
        jugador._victorias_por_dia[fecha] = jugador._victorias_por_dia.get(fecha, 0) + 1
        self._historial.append({"tipo": "registrar_victoria", "jugador": jugador_id, "fecha": fecha})

    def cartas_de(self, jugador_id: str, filtro: Optional[Callable[[Carta], bool]] = None) -> List[Carta]:
        jugador = self._jugadores[jugador_id]
        cartas = [self._cartas[carta_id] for carta_id in jugador._cartas if carta_id in self._cartas]
        if filtro is not None:
            return [carta for carta in cartas if filtro(carta)]
        return cartas

    def coleccion_de(self, jugador_id: str) -> Dict[str, int]:
        jugador = self._jugadores[jugador_id]
        coleccion: Dict[str, int] = {}
        for carta_id in jugador._cartas:
            coleccion[carta_id] = coleccion.get(carta_id, 0) + 1
        return coleccion
