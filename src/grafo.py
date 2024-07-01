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
    return fig

# %%

def verGrafoCentralizado(df):
    fig, ax = plt.subplots(figsize=(40, 40))
    plt.axis("off")
    G = nx.DiGraph(df)

    centrality = nx.eigenvector_centrality(G, max_iter=1000)
    values = np.array(list(centrality.values()))
    norm_values = (values - values.min()) / (values.max() - values.min())

    colores_nodo = plt.cm.viridis(norm_values)

    grado_nodo = np.array([G.out_degree[i] for i in range(len(G))])
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
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Centralidad de autovectores', fontsize=15)
    plt.title('Visualización de la matriz Insumo Producto')

    plt.show()
    return fig


def verGrafoAbierto(df):
    fig, ax = plt.subplots(figsize=(25, 25))
    plt.axis("off")
    G = nx.DiGraph()
    N = len(df)

    # Agrego nodos.
    for i, col in enumerate(df.columns):
        G.add_node(col)

    grado_nodo = np.zeros(len(df))
    for i in range(len(df)):
        aristas = 0;
        for j in range(len(df)):
            if df.iloc[i, j] > 0.2:
                aristas = aristas + 1
        grado_nodo[i] = aristas
    tamaños_nodo = 400 + (grado_nodo * 200)
    edge_widths = []
    for i in range(N):
        for j in range(N):
            a = df.iloc[i, j]
            G.add_edge(df.columns[i], df.columns[j])
            width = a
            edge_widths.append(width)

    pos_nodos = nx.spring_layout(G)
    H = nx.DiGraph(df.to_numpy())
    centrality = nx.eigenvector_centrality(H, max_iter=1000)
    values = np.array(list(centrality.values()))
    norm_values = (values - values.min()) / (values.max() - values.min())
    colores_nodo = plt.cm.viridis(norm_values)

    nx.draw_networkx_nodes(G,
                           pos_nodos,
                           node_color=colores_nodo,
                           node_size=tamaños_nodo,
                           edgecolors=colores_nodo,
                           linewidths=10,
                           alpha=0.6,
                           ax=ax
                           )

    nx.draw_networkx_edges(G,
                           pos_nodos,
                           edge_color=colores_nodo,
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
                            font_size=10,
                            ax=ax
                            )

    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=values.min(), vmax=values.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Influencia', fontsize=10)
    plt.title('Grafo desenredado')

    plt.show()
    return fig


def verInflacion(df, precios_finales, precios_iniciales):
    fig, ax = plt.subplots(figsize=(25, 25))
    plt.axis("off")

    G = nx.DiGraph()
    N = len(df)

    # Agrego nodos.
    for i, col in enumerate(df.columns):
        G.add_node(col)
    edge_colors = []
    edge_widths = []
    for i in range(N):
        for j in range(N):
            a = df.iloc[i, j]
            G.add_edge(df.columns[i], df.columns[j])
            width = a
            edge_widths.append(width)

    grado_nodo = np.array([G.out_degree[(sector)] for sector in df.columns])
    price_changes = np.array(precios_finales) - np.array(precios_iniciales)

    max_change = max(price_changes)
    min_change = min(price_changes)
    norm_changes = (price_changes - min_change) / (max_change - min_change)

    colors = plt.cm.Reds(norm_changes)
    tamaños_nodo = 400 + (grado_nodo * 200)
    tamaños_nodo.tolist()

    pos_nodos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G,
                           pos_nodos,
                           node_color=colors,
                           node_size=tamaños_nodo,
                           edgecolors=colors,
                           linewidths=10,
                           alpha=1,
                           ax=ax
                           )

    nx.draw_networkx_edges(G,
                           pos_nodos,
                           edge_color='gray',
                           width=1,
                           arrows=True,
                           arrowsize=5,
                           alpha=0.6,
                           ax=ax,
                           arrowstyle='->',
                           node_size=10,
                           connectionstyle='arc3,rad=0.15')

    nx.draw_networkx_labels(G,
                            pos_nodos,
                            font_size=12,
                            ax=ax
                            )

    sm = plt.cm.ScalarMappable(cmap=plt.cm.Reds, norm=plt.Normalize(vmin=min_change, vmax=max_change))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Variación de precios', fontsize=10)
    plt.title('Variación de la inflación en los sectores')

    plt.show()
    return fig
