#Pedro e Roberto
import numpy as np
import heapq
from typing import Tuple, List, Optional, Dict, Set
import time




def aEstrela(labirinto):
    """
    Algoritmo A star que encontra o caminho mímimo final

    Feito por Roberto e Pedro

    """

    inicio = time.time()
    print("Encontrando caminho final")
    #posição inicial fixa
    posicaoInicial = (1, 1)
    #posição final precisa ser buscada, é o elemento 3 na matriz do labirinto
    #np.where retorna uma tupla com os índices onde o elemento é encontrado
    procuraFinal = np.where(labirinto == 3)
    #converte
    posicaoFinal = (procuraFinal[0][0], procuraFinal[1][0])

    vetorAberto = [(0, 0, posicaoInicial)] 
    vetorFechado = set()  
    pais = {posicaoInicial: None}  
    gCustos = {posicaoInicial: 0} 
    
    historico = []
    altura, largura = labirinto.shape

    while vetorAberto:
        fAtual, gAtual, posicaoAtual = heapq.heappop(vetorAberto)

        if posicaoAtual in vetorFechado:
            continue 

        historico.append(posicaoAtual)
        vetorFechado.add(posicaoAtual)  

        if posicaoAtual == posicaoFinal:
            caminho = [] # declaro o caminho como uma lista vazia, nele vo armezenar o caminho percorrido
            atual = posicaoAtual
            while atual is not None:
                caminho.append(atual)
                atual = pais.get(atual) # lembrando que pai é implementado em um dicionário
            caminho.reverse()  # Inverte o caminho para obter a ordem correta
            print(f"Caminho mínimo encontrado em {time.time()- inicio}s")
            
            return caminho

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
            hNovo = abs(vizinho[0] - posicaoFinal[0]) + abs(vizinho[1] - posicaoFinal[1])
            fNovo = gNovo + hNovo

            # verifico se este é o melhor caminho para o vizinhança
            if vizinho not in gCustos or gNovo < gCustos[vizinho]:
                # Atualiza o custo g do vizinho
                gCustos[vizinho] = gNovo
                # Atualiza o pai do vizinho
                pais[vizinho] = posicaoAtual
                # Adiciona o vizinho ao vetor aberto
                heapq.heappush(vetorAberto, (fNovo, hNovo, vizinho))
    
    print("ERRO: Caminho final não encontrado")
    return []