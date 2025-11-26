import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from grafo import criar_grafo, mostrar_grafo, caminho_mais_curto
from config import POSICOES_FIXAS


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Rede de Transporte")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e1e")

        self.G = None  # grafo original
        self.G_atual = None  # grafo atual (pode ter arestas removidas)
        self.origem = None
        self.destino = None
        self.caminho_atual = None
        self.modo_remocao = False  # Controla se está no modo de remoção

        self.frame_top = tk.Frame(root, bg="#1e1e1e", pady=10)
        self.frame_top.pack()

        # Combos
        tk.Label(self.frame_top, text="Origem:", fg="white", bg="#1e1e1e").grid(row=0, column=0)
        tk.Label(self.frame_top, text="Destino:", fg="white", bg="#1e1e1e").grid(row=0, column=2)

        nos = list(POSICOES_FIXAS.keys())

        self.combo_origem = ttk.Combobox(self.frame_top, values=nos, width=15)
        self.combo_destino = ttk.Combobox(self.frame_top, values=nos, width=15)

        self.combo_origem.grid(row=0, column=1, padx=5)
        self.combo_destino.grid(row=0, column=3, padx=5)

        # Botão Mostrar Rede
        self.btn_mostrar_rede = tk.Button(
            self.frame_top, text="Mostrar Rede", command=self.mostrar_rede,
            bg="#444", fg="white", padx=20, pady=5
        )
        self.btn_mostrar_rede.grid(row=0, column=4, padx=10)

        # Botão calcular rota
        self.btn_calcular = tk.Button(
            self.frame_top, text="Calcular Rota", command=self.calcular_rota,
            bg="#007acc", fg="white", padx=20, pady=5
        )
        self.btn_calcular.grid(row=0, column=5, padx=10)

        # Botão resetar rede
        self.btn_resetar = tk.Button(
            self.frame_top, text="Resetar Rede", command=self.resetar_rede,
            bg="#dc3545", fg="white", padx=20, pady=5
        )
        self.btn_resetar.grid(row=0, column=6, padx=10)

        # Label para instruções
        self.lbl_instrucao = tk.Label(
            self.frame_top, 
            text="Selecione origem e destino, depois clique em 'Calcular Rota'",
            fg="lightblue", bg="#1e1e1e"
        )
        self.lbl_instrucao.grid(row=1, column=0, columnspan=7, pady=5)

        # Figura
        self.fig = plt.Figure(figsize=(10, 5), facecolor="#212121")
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Conectar evento de clique
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def mostrar_rede(self):
        """Mostra a rede completa inicial"""
        self.G = criar_grafo()  # grafo original
        self.G_atual = self.G  # grafo que pode ser modificado
        self.caminho_atual = None
        self.modo_remocao = False
        
        mostrar_grafo(
            self.fig, self.G_atual, POSICOES_FIXAS, 
            caminho=None, 
            titulo="Rede de Transporte Completa"
        )
        self.canvas.draw()
        self.lbl_instrucao.config(
            text="Selecione origem e destino, depois clique em 'Calcular Rota'",
            fg="lightblue"
        )

    def calcular_rota(self):
        """Calcula a rota baseada na origem e destino selecionados"""
        if self.G_atual is None:
            messagebox.showwarning("Atenção", "Clique primeiro em 'Mostrar Rede'.")
            return

        self.origem = self.combo_origem.get()
        self.destino = self.combo_destino.get()

        if self.origem == "" or self.destino == "":
            messagebox.showwarning("Erro", "Escolha origem e destino.")
            return

        if self.origem == self.destino:
            messagebox.showwarning("Erro", "Origem e destino devem ser diferentes.")
            return

        # Calcular rota
        self.caminho_atual, custo = caminho_mais_curto(self.G_atual, self.origem, self.destino)

        if not self.caminho_atual:
            messagebox.showwarning("Falha", "Nenhum caminho disponível.")
            mostrar_grafo(
                self.fig, self.G_atual, POSICOES_FIXAS, None,
                f"Rede Atual - Nenhum caminho de {self.origem} para {self.destino}"
            )
            self.canvas.draw()
            return

        self.modo_remocao = True
        
        mostrar_grafo(
            self.fig, self.G_atual, POSICOES_FIXAS, self.caminho_atual,
            f"Rota: {self.origem} → {self.destino} ({custo} km)"
        )
        self.canvas.draw()
        
        self.lbl_instrucao.config(
            text="Agora clique em qualquer aresta para removê-la",
            fg="yellow"
        )

    def on_click(self, event):
        """Detecta clique em uma aresta para remoção imediata"""
        if not self.modo_remocao or self.G_atual is None or event.xdata is None or event.ydata is None:
            return

        # Procura a aresta mais próxima do clique
        aresta_encontrada = None
        min_dist = float('inf')
        
        for edge in list(self.G_atual.edges()):
            x1, y1 = POSICOES_FIXAS[edge[0]]
            x2, y2 = POSICOES_FIXAS[edge[1]]
            
            # Ponto médio da aresta
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            
            # Distância do clique ao ponto médio
            dist = ((event.xdata - mx) ** 2 + (event.ydata - my) ** 2) ** 0.5
            
            if dist < min_dist and dist < 0.3:
                min_dist = dist
                aresta_encontrada = edge

        if aresta_encontrada:
            # Remove a aresta imediatamente
            if self.G_atual.has_edge(*aresta_encontrada):
                self.G_atual.remove_edge(*aresta_encontrada)
                
                # Recalcular rota automaticamente se havia um caminho calculado
                if self.origem and self.destino and self.caminho_atual:
                    self.recalcular_apos_remocao(aresta_encontrada)
                else:
                    # Apenas atualiza o gráfico sem caminho
                    mostrar_grafo(
                        self.fig, self.G_atual, POSICOES_FIXAS, None,
                        f"Rede Atual - Aresta {aresta_encontrada} removida"
                    )
                    self.canvas.draw()

    def recalcular_apos_remocao(self, aresta_removida):
        """Recalcula a rota automaticamente após remoção de aresta"""
        if self.origem is None or self.destino is None:
            return

        # Tenta encontrar novo caminho
        novo_caminho, novo_custo = caminho_mais_curto(self.G_atual, self.origem, self.destino)

        if novo_caminho:
            self.caminho_atual = novo_caminho
            mostrar_grafo(
                self.fig, self.G_atual, POSICOES_FIXAS, novo_caminho,
                f"Rota Atualizada: {self.origem} → {self.destino} ({novo_custo} km)"
            )
            self.canvas.draw()
        else:
            self.caminho_atual = None
            mostrar_grafo(
                self.fig, self.G_atual, POSICOES_FIXAS, None,
                f"Sem caminho de {self.origem} para {self.destino}"
            )
            self.canvas.draw()
            messagebox.showwarning("Caminho Interrompido", 
                                 f"Não há mais caminho de {self.origem} para {self.destino}!")

    def resetar_rede(self):
        """Reseta a rede para o estado original"""
        if self.G is not None:
            self.G_atual = self.G.copy()
            self.caminho_atual = None
            self.modo_remocao = False
            mostrar_grafo(
                self.fig, self.G_atual, POSICOES_FIXAS, None,
                "Rede Resetada - Estado Original"
            )
            self.canvas.draw()
            self.lbl_instrucao.config(
                text="Selecione origem e destino, depois clique em 'Calcular Rota'",
                fg="lightblue"
            )
            messagebox.showinfo("Rede Resetada", "Todas as arestas foram restauradas!")
        else:
            messagebox.showwarning("Atenção", "Mostre a rede primeiro.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()