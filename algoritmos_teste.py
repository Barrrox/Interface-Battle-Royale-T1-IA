"""
Código com os algoritmos teste usados durante implementação da interface
"""
import random

def algoritmo_dfs(labirinto, inicio, fim):
    """Busca em Profundidade (Depth-First Search)"""
    historico = []
    pilha = [(inicio, [inicio])]
    visitados = set([inicio])
    
    while pilha:
        (pos_atual, caminho_parcial) = pilha.pop()
        
        
        # Adiciona a iteração ao histórico no formato pedido
        # (posição atual, células visitadas na iteração) - aqui, visitados é o conjunto total até agora
        historico.append(pos_atual)
        
        if pos_atual == fim:
            print("SUCESSO!")
            return historico # Sucesso
        
        (y, x) = pos_atual
        vizinhos = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
        random.shuffle(vizinhos) # Adiciona um pouco de aleatoriedade ao DFS

        for vizinho in vizinhos:
            (vy, vx) = vizinho
            if 0 <= vy < len(labirinto) and 0 <= vx < len(labirinto[0]) and labirinto[vy][vx] != 1 and vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append((vizinho, caminho_parcial + [vizinho]))
    
    print("FALHA!")
    return historico # Falha


def algoritmo_bfs(labirinto, inicio, fim):
    """Busca em Largura (Breadth-First Search)"""
    historico = []
    fila = [(inicio, [inicio])]
    visitados = set([inicio])
    
    while fila:
        (pos_atual, caminho_parcial) = fila.pop(0)
        
        # Alteração: Adiciona apenas a posição atual (tupla) ao histórico
        historico.append(pos_atual)
        
        if pos_atual == fim:
            # Alteração: Remove o append extra do caminho, pois o objetivo é retornar
            # apenas as posições visitadas. A posição final já foi adicionada acima.
            return historico

        (y, x) = pos_atual
        vizinhos = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]

        for vizinho in vizinhos:
            (vy, vx) = vizinho
            if 0 <= vy < len(labirinto) and 0 <= vx < len(labirinto[0]) and labirinto[vy][vx] != 1 and vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho_parcial + [vizinho]))
    
    return historico

def algoritmo_stub(labirinto, inicio, fim):
    """Um algoritmo 'bobo' para demonstração."""
    historico = []
    pos_atual = inicio
    visitados = set([inicio])
    
    while pos_atual != fim:
        # Alteração: Adiciona apenas a posição atual (tupla) ao histórico
        historico.append(pos_atual)
        (y, x) = pos_atual
        
        # Move-se na diagonal, se possível, de forma ineficiente
        if x < fim[1] and labirinto[y][x+1] != 1:
            x += 1
        elif y < fim[0] and labirinto[y+1][x] != 1:
            y += 1
        else: # Beco sem saída, termina
            break
            
        pos_atual = (y, x)

    # Alteração: Adiciona a posição final (ou a última posição antes de parar) ao histórico
    historico.append(pos_atual)
    return historico