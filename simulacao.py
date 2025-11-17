import random
import networkx as nx
from utils import mostrar_grafo

def simular_falha_aleatoria(G, origem, destino):
    if not G.edges:
        print("Grafo sem estradas para simular falha.")
        return

    todas_arestas = list(G.edges())
    falha = random.choice(todas_arestas)
    print(f"Falha aleatória na estrada {falha}.")

    G_temp = G.copy()
    G_temp.remove_edge(*falha)

    mostrar_grafo(G_temp, titulo=f"Rede após falha em {falha}")

    try:
        caminho_alt = nx.shortest_path(G_temp, origem, destino, weight="weight")
        custo_alt = nx.shortest_path_length(G_temp, origem, destino, weight="weight")
        print(f"Rota alternativa: {caminho_alt} (Custo: {custo_alt})")
        mostrar_grafo(G_temp, caminho_alt, titulo="Rota alternativa após falha")
    except nx.NetworkXNoPath:
        print("Nenhuma rota alternativa disponível.")