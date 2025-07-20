"""
Código com os algoritmos teste usados durante implementação da interface
"""
import numpy as np
import heapq
import numpy as np


"""
Algoritmo A*

Autores: Pedro e Roberto

"""
def aEstrelaAlg(labirinto):
    posicaoInicial = (1, 1)  
    procuraFinal = np.where(labirinto == 3)
    posicaoFinal = (procuraFinal[0][0], procuraFinal[1][0])

    vetorAberto = [(0, 0, posicaoInicial)] 
    vetorFechado = set()  
    pais = {posicaoInicial: None}  
    gCustos = {posicaoInicial: 0} 
    
    historico = []
    altura, largura = labirinto.shape

    while vetorAberto:
        fAtual, hAtual, posicaoAtual = heapq.heappop(vetorAberto)

        if posicaoAtual in vetorFechado:
            continue 

        historico.append(posicaoAtual)
        vetorFechado.add(posicaoAtual)  

        if posicaoAtual == posicaoFinal:
            return historico
            
        vizinhos = []
        x, y = posicaoAtual
        
        if x > 0 and labirinto[x-1, y] != 1:
            vizinhos.append((x-1, y))
        # Depois pra baixo
        if x < (altura - 1) and labirinto[x+1, y] != 1:
            vizinhos.append((x+1, y))
        # Depois pra esquerda
        if y > 0 and labirinto[x, y-1] != 1:
            vizinhos.append((x, y-1))
        # Depois pra direita
        if y < (largura - 1) and labirinto[x, y+1] != 1:
            vizinhos.append((x, y+1))
        
        gAtual = gCustos[posicaoAtual]
        
        for vizinho in vizinhos:
            if vizinho in vetorFechado:
                continue

            # Calcula o custo g do vizinho
            gNovo = gAtual + 1  # Custo de mover para o vizinho

            # verifico se este é o melhor caminho para o vizinhança
            if vizinho not in gCustos or gNovo < gCustos[vizinho]:
                # Atualiza o custo g do vizinho
                gCustos[vizinho] = gNovo
                # Atualiza o pai do vizinho
                pais[vizinho] = posicaoAtual
                # HEURISTICA
                hNovo = abs(vizinho[0] - posicaoFinal[0]) + abs(vizinho[1] - posicaoFinal[1])
                fNovo = gNovo + hNovo
                
                # Adiciona o vizinho ao vetor aberto
                heapq.heappush(vetorAberto, (fNovo, hNovo, vizinho))
    return historico

"""
Algoritmo Greedy Best-First Search

Autores: Matheus Barros e André

"""
def algoritmo_gbfs(labirinto):
    copia_labirinto = labirinto.copy()
    altura = len(copia_labirinto)
    largura = len(copia_labirinto[0])
    fim_0, fim_1 = None, None
    for x in range(largura):
        if copia_labirinto[altura - 1][x] == 3:
            fim_0 = altura - 1 
            fim_1 = x
            break
    if fim_0 is None:
        for y in range(altura):
            if copia_labirinto[y][largura - 1] == 3:
                fim_0 = y
                fim_1 = largura - 1
                break
    historico = []
    conjunto_aberto = [(None, (1,1))]
    while conjunto_aberto:
        _, pos_atual = heapq.heappop(conjunto_aberto)
        (y, x) = pos_atual
        historico.append(pos_atual)
        copia_labirinto[y][x] = 1
        for vizinho in [(y, x+1),(y+1, x),(y-1, x),(y, x-1)]:
            (vy, vx) = vizinho
            if copia_labirinto[vy][vx] != 1:
                if vy == fim_0 and vx == fim_1:
                    return historico
                heapq.heappush(conjunto_aberto, ((vizinho[0] - fim_0)**2 + (vizinho[1] - fim_1)**2, vizinho))
    print("FALHA: Caminho não encontrado!")
    return historico


"""
Algoritmo Depth First Search

Autores: Hermes e Rafael

"""

def encontrarFim(Labirinto, MaxLinha, MaxColuna):
    l = int(round(MaxLinha / 2, 0))
    c = int(round(MaxColuna / 2, 0))

    for i in range(l, MaxLinha):
      for j in range(c, MaxColuna):
        if Labirinto[i][j] == 3: # Chegada
          return (i, j)

def PreManhattan(max_linhas, max_colunas, destino):
    Fy, Fx = destino
    return [[abs(y - Fy) + abs(x - Fx)           # tabela inteira
             for x in range(max_colunas)]
             for y in range(max_linhas)]

def DFS(Labirinto):
    Historico = []
    Pilha = []
    push = Pilha.append
    pop = Pilha.pop

    MaxLinha = len(Labirinto)
    MaxColuna = len(Labirinto[0])

    DirecaoLinha = [1, 0, 0, -1]
    DirecaoColuna = [0, 1, -1, 0]

    Final = encontrarFim(Labirinto, MaxLinha, MaxColuna)
    H = PreManhattan(MaxLinha, MaxColuna, Final)

    Historico.append((1, 1))

    Baixo  = -1        
    if Labirinto[2][1] not in (1, 4):          
        Baixo = H[2][1]

    Direita = -1
    if Labirinto[1][2] not in (1, 4): 
        Direita= H[1][2]

    # empilha primeiro a direção com heurística MAIOR
    if Baixo >= Direita:
        if Baixo >= 0: 
          push((2, 1)) 
        if Direita >= 0: 
          push((1, 2)) 
    else:
        push((1, 2))
        if Baixo >= 0: 
          push((2, 1))

    while len(Pilha) > 0: # pilha não vazia
        LinhaAtual, ColunaAtual = pop()
        Historico.append((LinhaAtual, ColunaAtual))
        Labirinto[LinhaAtual][ColunaAtual] = 4

        # Baixo, Direita, Esquerda, Cima
        Vizinhos = []

        for IndiceDirecao in range(4): # DFS (4 direções)
            LinhaAdjacente = LinhaAtual + DirecaoLinha[IndiceDirecao] 
            ColunaAdjacente = ColunaAtual + DirecaoColuna[IndiceDirecao]

            if Labirinto[LinhaAdjacente][ColunaAdjacente] in (1, 4): # Antigo Is verify pula se for parede ou andado
                continue

            if (LinhaAdjacente, ColunaAdjacente) == Final:
              Historico.append((LinhaAdjacente, ColunaAdjacente))
              return (Historico)

            Vizinhos.append((H[LinhaAdjacente][ColunaAdjacente], IndiceDirecao, LinhaAdjacente, ColunaAdjacente))

        Vizinhos.sort(key=lambda t: (-t[0], t[1])) 

        for _, IndiceDirecao, LinhaAdjacente, ColunaAdjacente in Vizinhos:
          push((LinhaAdjacente, ColunaAdjacente))   