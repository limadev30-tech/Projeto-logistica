import networkx as nx
import matplotlib.pyplot as plt
import copy
import random
from config import UNIDADE_CUSTO, ORIGEM, DESTINO, ROTAS_SEM_CUSTO


def formatar_label(nome):
    partes = nome.split()
    if len(partes) > 1:
        meio = len(partes) // 2
        return " ".join(partes[:meio]) + "\n" + " ".join(partes[meio:])
    return nome


def criar_grafo():
    """Cria um grafo bidirecional com custos aleatórios."""
    G = nx.DiGraph()

    print("--- Custos Gerados Nesta Execução ---")
    for origem, destino in ROTAS_SEM_CUSTO:
        custo = random.randint(10, 50)
        G.add_edge(origem, destino, weight=custo)
        print(f"{origem} -> {destino} = {custo}")

    return G


def mostrar_grafo(fig, G, pos, caminho=None, titulo="Rede de Transporte"):
    """Desenha o grafo DENTRO da figura usada no Tkinter."""
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_facecolor("#212121")

    # Cores dos nós
    cores = []
    for n in G.nodes():
        if caminho and n in caminho:
            if n == caminho[0]:  # origem
                cores.append("#FFC800")  # amarelo
            elif n == caminho[-1]:  # destino
                cores.append("#00935B")  # verde
            else:  # nós no caminho
                cores.append("#FF6B6B")  # vermelho claro
        else:
            cores.append("#1E90FF")  # azul para outros nós

    labels_formatados = {n: formatar_label(n) for n in G.nodes()}

    # Desenhar nós
    nx.draw_networkx_nodes(G, pos, node_color=cores, node_size=4400, ax=ax, edgecolors="white", linewidths=2)
    nx.draw_networkx_labels(G, pos, labels=labels_formatados, font_weight="bold", ax=ax, font_size=8)
    
    # Desenhar arestas
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, edge_color="gray", width=2, ax=ax)

    # Labels das arestas (apenas para arestas existentes)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="red", ax=ax, font_size=8)

    # Destacar caminho se existir
    if caminho:
        edges_caminho = list(zip(caminho[:-1], caminho[1:]))
        nx.draw_networkx_edges(
            G, pos, edgelist=edges_caminho, 
            width=4, edge_color="green", ax=ax, 
            arrowstyle="->", arrowsize=25
        )

    ax.set_title(titulo, color="white", fontsize=12, pad=20)
    ax.axis("off")

    # Adicionar legenda apenas se há um caminho
    if caminho:
        ax.text(0.02, 0.98, "• Origem: Amarelo\n• Destino: Verde\n• Caminho: Vermelho", 
                transform=ax.transAxes, color="white", fontsize=9,
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7))


def caminho_mais_curto(G, origem, destino):
    try:
        caminho = nx.dijkstra_path(G, origem, destino, weight='weight')
        custo = nx.dijkstra_path_length(G, origem, destino, weight='weight')
        return caminho, custo
    except nx.NetworkXNoPath:
        return None, None


def simular_falha_no_caminho(G_original, caminho):
    """Remove exatamente UMA aresta real da rota gerada."""
    if not caminho or len(caminho) < 2:
        return None, None

    G_falha = copy.deepcopy(G_original)

    arestas = [(caminho[i], caminho[i + 1]) for i in range(len(caminho) - 1)]

    aresta_removida = random.choice(arestas)

    if G_falha.has_edge(*aresta_removida):
        G_falha.remove_edge(*aresta_removida)

    return G_falha, aresta_removida