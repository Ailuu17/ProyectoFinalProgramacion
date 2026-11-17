"""
Servidor Web para el Mercado de Cartas Mitológicas.
Conecta la Capa de Presentación (Frontend HTML/JS) con el Modelo de Dominio en Python (mercado_cartas).

Ejecución:
    python frontend/server.py
Luego abre en el navegador:
    http://localhost:8000
"""

import os
import sys
import json
from urllib.parse import unquote, urlsplit
from datetime import date
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Agregar directorio raíz para importar mercado_cartas
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from mercado_cartas import (
    Catalogo,
    Carta,
    Evento,
    Juego,
    Jugador,
    Mercado,
    Moneda,
    SobreEstable,
    SobreVariable,
    crear_catalogo_completo,
    crear_mercado_estandar,
    crear_evento_noche_eterna,
    MONEDA_COMUN,
    MONEDA_EVENTO,
)

# ==============================================================================
# Inicialización del Dominio del Juego
# ==============================================================================
catalogo_global = crear_catalogo_completo()
mercado_global = crear_mercado_estandar(catalogo_global)
evento_global = crear_evento_noche_eterna()

juego_global = Juego(
    catalogo=catalogo_global,
    mercado=mercado_global,
    eventos=[evento_global],
)

# Jugadores iniciales
jugador_ash = Jugador(id="j1", nombre="Ash")
jugador_misty = Jugador(id="j2", nombre="Misty")
juego_global.agregar_jugador(jugador_ash)
juego_global.agregar_jugador(jugador_misty)

FRONTEND_DIR = Path(__file__).resolve().parent
ARTWORK_DIR = ROOT_DIR / "Documentos" / "Imagenes"


class GameHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self):
        image_path = urlsplit(self.path).path
        artwork_routes = {
            "/Documentos/Imagenes/Personajes/": ARTWORK_DIR / "Personajes",
            "/Documentos/Imagenes/Monedas/": ARTWORK_DIR / "Monedas",
            "/Documentos/Imagenes/Sobres/": ARTWORK_DIR / "Sobres",
        }
        for route, artwork_dir in artwork_routes.items():
            if image_path.startswith(route):
                filename = unquote(image_path[len(route):])
                if (
                    not filename
                    or Path(filename).name != filename
                    or "\\" in filename
                    or Path(filename).suffix.lower() != ".png"
                ):
                    self.send_error(404)
                    return

                artwork_path = artwork_dir / filename
                if not artwork_path.is_file():
                    self.send_error(404)
                    return

                image = artwork_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(image)))
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                self.wfile.write(image)
                return

        # Endpoints API REST
        if self.path == "/api/estado":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            resumen = {
                "jugadores": {
                    j_id: juego_global.resumen_jugador(j_id)
                    for j_id in juego_global.jugadores
                },
                "evento": {
                    "nombre": evento_global.nombre,
                    "fecha_inicio": str(evento_global.fecha_inicio),
                    "fecha_fin": str(evento_global.fecha_fin),
                    "tasa_cambio": mercado_global.tasa_cambio,
                },
                "total_criaturas_catalogo": len(catalogo_global.plantillas),
            }
            self.wfile.write(json.dumps(resumen, ensure_ascii=False).encode("utf-8"))
            return

        # Servir archivos estáticos del frontend
        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8")) if body else {}

        if self.path == "/api/login":
            # Capa de presentación / sesión:
            jugador_id = data.get("jugador_id", "j1")
            try:
                jugador = juego_global._obtener_jugador(jugador_id)
                self.responder_json(200, {
                    "ok": True,
                    "jugador": juego_global.resumen_jugador(jugador.id)
                })
            except Exception as e:
                self.responder_json(400, {"ok": False, "error": str(e)})
            return

        if self.path == "/api/intercambiar":
            try:
                juego_global.intercambiar(
                    jugador_a_id=data["jugador_a_id"],
                    cartas_a_ids=data["cartas_a_ids"],
                    jugador_b_id=data["jugador_b_id"],
                    cartas_b_ids=data["cartas_b_ids"],
                    aceptado_a=data.get("aceptado_a", True),
                    aceptado_b=data.get("aceptado_b", True),
                )
                self.responder_json(200, {"ok": True, "mensaje": "Intercambio realizado exitosamente"})
            except Exception as e:
                self.responder_json(400, {"ok": False, "error": str(e)})
            return

        self.responder_json(404, {"ok": False, "error": "Ruta no encontrada"})

    def responder_json(self, status: int, payload: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def main():
    puerto = 8000
    servidor = HTTPServer(("localhost", puerto), GameHTTPRequestHandler)
    print("=" * 70)
    print(f" Servidor del Juego iniciado en http://localhost:{puerto}")
    print(f" Sirviendo archivos desde: {FRONTEND_DIR}")
    print(" Presiona Ctrl+C para detener el servidor.")
    print("=" * 70)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    main()
