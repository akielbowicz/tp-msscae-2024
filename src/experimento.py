
import queue
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
 

def plot_inflaciones(inflaciones, sectores, aumento, umbral_label=0.5):
    fig, (ax,ax2) = plt.subplots(1,2,figsize=(22, 10))
    ax.set_title(f"Valor de la inflación en el tiempo, a partir de un shock de {aumento}% \n para todos los sectores.")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Porcentaje de inflación")
    ax2.set_title(f"Variación de la inflación en el tiempo, a partir de un shock de {aumento}%, \n para todos los sectores.")
    ax2.set_xlabel("Tiempo")
    ax2.set_ylabel("Variación en el porcentaje de inflación")
    for i, inflacion in enumerate(inflaciones):
        tiempo = range(0,len(inflacion))
        if (max(inflacion) > umbral_label):
            ax.plot(tiempo, inflacion, label=sectores[i])
            ax2.plot(tiempo[1:],np.diff(inflacion), label=sectores[i])
        else:
            ax.plot(tiempo, inflacion)
            ax2.plot(tiempo[1:],np.diff(inflacion))
    ax.legend()
    ax2.legend()
    # plt.show()
    return fig

def verEvolucion(df, alfa):
    df = df.T
    df_diff = df.diff().dropna()
    window_size = 5  # Tamaño de la ventana para la media móvil
    df['mean'] = df.mean(axis=1).rolling(window=window_size).mean()
    df['max'] = df.max(axis=1)
    df['min'] = df.min(axis=1)
    df_diff['mean_diff'] = df_diff.mean(axis=1).rolling(window=window_size).mean()
    df_diff['max_diff'] = df_diff.max(axis=1)
    df_diff['min_diff'] = df_diff.min(axis=1)
    
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
    a = len(df)//10
    
    # Gráfico para datos absolutos
    axes[0].fill_between(df.index, df['min'], df['max'], color='red', alpha=0.3, label='Rango (Mín-Máx)')
    axes[0].plot(df.index, df['mean'], color='red', linewidth=2, label='Media Móvil')
    axes[0].set_title(f'Inflación Absoluta en 123 simulaciones para {alfa}')
    axes[0].set_xlabel('Tiempo en cantidad de iteraciones')
    axes[0].set_ylabel('Inflación absoluta')
    axes[0].set_xticks(df.index[::a])
    axes[0].legend()

    
    # Gráfico para diferencias de inflación
    axes[1].fill_between(df_diff.index, df_diff['min_diff'], df_diff['max_diff'], color='red', alpha=0.3, label='Rango (Mín-Máx)')
    axes[1].plot(df_diff.index, df_diff['mean_diff'], color='red', linewidth=2, label='Media Móvil')
    axes[1].set_title(f'Variación de inflación en 123 simulaciones para {alfa}')
    axes[1].set_xlabel('Tiempo en cantidad de iteraciones')
    axes[1].set_ylabel('Variación de Inflación')
    axes[1].set_xticks(df_diff.index[::a])
    axes[1].legend()

    
    # Ajustar el layout
    plt.tight_layout()
    
    # Mostrar los gráficos
    # plt.show()
    return fig