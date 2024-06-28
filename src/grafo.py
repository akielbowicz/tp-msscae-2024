import itertools as it
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def armar_grafo(dataframe, precios_random=True):
  graph = {}
  for index, row in dataframe.iterrows():
    d = {}
    for (k, v) in row.items():
      d[k] = {"w":v}
    graph[index] = d
  G_base = nx.DiGraph(graph) #Cambio a digrafo para los plots
  G = nx.DiGraph(graph)
  for (n1,n2,d) in G_base.edges(data=True):
    if d['w'] == 0:
      G.remove_edge(n1,n2)

  nodos = list(G.nodes())
  precios = {}

  nuevo_precio = (lambda : np.random.randint(0,100)) if precios_random else (lambda:100)

  for nodo in nodos:
      precios[nodo] = {'precio': nuevo_precio()}
      
  nx.set_node_attributes(G, precios)
  return G


def plot_grafo(grafo, labels=True, grande=False, node_data=True,):
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    tamaños = list(grafo.degree())
    for i in range(len(tamaños)):
      tamaños[i] = (tamaños[i][1] ** 2) / 9 if ((tamaños[i][1] ** 2) / 9 ) > 100 else 100
    pos = nx.kamada_kawai_layout(grafo)
    if grande:
      fig, ax = plt.subplots(figsize=(30, 30))
    else:
      fig,ax = plt.subplots(figsize=(8,8))
    plt.axis("off")
    nx.draw_networkx_nodes(grafo, pos, node_size=tamaños, ax = ax)
    nx.draw_networkx_labels(grafo, pos, font_size=10, ax=ax)
    nx.draw_networkx_edges(
        grafo, pos, edge_color="grey", connectionstyle=connectionstyle, ax=ax, arrows=True, arrowstyle='->',
    )
    if labels:
      labels = {
          tuple(edge): f"{'w'}={round(attrs['w'],3)}"
          for *edge, attrs in grafo.edges(keys=True, data=True)
      }
      nx.draw_networkx_edge_labels(
          grafo,
          pos,
          labels,
          connectionstyle=connectionstyle,
          label_pos=0.3,
          font_color="blue",
          bbox={"alpha": 0},
          ax=ax,
      )
      labels = dict(grafo.nodes(data=True))
      for key in labels:
        labels[key] = labels[key]['precio']
      for key in pos:
        pos[key] = pos[key] + 0.05
      nx.draw_networkx_labels(
          grafo,
          pos,
          labels,
          font_size = 10,
          font_color="red",
          ax=ax,
      )

