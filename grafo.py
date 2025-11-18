# grafo_funcoes.py

import networkx as nx
import matplotlib.pyplot as plt
import copy
import random
from config import UNIDADE_CUSTO, ORIGEM, DESTINO, ROTAS_SEM_CUSTO # Importa do config.py

# ============================================================
# CRIAÇÃO E MODELAGEM DO GRAFO
# ============================================================
def criar_grafo():
    """Cria um grafo direcionado e ponderado com custos randomizados."""
    
    G = nx.DiGraph()
    
    print("--- Custos Gerados Nesta Execução ---")
    for origem, destino in ROTAS_SEM_CUSTO:
        # Custo gerado aleatoriamente e fixado para esta execução (10 a 50)
        custo = random.randint(10, 50) 
        G.add_edge(origem, destino, weight=custo)
        print(f"Custo: {origem} -> {destino} = {custo}")
    
    return G

# ============================================================
# VISUALIZAÇÃO E SIMULAÇÃO
# ============================================================
def mostrar_grafo(G, pos, caminho=None, titulo="Rede de Transporte"):
    """Visualiza o grafo usando NetworkX e Matplotlib."""
    plt.figure(figsize=(10, 7))
    
    cores = ["gold" if n == ORIGEM else "skyblue" for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=cores, node_size=2200)
    nx.draw_networkx_labels(G, pos, font_weight='bold')
    
    # Desenha todas as arestas
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color="gray", width=1.5)
    
    # Adicionar labels de peso (custos)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color="red")
    
    # Destacar o caminho (Rota 1 ou Rota 2)
    if caminho:
        edges = list(zip(caminho[:-1], caminho[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="green", width=3)
    
    plt.title(titulo)
    plt.axis('off')
    plt.show()

def caminho_mais_curto(G, origem, destino):
    """Calcula o caminho e o custo mínimo usando o algoritmo de Dijkstra."""
    try:
        caminho = nx.dijkstra_path(G, origem, destino, weight='weight')
        custo = nx.dijkstra_path_length(G, origem, destino, weight='weight')
        print(f"Caminho mais curto de {origem} até {destino}: {' -> '.join(caminho)} (Custo: {custo} {UNIDADE_CUSTO})")
        return caminho, custo
    except nx.NetworkXNoPath:
        print(f"AVISO: Nenhum caminho disponível de {origem} até {destino}.")
        return None, None

def simular_falha_no_caminho(G_original, caminho_a_falhar):
    """Cria uma cópia do grafo, remove o primeiro trecho do caminho e retorna o novo grafo."""
    if not caminho_a_falhar or len(caminho_a_falhar) < 2:
        return None, None

    G_falha = copy.deepcopy(G_original)
    
    origem_falha = caminho_a_falhar[0]
    destino_falha = caminho_a_falhar[1]
    aresta_removida = (origem_falha, destino_falha)

    if G_falha.has_edge(origem_falha, destino_falha):
        G_falha.remove_edge(origem_falha, destino_falha)
        return G_falha, aresta_removida
    else:
        return G_falha, None