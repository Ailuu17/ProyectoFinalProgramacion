"""Definición de todas las plantillas de criaturas mitológicas del juego."""
from __future__ import annotations

from typing import Dict, List
try:
    from .principales import PlantillaCriatura
    from .catalogo import Catalogo
except (ImportError, ValueError):
    from principales import PlantillaCriatura
    from catalogo import Catalogo

dragonzuelo = PlantillaCriatura(
    codigo="CDRA",
    nombre="Dragonzuelo",
    rareza="Común",
    tipo="Dragónico",
    vida=50,
    ataque=12,
    defensa=7,
    habilidad="escupir fuego",
    descripcion_habilidad="ataque x2 sobre un enemigo",
    usos_habilidad=1,
)

hidra_bebe = PlantillaCriatura(
    codigo="CHDR",
    nombre="Hidra bebé",
    rareza="Común",
    tipo="Dragónico",
    vida=60,
    ataque=12,
    defensa=7,
    habilidad="veneno",
    descripcion_habilidad="le quita 1 de vida a un enemigo por 3 ataques",
    usos_habilidad=1,
)

cocatricito = PlantillaCriatura(
    codigo="CCOC",
    nombre="Cocatricito",
    rareza="Común",
    tipo="Dragónico",
    vida=50,
    ataque=10,
    defensa=7,
    habilidad="ataque de gallo",
    descripcion_habilidad="ataque x2 sobre un enemigo",
    usos_habilidad=1,
)

sirena = PlantillaCriatura(
    codigo="CSIR",
    nombre="Sirena",
    rareza="Común",
    tipo="Marino",
    vida=65,
    ataque=11,
    defensa=9,
    habilidad="ola arrasadora",
    descripcion_habilidad="ataque x2 sobre un enemigo",
    usos_habilidad=1,
)

sirena_del_pacifico = PlantillaCriatura(
    codigo="CSPA",
    nombre="Sirena del pacífico",
    rareza="Común",
    tipo="Marino",
    vida=65,
    ataque=11,
    defensa=9,
    habilidad="ola arrasadora",
    descripcion_habilidad="ataque x2 sobre un enemigo",
    usos_habilidad=1,
)

sirena_de_coral = PlantillaCriatura(
    codigo="CSCO",
    nombre="Sirena de coral",
    rareza="Común",
    tipo="Marino",
    vida=65,
    ataque=11,
    defensa=9,
    habilidad="ola arrasadora",
    descripcion_habilidad="ataque x2 sobre un enemigo",
    usos_habilidad=1,
)

sirena_curiosa = PlantillaCriatura(
    codigo="CSCU",
    nombre="Sirena curiosa",
    rareza="Común",
    tipo="Marino",
    vida=65,
    ataque=11,
    defensa=9,
    habilidad="ola arrasadora",
    descripcion_habilidad="ataque x2 sobre un enemigo",
    usos_habilidad=1,
)

nixie = PlantillaCriatura(
    codigo="CNIX",
    nombre="Nixie",
    rareza="Común",
    tipo="Marino",
    vida=65,
    ataque=9,
    defensa=14,
    habilidad="aguas sucias",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

triton_aprendiz = PlantillaCriatura(
    codigo="CTAP",
    nombre="Tritón aprendiz",
    rareza="Común",
    tipo="Marino",
    vida=70,
    ataque=11,
    defensa=7,
    habilidad="ataque marino",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

angel_mensajero = PlantillaCriatura(
    codigo="CAME",
    nombre="Ángel mensajero",
    rareza="Común",
    tipo="Celestial",
    vida=75,
    ataque=5,
    defensa=14,
    habilidad="mensaje divino",
    descripcion_habilidad="cura 20 de vida a un aliado",
    usos_habilidad=1,
)

angel_compasivo = PlantillaCriatura(
    codigo="CACO",
    nombre="Ángel compasivo",
    rareza="Común",
    tipo="Celestial",
    vida=75,
    ataque=5,
    defensa=14,
    habilidad="sanado celestial",
    descripcion_habilidad="cura 10 de vida a dos aliados",
    usos_habilidad=1,
)

angel_guardian = PlantillaCriatura(
    codigo="CAGU",
    nombre="Ángel guardián",
    rareza="Común",
    tipo="Celestial",
    vida=80,
    ataque=9,
    defensa=15,
    habilidad="defensa divina",
    descripcion_habilidad="desde el inicio se puede sacrificar para recibir el siguiente ataque que elimine a un aliado que tenga 10 de vida",
    usos_habilidad=1,
)

angel_justiciero = PlantillaCriatura(
    codigo="CAJU",
    nombre="Ángel justiciero",
    rareza="Común",
    tipo="Celestial",
    vida=75,
    ataque=6,
    defensa=12,
    habilidad="vida justa",
    descripcion_habilidad="reparte los puntos de vida de todos los aliados por igual",
    usos_habilidad=1,
)

angel_servicial = PlantillaCriatura(
    codigo="CASE",
    nombre="Ángel servicial",
    rareza="Común",
    tipo="Celestial",
    vida=70,
    ataque=5,
    defensa=15,
    habilidad="adorador",
    descripcion_habilidad="impulsa el ataque de un aliado x1.25 en el siguiente ataque",
    usos_habilidad=1,
)

oni_travieso = PlantillaCriatura(
    codigo="COTR",
    nombre="Oni travieso",
    rareza="Común",
    tipo="Infernal",
    vida=75,
    ataque=8,
    defensa=11,
    habilidad="caos menor",
    descripcion_habilidad="baja 2 de las defensas de los enemigos",
    usos_habilidad=1,
)

oni_castigador = PlantillaCriatura(
    codigo="COCA",
    nombre="Oni castigador",
    rareza="Común",
    tipo="Infernal",
    vida=75,
    ataque=5,
    defensa=14,
    habilidad="mazo de hierro",
    descripcion_habilidad="reduce 20 de vida de un enemigo",
    usos_habilidad=1,
)

diablillo = PlantillaCriatura(
    codigo="CDIA",
    nombre="Diablillo",
    rareza="Común",
    tipo="Infernal",
    vida=60,
    ataque=11,
    defensa=9,
    habilidad="pequeña travesura",
    descripcion_habilidad="reduce 2 de ataque de un enemigo",
    usos_habilidad=1,
)

demonio_solitario = PlantillaCriatura(
    codigo="CDSO",
    nombre="Demonio solitario",
    rareza="Común",
    tipo="Infernal",
    vida=65,
    ataque=12,
    defensa=10,
    habilidad="soledad roja",
    descripcion_habilidad="un enemigo al azar no puede participar del siguiente ataque",
    usos_habilidad=1,
)

demonio_infeliz = PlantillaCriatura(
    codigo="CDIN",
    nombre="Demonio infeliz",
    rareza="Común",
    tipo="Infernal",
    vida=60,
    ataque=5,
    defensa=10,
    habilidad="queja constante",
    descripcion_habilidad="reduce 3 de defensa de un enemigo",
    usos_habilidad=1,
)

pichon_de_fenix = PlantillaCriatura(
    codigo="CPFE",
    nombre="Pichón de Fénix",
    rareza="Común",
    tipo="Ave mística",
    vida=70,
    ataque=12,
    defensa=7,
    habilidad="llamarada",
    descripcion_habilidad="ataca a dos enemigos x0.5",
    usos_habilidad=1,
)

hada_del_bosque = PlantillaCriatura(
    codigo="CHBO",
    nombre="Hada del bosque",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=14,
    habilidad="cura natural",
    descripcion_habilidad="cura 15 de vida a un aliado",
    usos_habilidad=1,
)

hada_de_los_insectos = PlantillaCriatura(
    codigo="CHIN",
    nombre="Hada de los insectos",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=10,
    defensa=10,
    habilidad="ataque insecto",
    descripcion_habilidad="ataque x1.5 a un enemigo",
    usos_habilidad=1,
)

hada_artesana = PlantillaCriatura(
    codigo="CHAR",
    nombre="Hada artesana",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=7,
    defensa=13,
    habilidad="ataque artesanal",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

hada_del_agua = PlantillaCriatura(
    codigo="CHAG",
    nombre="Hada del agua",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=9,
    defensa=10,
    habilidad="torrencial",
    descripcion_habilidad="baja 3 de defensa de un enemigo",
    usos_habilidad=1,
)

hada_de_la_nieve = PlantillaCriatura(
    codigo="CHNI",
    nombre="Hada de la nieve",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=9,
    defensa=10,
    habilidad="nevada",
    descripcion_habilidad="baja 3 puntos de las defensas de un enemigo",
    usos_habilidad=1,
)

hada_sanadora = PlantillaCriatura(
    codigo="CHSA",
    nombre="Hada sanadora",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=14,
    habilidad="polvillo mágico",
    descripcion_habilidad="cura 15 de vida a un aliado",
    usos_habilidad=1,
)

hada_de_la_musica = PlantillaCriatura(
    codigo="CHMU",
    nombre="Hada de la música",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=7,
    defensa=13,
    habilidad="canción de cuna",
    descripcion_habilidad="un enemigo al azar no puede participar del siguiente ataque",
    usos_habilidad=1,
)

hada_bibliotecaria = PlantillaCriatura(
    codigo="CHBI",
    nombre="Hada bibliotecaria",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=12,
    defensa=14,
    habilidad="conocimiento antiguo",
    descripcion_habilidad="elimina 20 de vida de un enemigo",
    usos_habilidad=1,
)

flash_pixie = PlantillaCriatura(
    codigo="CFLA",
    nombre="Flash (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=50,
    ataque=10,
    defensa=15,
    habilidad="trunca reloj",
    descripcion_habilidad="un aliado recupera la posibilidad de participar en un combate tras haber sido revocada por un ataque",
    usos_habilidad=1,
)

amore_pixie = PlantillaCriatura(
    codigo="CAMO",
    nombre="Amore (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=55,
    ataque=7,
    defensa=13,
    habilidad="enamoramiento",
    descripcion_habilidad="un enemigo específico no puede atacarla por el resto del combate",
    usos_habilidad=1,
)

loquace_pixie = PlantillaCriatura(
    codigo="CLOQ",
    nombre="Loquace (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=50,
    ataque=7,
    defensa=12,
    habilidad="aturdimiento",
    descripcion_habilidad="un enemigo al azar no puede participar del siguiente ataque",
    usos_habilidad=1,
)

vita_pixie = PlantillaCriatura(
    codigo="CVIT",
    nombre="Vita (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=13,
    habilidad="entrega vida",
    descripcion_habilidad="entrega 20 de vida a un aliado",
    usos_habilidad=1,
)

sonno_pixie = PlantillaCriatura(
    codigo="CSON",
    nombre="Sonno (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=50,
    ataque=5,
    defensa=10,
    habilidad="sueño",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

colpo_pixie = PlantillaCriatura(
    codigo="CCOL",
    nombre="Colpo (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=5,
    defensa=15,
    habilidad="fuerza de ataque",
    descripcion_habilidad="impulsa el ataque de un aliado x1.25 en el siguiente ataque",
    usos_habilidad=1,
)

ombra_pixie = PlantillaCriatura(
    codigo="COMB",
    nombre="Ombra (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=10,
    habilidad="sombra",
    descripcion_habilidad="pierde 10 de vida y un enemigo al azar no puede participar del siguiente ataque",
    usos_habilidad=1,
)

fulmine_pixie = PlantillaCriatura(
    codigo="CFUL",
    nombre="Fulmine (Pixie)",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=10,
    habilidad="reanimación",
    descripcion_habilidad="pierde 10 de vida y un aliado recupera la posibilidad de participar en un combate tras haber sido revocada por un ataque",
    usos_habilidad=1,
)

duendecillo = PlantillaCriatura(
    codigo="CDUE",
    nombre="Duendecillo",
    rareza="Común",
    tipo="Feérico",
    vida=60,
    ataque=9,
    defensa=13,
    habilidad="eliminar molestias",
    descripcion_habilidad="elimina al enemigo con menos vida si hay enemigos con 10 o menos de vida",
    usos_habilidad=1,
)

trasgos_duende = PlantillaCriatura(
    codigo="CTRA",
    nombre="Trasgos (Duende)",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=5,
    defensa=14,
    habilidad="bromita",
    descripcion_habilidad="reduce 3 de defensa de un enemigo al azar por el siguiente ataque",
    usos_habilidad=1,
)

domovoi_duende = PlantillaCriatura(
    codigo="CDOM",
    nombre="Domovoi (Duende)",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=10,
    defensa=8,
    habilidad="protector del hogar",
    descripcion_habilidad="recibe el próximo ataque",
    usos_habilidad=1,
)

musgoso_duende = PlantillaCriatura(
    codigo="CMUS",
    nombre="Musgoso (Duende)",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=7,
    defensa=12,
    habilidad="ayuda musgosa",
    descripcion_habilidad="le entrega 2 de ataque o defensa a un aliado y se elimina de la combate",
    usos_habilidad=1,
)

brownie_duende = PlantillaCriatura(
    codigo="CBRO",
    nombre="Brownie (Duende)",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=5,
    defensa=13,
    habilidad="cuidado peludo",
    descripcion_habilidad="entrega 5 de vida y 2 de defensa a un aliado y se elimina de la combate",
    usos_habilidad=1,
)

boggart_duende = PlantillaCriatura(
    codigo="CBOG",
    nombre="Boggart (Duende)",
    rareza="Común",
    tipo="Feérico",
    vida=60,
    ataque=8,
    defensa=14,
    habilidad="bromita",
    descripcion_habilidad="reduce 3 de defensa de un enemigo al azar por el siguiente ataque",
    usos_habilidad=1,
)

nayades_ninfa = PlantillaCriatura(
    codigo="CNAY",
    nombre="Náyades (Ninfa)",
    rareza="Común",
    tipo="Feérico",
    vida=80,
    ataque=7,
    defensa=15,
    habilidad="agua pura",
    descripcion_habilidad="cura 20 de vida a un aliado",
    usos_habilidad=1,
)

napea_ninfa = PlantillaCriatura(
    codigo="CNAP",
    nombre="Napea (Ninfa)",
    rareza="Común",
    tipo="Feérico",
    vida=80,
    ataque=7,
    defensa=15,
    habilidad="tierra firme",
    descripcion_habilidad="otorga 2 de defensa a un aliado",
    usos_habilidad=1,
)

aurai_ninfa = PlantillaCriatura(
    codigo="CAUR",
    nombre="Aurai (Ninfa)",
    rareza="Común",
    tipo="Feérico",
    vida=80,
    ataque=7,
    defensa=15,
    habilidad="vientos fuertes",
    descripcion_habilidad="reduce 3 de defensa de un enemigo",
    usos_habilidad=1,
)

troll_de_montana = PlantillaCriatura(
    codigo="CTMO",
    nombre="Troll de montaña",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=15,
    habilidad="roca de troll",
    descripcion_habilidad="su defensa se duplica por el siguiente ataque",
    usos_habilidad=1,
)

troll_de_caverna = PlantillaCriatura(
    codigo="CTCA",
    nombre="Troll de caverna",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=15,
    habilidad="ataque sigiloso",
    descripcion_habilidad="ataca a un enemigo x1.5",
    usos_habilidad=1,
)

troll_de_las_nieves = PlantillaCriatura(
    codigo="CTNI",
    nombre="Troll de las nieves",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=5,
    defensa=15,
    habilidad="bolas de nieve",
    descripcion_habilidad="ataca a un enemigo x1.5",
    usos_habilidad=1,
)

elfo_de_la_luz = PlantillaCriatura(
    codigo="CELU",
    nombre="Elfo de la luz",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=5,
    defensa=15,
    habilidad="bondad luminosa",
    descripcion_habilidad="entrega 15 de vida a un aliado",
    usos_habilidad=1,
)

elfo_de_la_oscuridad = PlantillaCriatura(
    codigo="CEOS",
    nombre="Elfo de la oscuridad",
    rareza="Común",
    tipo="Feérico",
    vida=70,
    ataque=5,
    defensa=15,
    habilidad="ataque artesanal",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

elfo_del_bosque = PlantillaCriatura(
    codigo="CEBO",
    nombre="Elfo del bosque",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=12,
    defensa=10,
    habilidad="tiro certero",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

elfa_arquera = PlantillaCriatura(
    codigo="CEAR",
    nombre="Elfa arquera",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=12,
    defensa=10,
    habilidad="tiro certero",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

golem_de_piedra = PlantillaCriatura(
    codigo="CGPI",
    nombre="Golem de piedra",
    rareza="Común",
    tipo="Gigante",
    vida=80,
    ataque=5,
    defensa=15,
    habilidad="dureza de golem",
    descripcion_habilidad="defensa x2 en el siguiente ataque",
    usos_habilidad=1,
)

titan_nino = PlantillaCriatura(
    codigo="CTIN",
    nombre="Titán niño",
    rareza="Común",
    tipo="Gigante",
    vida=70,
    ataque=10,
    defensa=11,
    habilidad="gran ataque",
    descripcion_habilidad="ataca a un enemigo x1.5",
    usos_habilidad=1,
)

pequeno_ciclope = PlantillaCriatura(
    codigo="CPCI",
    nombre="Pequeño cíclope",
    rareza="Común",
    tipo="Gigante",
    vida=50,
    ataque=6,
    defensa=9,
    habilidad="doble ataque",
    descripcion_habilidad="ataca a dos enemigos a la vez",
    usos_habilidad=1,
)

nino_fauno = PlantillaCriatura(
    codigo="CNFA",
    nombre="Niño fauno",
    rareza="Común",
    tipo="Híbrido",
    vida=60,
    ataque=8,
    defensa=9,
    habilidad="lástima",
    descripcion_habilidad="no recibe el próximo ataque dirigido a él",
    usos_habilidad=1,
)

esfinge_cachorro = PlantillaCriatura(
    codigo="CECA",
    nombre="Esfinge cachorro",
    rareza="Común",
    tipo="Híbrido",
    vida=70,
    ataque=11,
    defensa=9,
    habilidad="zarpazo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

grifo_cachorro = PlantillaCriatura(
    codigo="CGCA",
    nombre="Grifo cachorro",
    rareza="Común",
    tipo="Híbrido",
    vida=70,
    ataque=12,
    defensa=8,
    habilidad="picotazo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

hipogrifo_cachorro = PlantillaCriatura(
    codigo="CHCA",
    nombre="Hipogrifo cachorro",
    rareza="Común",
    tipo="Híbrido",
    vida=70,
    ataque=12,
    defensa=8,
    habilidad="picotazo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

nino_centauro = PlantillaCriatura(
    codigo="CNCE",
    nombre="Niño centauro",
    rareza="Común",
    tipo="Híbrido",
    vida=70,
    ataque=10,
    defensa=9,
    habilidad="enojo",
    descripcion_habilidad="suma 2 de ataque en su próximo ataque",
    usos_habilidad=1,
)

espiritu_del_bosque = PlantillaCriatura(
    codigo="CESB",
    nombre="Espíritu del bosque",
    rareza="Común",
    tipo="Espíritu",
    vida=60,
    ataque=7,
    defensa=13,
    habilidad="ataque espiritual",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

espiritu_errante = PlantillaCriatura(
    codigo="CESE",
    nombre="Espíritu errante",
    rareza="Común",
    tipo="Espíritu",
    vida=60,
    ataque=5,
    defensa=13,
    habilidad="confusión",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

espiritu_dolido = PlantillaCriatura(
    codigo="CESD",
    nombre="Espíritu dolido",
    rareza="Común",
    tipo="Espíritu",
    vida=60,
    ataque=9,
    defensa=10,
    habilidad="sufre",
    descripcion_habilidad="ataque x2 a un enemigo al azar",
    usos_habilidad=1,
)

espiritu_oscuro = PlantillaCriatura(
    codigo="CESO",
    nombre="Espíritu oscuro",
    rareza="Común",
    tipo="Espíritu",
    vida=60,
    ataque=7,
    defensa=11,
    habilidad="penumbras",
    descripcion_habilidad="reduce 2 de la defensa de un enemigo",
    usos_habilidad=1,
)

kitsune_joven = PlantillaCriatura(
    codigo="CKIJ",
    nombre="Kitsune Joven",
    rareza="Común",
    tipo="Espíritu",
    vida=75,
    ataque=12,
    defensa=12,
    habilidad="garras afiladas",
    descripcion_habilidad="ataque x1.5 a un enemigo",
    usos_habilidad=1,
)

bakenko = PlantillaCriatura(
    codigo="CBAK",
    nombre="Bakenko",
    rareza="Común",
    tipo="Espíritu",
    vida=65,
    ataque=14,
    defensa=10,
    habilidad="bolas de fuego",
    descripcion_habilidad="hiere a todos los enemigos por un x0.25",
    usos_habilidad=1,
)

duendes_de_hollin = PlantillaCriatura(
    codigo="CDHO",
    nombre="Duendes de hollín",
    rareza="Común",
    tipo="Espíritu",
    vida=55,
    ataque=5,
    defensa=15,
    habilidad="polvo",
    descripcion_habilidad="uno de los enemigos no puede participar en el siguiente ataque",
    usos_habilidad=1,
)

bebe_yeti = PlantillaCriatura(
    codigo="CBYE",
    nombre="Bebé Yeti",
    rareza="Común",
    tipo="Bestia",
    vida=70,
    ataque=9,
    defensa=10,
    habilidad="bolas de nieve",
    descripcion_habilidad="ataca a un enemigo x1.5",
    usos_habilidad=1,
)

chupacabritas = PlantillaCriatura(
    codigo="CCHU",
    nombre="Chupacabritas",
    rareza="Común",
    tipo="Bestia",
    vida=55,
    ataque=12,
    defensa=10,
    habilidad="chupa vida",
    descripcion_habilidad="adquiere 10 de vida de un enemigo",
    usos_habilidad=1,
)

mooncalf = PlantillaCriatura(
    codigo="CMOO",
    nombre="Mooncalf",
    rareza="Común",
    tipo="Bestia",
    vida=75,
    ataque=5,
    defensa=13,
    habilidad="sacrificio tierno",
    descripcion_habilidad="entrega 20 de vida a un aliado",
    usos_habilidad=1,
)

kobold = PlantillaCriatura(
    codigo="CKOB",
    nombre="Kobold",
    rareza="Común",
    tipo="Feérico",
    vida=60,
    ataque=9,
    defensa=12,
    habilidad="Golpe Minero",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

alux = PlantillaCriatura(
    codigo="CALU",
    nombre="Alux",
    rareza="Común",
    tipo="Espíritu",
    vida=65,
    ataque=7,
    defensa=13,
    habilidad="Travesura mágica",
    descripcion_habilidad="reduce 3 de defensa de un enemigo durante 1 ataque",
    usos_habilidad=1,
)

cheneque = PlantillaCriatura(
    codigo="CCHE",
    nombre="Cheneque",
    rareza="Común",
    tipo="Espíritu",
    vida=65,
    ataque=8,
    defensa=12,
    habilidad="extraviar",
    descripcion_habilidad="un enemigo no puede participar del próximo ataque",
    usos_habilidad=1,
)

nisse = PlantillaCriatura(
    codigo="CNIS",
    nombre="Nisse",
    rareza="Común",
    tipo="Espíritu",
    vida=70,
    ataque=6,
    defensa=14,
    habilidad="protección del hogar",
    descripcion_habilidad="aumenta 5 de defensa a un aliado durante 1 ataque",
    usos_habilidad=1,
)

leprechaun = PlantillaCriatura(
    codigo="CLEP",
    nombre="Leprechaun",
    rareza="Común",
    tipo="Feérica",
    vida=60,
    ataque=8,
    defensa=12,
    habilidad="suerte irlandesa",
    descripcion_habilidad="esquiva el próximo ataque",
    usos_habilidad=1,
)

puckwudgie = PlantillaCriatura(
    codigo="CPUC",
    nombre="Puckwudgie",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=11,
    defensa=9,
    habilidad="espinas mágicas",
    descripcion_habilidad="suma 4 de ataque para herir a un enemigo y luego vuelve a 11 de ataque",
    usos_habilidad=1,
)

pixiu = PlantillaCriatura(
    codigo="CPIX",
    nombre="Pixiu",
    rareza="Común",
    tipo="Híbrido",
    vida=75,
    ataque=12,
    defensa=12,
    habilidad="guardián de tesoros",
    descripcion_habilidad="aumenta su defensa en 5 durante 1 ataques",
    usos_habilidad=1,
)

kodama = PlantillaCriatura(
    codigo="CKOD",
    nombre="Kodama",
    rareza="Común",
    tipo="Espírito",
    vida=70,
    ataque=5,
    defensa=14,
    habilidad="espíritu del árbol",
    descripcion_habilidad="cura 15 de vida a un aliado",
    usos_habilidad=1,
)

imp = PlantillaCriatura(
    codigo="CIMP",
    nombre="Imp",
    rareza="Común",
    tipo="Infernal",
    vida=55,
    ataque=11,
    defensa=8,
    habilidad="maldad menor",
    descripcion_habilidad="reduce 3 puntos de ataque a un enemigo durante 1 ataque",
    usos_habilidad=1,
)

baku_pequeno = PlantillaCriatura(
    codigo="CBPE",
    nombre="Baku pequeño",
    rareza="Común",
    tipo="Infernal",
    vida=65,
    ataque=7,
    defensa=12,
    habilidad="devorador de sueños",
    descripcion_habilidad="un enemigo no puede participar del próximo ataque",
    usos_habilidad=1,
)

carbunclo = PlantillaCriatura(
    codigo="CCAR",
    nombre="Carbunclo",
    rareza="Común",
    tipo="Feérico",
    vida=65,
    ataque=8,
    defensa=13,
    habilidad="luz brillante",
    descripcion_habilidad="cura 10 de vida a un aliado",
    usos_habilidad=1,
)

tatzelwurm_pequeno = PlantillaCriatura(
    codigo="CTPE",
    nombre="Tatzelwurm pequeño",
    rareza="Común",
    tipo="Híbrido",
    vida=70,
    ataque=12,
    defensa=9,
    habilidad="mordida alpina",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

caladrius = PlantillaCriatura(
    codigo="CCAL",
    nombre="Caladrius",
    rareza="Común",
    tipo="Ave mítica",
    vida=70,
    ataque=5,
    defensa=13,
    habilidad="ave sanadora",
    descripcion_habilidad="cura 20 puntos de vida a un aliado",
    usos_habilidad=1,
)

simargl_cachorro = PlantillaCriatura(
    codigo="CSCA",
    nombre="Simargl cachorro",
    rareza="Común",
    tipo="Híbrido",
    vida=75,
    ataque=11,
    defensa=11,
    habilidad="alas protectoras",
    descripcion_habilidad="recibe un ataque dirigido a un aliado",
    usos_habilidad=1,
)

wolpertinger = PlantillaCriatura(
    codigo="CWOL",
    nombre="Wolpertinger",
    rareza="Común",
    tipo="Híbrido",
    vida=60,
    ataque=10,
    defensa=9,
    habilidad="salto salvaje",
    descripcion_habilidad="ataque x1.5 a un enemigo",
    usos_habilidad=1,
)

jackalope = PlantillaCriatura(
    codigo="CJAC",
    nombre="Jackalope",
    rareza="Común",
    tipo="Híbrido",
    vida=55,
    ataque=12,
    defensa=8,
    habilidad="cornada veloz",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

ratatoskr = PlantillaCriatura(
    codigo="CRAT",
    nombre="Ratatoskr",
    rareza="Común",
    tipo="Feérico",
    vida=60,
    ataque=8,
    defensa=11,
    habilidad="mensajero veloz",
    descripcion_habilidad="aumenta x1.25 el próximo ataque de un aliado",
    usos_habilidad=1,
)

fenghuang_polluelo = PlantillaCriatura(
    codigo="CFPO",
    nombre="Fenghuang polluelo",
    rareza="Común",
    tipo="Ave mítica",
    vida=70,
    ataque=10,
    defensa=10,
    habilidad="Plumaje ardiente",
    descripcion_habilidad="ataque x1.5 a un enemigo",
    usos_habilidad=1,
)

qilin_bebe = PlantillaCriatura(
    codigo="CQBE",
    nombre="Qilin bebé",
    rareza="Común",
    tipo="Feérico",
    vida=75,
    ataque=9,
    defensa=13,
    habilidad="bendición sagrada",
    descripcion_habilidad="cura 15 de vida al aliado con menos vida",
    usos_habilidad=1,
)

dragon_de_fuego = PlantillaCriatura(
    codigo="RDFU",
    nombre="Dragón de Fuego",
    rareza="Rara",
    tipo="Dragónico",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="escupir fuego",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

dragon_de_hielo = PlantillaCriatura(
    codigo="RDHI",
    nombre="Dragón de Hielo",
    rareza="Rara",
    tipo="Dragónico",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="escupir hielo",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

dragon_de_trueno = PlantillaCriatura(
    codigo="RDTR",
    nombre="Dragón de Trueno",
    rareza="Rara",
    tipo="Dragónico",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="aturdir",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

trio_dragonico = PlantillaCriatura(
    codigo="RTDR",
    nombre="Trio dragónico",
    rareza="Rara",
    tipo="Dragónico",
    vida=110,
    ataque=20,
    defensa=18,
    habilidad="descontrol",
    descripcion_habilidad="un enemigo no puede participar en el siguiente ataque",
    usos_habilidad=1,
)

cocatrice = PlantillaCriatura(
    codigo="RCOC",
    nombre="Cocatrice",
    rareza="Rara",
    tipo="Dragónico",
    vida=90,
    ataque=20,
    defensa=18,
    habilidad="picotazo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

triton = PlantillaCriatura(
    codigo="RTRI",
    nombre="Tritón",
    rareza="Rara",
    tipo="Marino",
    vida=80,
    ataque=23,
    defensa=15,
    habilidad="fuerza marina",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

triton_de_las_profundidades = PlantillaCriatura(
    codigo="RTPR",
    nombre="Tritón de las profundidades",
    rareza="Rara",
    tipo="Marino",
    vida=85,
    ataque=25,
    defensa=15,
    habilidad="aguas profundas",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

triton_experimentado = PlantillaCriatura(
    codigo="RTEX",
    nombre="Tritón experimentado",
    rareza="Rara",
    tipo="Marino",
    vida=85,
    ataque=22,
    defensa=18,
    habilidad="escudo marino",
    descripcion_habilidad="agrega 10 de defensa para el siguiente ataque que reciba",
    usos_habilidad=1,
)

sirena_de_las_profundidades = PlantillaCriatura(
    codigo="RSPR",
    nombre="Sirena de las profundidades",
    rareza="Rara",
    tipo="Marino",
    vida=85,
    ataque=25,
    defensa=15,
    habilidad="aguas profundas",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

kelpie = PlantillaCriatura(
    codigo="RKEL",
    nombre="Kelpie",
    rareza="Rara",
    tipo="Marino",
    vida=120,
    ataque=15,
    defensa=15,
    habilidad="ahogamiento",
    descripcion_habilidad="se sacrifica para eliminar a un enemigo que tenga 20 o menos de vida",
    usos_habilidad=1,
)

valkiria = PlantillaCriatura(
    codigo="RVAL",
    nombre="Valkiria",
    rareza="Rara",
    tipo="Celestial",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="ataque de guerra",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

arcangel = PlantillaCriatura(
    codigo="RARC",
    nombre="Arcángel",
    rareza="Rara",
    tipo="Celestial",
    vida=120,
    ataque=25,
    defensa=25,
    habilidad="ataque divino",
    descripcion_habilidad="ataque a un enemigo x2",
    usos_habilidad=1,
)

oni_superior = PlantillaCriatura(
    codigo="ROSU",
    nombre="Oni superior",
    rareza="Rara",
    tipo="Infernal",
    vida=100,
    ataque=17,
    defensa=17,
    habilidad="dureza",
    descripcion_habilidad="por los primeros 3 ataques tiene 5 de defensa más",
    usos_habilidad=1,
)

diablo_de_jersey = PlantillaCriatura(
    codigo="RDJE",
    nombre="Diablo de Jersey",
    rareza="Rara",
    tipo="Infernal",
    vida=80,
    ataque=20,
    defensa=20,
    habilidad="ataque del infierno",
    descripcion_habilidad="ataque x1.5 a un enemigo",
    usos_habilidad=1,
)

cerberucito = PlantillaCriatura(
    codigo="RCER",
    nombre="Cerberucito",
    rareza="Rara",
    tipo="Infernal",
    vida=90,
    ataque=25,
    defensa=15,
    habilidad="mordida",
    descripcion_habilidad="ataque x1.5 a un enemigo",
    usos_habilidad=1,
)

simurgh = PlantillaCriatura(
    codigo="RSIM",
    nombre="Simurgh",
    rareza="Rara",
    tipo="Ave mística",
    vida=85,
    ataque=17,
    defensa=17,
    habilidad="ataque combinado",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

hada_guerrera = PlantillaCriatura(
    codigo="RHGU",
    nombre="Hada guerrera",
    rareza="Rara",
    tipo="Feérico",
    vida=100,
    ataque=22,
    defensa=18,
    habilidad="ataque de guerra",
    descripcion_habilidad="ataque x1.5 a dos enemigos",
    usos_habilidad=1,
)

reina_de_las_pixies = PlantillaCriatura(
    codigo="RRPI",
    nombre="Reina de las pixies",
    rareza="Rara",
    tipo="Feérico",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="liderazgo",
    descripcion_habilidad="entrega 20 de vida, 5 de ataque y 2 de defensa a tres aliados distintos",
    usos_habilidad=1,
)

duende_experimentado = PlantillaCriatura(
    codigo="RDEX",
    nombre="Duende experimentado",
    rareza="Rara",
    tipo="Feérico",
    vida=100,
    ataque=20,
    defensa=21,
    habilidad="experiencia",
    descripcion_habilidad="recupera 10 de vida",
    usos_habilidad=1,
)

goblin = PlantillaCriatura(
    codigo="RGOB",
    nombre="Goblin",
    rareza="Rara",
    tipo="Feérico",
    vida=90,
    ataque=20,
    defensa=18,
    habilidad="roba vida",
    descripcion_habilidad="le roba 10 de vida a un enemigo",
    usos_habilidad=1,
)

elfo_lider_guerrero = PlantillaCriatura(
    codigo="RELG",
    nombre="Elfo líder guerrero",
    rareza="Rara",
    tipo="Feérico",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="corte tajante",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

elfo_guerrero = PlantillaCriatura(
    codigo="REGU",
    nombre="Elfo guerrero",
    rareza="Rara",
    tipo="Feérico",
    vida=90,
    ataque=22,
    defensa=20,
    habilidad="flechazo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

golem_de_hierro = PlantillaCriatura(
    codigo="RGHI",
    nombre="Golem de hierro",
    rareza="Rara",
    tipo="Gigante",
    vida=120,
    ataque=22,
    defensa=25,
    habilidad="ataque metálico",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

golem_de_fuego = PlantillaCriatura(
    codigo="RGFU",
    nombre="Golem de fuego",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=17,
    habilidad="llamarada",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

golem_de_rayo = PlantillaCriatura(
    codigo="RGRA",
    nombre="Golem de rayo",
    rareza="Rara",
    tipo="Gigante",
    vida=90,
    ataque=22,
    defensa=20,
    habilidad="relámpago",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

golem_de_hielo = PlantillaCriatura(
    codigo="RGLO",
    nombre="Golem de hielo",
    rareza="Rara",
    tipo="Gigante",
    vida=95,
    ataque=22,
    defensa=20,
    habilidad="tiros helados",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

titan_de_tierra = PlantillaCriatura(
    codigo="RTTI",
    nombre="Titán de Tierra",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="fisura",
    descripcion_habilidad="ataca a todos los enemigos con 15 de ataque",
    usos_habilidad=1,
)

titan_del_oceano = PlantillaCriatura(
    codigo="RTOC",
    nombre="Titán del océano",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="remolino de agua",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

titan_del_trueno = PlantillaCriatura(
    codigo="RTTR",
    nombre="Titán del trueno",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="tormenta eléctrica",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

titan_de_las_nieves = PlantillaCriatura(
    codigo="RTNI",
    nombre="Titán de las nieves",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="avalancha",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

titan_del_viento = PlantillaCriatura(
    codigo="RTVI",
    nombre="Titán del viento",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="tifón",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

titan_de_lava = PlantillaCriatura(
    codigo="RTLA",
    nombre="Titán de lava",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="magma",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

gigante = PlantillaCriatura(
    codigo="RGIG",
    nombre="Gigante",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=20,
    defensa=22,
    habilidad="pisotón",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

madre_de_gigantes = PlantillaCriatura(
    codigo="RMGI",
    nombre="Madre de gigantes",
    rareza="Rara",
    tipo="Gigante",
    vida=100,
    ataque=20,
    defensa=22,
    habilidad="instinto materno",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

esfinge = PlantillaCriatura(
    codigo="RESF",
    nombre="Esfinge",
    rareza="Rara",
    tipo="Híbrido",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="papiro",
    descripcion_habilidad="se cura 20 de vida",
    usos_habilidad=1,
)

hipogrifo = PlantillaCriatura(
    codigo="RHIP",
    nombre="Hipogrifo",
    rareza="Rara",
    tipo="Híbrido",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="esquiva",
    descripcion_habilidad="esquiva uno de los ataque que recibiría durante el combate",
    usos_habilidad=1,
)

grifo = PlantillaCriatura(
    codigo="RGRI",
    nombre="Grifo",
    rareza="Rara",
    tipo="Híbrido",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="furia de grifo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

minotauro = PlantillaCriatura(
    codigo="RMIN",
    nombre="Minotauro",
    rareza="Rara",
    tipo="Híbrido",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="ataque mutante",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

centauro = PlantillaCriatura(
    codigo="RCEN",
    nombre="Centauro",
    rareza="Rara",
    tipo="Híbrido",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="esquiva",
    descripcion_habilidad="esquiva un ataque durante el combate",
    usos_habilidad=1,
)

gritablilu = PlantillaCriatura(
    codigo="RBIL",
    nombre="Gritablilu",
    rareza="Rara",
    tipo="Híbrido",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="veneno asesino",
    descripcion_habilidad="elimina a un enemigo si le quedan 20 o menos de vida",
    usos_habilidad=1,
)

dama_blanca = PlantillaCriatura(
    codigo="RDBL",
    nombre="Dama blanca",
    rareza="Rara",
    tipo="Espíritu",
    vida=95,
    ataque=22,
    defensa=20,
    habilidad="toma vida",
    descripcion_habilidad="elimina a un enemigo si le queda 20 o menos de vida",
    usos_habilidad=1,
)

nekomata = PlantillaCriatura(
    codigo="RNEK",
    nombre="Nekomata",
    rareza="Rara",
    tipo="Espíritu",
    vida=95,
    ataque=23,
    defensa=18,
    habilidad="ataque felino",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

genio_azul = PlantillaCriatura(
    codigo="RGEN",
    nombre="Genio (azul)",
    rareza="Rara",
    tipo="Espíritu",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="desaparición",
    descripcion_habilidad="elimina a un enemigo con 20 o menos de vida y se elimina del combate",
    usos_habilidad=1,
)

yeti_joven = PlantillaCriatura(
    codigo="RYJO",
    nombre="Yeti Jóven",
    rareza="Rara",
    tipo="Bestia",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="avalancha",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

mothman = PlantillaCriatura(
    codigo="RMOT",
    nombre="Mothman",
    rareza="Rara",
    tipo="Bestia",
    vida=80,
    ataque=15,
    defensa=15,
    habilidad="ojos sangrientos",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

chupacabras = PlantillaCriatura(
    codigo="RCHU",
    nombre="Chupacabras",
    rareza="Rara",
    tipo="Bestia",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="devorador",
    descripcion_habilidad="ataque x1.5 a un enemigo y le roba 10 de vida",
    usos_habilidad=1,
)

wendigo = PlantillaCriatura(
    codigo="RWEN",
    nombre="Wendigo",
    rareza="Rara",
    tipo="Bestia",
    vida=110,
    ataque=20,
    defensa=20,
    habilidad="come vida",
    descripcion_habilidad="roba 20 de vida de un enemigo",
    usos_habilidad=1,
)

bunyip = PlantillaCriatura(
    codigo="RBUN",
    nombre="Bunyip",
    rareza="Rara",
    tipo="Bestia",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="come enemigos",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

ahool = PlantillaCriatura(
    codigo="RAHO",
    nombre="Ahool",
    rareza="Rara",
    tipo="Bestia",
    vida=100,
    ataque=20,
    defensa=18,
    habilidad="chupasangre",
    descripcion_habilidad="roba 10 de vida de un enemigo",
    usos_habilidad=1,
)

barghest = PlantillaCriatura(
    codigo="RBAR",
    nombre="Barghest",
    rareza="Rara",
    tipo="Bestia",
    vida=100,
    ataque=25,
    defensa=20,
    habilidad="presagio de muerte",
    descripcion_habilidad="deja a un enemigo con 5 de vida si éste tiene entre 30 y 40 de vida",
    usos_habilidad=1,
)

ammit = PlantillaCriatura(
    codigo="RAMM",
    nombre="Ammit",
    rareza="Rara",
    tipo="Bestia",
    vida=100,
    ataque=25,
    defensa=25,
    habilidad="come corazones",
    descripcion_habilidad="reduce 30 de vida de un enemigo",
    usos_habilidad=1,
)

nian = PlantillaCriatura(
    codigo="RNIA",
    nombre="Nian",
    rareza="Rara",
    tipo="Bestia",
    vida=110,
    ataque=25,
    defensa=20,
    habilidad="rugido del Nian",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque",
    usos_habilidad=1,
)

simargl = PlantillaCriatura(
    codigo="RARG",
    nombre="Simargl",
    rareza="Rara",
    tipo="Celestial",
    vida=100,
    ataque=23,
    defensa=20,
    habilidad="alas sagradas",
    descripcion_habilidad="aumenta 10 de defensa a un aliado durante hasta el próximo ataque",
    usos_habilidad=1,
)

grootslang = PlantillaCriatura(
    codigo="RGRO",
    nombre="Grootslang",
    rareza="Rara",
    tipo="Bestia",
    vida=120,
    ataque=25,
    defensa=23,
    habilidad="constricción monstruosa",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

ahuizotl = PlantillaCriatura(
    codigo="RAHU",
    nombre="Ahuízotl",
    rareza="Rara",
    tipo="Bestia",
    vida=90,
    ataque=22,
    defensa=18,
    habilidad="garra acuática",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

amarok = PlantillaCriatura(
    codigo="RAMA",
    nombre="Amarok",
    rareza="Rara",
    tipo="Bestia",
    vida=110,
    ataque=25,
    defensa=18,
    habilidad="furia del lobo",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

tarasca = PlantillaCriatura(
    codigo="RTAR",
    nombre="Tarasca",
    rareza="Rara",
    tipo="Híbrido",
    vida=120,
    ataque=20,
    defensa=20,
    habilidad="caparazón impenetrable",
    descripcion_habilidad="duplica su defensa para el siguiente ataque",
    usos_habilidad=1,
)

nandi_bear = PlantillaCriatura(
    codigo="RNBE",
    nombre="Nandi Bear",
    rareza="Rara",
    tipo="Bestia",
    vida=105,
    ataque=24,
    defensa=20,
    habilidad="embestida feroz",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

goblin_ingeniera = PlantillaCriatura(
    codigo="RGIN",
    nombre="Goblin Ingeniera",
    rareza="Rara",
    tipo="Feérico",
    vida=90,
    ataque=18,
    defensa=17,
    habilidad="invento explosivo",
    descripcion_habilidad="inflige 12 de daño a dos enemigos",
    usos_habilidad=1,
)

goblin_cavernicola = PlantillaCriatura(
    codigo="RGCA",
    nombre="Goblin Cavernícola",
    rareza="Rara",
    tipo="Feérico",
    vida=100,
    ataque=25,
    defensa=15,
    habilidad="ataque goblin",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=1,
)

dragon_chino = PlantillaCriatura(
    codigo="SDCH",
    nombre="Dragón chino",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=160,
    ataque=34,
    defensa=34,
    habilidad="lluvia bendita",
    descripcion_habilidad="cura 20 de vida a todos los aliados",
    usos_habilidad=1,
)

dragon_de_fuego_y_hielo = PlantillaCriatura(
    codigo="SDFH",
    nombre="Dragón de fuego y hielo",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=165,
    ataque=40,
    defensa=32,
    habilidad="aliento de hielo y fuego",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque y cuando pueda pierde 40 de vida",
    usos_habilidad=1,
)

wyvern = PlantillaCriatura(
    codigo="SWYV",
    nombre="Wyvern",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=140,
    ataque=38,
    defensa=28,
    habilidad="cola venenosa",
    descripcion_habilidad="quita 10 de vida a un enemigo por tres ataques que le toquen a su equipo",
    usos_habilidad=1,
)

basilisco = PlantillaCriatura(
    codigo="SBAS",
    nombre="Basilisco",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=135,
    ataque=34,
    defensa=36,
    habilidad="mirada mortal",
    descripcion_habilidad="elimina a un enemigo con 40 o menos de vida",
    usos_habilidad=1,
)

anfisbena = PlantillaCriatura(
    codigo="SANS",
    nombre="Anfisbena",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=130,
    ataque=35,
    defensa=30,
    habilidad="doble muerte",
    descripcion_habilidad="ataque x2 a dos enemigos a la vez",
    usos_habilidad=1,
)

quetzalcoatl = PlantillaCriatura(
    codigo="SQUE",
    nombre="Quetzalcóatl",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=175,
    ataque=38,
    defensa=36,
    habilidad="plumas solares",
    descripcion_habilidad="da 5 de ataque y defensa a todos los aliados",
    usos_habilidad=1,
)

anfiptero = PlantillaCriatura(
    codigo="SANP",
    nombre="Anfíptero",
    rareza="Super Rara",
    tipo="Dragónico",
    vida=125,
    ataque=35,
    defensa=28,
    habilidad="ataque en picada",
    descripcion_habilidad="ataque x2 a un enemigo",
    usos_habilidad=2,
)

kraken_joven = PlantillaCriatura(
    codigo="SKJO",
    nombre="Kraken Joven",
    rareza="Super Rara",
    tipo="Marino",
    vida=150,
    ataque=35,
    defensa=30,
    habilidad="abrazo de tentáculos",
    descripcion_habilidad="inmoviliza al enemigo por los próximos dos ataques",
    usos_habilidad=1,
)

kraken_viejo = PlantillaCriatura(
    codigo="SKVI",
    nombre="Kraken Viejo",
    rareza="Super Rara",
    tipo="Marino",
    vida=175,
    ataque=40,
    defensa=36,
    habilidad="tinta abismal",
    descripcion_habilidad="todos los enemigos pierden 5 de ataque",
    usos_habilidad=1,
)

sirena_mayor = PlantillaCriatura(
    codigo="SMAS",
    nombre="Sirena Mayor",
    rareza="Super Rara",
    tipo="Marino",
    vida=140,
    ataque=32,
    defensa=32,
    habilidad="canto hipnótico",
    descripcion_habilidad="el próximo ataque enemigo es dirigido al propio equipo enemigo",
    usos_habilidad=1,
)

escila = PlantillaCriatura(
    codigo="SESC",
    nombre="Escila",
    rareza="Super Rara",
    tipo="Marino",
    vida=165,
    ataque=42,
    defensa=30,
    habilidad="devora marineros",
    descripcion_habilidad="elimina a un enemigo con 40 o menos de vida",
    usos_habilidad=1,
)

arcangel_maestro = PlantillaCriatura(
    codigo="SAMA",
    nombre="Arcángel Maestro",
    rareza="Super Rara",
    tipo="Celestial",
    vida=170,
    ataque=40,
    defensa=40,
    habilidad="espada bendita",
    descripcion_habilidad="ataca x2 a un enemigo y suma 5 de defensa propia",
    usos_habilidad=1,
)

ifrit = PlantillaCriatura(
    codigo="SIFR",
    nombre="Ifrit",
    rareza="Super Rara",
    tipo="Infernal",
    vida=140,
    ataque=42,
    defensa=28,
    habilidad="fuego infernal",
    descripcion_habilidad="ataca x2 a un enemigo",
    usos_habilidad=2,
)

fenix_domestico = PlantillaCriatura(
    codigo="SFDO",
    nombre="Fénix doméstico",
    rareza="Super Rara",
    tipo="Ave mística",
    vida=130,
    ataque=30,
    defensa=28,
    habilidad="renacer",
    descripcion_habilidad="al morir por primera vez revive con 50 de vida",
    usos_habilidad=1,
)

pegaso = PlantillaCriatura(
    codigo="SPEG",
    nombre="Pegaso",
    rareza="Super Rara",
    tipo="Feérico",
    vida=140,
    ataque=32,
    defensa=30,
    habilidad="vuelo veloz",
    descripcion_habilidad="esquiva un ataque",
    usos_habilidad=2,
)

pegaso_antiguo = PlantillaCriatura(
    codigo="SPAN",
    nombre="Pegaso antiguo",
    rareza="Super Rara",
    tipo="Feérico",
    vida=160,
    ataque=36,
    defensa=34,
    habilidad="galope celestial",
    descripcion_habilidad="ataca x2 a un enemigo y esquiva el siguiente ataque que reciba",
    usos_habilidad=1,
)

pegaso_del_bosque = PlantillaCriatura(
    codigo="SPBO",
    nombre="Pegaso del bosque",
    rareza="Super Rara",
    tipo="Feérico",
    vida=150,
    ataque=30,
    defensa=32,
    habilidad="fuente de vida",
    descripcion_habilidad="cura 25 de vida a los aliados",
    usos_habilidad=1,
)

unicornio = PlantillaCriatura(
    codigo="SUNI",
    nombre="Unicornio",
    rareza="Super Rara",
    tipo="Feérico",
    vida=140,
    ataque=30,
    defensa=30,
    habilidad="cuerno sanador",
    descripcion_habilidad="cura 25 de vida a un aliado",
    usos_habilidad=2,
)

unicornio_mistico = PlantillaCriatura(
    codigo="SUMI",
    nombre="Unicornio místico",
    rareza="Super Rara",
    tipo="Feérico",
    vida=150,
    ataque=32,
    defensa=34,
    habilidad="luz purificadora",
    descripcion_habilidad="elimina los efectos negativos que le hayan aplicado a sus aliados y les cura 15 de vida",
    usos_habilidad=1,
)

unicornio_antiguo = PlantillaCriatura(
    codigo="SUAN",
    nombre="Unicornio antiguo",
    rareza="Super Rara",
    tipo="Feérico",
    vida=170,
    ataque=36,
    defensa=38,
    habilidad="embestida del cuerno",
    descripcion_habilidad="ataca x2 a un enemigo y se cura 15 de vida a sí mismo",
    usos_habilidad=1,
)

hada_heroina = PlantillaCriatura(
    codigo="SHHE",
    nombre="Hada heroína",
    rareza="Super Rara",
    tipo="Feérico",
    vida=130,
    ataque=34,
    defensa=30,
    habilidad="protección heroica",
    descripcion_habilidad="agrega 10 de defensa a todos los aliados por el siguiente ataque",
    usos_habilidad=1,
)

hada_reina = PlantillaCriatura(
    codigo="SHRE",
    nombre="Hada reina",
    rareza="Super Rara",
    tipo="Feérico",
    vida=150,
    ataque=38,
    defensa=36,
    habilidad="decreto real",
    descripcion_habilidad="da 30 de vida, 8 de ataque y 5 de defensa a 2 aliados",
    usos_habilidad=1,
)

goblin_habilidoso = PlantillaCriatura(
    codigo="SGHA",
    nombre="Goblin habilidoso",
    rareza="Super Rara",
    tipo="Feérico",
    vida=130,
    ataque=34,
    defensa=30,
    habilidad="robo habilidoso",
    descripcion_habilidad="le roba 25 de vida a un enemigo",
    usos_habilidad=1,
)

troll_hechicero = PlantillaCriatura(
    codigo="STHE",
    nombre="Troll hechicero",
    rareza="Super Rara",
    tipo="Feérico",
    vida=160,
    ataque=35,
    defensa=32,
    habilidad="regeneración",
    descripcion_habilidad="recupera 5 de vida por 5 ataques",
    usos_habilidad=1,
)

golem_amatista = PlantillaCriatura(
    codigo="SGAM",
    nombre="Golem amatista",
    rareza="Super Rara",
    tipo="Gigante",
    vida=170,
    ataque=37,
    defensa=40,
    habilidad="coraza cristalina",
    descripcion_habilidad="obtiene 15 de defensa extra por los siguientes 2 ataques",
    usos_habilidad=1,
)

titan_del_tiempo = PlantillaCriatura(
    codigo="STTI",
    nombre="Titán del tiempo",
    rareza="Super Rara",
    tipo="Gigante",
    vida=165,
    ataque=40,
    defensa=38,
    habilidad="detener el tiempo",
    descripcion_habilidad="un aliado ataca dos veces (con un ataque normal) en el siguiente ataque",
    usos_habilidad=1,
)

titan_de_las_constelaciones = PlantillaCriatura(
    codigo="STCO",
    nombre="Titán de las constelaciones",
    rareza="Super Rara",
    tipo="Gigante",
    vida=160,
    ataque=45,
    defensa=35,
    habilidad="lluvia de estrellas",
    descripcion_habilidad="ataca a todos los enemigos con 30 de ataque",
    usos_habilidad=1,
)

rey_de_los_gigantes = PlantillaCriatura(
    codigo="SRGI",
    nombre="Rey de los Gigantes",
    rareza="Super Rara",
    tipo="Gigante",
    vida=180,
    ataque=40,
    defensa=38,
    habilidad="grito de rey",
    descripcion_habilidad="da 8 de ataque a todos los aliados",
    usos_habilidad=1,
)

ciclope_rey = PlantillaCriatura(
    codigo="SCRE",
    nombre="Cíclope rey",
    rareza="Super Rara",
    tipo="Gigante",
    vida=170,
    ataque=42,
    defensa=34,
    habilidad="lanzamiento de roca",
    descripcion_habilidad="ataca x2 a un enemigo y lo inhabilita por el siguiente ataque",
    usos_habilidad=1,
)

manticora = PlantillaCriatura(
    codigo="SMAN",
    nombre="Mantícora",
    rareza="Super Rara",
    tipo="Híbrido",
    vida=150,
    ataque=40,
    defensa=30,
    habilidad="aguijón",
    descripcion_habilidad="le va quitando 10 de vida a un enemigo por cuatro ataques",
    usos_habilidad=1,
)

esfinge_alada = PlantillaCriatura(
    codigo="SEAL",
    nombre="Esfinge alada",
    rareza="Super Rara",
    tipo="Híbrido",
    vida=150,
    ataque=36,
    defensa=36,
    habilidad="enigma",
    descripcion_habilidad="un enemigo no puede participar del siguiente ataque y se cura 20 de vida",
    usos_habilidad=1,
)

hipogrifo_antiguo = PlantillaCriatura(
    codigo="SHAN",
    nombre="Hipogrifo antiguo",
    rareza="Super Rara",
    tipo="Híbrido",
    vida=145,
    ataque=38,
    defensa=32,
    habilidad="esquiva suprema",
    descripcion_habilidad="esquiva dos ataques al azar durante el combate",
    usos_habilidad=1,
)

grifo_antiguo = PlantillaCriatura(
    codigo="SGAN",
    nombre="Grifo antiguo",
    rareza="Super Rara",
    tipo="Híbrido",
    vida=160,
    ataque=42,
    defensa=34,
    habilidad="custodio del tesoro",
    descripcion_habilidad="ataca x2 a un enemigo y suma 10 de defensa propia por el siguiente ataque",
    usos_habilidad=1,
)

kitsune_de_tres_colas = PlantillaCriatura(
    codigo="SKTR",
    nombre="Kitsune de tres colas",
    rareza="Super Rara",
    tipo="Espíritu",
    vida=130,
    ataque=36,
    defensa=30,
    habilidad="fuego centenar",
    descripcion_habilidad="ataca x2 a un enemigo y le saca 10 de vida por los tres próximos ataques",
    usos_habilidad=1,
)

nurikabe = PlantillaCriatura(
    codigo="SNUR",
    nombre="Nurikabe",
    rareza="Super Rara",
    tipo="Espíritu",
    vida=175,
    ataque=25,
    defensa=45,
    habilidad="muro impenetrable",
    descripcion_habilidad="da 8 de defensa a todos los aliados y 12 a sí mismo por los próximos dos ataques",
    usos_habilidad=1,
)

leshy = PlantillaCriatura(
    codigo="SLES",
    nombre="Leshy",
    rareza="Super Rara",
    tipo="Espíritu",
    vida=150,
    ataque=32,
    defensa=34,
    habilidad="metamorfosis",
    descripcion_habilidad="copia el poder de ataque del enemigo con mayor ataque por los próximos dos ataques",
    usos_habilidad=1,
)

genia_rosa = PlantillaCriatura(
    codigo="SGRO",
    nombre="Genia (rosa)",
    rareza="Super Rara",
    tipo="Espíritu",
    vida=135,
    ataque=34,
    defensa=32,
    habilidad="deseo concedido",
    descripcion_habilidad="cura 35 de vida y da 5 de ataque a un aliado",
    usos_habilidad=1,
)

gran_yeti = PlantillaCriatura(
    codigo="SGYE",
    nombre="Gran Yeti",
    rareza="Super Rara",
    tipo="Bestia",
    vida=175,
    ataque=40,
    defensa=38,
    habilidad="ventisca",
    descripcion_habilidad="dos enemigos no pueden participar del siguiente ataque",
    usos_habilidad=1,
)

ahool_mayor = PlantillaCriatura(
    codigo="SAHM",
    nombre="Ahool mayor",
    rareza="Super Rara",
    tipo="Bestia",
    vida=145,
    ataque=35,
    defensa=30,
    habilidad="chupasangre voraz",
    descripcion_habilidad="le roba 20 de vida a un enemigo",
    usos_habilidad=2,
)

medusa = PlantillaCriatura(
    codigo="SMED",
    nombre="Medusa",
    rareza="Super Rara",
    tipo="Híbrido",
    vida=140,
    ataque=38,
    defensa=34,
    habilidad="mirada petrificante",
    descripcion_habilidad="un enemigo no puede participar de los siguientes 3 ataques",
    usos_habilidad=1,
)

dragon_de_oscuridad = PlantillaCriatura(
    codigo="SSDO",
    nombre="Dragón de Oscuridad",
    rareza="Super Super Rara",
    tipo="Dragónico",
    vida=250,
    ataque=65,
    defensa=55,
    habilidad="amplia oscuridad",
    descripcion_habilidad="ataca x2 a un enemigo y el enemigo pierde 10 de ataque",
    usos_habilidad=2,
)

dragon_de_luz = PlantillaCriatura(
    codigo="SSDL",
    nombre="Dragón de Luz",
    rareza="Super Super Rara",
    tipo="Dragónico",
    vida=250,
    ataque=60,
    defensa=60,
    habilidad="aliento cegador",
    descripcion_habilidad="ataca x2 a un enemigo y se cura 50 de vida",
    usos_habilidad=2,
)

hidra_de_lerna = PlantillaCriatura(
    codigo="SSLE",
    nombre="Hidra de Lerna",
    rareza="Super Super Rara",
    tipo="Dragónico",
    vida=240,
    ataque=58,
    defensa=55,
    habilidad="cabezas regeneradas",
    descripcion_habilidad="recupera 25 de vida por los próximos cuatro ataques",
    usos_habilidad=1,
)

basilisco_milenario = PlantillaCriatura(
    codigo="SSBM",
    nombre="Basilisco milenario",
    rareza="Super Super Rara",
    tipo="Dragónico",
    vida=210,
    ataque=55,
    defensa=60,
    habilidad="aliento venenoso",
    descripcion_habilidad="ataca x2 a un enemigo y le saca 6 de vida por los próximos cuatro ataques",
    usos_habilidad=1,
)

anfisbena_explosiva = PlantillaCriatura(
    codigo="SSAE",
    nombre="Anfisbena explosiva",
    rareza="Super Super Rara",
    tipo="Dragónico",
    vida=190,
    ataque=65,
    defensa=50,
    habilidad="estallido doble",
    descripcion_habilidad="ataca a todos los enemigos con 80 de ataque y pierde 30 de vida propia",
    usos_habilidad=1,
)

aspidochelone = PlantillaCriatura(
    codigo="SSAS",
    nombre="Aspidochelone",
    rareza="Super Super Rara",
    tipo="Marino",
    vida=250,
    ataque=45,
    defensa=70,
    habilidad="isla engañosa",
    descripcion_habilidad="agrega 20 de defensa a todos los aliados por 2 ataques",
    usos_habilidad=1,
)

querubin = PlantillaCriatura(
    codigo="SSQE",
    nombre="Querubín",
    rareza="Super Super Rara",
    tipo="Celestial",
    vida=250,
    ataque=45,
    defensa=70,
    habilidad="palabra de Dios",
    descripcion_habilidad="agrega 20 de defensa a todos los aliados por 2 ataques",
    usos_habilidad=1,
)

serafin = PlantillaCriatura(
    codigo="SSSE",
    nombre="Serafín",
    rareza="Super Super Rara",
    tipo="Celestial",
    vida=250,
    ataque=65,
    defensa=65,
    habilidad="fuego purificador",
    descripcion_habilidad="ataca a todos los enemigos y cura 15 de vida a todos los aliados",
    usos_habilidad=1,
)

tronos = PlantillaCriatura(
    codigo="SSCR",
    nombre="Tronos",
    rareza="Super Super Rara",
    tipo="Celestial",
    vida=250,
    ataque=60,
    defensa=60,
    habilidad="justicia divina",
    descripcion_habilidad="si un enemigo eliminó a un aliado, lo elimina instantáneamente a menos que sea Legendario",
    usos_habilidad=1,
)

rakshasa = PlantillaCriatura(
    codigo="SSRA",
    nombre="Rakshasa",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=210,
    ataque=60,
    defensa=50,
    habilidad="cambia formas",
    descripcion_habilidad="copia el ataque del enemigo con más ataque por los próximos tres ataques",
    usos_habilidad=1,
)

hija_de_lucifer = PlantillaCriatura(
    codigo="SSHL",
    nombre="Hija de Lucifer",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=60,
    defensa=50,
    habilidad="herencia infernal",
    descripcion_habilidad="ataca x2 a un enemigo y le roba 30 de vida",
    usos_habilidad=2,
)

orgullo = PlantillaCriatura(
    codigo="SSOR",
    nombre="Orgullo",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=220,
    ataque=60,
    defensa=60,
    habilidad="soberbia",
    descripcion_habilidad="suma 10 de ataque y defensa a sí mismo",
    usos_habilidad=1,
)

avaricia = PlantillaCriatura(
    codigo="SSAV",
    nombre="Avaricia",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=60,
    defensa=60,
    habilidad="codicia",
    descripcion_habilidad="le roba 30 de vida y 5 de ataque a un enemigo",
    usos_habilidad=2,
)

lujuria = PlantillaCriatura(
    codigo="SSLU",
    nombre="Lujuria",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=50,
    defensa=50,
    habilidad="seducción",
    descripcion_habilidad="un enemigo en específico no puede atacar a un aliado en específico por dos ataques",
    usos_habilidad=2,
)

ira = PlantillaCriatura(
    codigo="SSIR",
    nombre="Ira",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=70,
    defensa=45,
    habilidad="furia desatada",
    descripcion_habilidad="ataca x2 a un enemigo y pierde 20 de vida propia",
    usos_habilidad=2,
)

gula = PlantillaCriatura(
    codigo="SSGU",
    nombre="Gula",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=50,
    defensa=50,
    habilidad="glotonería",
    descripcion_habilidad="le roba 40 de vida a un enemigo",
    usos_habilidad=3,
)

envidia = PlantillaCriatura(
    codigo="SSEN",
    nombre="Envidia",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=55,
    defensa=55,
    habilidad="celos",
    descripcion_habilidad="le roba 10 de ataque y defensa a un enemigo y la siguiente vez roba 30 de vida",
    usos_habilidad=2,
)

pereza = PlantillaCriatura(
    codigo="SSPE",
    nombre="Pereza",
    rareza="Super Super Rara",
    tipo="Infernal",
    vida=200,
    ataque=55,
    defensa=60,
    habilidad="vagancia",
    descripcion_habilidad="no participa por dos ataques pero tampoco puede ser atacado",
    usos_habilidad=2,
)

thunderbird = PlantillaCriatura(
    codigo="SSTH",
    nombre="Thunderbird",
    rareza="Super Super Rara",
    tipo="Ave mística",
    vida=220,
    ataque=65,
    defensa=50,
    habilidad="batir de alas",
    descripcion_habilidad="ataca x2 a un enemigo y lo inhabilita por el siguiente ataque",
    usos_habilidad=2,
)

qilin = PlantillaCriatura(
    codigo="SSQI",
    nombre="Qilin",
    rareza="Super Super Rara",
    tipo="Feérico",
    vida=210,
    ataque=55,
    defensa=60,
    habilidad="pureza benévola",
    descripcion_habilidad="cura 30 de vida a todos los aliados y elimina sus efectos negativos",
    usos_habilidad=2,
)

surt = PlantillaCriatura(
    codigo="SSSU",
    nombre="Surt",
    rareza="Super Super Rara",
    tipo="Gigante",
    vida=230,
    ataque=70,
    defensa=55,
    habilidad="llamas del destino",
    descripcion_habilidad="les quita 15 de vida a todos sus enemigos",
    usos_habilidad=3,
)

quimera = PlantillaCriatura(
    codigo="SSQU",
    nombre="Quimera",
    rareza="Super Super Rara",
    tipo="Híbrido",
    vida=220,
    ataque=65,
    defensa=50,
    habilidad="triple ataque",
    descripcion_habilidad="ataca con 90 de ataque a tres enemigos",
    usos_habilidad=2,
)

dracula = PlantillaCriatura(
    codigo="SSDR",
    nombre="Drácula",
    rareza="Super Super Rara",
    tipo="Híbrido",
    vida=215,
    ataque=60,
    defensa=55,
    habilidad="mordida vampírica",
    descripcion_habilidad="ataca a un enemigo y le roba 30 de vida",
    usos_habilidad=2,
)

kitsune_de_6_colas = PlantillaCriatura(
    codigo="SSKS",
    nombre="Kitsune de 6 colas",
    rareza="Super Super Rara",
    tipo="Espíritu",
    vida=200,
    ataque=60,
    defensa=50,
    habilidad="ilusión de zorro",
    descripcion_habilidad="los enemigos se atacan entre sí por los próximos tres ataques",
    usos_habilidad=1,
)

jinete_sin_cabeza = PlantillaCriatura(
    codigo="SSJC",
    nombre="Jinete sin cabeza",
    rareza="Super Super Rara",
    tipo="Espíritu",
    vida=200,
    ataque=65,
    defensa=50,
    habilidad="decapitación",
    descripcion_habilidad="elimina automáticamente a un enemigo si este tiene 40 o menos de vida y le roba 20 de vida",
    usos_habilidad=2,
)

gran_genio = PlantillaCriatura(
    codigo="SSGG",
    nombre="Gran genio",
    rareza="Super Super Rara",
    tipo="Espíritu",
    vida=210,
    ataque=60,
    defensa=55,
    habilidad="tres deseos",
    descripcion_habilidad="1° deseo: da 50 de vida a un aliado, 2° deseo: da 20 de ataque a un aliado y 3° deseo: da 20 de defensa a un aliado",
    usos_habilidad=3,
)

dragon_de_oscuridad_y_luz = PlantillaCriatura(
    codigo="LDOL",
    nombre="Dragón de Oscuridad y Luz",
    rareza="Legendaria",
    tipo="Dragónico",
    vida=360,
    ataque=110,
    defensa=100,
    habilidad="equilibrio primordial",
    descripcion_habilidad="ataca x2 a un enemigo y cura 30 de vida a todos los aliados",
    usos_habilidad=2,
)

leviatan = PlantillaCriatura(
    codigo="LLEV",
    nombre="Leviatán",
    rareza="Legendaria",
    tipo="Marino",
    vida=380,
    ataque=100,
    defensa=115,
    habilidad="furia del abismo",
    descripcion_habilidad="ataca x2 a todos los enemigos y suma 15 de defensa",
    usos_habilidad=2,
)

kraken = PlantillaCriatura(
    codigo="LKRA",
    nombre="Kraken",
    rareza="Legendaria",
    tipo="Marino",
    vida=370,
    ataque=105,
    defensa=95,
    habilidad="naufragio",
    descripcion_habilidad="ataca a todos los enemigos y uno de ellos no puede participar por el siguiente ataque",
    usos_habilidad=2,
)

dios = PlantillaCriatura(
    codigo="LDIO",
    nombre="Dios",
    rareza="Legendaria",
    tipo="Celestial",
    vida=400,
    ataque=120,
    defensa=120,
    habilidad="soberano",
    descripcion_habilidad="revive a un aliado caído con toda su vida y cura a todos los aliados",
    usos_habilidad=1,
)

lucifer = PlantillaCriatura(
    codigo="LLUC",
    nombre="Lucifer",
    rareza="Legendaria",
    tipo="Infernal",
    vida=390,
    ataque=115,
    defensa=115,
    habilidad="caída del ángel",
    descripcion_habilidad="elimina a un enemigo que tenga 100 o menos de vida y todos los demás pierden 10 de defensa",
    usos_habilidad=1,
)

cerberus = PlantillaCriatura(
    codigo="LCER",
    nombre="Cerberus",
    rareza="Legendaria",
    tipo="Infernal",
    vida=350,
    ataque=110,
    defensa=95,
    habilidad="guardián del inframundo",
    descripcion_habilidad="ataca a tres enemigos y les quita 15 de vida por tres turnos",
    usos_habilidad=2,
)

fenix_legendario = PlantillaCriatura(
    codigo="LFLE",
    nombre="Fénix legendario",
    rareza="Legendaria",
    tipo="Ave mística",
    vida=300,
    ataque=90,
    defensa=80,
    habilidad="renacer en llamas",
    descripcion_habilidad="la primera vez que muere revive con 350 de vida, 100 de ataque y 80 de defensa y ataca a todos los enemigos",
    usos_habilidad=1,
)

alicornio_superior = PlantillaCriatura(
    codigo="LALS",
    nombre="Alicornio superior",
    rareza="Legendaria",
    tipo="Feérico",
    vida=330,
    ataque=100,
    defensa=100,
    habilidad="luz del alicornio",
    descripcion_habilidad="cura 50 de vida a todos los aliados y les suma 10 de defensa",
    usos_habilidad=1,
)

kitsune_primordial = PlantillaCriatura(
    codigo="LKNU",
    nombre="Kitsune primordial",
    rareza="Legendaria",
    tipo="Espíritu",
    vida=320,
    ataque=100,
    defensa=90,
    habilidad="ilusión de las 9 colas",
    descripcion_habilidad="todos los enemigos se atacan entre sí en el siguiente ataque",
    usos_habilidad=2,
)

monstruo_del_lago_ness = PlantillaCriatura(
    codigo="LMLN",
    nombre="Monstruo del Lago Ness",
    rareza="Legendaria",
    tipo="Bestia",
    vida=320,
    ataque=75,
    defensa=90,
    habilidad="ataque de las profundidades",
    descripcion_habilidad="ataca x2 a dos enemigos y se cura 40 de vida",
    usos_habilidad=2,
)

jormungandr = PlantillaCriatura(
    codigo="LJOR",
    nombre="Jörmungandr",
    rareza="Legendaria",
    tipo="Bestia",
    vida=380,
    ataque=105,
    defensa=110,
    habilidad="Ragnarök",
    descripcion_habilidad="le quita 100 de vida a todos los enemigos y por los siguientes tres turnos van perdiendo 20 de vida",
    usos_habilidad=1,
)

apep = PlantillaCriatura(
    codigo="LAPE",
    nombre="Apep",
    rareza="Legendaria",
    tipo="Infernal",
    vida=300,
    ataque=100,
    defensa=90,
    habilidad="oscuridad eterna",
    descripcion_habilidad="todos los enemigos no pueden participar del siguiente ataque y pierden 10 de ataque",
    usos_habilidad=2,
)

CRIATURAS: List[PlantillaCriatura] = [
    dragonzuelo,
    hidra_bebe,
    cocatricito,
    sirena,
    sirena_del_pacifico,
    sirena_de_coral,
    sirena_curiosa,
    nixie,
    triton_aprendiz,
    angel_mensajero,
    angel_compasivo,
    angel_guardian,
    angel_justiciero,
    angel_servicial,
    oni_travieso,
    oni_castigador,
    diablillo,
    demonio_solitario,
    demonio_infeliz,
    pichon_de_fenix,
    hada_del_bosque,
    hada_de_los_insectos,
    hada_artesana,
    hada_del_agua,
    hada_de_la_nieve,
    hada_sanadora,
    hada_de_la_musica,
    hada_bibliotecaria,
    flash_pixie,
    amore_pixie,
    loquace_pixie,
    vita_pixie,
    sonno_pixie,
    colpo_pixie,
    ombra_pixie,
    fulmine_pixie,
    duendecillo,
    trasgos_duende,
    domovoi_duende,
    musgoso_duende,
    brownie_duende,
    boggart_duende,
    nayades_ninfa,
    napea_ninfa,
    aurai_ninfa,
    troll_de_montana,
    troll_de_caverna,
    troll_de_las_nieves,
    elfo_de_la_luz,
    elfo_de_la_oscuridad,
    elfo_del_bosque,
    elfa_arquera,
    golem_de_piedra,
    titan_nino,
    pequeno_ciclope,
    nino_fauno,
    esfinge_cachorro,
    grifo_cachorro,
    hipogrifo_cachorro,
    nino_centauro,
    espiritu_del_bosque,
    espiritu_errante,
    espiritu_dolido,
    espiritu_oscuro,
    kitsune_joven,
    bakenko,
    duendes_de_hollin,
    bebe_yeti,
    chupacabritas,
    mooncalf,
    kobold,
    alux,
    cheneque,
    nisse,
    leprechaun,
    puckwudgie,
    pixiu,
    kodama,
    imp,
    baku_pequeno,
    carbunclo,
    tatzelwurm_pequeno,
    caladrius,
    simargl_cachorro,
    wolpertinger,
    jackalope,
    ratatoskr,
    fenghuang_polluelo,
    qilin_bebe,
    dragon_de_fuego,
    dragon_de_hielo,
    dragon_de_trueno,
    trio_dragonico,
    cocatrice,
    triton,
    triton_de_las_profundidades,
    triton_experimentado,
    sirena_de_las_profundidades,
    kelpie,
    valkiria,
    arcangel,
    oni_superior,
    diablo_de_jersey,
    cerberucito,
    simurgh,
    hada_guerrera,
    reina_de_las_pixies,
    duende_experimentado,
    goblin,
    elfo_lider_guerrero,
    elfo_guerrero,
    golem_de_hierro,
    golem_de_fuego,
    golem_de_rayo,
    golem_de_hielo,
    titan_de_tierra,
    titan_del_oceano,
    titan_del_trueno,
    titan_de_las_nieves,
    titan_del_viento,
    titan_de_lava,
    gigante,
    madre_de_gigantes,
    esfinge,
    hipogrifo,
    grifo,
    minotauro,
    centauro,
    gritablilu,
    dama_blanca,
    nekomata,
    genio_azul,
    yeti_joven,
    mothman,
    chupacabras,
    wendigo,
    bunyip,
    ahool,
    barghest,
    ammit,
    nian,
    simargl,
    grootslang,
    ahuizotl,
    amarok,
    tarasca,
    nandi_bear,
    goblin_ingeniera,
    goblin_cavernicola,
    dragon_chino,
    dragon_de_fuego_y_hielo,
    wyvern,
    basilisco,
    anfisbena,
    quetzalcoatl,
    anfiptero,
    kraken_joven,
    kraken_viejo,
    sirena_mayor,
    escila,
    arcangel_maestro,
    ifrit,
    fenix_domestico,
    pegaso,
    pegaso_antiguo,
    pegaso_del_bosque,
    unicornio,
    unicornio_mistico,
    unicornio_antiguo,
    hada_heroina,
    hada_reina,
    goblin_habilidoso,
    troll_hechicero,
    golem_amatista,
    titan_del_tiempo,
    titan_de_las_constelaciones,
    rey_de_los_gigantes,
    ciclope_rey,
    manticora,
    esfinge_alada,
    hipogrifo_antiguo,
    grifo_antiguo,
    kitsune_de_tres_colas,
    nurikabe,
    leshy,
    genia_rosa,
    gran_yeti,
    ahool_mayor,
    medusa,
    dragon_de_oscuridad,
    dragon_de_luz,
    hidra_de_lerna,
    basilisco_milenario,
    anfisbena_explosiva,
    aspidochelone,
    querubin,
    serafin,
    tronos,
    rakshasa,
    hija_de_lucifer,
    orgullo,
    avaricia,
    lujuria,
    ira,
    gula,
    envidia,
    pereza,
    thunderbird,
    qilin,
    surt,
    quimera,
    dracula,
    kitsune_de_6_colas,
    jinete_sin_cabeza,
    gran_genio,
    dragon_de_oscuridad_y_luz,
    leviatan,
    kraken,
    dios,
    lucifer,
    cerberus,
    fenix_legendario,
    alicornio_superior,
    kitsune_primordial,
    monstruo_del_lago_ness,
    jormungandr,
    apep,
]

PLANTILLAS_CRIATURAS: Dict[str, PlantillaCriatura] = {
    c.codigo: c for c in CRIATURAS
}

def crear_catalogo_completo() -> Catalogo:
    """Crea y retorna una instancia de Catalogo con las 227 criaturas."""
    catalogo = Catalogo()
    for criatura in CRIATURAS:
        catalogo.plantillas[criatura.codigo] = criatura
    return catalogo
