import matplotlib.pyplot as plt
import networkx as nx

def mostrar_grafo(G, caminho=None, titulo="Rede de Transporte"):
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 7))

    cores = ["gold" if n == "Armazem" else "skyblue" for n in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=cores, node_size=2200, arrows=True)

    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="red")

    if caminho:
        edges = list(zip(caminho[:-1], caminho[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="green", width=3)

    plt.title(titulo)
    plt.show()