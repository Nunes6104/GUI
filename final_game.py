import random
import tkinter as tk # Importa a biblioteca gráfica
janela = tk.Tk() # Cria a janela principal
janela.title("Mapa Visual com Obstáculos") # Define o título
janela.geometry("400x450") # Define o tamanho da janela
frame_mapa = tk.Frame(janela) # Cria um frame para colocar os elementos
frame_mapa.pack() # Adiciona o frame à janela

caixa_mensagens = tk.Text(janela, width=40, height=2, state="disabled", wrap="word")
caixa_mensagens.pack(pady=10)
def escrever_mensagem(mensagem):
    caixa_mensagens.config(state="normal")  # Permite escrever
    caixa_mensagens.insert(tk.END, mensagem)
    caixa_mensagens.config(state="disabled")  # Bloqueia edição
    caixa_mensagens.see(tk.END)  # Faz scroll até à última linha

def ler_mapa(nome_ficheiro):
    with open(nome_ficheiro, "r") as f:
        return [linha.strip().split() for linha in f.readlines()]
    
labels = [] # Células do mapa (Labels)
inicio = None # Ponto inicial
fim = None # Ponto final
estado = "inicio" # Estado da definição (início ou fim)
jogando = False # Está a jogar?
pos_jogador = None # Posição atual do jogador
modo = "editar" # Modo atual: editar, definir ou jogar
cont = 0 #contador de cliques no jogo

def mostrar_mapa():
    for i in range(10):
        for j in range(10):
            cor = "green" if mapa[i][j] == "." else "red"
            lbl = tk.Label(frame_mapa, width=2, height=1, bg=cor,
            relief="solid", borderwidth=1)
            lbl.grid(row=i, column=j, padx=1, pady=1) 

def clicar(i, j):
    global inicio, fim, estado, jogando, pos_jogador, modo, cont
    if modo == "editar": 
        alternar_celula(i, j) # altera entre livre e obstáculo
        cont = 0
        return
    if modo == "definir":
        if mapa[i][j] == "#":
            return # não permite início/fim em obstáculo
        if estado == "inicio":
            inicio = (i, j) # define ponto inicial
            labels[i][j].config(bg="blue")
            estado = "fim"
        elif estado == "fim":
            fim = (i, j) # define ponto final
            labels[i][j].config(bg="orange")
            estado = "feito"
            comecar_jogo()
        cont = 0
        return
    if modo == "jogar" and jogando:
        # só permite mover para células livres adjacentes
        if abs(i - pos_jogador[0]) + abs(j - pos_jogador[1]) == 1 and mapa[i][j] == ".":
            labels[pos_jogador[0]][pos_jogador[1]].config(bg= random.choice(["lightblue", "lightyellow"])) #marca caminho
            pos_jogador = (i, j)
            cont += 1
            labels[i][j].config(bg="blue") # nova posição
            if pos_jogador == fim:
                labels[i][j].config(bg="purple") # chegou ao fim
                escrever_mensagem(f"\nChegou ao fim!!Usou {cont + 1} cliques para chegar ao destino")
                cont = 0
                
#criar alterar entre obstaculo livre
def alternar_celula(i, j):   
    if mapa[i][j] == "#":
            labels[i][j].config(bg="green") # nova posição
            mapa[i][j] = "."
    else:
        labels[i][j].config(bg="red") # nova posição
        mapa[i][j] = "#"
                            
def desenhar_grelha():
    labels.clear() # limpa grelha anterior
    for i in range(10):
        linha = []
        for j in range(10):
            cor = "green" if mapa[i][j] == "." else "red" # livre ou obstáculo
            lbl = tk.Label(frame_mapa, width=2, height=1, bg=cor,
            relief="solid", borderwidth=1)
            lbl.grid(row=i, column=j, padx=1, pady=1) # posiciona na grelha
            lbl.bind("<Button-1>", lambda e, x=i, y=j: clicar(x, y)) # liga ao clique
            linha.append(lbl)
        labels.append(linha) # adiciona linha à grelha

def comecar_jogo():
    global jogando, pos_jogador, modo
    if inicio and fim:
        modo = "jogar"
        jogando = True
        pos_jogador = inicio
        escrever_mensagem("\nJogo iniciado. Clique ao lado do jogador para mover.")
        
def reiniciar():
    global inicio, fim, estado, jogando, pos_jogador, modo
    inicio = fim = None
    estado = "inicio"
    jogando = False
    pos_jogador = None
    modo = "editar"
    for i in range(10):
        for j in range(10):
            if mapa[i][j] == ".":
                labels[i][j].config(bg="green")
            elif mapa[i][j] == "#":
                labels[i][j].config(bg="red")
                
def clearAll():
    global inicio, fim, estado, jogando, pos_jogador, modo, cont
    inicio = fim = None
    estado = "inicio"
    jogando = False
    pos_jogador = None
    modo = "editar"
    for i in range(10):
        for j in range(10):
            labels[i][j].config(bg="green")
            mapa[i][j] = "."

def ativar_edicao():
    global modo
    if modo == "jogar":
        for i in range(10):
            for j in range(10):
                if mapa[i][j] == ".":
                    labels[i][j].config(bg="green")
                elif mapa[i][j] == "#":
                    labels[i][j].config(bg="red")
    modo = "editar"
    escrever_mensagem("\n\nModo de edição ativado.")
    
def ativar_definicao():
    global modo, estado
    modo = "definir"
    estado = "inicio"
    escrever_mensagem("\nModo de definição ativado. Clique em início e depois em fim.")
    
tk.Button(janela, text="Definir Inicio/Fim", command=ativar_definicao).place(x=25, y=300)
tk.Button(janela, text="Começar Jogo", command=comecar_jogo).place(x=165, y=300)
tk.Button(janela, text="Editar Mapa", command=ativar_edicao).place(x=300, y=300)
tk.Button(janela, text="Reiniciar Jogo", command=reiniciar).place(x=25, y=350)
tk.Button(janela, text="Clear All", command=clearAll).place(x=175, y=350)


mapa = ler_mapa("mapa.txt") # lê o ficheiro
desenhar_grelha()
janela.mainloop() # inicia a interface