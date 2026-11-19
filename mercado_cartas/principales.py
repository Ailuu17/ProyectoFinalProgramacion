from datetime import date
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, List, Optional, Sequence, Set, Union

if TYPE_CHECKING:
    try:
        from .catalogo import Catalogo
        from .jugador import Jugador
    except (ImportError, ValueError):
        from catalogo import Catalogo
        from jugador import Jugador


def _tirar_opcion(
    tirar: Optional[Callable[[Sequence[Any], Optional[Sequence[float]]], Any]],
    opciones: Sequence[Any],
    pesos: Optional[Sequence[float]] = None,
) -> Any:
    if not opciones:
        raise ValueError("No hay opciones disponibles para elegir.")
    if tirar is not None:
        return tirar(opciones, pesos)

    import random
    if pesos is not None:
        return random.choices(list(opciones), weights=list(pesos), k=1)[0]
    return random.choice(list(opciones))



class Moneda:
    def __init__(self, nombre: str, evento: str = "") -> None:
        self.nombre = nombre
        self.evento = evento

    def __hash__(self) -> int:
        return hash((self.nombre, self.evento))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Moneda):
            return False
        return (self.nombre, self.evento) == (other.nombre, other.evento)

    def __repr__(self) -> str:
        if self.evento:
            return f"Moneda(nombre={self.nombre!r}, evento={self.evento!r})"
        return f"Moneda(nombre={self.nombre!r})"


# Cartas exclusivas del evento Noche Eterna
# Chupacabritas (Comun), Espíritu oscuro (Comun) y Wendigo (Rara)
# No se pueden conseguir en ningún sobre que no sea el de evento
CODIGOS_CARTAS_EVENTO_EXCLUSIVAS: Set[str] = {"CCHU", "CESO", "RWEN"}


class PlantillaCriatura:
    def __init__(
        self,
        codigo: str,
        nombre: str,
        rareza: str,
        tipo: str,
        vida: int,
        ataque: int,
        defensa: int,
        habilidad: str,
        descripcion_habilidad: str,
        usos_habilidad: int = 1,
    ) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa
        self.habilidad = habilidad
        self.descripcion_habilidad = descripcion_habilidad
        self.usos_habilidad = usos_habilidad
        self.rareza = rareza
        if self.rareza:
            r = self.rareza.strip().lower().replace("ú", "u")
            if r in ("c", "comun"):
                self.rareza = "Comun"
            elif r in ("r", "rara", "raro"):
                self.rareza = "Rara"
            elif r in ("sr", "super rara", "super_rara"):
                self.rareza = "Super Rara"
            elif r in ("ssr", "super super rara", "super_super_rara"):
                self.rareza = "Super Super Rara"
            elif r in ("l", "legendaria", "legendario"):
                self.rareza = "Legendaria"

    def __repr__(self) -> str:
        return f"PlantillaCriatura(codigo={self.codigo!r}, nombre={self.nombre!r}, rareza={self.rareza!r})"

    @property
    def contador(self) -> int:
        from .juego import Juego
        return Juego.contador_de(self.codigo)

    @contador.setter
    def contador(self, valor: int) -> None:
        from .juego import Juego
        Juego.establecer_contador(self.codigo, valor)

    @property
    def _contador(self) -> int:
        return self.contador

    @_contador.setter
    def _contador(self, valor: int) -> None:
        self.contador = valor

    def crear_carta(self, juego: Any = None) -> 'Carta':
        from .juego import Juego
        if juego is not None and hasattr(juego, "obtener_siguiente_contador"):
            num = juego.obtener_siguiente_contador(self.codigo)
        else:
            num = Juego.obtener_siguiente_contador(self.codigo)
        carta_id = f"{self.codigo}-{num}"
        return Carta(id=carta_id, plantilla=self)

    def __hash__(self) -> int:
        return hash(self.codigo)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlantillaCriatura):
            return False
        return self.codigo == other.codigo

    def a_dict(self) -> Dict[str, Any]:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "rareza": self.rareza,
            "tipo": self.tipo,
            "vida": self.vida,
            "ataque": self.ataque,
            "defensa": self.defensa,
            "habilidad": self.habilidad,
            "descripcion_habilidad": self.descripcion_habilidad,
            "usos_habilidad": self.usos_habilidad,
        }


class Carta:
    def __init__(
        self,
        id_o_plantilla: Union[str, PlantillaCriatura, None] = None,
        plantilla: Optional[PlantillaCriatura] = None,
        id: Optional[str] = None,
        contador: Optional[int] = None,
        _contador: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        if isinstance(id_o_plantilla, PlantillaCriatura):
            self.plantilla = id_o_plantilla
            carta_id = id
        elif isinstance(id_o_plantilla, str):
            carta_id = id_o_plantilla
            self.plantilla = plantilla  # type: ignore
        else:
            self.plantilla = plantilla  # type: ignore
            carta_id = id

        if self.plantilla is None:
            raise ValueError("Se requiere una PlantillaCriatura para la carta.")

        if carta_id is not None:
            self.id = carta_id
        else:
            c_val = contador if contador is not None else _contador
            if c_val is not None and c_val > 0:
                self.id = f"{self.plantilla.codigo}-{c_val}"
            else:
                from .juego import Juego
                num = Juego.obtener_siguiente_contador(self.plantilla.codigo)
                self.id = f"{self.plantilla.codigo}-{num}"

    @property
    def contador(self) -> int:
        try:
            return int(self.id.split("-")[-1])
        except (ValueError, IndexError):
            return 0

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Carta):
            return False
        return self.id == other.id

    def __repr__(self) -> str:
        return f"Carta(id={self.id!r}, plantilla={self.plantilla.nombre!r})"

    def a_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "contador": self.contador,
            "plantilla": self.plantilla.a_dict(),
        }


class TipoSobre:
    def __init__(
        self,
        nombre: str,
        cantidad_cartas: int,
        precio: int,
        moneda: Moneda,
        azar_rareza: Dict[str, float] = None,
        azar_criatura_c: Dict[Any, float] = None,
        azar_criatura_r: Dict[Any, float] = None,
        azar_criatura_sr: Dict[Any, float] = None,
    ) -> None:
        self.nombre: str = nombre
        self.cantidad_cartas: int = cantidad_cartas
        self.precio: int = precio
        self.moneda: Moneda = moneda
        self.azar_rareza: Dict[str, float] = dict(azar_rareza) if azar_rareza is not None else {}
        self.azar_criatura_c: Dict[Any, float] = dict(azar_criatura_c) if azar_criatura_c is not None else {}
        self.azar_criatura_r: Dict[Any, float] = dict(azar_criatura_r) if azar_criatura_r is not None else {}
        self.azar_criatura_sr: Dict[Any, float] = dict(azar_criatura_sr) if azar_criatura_sr is not None else {}

    def _dict_para_rareza(self, rareza: str) -> Dict[Any, float]:
        r = rareza.strip().lower().replace("ú", "u")
        if r in ("c", "comun"):
            return self.azar_criatura_c
        elif r in ("r", "rara", "raro"):
            return self.azar_criatura_r
        elif r in ("sr", "super rara", "super_rara"):
            return self.azar_criatura_sr
        return {}

    def obtener_carta(
        self,
        catalogo: "Catalogo",
        evento: Optional["Evento"] = None,
        tirar: Optional[Callable] = None,
        juego: Optional[Any] = None,
    ) -> Carta:
        if self.azar_rareza:
            opciones_r = list(self.azar_rareza.keys())
            pesos_r = list(self.azar_rareza.values())
            rareza = _tirar_opcion(tirar, opciones_r, pesos_r)
        else:
            rareza = "Comun"

        rareza_str = str(rareza).strip()
        dict_criaturas = self._dict_para_rareza(rareza_str)
        if dict_criaturas:
            opciones_c = list(dict_criaturas.keys())
            pesos_c = list(dict_criaturas.values())
            elegido = _tirar_opcion(tirar, opciones_c, pesos_c)
        elif "evento" in rareza_str.lower() or "exclusiv" in rareza_str.lower():
            if evento is not None and evento.pesos_cartas:
                opciones_ev = list(evento.pesos_cartas.keys())
                pesos_ev = list(evento.pesos_cartas.values())
                elegido = _tirar_opcion(tirar, opciones_ev, pesos_ev)
            else:
                elegido = _tirar_opcion(tirar, list(CODIGOS_CARTAS_EVENTO_EXCLUSIVAS))
        else:
            plantillas = catalogo.de_rareza(rareza_str)
            # Regla: Las cartas exclusivas de evento (Chupacabritas, Espíritu oscuro, Wendigo)
            # NO se pueden conseguir en ningún sobre que no sea el de evento
            plantillas = [
                p for p in plantillas
                if p.codigo not in CODIGOS_CARTAS_EVENTO_EXCLUSIVAS
            ]
            if not plantillas:
                if evento is not None and evento.pesos_cartas:
                    opciones_ev = list(evento.pesos_cartas.keys())
                    pesos_ev = list(evento.pesos_cartas.values())
                    elegido = _tirar_opcion(tirar, opciones_ev, pesos_ev)
                else:
                    plantillas = [
                        p for p in catalogo.plantillas.values()
                        if p.codigo not in CODIGOS_CARTAS_EVENTO_EXCLUSIVAS
                    ]
                    if not plantillas:
                        raise ValueError(f"No hay cartas disponibles en el catálogo para la rareza {rareza}.")
                    elegido = _tirar_opcion(tirar, plantillas)
            else:
                elegido = _tirar_opcion(tirar, plantillas)

        if isinstance(elegido, PlantillaCriatura):
            plantilla = elegido
        else:
            plantilla = catalogo.buscar(str(elegido))

        return plantilla.crear_carta(juego=juego)

    def abrir(
        self,
        catalogo: "Catalogo",
        evento: Optional["Evento"] = None,
        tirar: Optional[Callable] = None,
        juego: Optional[Any] = None,
    ) -> List[Carta]:
        return [self.obtener_carta(catalogo, evento, tirar, juego=juego) for _ in range(self.cantidad_cartas)]


class SobreEstable(TipoSobre):
    def __init__(
        self,
        nombre: str,
        cantidad_cartas: int,
        precio: int,
        moneda: Moneda,
        azar_rareza: Dict[str, float] = None,
        azar_criatura_c: Dict[Any, float] = None,
        azar_criatura_r: Dict[Any, float] = None,
        azar_criatura_sr: Dict[Any, float] = None,
        azar_criatura_ssr: Dict[Any, float] = None,
        azar_criatura_l: Dict[Any, float] = None,
    ) -> None:
        super().__init__(
            nombre=nombre,
            cantidad_cartas=cantidad_cartas,
            precio=precio,
            moneda=moneda,
            azar_rareza=azar_rareza,
            azar_criatura_c=azar_criatura_c,
            azar_criatura_r=azar_criatura_r,
            azar_criatura_sr=azar_criatura_sr,
        )
        self.azar_criatura_ssr: Dict[Any, float] = dict(azar_criatura_ssr) if azar_criatura_ssr is not None else {}
        self.azar_criatura_l: Dict[Any, float] = dict(azar_criatura_l) if azar_criatura_l is not None else {}

    def _dict_para_rareza(self, rareza: str) -> Dict[Any, float]:
        r = rareza.strip().lower().replace("ú", "u")
        if r in ("ssr", "super super rara", "super_super_rara"):
            return self.azar_criatura_ssr
        elif r in ("l", "legendaria", "legendario"):
            return self.azar_criatura_l
        return super()._dict_para_rareza(rareza)


class SobreVariable(TipoSobre):
    def __init__(
        self,
        nombre: str,
        cantidad_cartas: int,
        precio: int,
        moneda: Moneda,
        azar_rareza: Dict[str, float] = None,
        azar_criatura_c: Dict[Any, float] = None,
        azar_criatura_r: Dict[Any, float] = None,
        azar_criatura_sr: Dict[Any, float] = None,
    ) -> None:
        super().__init__(
            nombre=nombre,
            cantidad_cartas=cantidad_cartas,
            precio=precio,
            moneda=moneda,
            azar_rareza=azar_rareza,
            azar_criatura_c=azar_criatura_c,
            azar_criatura_r=azar_criatura_r,
            azar_criatura_sr=azar_criatura_sr,
        )
        if self.azar_rareza:
            for k in self.azar_rareza.keys():
                k_norm = str(k).strip().lower().replace("ú", "u")
                if k_norm in ("ssr", "super super rara", "super_super_rara", "l", "legendaria", "legendario"):
                    raise ValueError(
                        f"El sobre de evento no maneja cartas SSR o Legendarias: {k}"
                    )


class Evento:
    def __init__(
        self,
        nombre: str,
        fecha_inicio: date,
        fecha_fin: date,
        moneda: Moneda,
        sobre: SobreVariable,
        pesos_cartas: Dict[Any, float] = None,
    ) -> None:
        self.nombre: str = nombre
        self.fecha_inicio: date = fecha_inicio
        self.fecha_fin: date = fecha_fin
        self.moneda: Moneda = moneda
        self.sobre: SobreVariable = sobre
        self.pesos_cartas: Dict[Any, float] = dict(pesos_cartas) if pesos_cartas is not None else {}

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


class Actividad:
    def __init__(
        self,
        nombre: str,
        tipo: str = "Actividad",
        recompensa: int = 0,
        condicion: Any = "",
    ) -> None:
        self.nombre: str = nombre
        self.tipo: str = tipo
        self.recompensa: int = int(recompensa)
        self.condicion: Any = condicion

    def esta_cumplida(self, jugador: "Jugador", cartas: Sequence["Carta"]) -> bool:
        if callable(self.condicion):
            return bool(self.condicion(jugador, cartas))
        return False
