from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Union

if TYPE_CHECKING:
    from .catalogo import Catalogo
    from .jugador import Jugador


def _tirar_opcion(
    tirar: Optional[Callable],
    opciones: Sequence[Any],
    pesos: Optional[Sequence[float]] = None,
) -> Any:
    if not opciones:
        raise ValueError("No hay opciones disponibles para elegir.")
    if tirar is not None:
        try:
            return tirar(opciones, pesos)
        except TypeError:
            pass
        try:
            return tirar(opciones)
        except TypeError:
            pass
        try:
            resultado = tirar()
            if resultado in opciones:
                return resultado
            if isinstance(resultado, (int, float)):
                total = sum(pesos) if pesos else float(len(opciones))
                val = float(resultado)
                if val < 1.0 and total > 1.0:
                    val = val * total
                acumulado = 0.0
                pesos_lista = pesos if pesos else [1.0] * len(opciones)
                for op, p in zip(opciones, pesos_lista):
                    acumulado += p
                    if val < acumulado:
                        return op
                return opciones[-1]
            return resultado
        except TypeError:
            pass

    import random
    if pesos is not None:
        return random.choices(list(opciones), weights=list(pesos), k=1)[0]
    return random.choice(list(opciones))


@dataclass
class Moneda:
    nombre: str
    color: str
    diseno: str

    def __hash__(self) -> int:
        return hash((self.nombre, self.color, self.diseno))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Moneda):
            return False
        return (self.nombre, self.color, self.diseno) == (other.nombre, other.color, other.diseno)


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
    usos_habilidad: int = 1
    _contador: int = field(default=0, init=False, repr=False)

    @property
    def contador(self) -> int:
        return self._contador

    @contador.setter
    def contador(self, valor: int) -> None:
        self._contador = valor

    def crear_carta(self) -> Carta:
        self._contador += 1
        return Carta(id=f"{self.codigo}-{self._contador}", plantilla=self)

    def __hash__(self) -> int:
        return hash(self.codigo)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlantillaCriatura):
            return False
        return self.codigo == other.codigo


@dataclass
class Carta:
    id: str
    plantilla: PlantillaCriatura

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Carta):
            return False
        return self.id == other.id


@dataclass
class TipoSobre:
    nombre: str
    cantidad_cartas: int
    precio: int
    moneda: Moneda

    def abrir(
        self,
        catalogo: "Catalogo",
        evento: Optional["Evento"] = None,
        tirar: Optional[Callable] = None,
    ) -> List[Carta]:
        cartas: List[Carta] = []
        opciones = list(catalogo.plantillas.keys())
        if not opciones:
            return cartas
        for _ in range(self.cantidad_cartas):
            codigo = _tirar_opcion(tirar, opciones)
            plantilla = catalogo.buscar(codigo) if isinstance(codigo, str) else codigo
            cartas.append(plantilla.crear_carta())
        return cartas


@dataclass
class SobreEstable(TipoSobre):
    azar_rareza: Dict[str, float] = field(default_factory=dict)
    azar_criatura_c: Dict[Any, float] = field(default_factory=dict)
    azar_criatura_r: Dict[Any, float] = field(default_factory=dict)
    azar_criatura_sr: Dict[Any, float] = field(default_factory=dict)
    azar_criatura_ssr: Dict[Any, float] = field(default_factory=dict)
    azar_criatura_l: Dict[Any, float] = field(default_factory=dict)

    def _dict_para_rareza(self, rareza: str) -> Dict[Any, float]:
        r = rareza.strip().lower()
        if r in ("c", "comun", "común"):
            return self.azar_criatura_c
        elif r in ("r", "rara", "raro"):
            return self.azar_criatura_r
        elif r in ("sr", "super rara", "súper rara", "super_rara"):
            return self.azar_criatura_sr
        elif r in ("ssr", "super super rara", "súper súper rara", "super_super_rara"):
            return self.azar_criatura_ssr
        elif r in ("l", "legendaria", "legendario"):
            return self.azar_criatura_l
        return {}

    def abrir(
        self,
        catalogo: "Catalogo",
        evento: Optional["Evento"] = None,
        tirar: Optional[Callable] = None,
    ) -> List[Carta]:
        cartas: List[Carta] = []
        for _ in range(self.cantidad_cartas):
            if self.azar_rareza:
                opciones_r = list(self.azar_rareza.keys())
                pesos_r = list(self.azar_rareza.values())
                rareza = _tirar_opcion(tirar, opciones_r, pesos_r)
            else:
                rareza = "Común"

            dict_criaturas = self._dict_para_rareza(str(rareza))
            if dict_criaturas:
                opciones_c = list(dict_criaturas.keys())
                pesos_c = list(dict_criaturas.values())
                elegido = _tirar_opcion(tirar, opciones_c, pesos_c)
            else:
                plantillas = catalogo.de_rareza(str(rareza))
                if not plantillas:
                    plantillas = list(catalogo.plantillas.values())
                if not plantillas:
                    raise ValueError(f"No hay cartas disponibles en el catálogo para la rareza {rareza}.")
                elegido = _tirar_opcion(tirar, plantillas)

            if isinstance(elegido, PlantillaCriatura):
                plantilla = elegido
            else:
                plantilla = catalogo.buscar(str(elegido))

            cartas.append(plantilla.crear_carta())
        return cartas


@dataclass
class SobreVariable(TipoSobre):
    azar_rareza: Dict[str, float] = field(default_factory=dict)
    azar_criatura_c: Dict[Any, float] = field(default_factory=dict)
    azar_criatura_r: Dict[Any, float] = field(default_factory=dict)
    azar_criatura_sr: Dict[Any, float] = field(default_factory=dict)

    def _dict_para_rareza(self, rareza: str) -> Dict[Any, float]:
        r = rareza.strip().lower()
        if r in ("c", "comun", "común"):
            return self.azar_criatura_c
        elif r in ("r", "rara", "raro"):
            return self.azar_criatura_r
        elif r in ("sr", "super rara", "súper rara", "super_rara"):
            return self.azar_criatura_sr
        return {}

    def abrir(
        self,
        catalogo: "Catalogo",
        evento: Optional["Evento"] = None,
        tirar: Optional[Callable] = None,
    ) -> List[Carta]:
        cartas: List[Carta] = []
        for _ in range(self.cantidad_cartas):
            if self.azar_rareza:
                opciones_r = list(self.azar_rareza.keys())
                pesos_r = list(self.azar_rareza.values())
                rareza = _tirar_opcion(tirar, opciones_r, pesos_r)
            else:
                rareza = "Común"

            dict_criaturas = self._dict_para_rareza(str(rareza))
            if dict_criaturas:
                opciones_c = list(dict_criaturas.keys())
                pesos_c = list(dict_criaturas.values())
                elegido = _tirar_opcion(tirar, opciones_c, pesos_c)
            elif evento is not None and evento.pesos_cartas:
                opciones_ev = list(evento.pesos_cartas.keys())
                pesos_ev = list(evento.pesos_cartas.values())
                elegido = _tirar_opcion(tirar, opciones_ev, pesos_ev)
            else:
                plantillas = catalogo.de_rareza(str(rareza))
                if not plantillas:
                    plantillas = list(catalogo.plantillas.values())
                if not plantillas:
                    raise ValueError(f"No hay cartas disponibles en el catálogo para la rareza {rareza}.")
                elegido = _tirar_opcion(tirar, plantillas)

            if isinstance(elegido, PlantillaCriatura):
                plantilla = elegido
            else:
                plantilla = catalogo.buscar(str(elegido))

            cartas.append(plantilla.crear_carta())
        return cartas


@dataclass
class Evento:
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    moneda: Moneda
    sobre: SobreVariable
    pesos_cartas: Dict[Any, int] = field(default_factory=dict)

    def carta_para(self, numero: int) -> Any:
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
        return int(cantidad * self.factor)
