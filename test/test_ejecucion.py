import init
import sys
print(sys.path)
import experimento


def test_ejecucion():
    assert experimento.ejemplo("ASD") == 2