import networkx as nx
import random

def criar_grafo(cidades=None, chance_rota=0.6):
    if cidades is None:
        cidades = ["Armazem", "Cidade_A", "Cidade_B", "Cidade_C", "Cidade_D"]

    G = nx.DiGraph()

    for origem in cidades:
        for destino in cidades:
            if origem != destino and random.random() < chance_rota:
                custo = random.randint(5, 50)
                G.add_edge(origem, destino, weight=custo)
    return G, cidades