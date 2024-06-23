
def ejemplo(str):
    return f"Esto es una función de ejemplo: {str}"

class Experimento:

    def __init__(self, grafo, funcion_de_update, metricas=None):
        self.grafo = grafo
        self.update = funcion_de_update
        self.metricas = metricas or {}
        self._curr_step = 0
        self._metricas_evaluadas = {nombre:[] for nombre in self.metricas}

    def step(self, n=1):
        for _ in range(n):
            self._single_step()
            self._calcular_metricas()
            self._curr_step += 1

    def _single_step(self):
        # evaluar la funcion de update sobre los nodos
        pass

    def _calcular_metricas(self):
        for nombre, metrica in self.metricas.items():
            self._metricas_evaluadas[nombre].append(metrica(self.grafo))

    def __str__(self):
        return str(self.to_dict())
    
    def __repr__(self):
        return str(self)
    
    def to_dict(self):
        return {"id_grafo": hash(self.grafo), "step": self._curr_step, "metricas": self._metricas_evaluadas}