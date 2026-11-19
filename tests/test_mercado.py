import sys
from datetime import date
from pathlib import Path
import unittest

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from mercado_cartas import (
    Actividad,
    Billetera,
    Carta,
    Catalogo,
    CRIATURAS,
    Evento,
    Juego,
    Jugador,
    Mercado,
    Moneda,
    PlantillaCriatura,
    PLANTILLAS_CRIATURAS,
    SobreEstable,
    SobreVariable,
    TipoSobre,
    crear_catalogo_completo,
    # Economía
    MONEDA_COMUN,
    MONEDA_EVENTO,
    NOMBRE_MONEDA_COMUN,
    NOMBRE_MONEDA_EVENTO,
    NOMBRE_SOBRE_EVENTO,
    NOMBRE_EVENTO_VIGENTE,
    PRECIO_SOBRE_COMUN,
    PRECIO_SOBRE_ESPECIAL,
    PRECIO_SOBRE_LEGENDARIO,
    PRECIO_SOBRE_EVENTO,
    PRECIO_CARTA_COMUN,
    PRECIO_CARTA_RARA,
    PRECIO_CARTA_SUPER_RARA,
    TASA_CAMBIO_NORMAL_A_EVENTO,
    PROBABILIDADES_SOBRE_EVENTO,
    CODIGOS_CARTAS_EVENTO_EXCLUSIVAS,
    CARTAS_EVENTO_NOCHE_ETERNA,
    calcular_pesos_cartas_evento,
    crear_sobres_estandar,
    crear_sobre_evento,
    crear_evento_noche_eterna,
    crear_mercado_estandar,
    crear_actividades,
    crear_misiones,
    crear_desafios,
)
from mercado_cartas.criaturas import (
    dragonzuelo,
    apep,
    sirena,
)


class TestMercadoCartasUML(unittest.TestCase):
    def setUp(self):
        dragonzuelo.contador = 0
        sirena.contador = 0
        apep.contador = 0

        self.moneda_comun = Moneda("Comun")
        self.moneda_evento = Moneda("Evento Lunar", "Festival de Luna")

        self.catalogo = crear_catalogo_completo()

        self.sobre_estable = SobreEstable(
            nombre="Sobre Clásico",
            cantidad_cartas=2,
            precio=50,
            moneda=self.moneda_comun,
            azar_rareza={"Comun": 80, "Rara": 20},
            azar_criatura_c={"CDRA": 100},
            azar_criatura_r={"RDFU": 100},
        )

        self.sobre_variable = SobreVariable(
            nombre="Sobre Exclusivo",
            cantidad_cartas=1,
            precio=100,
            moneda=self.moneda_evento,
            azar_rareza={"Exclusiva": 100},
        )

        self.evento = Evento(
            nombre="Festival de Luna",
            fecha_inicio=date(2026, 11, 1),
            fecha_fin=date(2026, 11, 30),
            moneda=self.moneda_evento,
            sobre=self.sobre_variable,
            pesos_cartas={"LAPE": 100},
        )

        self.mercado = Mercado(
            ofertas={"CDRA": 25, "RDFU": 75},
            sobres=[self.sobre_estable],
            tasa_cambio=5,
        )

        self.juego = Juego(
            catalogo=self.catalogo,
            mercado=self.mercado,
            eventos=[self.evento],
        )

        self.jugador_1 = Jugador(id="j1", nombre="Ash")
        self.jugador_2 = Jugador(id="j2", nombre="Misty")
        self.juego.agregar_jugador(self.jugador_1)
        self.juego.agregar_jugador(self.jugador_2)

    def test_criaturas_cargadas_correctamente(self):
        """Verifica que las 227 criaturas del Word estén instanciadas con sus atributos."""
        self.assertEqual(len(CRIATURAS), 227)
        self.assertEqual(len(PLANTILLAS_CRIATURAS), 227)

        # Verificar Dragonzuelo
        self.assertEqual(dragonzuelo.codigo, "CDRA")
        self.assertEqual(dragonzuelo.nombre, "Dragonzuelo")
        self.assertEqual(dragonzuelo.rareza, "Comun")
        self.assertEqual(dragonzuelo.tipo, "Dragónico")
        self.assertEqual(dragonzuelo.vida, 50)
        self.assertEqual(dragonzuelo.ataque, 12)
        self.assertEqual(dragonzuelo.defensa, 7)
        self.assertEqual(dragonzuelo.habilidad, "escupir fuego")
        self.assertEqual(dragonzuelo.descripcion_habilidad, "ataque x2 sobre un enemigo")
        self.assertEqual(dragonzuelo.usos_habilidad, 1)
        self.assertEqual(dragonzuelo.contador, 0)

        # Verificar Apep
        self.assertEqual(apep.codigo, "LAPE")
        self.assertEqual(apep.rareza, "Legendaria")
        self.assertEqual(apep.usos_habilidad, 2)

        # Verificar que no hay códigos duplicados entre las criaturas
        codigos = [c.codigo for c in CRIATURAS]
        self.assertEqual(len(codigos), len(set(codigos)), "Hay códigos de criaturas repetidos.")

        # Verificar que todos los tipos tienen la primera letra en mayúscula
        for c in CRIATURAS:
            self.assertTrue(
                c.tipo and c.tipo[0].isupper(),
                f"El tipo '{c.tipo}' de la criatura {c.nombre} no empieza con mayúscula.",
            )

    def test_invariante_saldo_no_negativo(self):
        """Regla: La billetera nunca permite saldo negativo ni retiro superior al saldo."""
        billetera = Billetera()
        billetera.depositar(self.moneda_comun, 100)
        self.assertEqual(billetera.saldo(self.moneda_comun), 100)

        with self.assertRaises(ValueError):
            billetera.retirar(self.moneda_comun, 150)

        with self.assertRaises(ValueError):
            billetera.depositar(self.moneda_comun, -10)

        self.assertEqual(billetera.saldo(self.moneda_comun), 100)

    def test_invariante_contador_plantilla_produce_ids_unicos(self):
        """Regla: Cada carta creada a partir de una plantilla recibe un ID único y secuencial."""
        c1 = dragonzuelo.crear_carta()
        c2 = dragonzuelo.crear_carta()
        self.assertEqual(c1.id, "CDRA-1")
        self.assertEqual(c2.id, "CDRA-2")
        self.assertEqual(dragonzuelo.contador, 2)

    def test_azar_determinista_apertura_sobre(self):
        """Regla: Con el mismo azar inyectado, la apertura de sobre produce el mismo resultado."""
        # Se inyecta una función de azar determinista que devuelve 'CDRA'
        cartas = self.sobre_estable.abrir(
            self.catalogo,
            evento=None,
            tirar=lambda ops, pesos=None: "CDRA" if "CDRA" in ops else ops[0],
        )
        self.assertEqual(len(cartas), 2)
        self.assertEqual(cartas[0].plantilla.codigo, "CDRA")
        self.assertEqual(cartas[1].plantilla.codigo, "CDRA")

    def test_error_en_tirar_se_propaga_sin_ser_silenciado(self):
        """Regla: Si la función de azar inyectada falla o tiene un bug, el error se propaga y no se oculta."""
        # 1. Error con excepción estándar (RuntimeError): no debe ser capturado ni reemplazado por random
        def tirar_con_error(opciones, pesos=None):
            raise RuntimeError("Fallo deliberado en el generador de azar inyectado.")

        with self.assertRaises(RuntimeError) as ctx:
            self.sobre_estable.abrir(
                self.catalogo,
                evento=None,
                tirar=tirar_con_error,
            )
        self.assertIn("Fallo deliberado", str(ctx.exception))

        # 2. Error de tipo (TypeError): anteriormente este error era capturado silenciosamente por
        # 'except TypeError: pass' y el sistema elegía al azar sin avisar. Ahora se propaga visiblemente.
        def tirar_con_type_error(opciones, pesos=None):
            return "texto" + 123  # TypeError real dentro de la función de azar

        with self.assertRaises(TypeError):
            self.sobre_estable.abrir(
                self.catalogo,
                evento=None,
                tirar=tirar_con_type_error,
            )

    def test_comprar_sobre_y_carta(self):
        """Regla: Al comprar un sobre o carta se descuenta la moneda y se asignan las cartas en orden seguro."""
        self.jugador_1.billetera.depositar(self.moneda_comun, 200)

        # Compra exitosa de sobre: entrega cartas y luego debita saldo
        cartas = self.juego.comprar_sobre(
            "j1", self.sobre_estable, date(2026, 11, 15)
        )
        self.assertEqual(len(cartas), 2)
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 150)
        self.assertEqual(len(self.jugador_1.cartas), 2)

        # Compra exitosa de carta
        cid = self.juego.comprar_carta("j1", "CDRA")
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 125)
        self.assertIn(cid, self.jugador_1.cartas)

        # Si el jugador no tiene saldo suficiente, la compra falla sin modificar saldo ni entregar cartas
        self.jugador_2.billetera.depositar(self.moneda_comun, 10)  # Sobre cuesta 50
        with self.assertRaises(ValueError):
            self.juego.comprar_sobre("j2", self.sobre_estable, date(2026, 11, 15))
        self.assertEqual(self.jugador_2.billetera.saldo(self.moneda_comun), 10)
        self.assertEqual(len(self.jugador_2.cartas), 0)

    def test_invariante_intercambio_cartas_sin_duplicacion(self):
        """Regla: En un intercambio, la carta sale de un jugador y entra al otro; no se duplica."""
        c1 = dragonzuelo.crear_carta()
        c2 = sirena.crear_carta()
        self.juego.cartas[c1.id] = c1
        self.juego.cartas[c2.id] = c2

        self.jugador_1.agregar_carta(c1.id)
        self.jugador_2.agregar_carta(c2.id)

        self.juego.intercambiar("j1", [c1.id], "j2", [c2.id])

        self.assertIn(c2.id, self.jugador_1.cartas)
        self.assertNotIn(c1.id, self.jugador_1.cartas)
        self.assertIn(c1.id, self.jugador_2.cartas)
        self.assertNotIn(c2.id, self.jugador_2.cartas)

    def test_invariante_intercambio_invalido_sin_rastros(self):
        """Regla: Una operación inválida falla y no modifica las cartas de los participantes."""
        c1 = dragonzuelo.crear_carta()
        self.jugador_1.agregar_carta(c1.id)

        # j2 intenta intercambiar una carta que no posee
        with self.assertRaises(ValueError):
            self.juego.intercambiar("j1", [c1.id], "j2", ["CARTA_FANTASMA"])

        # Ninguno cambió sus cartas
        self.assertIn(c1.id, self.jugador_1.cartas)
        self.assertEqual(len(self.jugador_2.cartas), 0)

    def test_intercambio_reglas_maximo_tres_cartas_y_ambos_aceptan(self):
        """Regla: Intercambio limitado a un máximo de 3 cartas por jugador y requiere mutuo acuerdo."""
        # Preparar 4 cartas para jugador 1
        c1 = dragonzuelo.crear_carta()
        c2 = dragonzuelo.crear_carta()
        c3 = dragonzuelo.crear_carta()
        c4 = dragonzuelo.crear_carta()
        cb = sirena.crear_carta()

        for c in (c1, c2, c3, c4):
            self.juego.cartas[c.id] = c
            self.jugador_1.agregar_carta(c.id)
        self.juego.cartas[cb.id] = cb
        self.jugador_2.agregar_carta(cb.id)

        # 1. Intentar intercambiar más de 3 cartas (4 cartas) debe ser rechazado
        with self.assertRaises(ValueError):
            self.juego.intercambiar("j1", [c1.id, c2.id, c3.id, c4.id], "j2", [cb.id])

        # 2. Intentar intercambiar consigo mismo debe ser rechazado
        with self.assertRaises(ValueError):
            self.juego.intercambiar("j1", [c1.id], "j1", [c2.id])

        # 3. Si uno de los jugadores no acepta el intercambio, se rechaza
        with self.assertRaises(ValueError):
            self.juego.intercambiar("j1", [c1.id], "j2", [cb.id], aceptado_b=False)

        # 4. No se permiten cartas duplicadas en la misma oferta
        with self.assertRaises(ValueError):
            self.juego.intercambiar("j1", [c1.id, c1.id], "j2", [cb.id])

        # 5. Intercambio legítimo de hasta 3 cartas con aceptación mutua
        self.juego.intercambiar("j1", [c1.id, c2.id, c3.id], "j2", [cb.id], aceptado_a=True, aceptado_b=True)
        self.assertIn(cb.id, self.jugador_1.cartas)
        self.assertIn(c1.id, self.jugador_2.cartas)
        self.assertIn(c2.id, self.jugador_2.cartas)
        self.assertIn(c3.id, self.jugador_2.cartas)

    def test_batalla_no_implementada_documentada(self):
        """Regla: El sistema de batalla está reservado y señalizado con NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.juego.batallar("j1", "j2")

    def test_sobres_disponibles_segun_vigencia_evento(self):
        """Regla: El sobre exclusivo de un evento solo está disponible durante su vigencia."""
        fecha_en_evento = date(2026, 11, 15)
        fecha_fuera_evento = date(2026, 12, 1)

        sobres_en = self.mercado.sobres_disponibles([self.evento], fecha_en_evento)
        self.assertEqual(len(sobres_en), 2)
        self.assertIn(self.sobre_estable, sobres_en)
        self.assertIn(self.sobre_variable, sobres_en)

        sobres_fuera = self.mercado.sobres_disponibles([self.evento], fecha_fuera_evento)
        self.assertEqual(len(sobres_fuera), 1)
        self.assertIn(self.sobre_estable, sobres_fuera)
        self.assertNotIn(self.sobre_variable, sobres_fuera)

        # Si el jugador intenta comprar el sobre exclusivo fuera de la vigencia del evento, falla
        self.jugador_1.billetera.depositar(self.moneda_evento, 200)
        with self.assertRaises(ValueError):
            self.juego.comprar_sobre("j1", self.sobre_variable, fecha_fuera_evento)

    def test_convertir_moneda_vigencia_evento(self):
        """Regla: Solo se puede convertir moneda si hay un evento vigente."""
        self.jugador_1.billetera.depositar(self.moneda_comun, 20)

        # Cinco Aureos se convierten en un Jack.
        self.juego.convertir_moneda("j1", 5, date(2026, 11, 15))
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 15)
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_evento), 1)

        # No se deben consumir Aureos si no alcanzan para un Jack completo.
        with self.assertRaises(ValueError):
            self.juego.convertir_moneda("j1", 4, date(2026, 11, 15))
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 15)
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_evento), 1)

        # Fuera de evento falla
        with self.assertRaises(ValueError):
            self.juego.convertir_moneda("j1", 10, date(2026, 12, 1))

    def test_actividad_mision_recompensa_unica(self):
        """Regla: Una actividad solo se recompensa si se cumple y no puede cobrarse dos veces."""
        mision = Actividad(
            nombre="Tener Dragón",
            tipo="Misión",
            recompensa=30,
            condicion=lambda j, cartas: any(c.plantilla.tipo == "Dragónico" for c in cartas),
        )

        # Sin la carta no se cumple
        with self.assertRaises(ValueError):
            self.juego.completar_actividad("j1", mision)

        # Se agrega la carta y se cumple
        c1 = dragonzuelo.crear_carta()
        self.juego.cartas[c1.id] = c1
        self.jugador_1.agregar_carta(c1.id)

        self.juego.completar_actividad("j1", mision)
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 30)
        self.assertIn("Tener Dragón", self.jugador_1.actividades_completadas)

        # No se puede repetir
        with self.assertRaises(ValueError):
            self.juego.completar_actividad("j1", mision)

    def test_coincidencia_con_uml(self):
        """Verifica que las clases, métodos y atributos coincidan con el diagrama UML."""
        # 1. Moneda: únicamente atributos nombre y evento (sin color ni diseno)
        m = Moneda(nombre="Oro", evento="Festival Lunar")
        self.assertEqual(m.nombre, "Oro")
        self.assertEqual(m.evento, "Festival Lunar")
        self.assertFalse(hasattr(m, "color"))
        self.assertFalse(hasattr(m, "diseno"))

        # 2. PlantillaCriatura y Carta: relación, ID y contador generado dinámicamente
        c1 = dragonzuelo.crear_carta()
        self.assertIsInstance(c1, Carta)
        self.assertEqual(c1.plantilla, dragonzuelo)
        self.assertEqual(c1.id, "CDRA-1")
        self.assertEqual(c1.contador, 1)

        # La siguiente carta creada busca el contador más alto existente (1) y suma 1
        c2 = dragonzuelo.crear_carta()
        self.assertEqual(c2.id, "CDRA-2")
        self.assertEqual(c2.contador, 2)
        self.assertEqual(dragonzuelo.contador, 2)

        # 3. TipoSobre: atributos base y método obtener_carta
        carta_individual = self.sobre_estable.obtener_carta(self.catalogo)
        self.assertIsInstance(carta_individual, Carta)
        self.assertTrue(hasattr(self.sobre_estable, "azar_rareza"))
        self.assertTrue(hasattr(self.sobre_estable, "azar_criatura_c"))
        self.assertTrue(hasattr(self.sobre_estable, "azar_criatura_r"))
        self.assertTrue(hasattr(self.sobre_estable, "azar_criatura_sr"))
        self.assertTrue(hasattr(self.sobre_estable, "azar_criatura_ssr"))
        self.assertTrue(hasattr(self.sobre_estable, "azar_criatura_l"))

        # 4. SobreVariable: hereda atributos base de TipoSobre
        self.assertTrue(issubclass(SobreVariable, TipoSobre))
        self.assertTrue(hasattr(self.sobre_variable, "azar_rareza"))
        self.assertTrue(hasattr(self.sobre_variable, "azar_criatura_c"))
        self.assertTrue(hasattr(self.sobre_variable, "azar_criatura_r"))
        self.assertTrue(hasattr(self.sobre_variable, "azar_criatura_sr"))

        # 5. Actividad: atributos nombre, tipo, recompensa, condicion
        act = Actividad(nombre="Batalla diaria", tipo="Desafío", recompensa=10)
        self.assertEqual(act.nombre, "Batalla diaria")
        self.assertEqual(act.tipo, "Desafío")
        self.assertEqual(act.recompensa, 10)
        self.assertTrue(hasattr(act, "esta_cumplida"))

        # 6. Catalogo: búsqueda por código, de_rareza y de_tipo
        dragones = self.catalogo.de_tipo("Dragónico")
        self.assertGreaterEqual(len(dragones), 1)
        self.assertIn(dragonzuelo, dragones)

        comunes = self.catalogo.de_rareza("Comun")
        self.assertGreaterEqual(len(comunes), 1)
        self.assertIn(dragonzuelo, comunes)

        # 7. Juego: contadores es una list<dict>
        self.assertIsInstance(self.juego.contadores, list)
        for item in self.juego.contadores:
            self.assertIsInstance(item, dict)
            self.assertIn("codigo", item)
            self.assertIn("cantidad", item)


    def test_economia_mercado_estandar_precios_y_sobres(self):
        """Regla: El mercado estándar tiene exactamente 3 sobres con los precios oficiales."""
        catalogo = crear_catalogo_completo()
        moneda = Moneda("Comun")
        mercado = crear_mercado_estandar(catalogo=catalogo, moneda_comun=moneda)

        self.assertIsInstance(mercado, Mercado)
        self.assertEqual(len(mercado.sobres), 3)

        # Comprobar precios y cantidad de cartas de los sobres (6 cartas por sobre estándar)
        precios = {s.nombre: s.precio for s in mercado.sobres}
        self.assertEqual(precios["Sobre Comun"], PRECIO_SOBRE_COMUN)          # 20
        self.assertEqual(precios["Sobre especial"], PRECIO_SOBRE_ESPECIAL)    # 45
        self.assertEqual(precios["Sobre legendario"], PRECIO_SOBRE_LEGENDARIO)  # 80
        for s in mercado.sobres:
            self.assertEqual(s.cantidad_cartas, 6)

        # Comprobar tasa de cambio
        self.assertEqual(mercado.tasa_cambio, TASA_CAMBIO_NORMAL_A_EVENTO)    # 5

        # Comprobar que las ofertas de cartas contienen solo C, R y SR (no SSR ni L)
        from mercado_cartas import CRIATURAS
        RAREZAS_SR = ("Súper Rara", "Super Rara", "SR")
        for codigo, precio in mercado.ofertas.items():
            plantilla = next((c for c in CRIATURAS if c.codigo == codigo), None)
            if plantilla:
                rareza_norm = plantilla.rareza
                is_comun = rareza_norm.lower() in ("común", "comun")
                is_rara = rareza_norm.lower() in ("rara", "raro")
                is_sr = rareza_norm in RAREZAS_SR or rareza_norm.lower() in ("súper rara", "super rara", "sr")
                self.assertTrue(is_comun or is_rara or is_sr,
                                f"El mercado no debería vender {rareza_norm}: {codigo}")
                if is_comun:
                    self.assertEqual(precio, PRECIO_CARTA_COMUN)
                elif is_rara:
                    self.assertEqual(precio, PRECIO_CARTA_RARA)
                elif is_sr:
                    self.assertEqual(precio, PRECIO_CARTA_SUPER_RARA)

    def test_economia_crear_actividades_cantidad_y_tipos(self):
        """Regla: crear_actividades() devuelve 12 actividades (7 misiones + 5 desafíos)."""
        actividades = crear_actividades()
        misiones = crear_misiones()
        desafios = crear_desafios()

        self.assertEqual(len(actividades), 12)
        self.assertEqual(len(misiones), 7)
        self.assertEqual(len(desafios), 5)

        # Verificar que todos son instancias de Actividad y tienen el tipo correcto según el UML
        for m in misiones:
            self.assertIsInstance(m, Actividad)
            self.assertEqual(m.tipo, "Misión")
        for d in desafios:
            self.assertIsInstance(d, Actividad)
            self.assertEqual(d.tipo, "Desafío")

        # Verificar que las recompensas son positivas
        for act in actividades:
            self.assertGreater(act.recompensa, 0,
                               f"La actividad '{act.nombre}' tiene recompensa <= 0")

    def test_economia_pesos_cartas_evento(self):
        """Regla: calcular_pesos_cartas_evento distribuye el 15% proporcionalmente por rareza y rechaza SSR/L."""
        # Caso vacío
        self.assertEqual(calcular_pesos_cartas_evento([]), {})

        # Caso 2 Comunes + 1 Rara → según la fórmula: peso C=2, R=1; total_rel = 5
        # C1: 15*(2/5) = 6.0, C2: 15*(2/5) = 6.0, R: 15*(1/5) = 3.0
        comun1 = PlantillaCriatura(
            codigo="TC01", nombre="TestComun1", rareza="Comun", tipo="Prueba",
            vida=10, ataque=1, defensa=1, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        comun2 = PlantillaCriatura(
            codigo="TC02", nombre="TestComun2", rareza="Comun", tipo="Prueba",
            vida=10, ataque=1, defensa=1, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        rara1 = PlantillaCriatura(
            codigo="TR01", nombre="TestRara1", rareza="Rara", tipo="Prueba",
            vida=20, ataque=5, defensa=3, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        pesos = calcular_pesos_cartas_evento([comun1, comun2, rara1])
        self.assertAlmostEqual(pesos["TC01"], 6.0, places=1)
        self.assertAlmostEqual(pesos["TC02"], 6.0, places=1)
        self.assertAlmostEqual(pesos["TR01"], 3.0, places=1)
        self.assertAlmostEqual(sum(pesos.values()), 15.0, places=1)

        # Regla: El sobre de evento no maneja cartas SSR o Legendarias
        ssr1 = PlantillaCriatura(
            codigo="TSSR", nombre="TestSSR", rareza="Super Super Rara", tipo="Prueba",
            vida=30, ataque=10, defensa=8, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        leg1 = PlantillaCriatura(
            codigo="TLEG", nombre="TestLeg", rareza="Legendaria", tipo="Prueba",
            vida=50, ataque=20, defensa=15, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        with self.assertRaises(ValueError):
            calcular_pesos_cartas_evento([comun1, ssr1])
        with self.assertRaises(ValueError):
            calcular_pesos_cartas_evento([comun1, leg1])

    def test_economia_nombres_oficiales_evento_y_monedas(self):
        """Regla: Moneda común es Aureos, moneda evento es Jacks, sobre y evento son Noche Eterna."""
        # Verificación de nombres y constantes oficiales
        self.assertEqual(NOMBRE_MONEDA_COMUN, "Aureos")
        self.assertEqual(NOMBRE_MONEDA_EVENTO, "Jacks")
        self.assertEqual(NOMBRE_SOBRE_EVENTO, "Noche Eterna")
        self.assertEqual(NOMBRE_EVENTO_VIGENTE, "Noche Eterna")

        self.assertEqual(MONEDA_COMUN.nombre, "Aureos")
        self.assertEqual(MONEDA_EVENTO.nombre, "Jacks")
        self.assertEqual(MONEDA_EVENTO.evento, "Noche Eterna")

        # Sobre de evento por defecto: nombre 'Noche Eterna', moneda 'Jacks', precio 20 Jacks, 3 cartas
        sobre_evento = crear_sobre_evento()
        self.assertEqual(sobre_evento.nombre, "Noche Eterna")
        self.assertEqual(sobre_evento.moneda.nombre, "Jacks")
        self.assertEqual(sobre_evento.precio, 20)
        self.assertEqual(sobre_evento.cantidad_cartas, 3)

        # El sobre de evento no tiene SSR ni Legendaria en sus probabilidades
        self.assertNotIn("Super Super Rara", sobre_evento.azar_rareza)
        self.assertNotIn("SSR", sobre_evento.azar_rareza)
        self.assertNotIn("Legendaria", sobre_evento.azar_rareza)
        self.assertNotIn("L", sobre_evento.azar_rareza)
        self.assertEqual(sobre_evento.azar_rareza.get("Cartas del evento"), 15.0)

        # Crear sobre de evento con SSR o Legendaria debe fallar
        leg = PlantillaCriatura(
            codigo="TLEG", nombre="TestLeg", rareza="Legendaria", tipo="Prueba",
            vida=50, ataque=20, defensa=15, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        with self.assertRaises(ValueError):
            crear_sobre_evento(cartas_evento=[leg])

        with self.assertRaises(ValueError):
            SobreVariable(
                nombre="Sobre Invalido",
                cantidad_cartas=3,
                precio=20,
                moneda=MONEDA_EVENTO,
                azar_rareza={"Comun": 50, "Super Super Rara": 50},
            )

        # Evento oficial Noche Eterna
        c1 = PlantillaCriatura(
            codigo="TH01", nombre="Jackalope", rareza="Comun", tipo="Híbrido",
            vida=15, ataque=3, defensa=2, habilidad="h", descripcion_habilidad="d", usos_habilidad=1,
        )
        evento_ne = crear_evento_noche_eterna(cartas_evento=[c1])
        self.assertEqual(evento_ne.nombre, "Noche Eterna")
        self.assertEqual(evento_ne.moneda.nombre, "Jacks")
        self.assertEqual(evento_ne.sobre.nombre, "Noche Eterna")
        self.assertEqual(evento_ne.sobre.cantidad_cartas, 3)
        self.assertIn("TH01", evento_ne.pesos_cartas)

    def test_economia_mision_comprar_cartas_mercado(self):
        """Regla: La misión 'Comprar 3 cartas del mercado' se cumple tras 3 compras."""
        mision = next(m for m in crear_misiones() if "3 cartas del mercado" in m.nombre)

        moneda = Moneda("Comun")
        jugador = Jugador(id="jtest", nombre="Tester")
        jugador.billetera.depositar(moneda, 500)
        self.juego.agregar_jugador(jugador)

        # Sin compras, la condición no se cumple
        self.assertFalse(mision.esta_cumplida(jugador, []))

        # Comprar 3 cartas del mercado (CDRA cuesta 25 en el mercado de test)
        for _ in range(3):
            self.juego.comprar_carta("jtest", "CDRA")

        self.assertTrue(mision.esta_cumplida(jugador, []))
        self.assertEqual(jugador.cartas_compradas_mercado, 3)
        self.assertEqual(mision.recompensa, 50)

    def test_economia_misiones_abrir_sobres_intercambio_y_coleccion(self):
        """Las misiones nuevas cuentan sobres, intercambios y cartas en posesión."""
        misiones = {m.nombre: m for m in crear_misiones()}

        abrir_sobres = misiones["Abrir 2 sobres"]
        intercambio = misiones["Completar 1 intercambio"]
        coleccion = misiones["Tener 15 cartas"]

        self.jugador_1._sobres_comprados = {"Sobre común": 2}
        self.assertTrue(abrir_sobres.esta_cumplida(self.jugador_1, []))

        c1 = dragonzuelo.crear_carta()
        c2 = sirena.crear_carta()
        self.juego.cartas[c1.id] = c1
        self.juego.cartas[c2.id] = c2
        self.jugador_1.agregar_carta(c1.id)
        self.jugador_2.agregar_carta(c2.id)
        self.juego.intercambiar("j1", [c1.id], "j2", [c2.id])
        self.assertEqual(self.jugador_1.intercambios_completados, 1)
        self.assertTrue(intercambio.esta_cumplida(self.jugador_1, []))

        for i in range(15):
            carta = dragonzuelo.crear_carta()
            self.juego.cartas[carta.id] = carta
            self.jugador_1.agregar_carta(carta.id)
        self.assertTrue(coleccion.esta_cumplida(self.jugador_1, []))

    def test_economia_mision_conseguir_leviatan(self):
        """Regla: La misión 'Conseguir al Leviatán' se cumple al tener la carta LLEV."""
        mision = next(m for m in crear_misiones() if "Leviatán" in m.nombre)

        jugador = Jugador(id="jlev", nombre="Coleccionista")
        self.juego.agregar_jugador(jugador)

        # Sin la carta del Leviatán, no se cumple
        self.assertFalse(mision.esta_cumplida(jugador, []))

        # Crear carta de Leviatán desde el catálogo
        leviatan = self.catalogo.buscar("LLEV")
        self.assertIsNotNone(leviatan, "La criatura LLEV (Leviatán) debe existir en el catálogo")
        carta_lev = leviatan.crear_carta(juego=self.juego)
        self.juego.cartas[carta_lev.id] = carta_lev
        jugador.agregar_carta(carta_lev.id)

        cartas_jugador = [self.juego.cartas[cid] for cid in jugador.cartas if cid in self.juego.cartas]
        self.assertTrue(mision.esta_cumplida(jugador, cartas_jugador))

    def test_economia_desafio_victorias_consecutivas(self):
        """Regla: El desafío 'Ganar 3 combates consecutivos' requiere 3 victorias seguidas."""
        desafio_3 = next(d for d in crear_desafios() if "3 combates consecutivos" in d.nombre)

        jugador = Jugador(id="jvic", nombre="Luchador")
        self.juego.agregar_jugador(jugador)

        # Sin victorias, no se cumple
        self.assertFalse(desafio_3.esta_cumplida(jugador, []))

        # Registrar 2 victorias → todavía no
        self.juego.registrar_victoria("jvic", date(2026, 11, 15))
        self.juego.registrar_victoria("jvic", date(2026, 11, 15))
        self.assertFalse(desafio_3.esta_cumplida(jugador, []))

        # Registrar la 3ª victoria → se cumple
        self.juego.registrar_victoria("jvic", date(2026, 11, 15))
        self.assertTrue(desafio_3.esta_cumplida(jugador, []))
        self.assertEqual(jugador.victorias_consecutivas, 3)

    def test_economia_registrar_derrota_reinicia_consecutivas(self):
        """Regla: Registrar una derrota reinicia el contador de victorias consecutivas a cero."""
        jugador = Jugador(id="jder", nombre="Aspirante")
        self.juego.agregar_jugador(jugador)

        self.juego.registrar_victoria("jder", date(2026, 11, 15))
        self.juego.registrar_victoria("jder", date(2026, 11, 15))
        self.assertEqual(jugador.victorias_consecutivas, 2)

        # Registrar derrota → se reinicia
        self.juego.registrar_derrota("jder")
        self.assertEqual(jugador.victorias_consecutivas, 0)

        # Una nueva victoria empieza desde 1
        self.juego.registrar_victoria("jder", date(2026, 11, 15))
        self.assertEqual(jugador.victorias_consecutivas, 1)

    def test_sobre_evento_probabilidades_y_cartas_exclusivas(self):
        """Regla: Sobre de evento tiene 40% Comun, 30% Rara, 15% Super Rara, 15% Cartas de evento.
        Sin SSR ni Legendarias. Las 3 exclusivas son Chupacabritas (Comun), Espíritu oscuro (Comun)
        y Wendigo (Rara), con pesos proporcionales (6%, 6%, 3%).
        """
        sobre = crear_sobre_evento()
        self.assertEqual(sobre.azar_rareza.get("Comun"), 40.0)
        self.assertEqual(sobre.azar_rareza.get("Rara"), 30.0)
        self.assertEqual(sobre.azar_rareza.get("Super Rara"), 15.0)
        self.assertEqual(sobre.azar_rareza.get("Cartas del evento"), 15.0)
        self.assertNotIn("SSR", sobre.azar_rareza)
        self.assertNotIn("Super Super Rara", sobre.azar_rareza)
        self.assertNotIn("Legendaria", sobre.azar_rareza)

        # Pesos oficiales del evento Noche Eterna
        evento = crear_evento_noche_eterna()
        self.assertEqual(evento.pesos_cartas.get("CCHU"), 6.0)
        self.assertEqual(evento.pesos_cartas.get("CESO"), 6.0)
        self.assertEqual(evento.pesos_cartas.get("RWEN"), 3.0)
        self.assertEqual(sum(evento.pesos_cartas.values()), 15.0)

    def test_cartas_exclusivas_no_obtenibles_en_sobres_regulares(self):
        """Regla: Chupacabritas, Espíritu oscuro y Wendigo no se pueden conseguir en ningún sobre regular."""
        sobres_regulares = crear_sobres_estandar()
        catalogo = crear_catalogo_completo()

        # Abrir repetidamente sobres comunes y especiales: nunca debe salir CCHU, CESO ni RWEN
        for sobre in sobres_regulares:
            cartas = sobre.abrir(catalogo=catalogo)
            for carta in cartas:
                self.assertNotIn(
                    carta.plantilla.codigo,
                    CODIGOS_CARTAS_EVENTO_EXCLUSIVAS,
                    f"La carta exclusiva {carta.plantilla.nombre} ({carta.plantilla.codigo}) apareció en {sobre.nombre}."
                )

    def test_mercado_ofertas_oficiales_25_cartas(self):
        """Regla: El mercado ofrece exactamente 25 cartas oficiales (15 Comunes, 7 Raras, 3 Super Raras)."""
        mercado = crear_mercado_estandar()
        self.assertEqual(len(mercado.ofertas), 25)
        # Diablo de Jersey aparece en el mercado (Rara)
        self.assertIn("RDJE", mercado.ofertas)
        self.assertEqual(mercado.ofertas["RDJE"], PRECIO_CARTA_RARA)
        # Las 3 exclusivas del evento no están en ofertas directas del mercado
        self.assertNotIn("RWEN", mercado.ofertas)
        self.assertNotIn("CCHU", mercado.ofertas)
        self.assertNotIn("CESO", mercado.ofertas)


if __name__ == "__main__":
    unittest.main()
