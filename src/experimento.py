
import queue
import networkx as nx

def ejemplo(str):
    return f"Esto es una función de ejemplo: {str}"

class Experimento:
  def __init__(self, grafo, dinamica, duracion_periodo = 10, metricas=None, calcular_inflacion=None, alpha = 0.5): 
    """
    Inicializa una instancia de la clase Experimento.

    Parámetros
    ----------
    grafo : DiGraph
      Grafo que representa el MIP
    dinamica : Callable 
      Función con la siguiente signatura : (aumento, peso_arista, inflacion, alpha)
    duracion_periodo : int, opcional
        La duración de cada período en pasos para actualizar la inflacion, por defecto 10 pasos.
    metricas : Dict(string,Callable), opcional
        Diccionario de con metricas a computar sobre el grafo, ej, {"cantidad_nodos", lambda grafo: len(grafo)}
    calcular_inflacion : Callable, opcional
        Función para calcular la inflación en un período, recibe dos arrays de precios. ej, calc(precios_actual, precios_pasado)
    alpha : float, opcional
        Parametro de ponderacion
        El alpha es CUANTO ve la inflación. 
        Alpha == 1 es lo mismo que la dinamica 2. 
        Alpha == 0 es lo mismo que la dinamica 1.
    """
    self.grafo = grafo.copy()
    self.dinamica = dinamica
    self.metricas = metricas or {}
    self._curr_step = 0
    self.metricas_evaluadas = {nombre:[] for nombre in self.metricas}
    self.metricas_evaluadas['inflacion'] = []
    self.queue = queue.Queue() #Fila de tuplas (Nodo, aumento)
    self.duracion_periodo = duracion_periodo
    self.precios_periodo_pasado = {}
    for nodo in self.grafo.nodes:
      self.precios_periodo_pasado[nodo] = self.grafo.nodes[nodo]['precio']

    self._calc_inflacion = calcular_inflacion or (lambda actual, pasado: 0.0)
    self.inflacion = 0 # Expresada en %. (50 para 50%, 12 para 12%)
    assert 0.0 <= alpha <= 1.0
    self.alpha = alpha

  def shock(self, nodo, aumento):
    precio_actual = self.grafo.nodes[nodo]['precio']
    nuevo_precio = { nodo : { 'precio': (precio_actual * (1 + (aumento/100)))}}
    nx.set_node_attributes(self.grafo, nuevo_precio)
    vecinos = self.grafo[nodo].items()
    aumentos_a_pasar = []
    for vecino in vecinos:
      aumento_vecino = self.actualizar(vecino,aumento)
      aumentos_a_pasar.append(aumento_vecino)
    for i, vecino in enumerate(vecinos):
      self.queue.put((vecino[0], aumentos_a_pasar[i]))

  def step(self, n=1): # aumento pasado en %.
    for _ in range(n):
        self._single_step()
        self._calcular_metricas()
        self._curr_step += 1

  def actualizar(self, vecino, aumento):   
    nodo_vecino = vecino[0]
    precio_actual = self.grafo.nodes[nodo_vecino]['precio']
    peso_arista = vecino[1]['w']
    aumento_vecino = self.dinamica(aumento, peso_arista, self.inflacion, self.alpha)
    nuevo_precio = {nodo_vecino : {'precio':  (precio_actual * (1 + (aumento_vecino / 100)))}}
    nx.set_node_attributes(self.grafo, nuevo_precio)
    return aumento_vecino

  def _single_step(self):
    if self._curr_step % self.duracion_periodo == 0:
      self.actualizar_inflacion()

    if not self.queue.empty():
      nodo_actual, aumento = self.queue.get()
      vecinos = self.grafo[nodo_actual].items()
      aumentos_a_pasar = []
      for vecino in vecinos:
        aumento_vecino = self.actualizar(vecino,aumento) #Side effect actualiza ese vecino.
        aumentos_a_pasar.append(aumento_vecino)
      for i, vecino in enumerate(vecinos):
        self.queue.put((vecino[0], aumentos_a_pasar[i]))

  def actualizar_inflacion(self): 
      precios_periodo_actual = {}
      for nodo in self.grafo.nodes:
        precios_periodo_actual[nodo] = self.grafo.nodes[nodo]['precio']      
      self.inflacion = self._calc_inflacion(precios_periodo_actual.values(), self.precios_periodo_pasado.values())
      self.precios_periodo_pasado = precios_periodo_actual.copy()
  def _calcular_metricas(self):
    self.metricas_evaluadas['inflacion'].append(self.inflacion)
    for nombre, metrica in self.metricas.items():
          self.metricas_evaluadas[nombre].append(metrica(self.grafo))

  def __str__(self):
      return str(self.to_dict())

  def __repr__(self):
      return str(self)

  def to_dict(self):
      return {"id_grafo": hash(self.grafo), "step": self._curr_step, "metricas": self._metricas_evaluadas}
 

