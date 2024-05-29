# Hack para poder importar los modulos facilmente
import sys
from pathlib import Path
src = Path("src").resolve()
sys.path.append(str(src))