import heapq
import numpy as np


"""
Algoritmo A*

Autores: Pedro e Roberto

"""
def aEstrelaAlg(labirinto):
    posicaoInicial = (1, 1)  # posição fixa inicial
    procuraFinal = np.where(labirinto == 3) # prucura a posição final
    posicaoFinal = (procuraFinal[0][0], procuraFinal[1][0]) # converte de array para tupla

    vetorAberto = [(0, 0, posicaoInicial)] # inicia a lista aberta com o nó inicial
    vetorFechado = set() # lista fechada para evitar repetição de nós
    gCustos = {posicaoInicial: 0}  # dicionário para armazenar os custos g dos nós
    
    historico = [] # lista para armazenar o histórico de posições visitadas
    altura, largura = labirinto.shape # obtém as dimensões do labirinto para verificação dos limites

    while vetorAberto: # laço principal do algoritmo
        fAtual, hAtual, posicaoAtual = heapq.heappop(vetorAberto) # remove o nó com menor custo f da lista aberta
        # fAtual e hAtual nao são utilizados, mas são necessários para manter a estrutura do heapq
        # apenas a posicaoAtual é utilizada para verificar que é utilizado para verificar a posição atual
        # verifica se a posição atual já foi visitada
        # se sim, ignora e continua com o próximo nó
        if posicaoAtual in vetorFechado: # se o nó já foi visitado, ignora
            continue 

        historico.append(posicaoAtual) # adiciona a posição atual ao histórico
        vetorFechado.add(posicaoAtual)  # adiciona a posição atual à lista fechada

        if posicaoAtual == posicaoFinal: # se a posição atual é a final, retorna o histórico
            return historico
            
        vizinhos = [] # lista para armazenar os vizinhos válidos
        x, y = posicaoAtual # obtém as coordenadas x e y da posição atual
        
        if x > 0 and labirinto[x-1, y] != 1: # verifica se o vizinho acima é válido
            vizinhos.append((x-1, y))
        
        if x < (altura - 1) and labirinto[x+1, y] != 1: # verifica se o vizinho abaixo é válido
            vizinhos.append((x+1, y))
        
        if y > 0 and labirinto[x, y-1] != 1: # verifica se o vizinho à esquerda é válido
            vizinhos.append((x, y-1))

        if y < (largura - 1) and labirinto[x, y+1] != 1: # verifica se o vizinho à direita é válido
            vizinhos.append((x, y+1))

        gAtual = gCustos[posicaoAtual] # obtém o custo g da posição atual

        for vizinho in vizinhos: # itera sobre os vizinhos válidos
            if vizinho in vetorFechado: # se o vizinho já foi visitado, ignora
                continue

            gNovo = gAtual + 1 # atualiza o custo g do vizinho

            if vizinho not in gCustos or gNovo < gCustos[vizinho]: # verifica se é o melhor caminho para o vizinho
                gCustos[vizinho] = gNovo # atualiza o custo g do vizinho
                # HEURÍSTICA: calcula o custo h (distância Manhattan) do vizinho até o destino
                hNovo = abs(vizinho[0] - posicaoFinal[0]) + abs(vizinho[1] - posicaoFinal[1]) 
                fNovo = gNovo + hNovo # calcula o custo f do vizinho
                heapq.heappush(vetorAberto, (fNovo, hNovo, vizinho)) # adiciona o vizinho à lista aberta com o novo custo f

    return historico # no caso de falha retorna o historico igual

"""
Algoritmo Greedy Best-First Search

Autores: Matheus Barros e André

"""
import heapq # É necessário importar a biblioteca heapq para usar a fila de prioridade (min-heap).

def algoritmo_gbfs(labirinto):
    # Cria uma cópia do labirinto para evitar modificar o original.
    copia_labirinto = labirinto.copy()
    
    # Obtém as dimensões do labirinto
    altura = len(copia_labirinto)
    largura = len(copia_labirinto[0])
    
    # Inicializa as coordenadas do ponto final (objetivo) como None.
    fim_0, fim_1 = None, None
    
    # Procura pela posição do fim (valor 3) na última linha do labirinto.
    # Esta busca é otimizada para verificar apenas as paredes e também para
    # procurar apenas até encontrar o fim, encerrando o loop em seguida
    for x in range(largura):
        if copia_labirinto[altura - 1][x] == 3:
            fim_0 = altura - 1 
            fim_1 = x
            break # Encerra o loop assim que encontrar o fim.
    # Se o fim não foi encontrado na última linha, procura na última coluna.
    if fim_0 is None:
        for y in range(altura):
            if copia_labirinto[y][largura - 1] == 3:
                fim_0 = y
                fim_1 = largura - 1
                break # Encerra o loop assim que encontrar o fim.

    # historico armazena o percurso percorrido pelo algoritmo
    historico = []
    
    # 'conjunto_aberto' é uma lista que será tratada como fila de prioridade 
    # para armazenar os nós a serem explorados.
    # 
    # Cada elemento é uma tupla: (valor_heuristico, (y, x)).
    # Começamos com o ponto inicial (1,1) e um valor heurístico 
    # inicial (None, que será tratado como 0 pelo heap).
    conjunto_aberto = [(None, (1,1))]
    
    # Loop enquanto existirem nós abertos
    while conjunto_aberto:
        # Extrai o nó com o menor valor heurístico da fila de prioridade.
        _, pos_atual = heapq.heappop(conjunto_aberto)
        (y, x) = pos_atual
        
        # Adiciona a posição atual ao histórico e marca como parede
        # para evitar revisitá-la (funcionando como um "conjunto fechado").
        historico.append(pos_atual)
        copia_labirinto[y][x] = 1 
        
        # Para cada vizinho da posição atual (direita, baixo, cima, esquerda).
        for vizinho in [(y, x+1), (y+1, x), (y-1, x), (y, x-1)]:
            (vy, vx) = vizinho
            
            # Verifica se o vizinho não é uma parede (ou uma célula já visitada).
            if copia_labirinto[vy][vx] != 1:
                # Se o vizinho for a posição final, encontrou o fim
                if vy == fim_0 and vx == fim_1:
                    return historico
                
                # Adiciona o vizinho ao conjunto aberto com seu valor heuristico
                heapq.heappush(conjunto_aberto, ((vizinho[0] - fim_0)**2 + (vizinho[1] - fim_1)**2, vizinho))

    # se chegou até aqui então FALHOU
    # Se o loop terminar, significa que o conjunto aberto está vazio
    # e o fim não foi alcançado.
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