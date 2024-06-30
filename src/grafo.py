import itertools as it
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import quantecon_book_networks
import quantecon_book_networks.input_output as qbn_io
import quantecon_book_networks.plotting as qbn_plt
import quantecon_book_networks.data as qbn_data

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


# %%
def verGrafoCentralizado(G,df):
    ig, ax = plt.subplots(figsize=(40, 40))
    plt.axis("off")
    N = len(G)
    centrality = nx.eigenvector_centrality(G, max_iter=1000)  # Funcion para sacar colores lindos para el grafo.
    values = np.array(list(centrality.values()))
    norm_values = (values - values.min()) / (values.max() - values.min())

    colores_nodo = plt.cm.viridis(norm_values)

    grado_nodo = np.array([G.out_degree[(sector)] for sector in df.columns])
    tamaños_nodo = 400 + (grado_nodo * 200)
    edge_widths = qbn_io.normalise_weights(qbn_io.edge_weights(G), 10)

    node_colors = qbn_io.colorise_weights(list(centrality), beta=False)
    node_to_color = dict(zip(G.nodes, node_colors))
    edge_colors = []
    for src, _ in G.edges:
        edge_colors.append(node_to_color[src])

    pos_nodos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G,
                           pos_nodos,
                           node_color=colores_nodo,
                           node_size=tamaños_nodo,
                           edgecolors='grey',
                           linewidths=10,
                           alpha=0.6,
                           ax=ax
                           )

    nx.draw_networkx_edges(G,
                           pos_nodos,
                           edge_color=edge_colors,
                           width=edge_widths,
                           arrows=True,
                           arrowsize=5,
                           alpha=0.6,
                           ax=ax,
                           arrowstyle='->',
                           node_size=10,
                           connectionstyle='arc3,rad=0.15')

    nx.draw_networkx_labels(G,
                            pos_nodos,
                            font_size=17,
                            ax=ax,
                            labels=None
                            )

    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=values.min(), vmax=values.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, font_size=15)
    cbar.set_label('Influencia', font_size=15)

    plt.show()