# Hack para importar los modulos facilmente
import sys
from pathlib import Path
src = Path("../src").resolve() # ../src es relativo desde donde se corre el notebook
sys.path.append(str(src))