from grafo import criar_grafo
from utils import mostrar_grafo
from analise import caminho_mais_curto, analisar_robustez
from simulacao import simular_falha_aleatoria

if __name__ == "__main__":
    G, cidades = criar_grafo()

    mostrar_grafo(G, titulo="Rede de Transporte Aleatória")

    origem = "Armazem"
    destino = "Cidade_D"

    caminho, custo = caminho_mais_curto(G, origem, destino)
    mostrar_grafo(G, caminho, titulo="Caminho mais curto até Cidade_D")

    simular_falha_aleatoria(G, origem, destino)
    analisar_robustez(G)