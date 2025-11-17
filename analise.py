import networkx as nx

def caminho_mais_curto(G, origem, destino):
    try:
        caminho = nx.shortest_path(G, origem, destino, weight="weight")
        custo = nx.shortest_path_length(G, origem, destino, weight="weight")
        print(f"Caminho mais curto de {origem} até {destino}: {caminho} (Custo: {custo})")
        return caminho, custo
    except nx.NetworkXNoPath:
        print(f"Nenhum caminho disponível de {origem} até {destino}.")
        return None, None

def analisar_robustez(G):
    print("\nAnálise de robustez da rede:")
    for edge in G.edges():
        G_temp = G.copy()
        G_temp.remove_edge(*edge)
        conectado = nx.is_strongly_connected(G_temp)
        status = "Rede ainda conectada" if conectado else "Rede desconectada"
        print(f"Estrada {edge}: {status}")