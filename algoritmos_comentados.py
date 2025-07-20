import heapq
import numpy as np


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