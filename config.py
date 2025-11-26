# --- Configurações de Posições e Rótulos ---
UNIDADE_CUSTO = "km" 
ORIGEM = "Centro"
DESTINO = "Ubatiba"

# Posições fixas para manter a consistência visual em todos os gráficos
POSICOES_FIXAS = {
    "Centro": (0, 0),
    "Itaipuaçu": (1, 1),
    "Ponta Negra": (1, -1),
    "Cova da Onça": (2, 1),
    "Ubatiba": (3, 0)
}

# Definição das rotas (arestas) bidirecionais
ROTAS_SEM_CUSTO = [
    # Rotas de ida e volta
    ("Centro", "Itaipuaçu"),
    ("Itaipuaçu", "Centro"),
    ("Centro", "Ponta Negra"),
    ("Ponta Negra", "Centro"),
    ("Itaipuaçu", "Cova da Onça"),
    ("Cova da Onça", "Itaipuaçu"),
    ("Ponta Negra", "Ubatiba"),
    ("Ubatiba", "Ponta Negra"),
    ("Cova da Onça", "Ubatiba"),
    ("Ubatiba", "Cova da Onça"),
    ("Itaipuaçu", "Ponta Negra"),
    ("Ponta Negra", "Itaipuaçu"),
    ("Ponta Negra", "Cova da Onça"),
    ("Cova da Onça", "Ponta Negra")
]