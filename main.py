# main.py

from config import ORIGEM, DESTINO, POSICOES_FIXAS
from grafo import criar_grafo, mostrar_grafo, caminho_mais_curto, simular_falha_no_caminho

# ============================================================
# EXECUÇÃO PRINCIPAL E ANÁLISE
# ============================================================
def executar_analise():
    """Sequência principal de execução do cálculo de rotas e simulação de falha."""
    
    # 1. Criação do grafo (com custos randomizados e fixados para esta execução)
    G_original = criar_grafo()
    
    # 2. Mostrar rede inicial
    print("\n--- PARTE 1: REDE ORIGINAL ---")
    mostrar_grafo(G_original, POSICOES_FIXAS, titulo="1. Rede de Transporte Inicial (Todas as Rotas)")

    # 3. Calcular o primeiro caminho (Rota 1)
    print("\n--- PARTE 2: CÁLCULO DA ROTA 1 ---")
    caminho_inicial, custo_inicial = caminho_mais_curto(G_original, ORIGEM, DESTINO)
    
    if caminho_inicial:
        mostrar_grafo(G_original, POSICOES_FIXAS, caminho_inicial, titulo="2. Rota 1: Caminho Mais Curto Original")

        # 4. Simular Falha no primeiro trecho da Rota 1
        G_falha, aresta_removida = simular_falha_no_caminho(G_original, caminho_inicial)

        # 5. Recalcular o novo caminho após a falha (Rota 2)
        print("\n--- PARTE 3: SIMULAÇÃO DE FALHA E ROTA 2 ---")
        if G_falha and aresta_removida:
            print(f"Falha Simulada: Estrada removida: {aresta_removida[0]} -> {aresta_removida[1]}")
            
            novo_caminho, novo_custo = caminho_mais_curto(G_falha, ORIGEM, DESTINO)
            
            # 6. Mostrar nova rede com Rota 2 e análise de impacto
            if novo_caminho:
                mostrar_grafo(G_falha, POSICOES_FIXAS, novo_caminho, titulo=f"3. Rota 2: Alternativa após Falha em {aresta_removida}")
                
                print("\n--- Análise de Impacto ---")
                print(f"Custo Original (Rota 1): {custo_inicial}")
                print(f"Custo Alternativo (Rota 2): {novo_custo}")
                print(f"Aumento no Custo: {novo_custo - custo_inicial} unidades")
                print("Robustez: Uma rota alternativa foi encontrada com sucesso.")
            else:
                mostrar_grafo(G_falha, POSICOES_FIXAS, titulo=f"3. Rede Inacessível após Falha em {aresta_removida}")
                print("A rede falhou: Nenhum caminho alternativo encontrado. Ponto de falha é crítico.")

if __name__ == "__main__":
    executar_analise()