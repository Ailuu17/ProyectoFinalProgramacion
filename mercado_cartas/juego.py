from datetime import date
from typing import Any, Callable, ClassVar, Dict, List, Optional, Sequence

try:
    from .catalogo import Catalogo, Mercado
    from .principales import Actividad, Carta, Evento, Moneda, TipoSobre
    from .jugador import Jugador
except (ImportError, ValueError):
    from catalogo import Catalogo, Mercado
    from principales import Actividad, Carta, Evento, Moneda, TipoSobre
    from jugador import Jugador


class Juego:
    _instancia_actual: ClassVar[Optional["Juego"]] = None
    _contadores_defecto: ClassVar[List[Dict[str, Any]]] = []

    def __init__(
        self,
        catalogo: Catalogo,
        mercado: Mercado,
        actividades: Optional[List[Actividad]] = None,
        eventos: Optional[List[Evento]] = None,
        jugadores: Optional[Dict[str, Jugador]] = None,
        cartas: Optional[Dict[str, Carta]] = None,
        historial: Optional[List[dict]] = None,
        contadores: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.catalogo = catalogo
        self.mercado = mercado
        self.actividades = list(actividades) if actividades is not None else []
        self.eventos = list(eventos) if eventos is not None else []
        self._jugadores = dict(jugadores) if jugadores is not None else {}
        self._cartas = dict(cartas) if cartas is not None else {}
        self._historial = list(historial) if historial is not None else []
        self._contadores = list(contadores) if contadores is not None else []
        Juego._instancia_actual = self

    @property
    def contadores(self) -> List[Dict[str, Any]]:
        return self._contadores

    def obtener_siguiente_contador(self, codigo: str) -> int:
        for item in self._contadores:
            if item.get("codigo") == codigo:
                item["cantidad"] = item.get("cantidad", 0) + 1
                return item["cantidad"]
        nuevo = {"codigo": codigo, "cantidad": 1}
        self._contadores.append(nuevo)
        return 1

    def contador_de(self, codigo: str) -> int:
        for item in self._contadores:
            if item.get("codigo") == codigo:
                return item.get("cantidad", 0)
        return 0

    def establecer_contador(self, codigo: str, valor: int) -> None:
        for item in self._contadores:
            if item.get("codigo") == codigo:
                if valor == 0:
                    self._contadores.remove(item)
                else:
                    item["cantidad"] = valor
                return
        if valor > 0:
            self._contadores.append({"codigo": codigo, "cantidad": valor})

    def reiniciar_contadores(self) -> None:
        self._contadores.clear()

    @classmethod
    def obtener_siguiente_contador_global(cls, codigo: str) -> int:
        if cls._instancia_actual is not None:
            return cls._instancia_actual.obtener_siguiente_contador(codigo)
        for item in cls._contadores_defecto:
            if item.get("codigo") == codigo:
                item["cantidad"] = item.get("cantidad", 0) + 1
                return item["cantidad"]
        nuevo = {"codigo": codigo, "cantidad": 1}
        cls._contadores_defecto.append(nuevo)
        return 1

    @classmethod
    def contador_global_de(cls, codigo: str) -> int:
        if cls._instancia_actual is not None:
            return cls._instancia_actual.contador_de(codigo)
        for item in cls._contadores_defecto:
            if item.get("codigo") == codigo:
                return item.get("cantidad", 0)
        return 0

    @classmethod
    def establecer_contador_global(cls, codigo: str, valor: int) -> None:
        if cls._instancia_actual is not None:
            cls._instancia_actual.establecer_contador(codigo, valor)
        for item in cls._contadores_defecto:
            if item.get("codigo") == codigo:
                if valor == 0:
                    cls._contadores_defecto.remove(item)
                else:
                    item["cantidad"] = valor
                return
        if valor > 0:
            cls._contadores_defecto.append({"codigo": codigo, "cantidad": valor})

    @classmethod
    def reiniciar_contadores_globales(cls) -> None:
        if cls._instancia_actual is not None:
            cls._instancia_actual.reiniciar_contadores()
        cls._contadores_defecto.clear()

    @property
    def jugadores(self) -> Dict[str, Jugador]:
        return self._jugadores

    @property
    def cartas(self) -> Dict[str, Carta]:
        return self._cartas

    @property
    def historial(self) -> List[dict]:
        return list(self._historial)

    def agregar_jugador(self, jugador: Jugador) -> None:
        self._jugadores[jugador.id] = jugador

    def _obtener_jugador(self, jugador_id: str) -> Jugador:
        if jugador_id not in self._jugadores:
            raise ValueError(f"El jugador {jugador_id} no existe.")
        return self._jugadores[jugador_id]

    def _moneda_comun(self) -> Moneda:
        for sobre in self.mercado.sobres:
            if sobre.moneda:
                return sobre.moneda
        return Moneda("Aureos")

    def comprar_sobre(self, jugador_id: str, sobre: TipoSobre, fecha: date) -> List[Carta]:
        jugador = self._obtener_jugador(jugador_id)
        # 1. Validar que el sobre esté disponible en el mercado en la fecha indicada
        sobres_disponibles = self.mercado.sobres_disponibles(self.eventos, fecha)
        if sobre not in sobres_disponibles:
            raise ValueError("El sobre no está disponible en la fecha especificada.")

        # 2. Validar saldo suficiente
        if jugador.billetera.saldo(sobre.moneda) < sobre.precio:
            raise ValueError("El jugador no tiene saldo suficiente para comprar el sobre.")

        # 3. Generar el sobre y determinar las cartas previo a cobrar
        evento = self.mercado.evento_vigente(self.eventos, fecha)
        cartas = sobre.abrir(self.catalogo, evento, None, juego=self)

        # 4. Entregar las cartas al jugador y registrarlas en el juego
        for carta in cartas:
            jugador.agregar_carta(carta.id)
            self._cartas[carta.id] = carta

        # 5. Cobrar al jugador después de generar y entregar las cartas
        jugador.billetera.retirar(sobre.moneda, sobre.precio)
        jugador._sobres_comprados[sobre.nombre] = jugador._sobres_comprados.get(sobre.nombre, 0) + 1

        self._historial.append({
            "tipo": "comprar_sobre",
            "jugador": jugador_id,
            "sobre": sobre.nombre,
            "fecha": fecha,
        })
        return cartas

    def comprar_carta(self, jugador_id: str, codigo: str) -> str:
        jugador = self._obtener_jugador(jugador_id)
        precio = self.mercado.precio_de(codigo)
        moneda = self._moneda_comun()
        # 1. Validar saldo
        if jugador.billetera.saldo(moneda) < precio:
            raise ValueError("El jugador no tiene saldo suficiente para comprar la carta.")

        # 2. Generar la carta primero
        if codigo in self.catalogo.plantillas:
            plantilla = self.catalogo.buscar(codigo)
            carta = plantilla.crear_carta(juego=self)
            carta_id = carta.id
            self._cartas[carta_id] = carta
        elif codigo in self._cartas:
            carta_id = codigo
        else:
            carta_id = codigo

        # 3. Entregar la carta al jugador
        jugador.agregar_carta(carta_id)
        jugador._cartas_compradas_mercado += 1

        # 4. Cobrar al jugador después de entregar la carta
        jugador.billetera.retirar(moneda, precio)

        self._historial.append({
            "tipo": "comprar_carta",
            "jugador": jugador_id,
            "codigo": codigo,
            "carta_id": carta_id,
        })
        return carta_id

    def intercambiar(
        self,
        jugador_a_id: str,
        cartas_a_ids: Sequence[str],
        jugador_b_id: str,
        cartas_b_ids: Sequence[str],
        aceptado_a: bool = True,
        aceptado_b: bool = True,
    ) -> None:
        if jugador_a_id == jugador_b_id:
            raise ValueError("Un jugador no puede intercambiar cartas consigo mismo.")
        if len(cartas_a_ids) > 3 or len(cartas_b_ids) > 3:
            raise ValueError("No se pueden ofrecer más de 3 cartas por jugador en un intercambio.")
        if len(cartas_a_ids) == 0 and len(cartas_b_ids) == 0:
            raise ValueError("El intercambio debe incluir al menos una carta.")
        if not aceptado_a or not aceptado_b:
            raise ValueError("El intercambio requiere la aceptación de ambos jugadores.")

        if len(cartas_a_ids) != len(set(cartas_a_ids)):
            raise ValueError("No se permiten cartas duplicadas en la oferta del jugador A.")
        if len(cartas_b_ids) != len(set(cartas_b_ids)):
            raise ValueError("No se permiten cartas duplicadas en la oferta del jugador B.")

        jugador_a = self._obtener_jugador(jugador_a_id)
        jugador_b = self._obtener_jugador(jugador_b_id)
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
        jugador_a._intercambios_completados += 1
        self._historial.append({
            "tipo": "intercambiar",
            "jugador_a": jugador_a_id,
            "jugador_b": jugador_b_id,
            "cartas_a": list(cartas_a_ids),
            "cartas_b": list(cartas_b_ids),
        })

    def batallar(self, jugador_a_id: str, jugador_b_id: str) -> None:
        """Sistema de batalla planificado para versiones futuras."""
        raise NotImplementedError("El sistema de batalla aún no está implementado.")

    def convertir_moneda(self, jugador_id: str, cantidad_comunes: int, fecha: date) -> None:
        if cantidad_comunes < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        jugador = self._obtener_jugador(jugador_id)
        evento = self.mercado.evento_vigente(self.eventos, fecha)
        if evento is None:
            raise ValueError("No hay un evento vigente en la fecha especificada.")

        moneda_origen = self._moneda_comun()
        moneda_destino = evento.moneda

        if jugador.billetera.saldo(moneda_origen) < cantidad_comunes:
            raise ValueError("No hay suficientes monedas comunes.")

        cantidad_convertida = self.mercado.cambiar_moneda(cantidad_comunes)
        jugador.billetera.retirar(moneda_origen, cantidad_comunes)
        jugador.billetera.depositar(moneda_destino, cantidad_convertida)
        self._historial.append({
            "tipo": "convertir_moneda",
            "jugador": jugador_id,
            "cantidad_comunes": cantidad_comunes,
            "cantidad_evento": cantidad_convertida,
            "fecha": fecha,
        })

    def completar_actividad(self, jugador_id: str, actividad: Actividad) -> None:
        jugador = self._obtener_jugador(jugador_id)
        if actividad.nombre in jugador._actividades_completadas:
            raise ValueError("La actividad ya fue completada.")
        cartas = [self._cartas[carta_id] for carta_id in jugador._cartas if carta_id in self._cartas]
        if not actividad.esta_cumplida(jugador, cartas):
            raise ValueError("La actividad aún no se cumple.")
        jugador._actividades_completadas.append(actividad.nombre)
        moneda_recompensa = self._moneda_comun()
        jugador.billetera.depositar(moneda_recompensa, actividad.recompensa)
        self._historial.append({
            "tipo": "completar_actividad",
            "jugador": jugador_id,
            "actividad": actividad.nombre,
        })

    def registrar_victoria(self, jugador_id: str, fecha: date) -> None:
        jugador = self._obtener_jugador(jugador_id)
        jugador._victorias_por_dia[fecha] = jugador._victorias_por_dia.get(fecha, 0) + 1
        jugador._victorias_consecutivas += 1
        self._historial.append({
            "tipo": "registrar_victoria",
            "jugador": jugador_id,
            "fecha": fecha,
        })

    def registrar_derrota(self, jugador_id: str) -> None:
        jugador = self._obtener_jugador(jugador_id)
        jugador._victorias_consecutivas = 0

    def cartas_de(self, jugador_id: str, filtro: Optional[Callable[[Carta], bool]] = None) -> List[Carta]:
        jugador = self._obtener_jugador(jugador_id)
        cartas = [self._cartas[carta_id] for carta_id in jugador._cartas if carta_id in self._cartas]
        if filtro is not None:
            return [carta for carta in cartas if filtro(carta)]
        return cartas

    def coleccion_de(self, jugador_id: str) -> Dict[str, int]:
        jugador = self._obtener_jugador(jugador_id)
        coleccion: Dict[str, int] = {}
        for carta_id in jugador._cartas:
            codigo = self._cartas[carta_id].plantilla.codigo if carta_id in self._cartas else carta_id
            coleccion[codigo] = coleccion.get(codigo, 0) + 1
        return coleccion

    def resumen_jugador(self, jugador_id: str) -> Dict[str, Any]:
        jugador = self._obtener_jugador(jugador_id)
        return {
            "id": jugador.id,
            "nombre": jugador.nombre,
            "saldos": {m.nombre: jugador.billetera.saldo(m) for m in jugador.billetera.saldos},
            "cartas": list(jugador.cartas),
            "coleccion": self.coleccion_de(jugador_id),
            "actividades_completadas": list(jugador.actividades_completadas),
            "sobres_comprados": dict(jugador.sobres_comprados),
            "cartas_compradas_mercado": jugador.cartas_compradas_mercado,
            "intercambios_completados": jugador.intercambios_completados,
            "victorias_por_dia": {str(k): v for k, v in jugador._victorias_por_dia.items()},
        }
