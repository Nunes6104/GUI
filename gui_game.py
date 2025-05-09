#Ex 1
import tkinter as tk
janela = tk.Tk() # Cria a janela
janela.title("Mapa com Obstaculos") # Define o título da janela

texto = tk.Text(janela, width=40, height=15)
texto.pack()
frame_mapa = tk.Frame(janela)
frame_mapa.pack()

def ler_mapa(nome_ficheiro):
    with open(nome_ficheiro, "r") as f:
        return [linha.strip().split() for linha in f.readlines()]

def mostrar_mapa():
    texto.delete("1.0", tk.END) #"1.0" é a posição inicial (linha 1, caractere 0)
    for linha in mapa:
        texto.insert(tk.END, " ".join(linha) + "\n")

def mostrar_mapa_codificado():
    texto.delete("1.0", tk.END)
    for linha in mapa:
        nova = ["~" if c == "." else "X" if c == "#" else c for c in linha]
        texto.insert(tk.END, " ".join(nova) + "\n")

def mostrar_obstaculos():
    texto.delete("1.0", tk.END)
    total = 0
    for i, linha in enumerate(mapa):
        for j, c in enumerate(linha):
            if c == "#":
                texto.insert(tk.END, f"Obstaculo na posicao ({i},{j})\n")
                total += 1
    texto.insert(tk.END, f"\nTotal de obstaculos: {total}")
    
#Ex 2
def desenhar_grelha():
    texto.delete("1.0", tk.END)
    for i in range(10):
        for j in range(10):
            cor = "green" if mapa[i][j] == "." else "red"
            lbl = tk.Label(frame_mapa, width=2, height=1, bg=cor,
            relief="solid", borderwidth=1)
            lbl.grid(row=i, column=j, padx=1, pady=1) 

tk.Button(janela, text="Mostrar mapa original", command=mostrar_mapa).pack()
tk.Button(janela, text="Mostrar mapa codificado", command=mostrar_mapa_codificado).pack()
tk.Button(janela, text="Mostrar obstaculos", command=mostrar_obstaculos).pack()
tk.Button(janela, text="Mostrar mapa Gráfico", command=desenhar_grelha).pack()
tk.Button(janela, text="Sair", command=janela.destroy).pack()   

mapa = ler_mapa("mapa.txt") # lê o ficheiro
janela.mainloop() # inicia a interface