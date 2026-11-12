import sys
from datetime import date
from pathlib import Path
import unittest

root_dir = Path(__file__).resolve().parent.parent
codigo_dir = root_dir / "Código del mercado de cartas"
if str(codigo_dir) not in sys.path:
    sys.path.insert(0, str(codigo_dir))

from principales import (
    Actividad,
    Carta,
    Desafio,
    Evento,
    Mision,
    Moneda,
    PlantillaCriatura,
    SobreEstable,
    SobreVariable,
    TipoSobre,
)
from catalogo import Catalogo, Mercado
from jugador import Billetera, Jugador
from juego import Juego
from criaturas import (
    CRIATURAS,
    PLANTILLAS_CRIATURAS,
    crear_catalogo_completo,
    dragonzuelo,
    apep,
    sirena,
)


class TestMercadoCartasUML(unittest.TestCase):
    def setUp(self):
        Carta.limpiar_registro()
        dragonzuelo.contador = 0
        sirena.contador = 0
        apep.contador = 0

        self.moneda_comun = Moneda("Común")
        self.moneda_evento = Moneda("Evento Lunar", "Festival de Luna")

        self.catalogo = crear_catalogo_completo()

        self.sobre_estable = SobreEstable(
            nombre="Sobre Clásico",
            cantidad_cartas=2,
            precio=50,
            moneda=self.moneda_comun,
            azar_rareza={"Común": 80, "Rara": 20},
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
        self.assertEqual(dragonzuelo.rareza, "Común")
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

    def test_comprar_sobre_y_carta(self):
        """Regla: Al comprar un sobre o carta se descuenta la moneda y se asignan las cartas."""
        self.jugador_1.billetera.depositar(self.moneda_comun, 200)

        cartas = self.juego.comprar_sobre(
            "j1", self.sobre_estable, date(2026, 11, 15)
        )
        self.assertEqual(len(cartas), 2)
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 150)
        self.assertEqual(len(self.jugador_1.cartas), 2)

        cid = self.juego.comprar_carta("j1", "CDRA")
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 125)
        self.assertIn(cid, self.jugador_1.cartas)

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

    def test_convertir_moneda_vigencia_evento(self):
        """Regla: Solo se puede convertir moneda si hay un evento vigente."""
        self.jugador_1.billetera.depositar(self.moneda_comun, 20)

        # Conversión exitosa durante evento (tasa_cambio = 5)
        self.juego.convertir_moneda("j1", 10, date(2026, 11, 15))
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_comun), 10)
        self.assertEqual(self.jugador_1.billetera.saldo(self.moneda_evento), 50)

        # Fuera de evento falla
        with self.assertRaises(ValueError):
            self.juego.convertir_moneda("j1", 10, date(2026, 12, 1))

    def test_actividad_mision_recompensa_unica(self):
        """Regla: Una actividad solo se recompensa si se cumple y no puede cobrarse dos veces."""
        mision = Mision(
            nombre="Tener Dragón",
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

        comunes = self.catalogo.de_rareza("Común")
        self.assertGreaterEqual(len(comunes), 1)
        self.assertIn(dragonzuelo, comunes)


if __name__ == "__main__":
    unittest.main()
