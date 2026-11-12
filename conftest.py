import sys
from pathlib import Path

codigo_path = Path(__file__).parent / "Código"
if str(codigo_path) not in sys.path:
    sys.path.insert(0, str(codigo_path))

