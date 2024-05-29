import init
import sys
print(sys.path)
import agentes


def test_ejecucion():
    assert agentes.ejemplo("ASD") == 2