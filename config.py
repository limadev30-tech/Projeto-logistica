# --- Configurações de Posições e Rótulos ---
UNIDADE_CUSTO = "unidades" 
ORIGEM = "Armazem"
DESTINO = "Cidade_D"

# Posições fixas para manter a consistência visual em todos os gráficos
POSICOES_FIXAS = {
    "Armazem": (0, 0),
    "Cidade_A": (1, 1),
    "Cidade_B": (1, -1),
    "Cidade_C": (2, 1),
    "Cidade_D": (3, 0)
}

# Definição das rotas (arestas) sem custos para a criação do grafo
ROTAS_SEM_CUSTO = [
    ("Armazem", "Cidade_A"),
    ("Armazem", "Cidade_B"),
    ("Cidade_A", "Cidade_C"),
    ("Cidade_B", "Cidade_D"),
    ("Cidade_C", "Cidade_D"),
    ("Cidade_A", "Cidade_B"),
    ("Cidade_B", "Cidade_C")
]