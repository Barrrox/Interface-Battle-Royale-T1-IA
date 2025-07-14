"""
Código redesenhado pelo gemini para implementar a função gerar_labirinto_kruskal(width, height)
que cria e retorna um labrinto em forma de matriz, seguindo o algoritmo de Kruskal

"""

import random
import numpy as np
import parametros
import time


class DisjointSet:
    """
    Estrutura de dados para o algoritmo de Kruskal.
    Ajuda a verificar se duas células já estão conectadas.
    Não necessita de alterações.
    """
    def __init__(self, nodes):
        self.node_mapping = {}
        for i, val in enumerate(nodes):
            n = self.DSNode(val, i)
            self.node_mapping[val] = n

    def find(self, node):
        return self.find_node(node).parent

    def find_node(self, node):
        if type(self.node_mapping[node].parent) is int:
            return self.node_mapping[node]
        else:
            parent_node = self.find_node(self.node_mapping[node].parent.val)
            self.node_mapping[node].parent = parent_node
            return parent_node

    def union(self, node1, node2):
        parent1 = self.find_node(node1)
        parent2 = self.find_node(node2)
        if parent1.parent != parent2.parent:
            parent1.parent = parent2

    class DSNode:
        def __init__(self, val, parent):
            self.val = val
            self.parent = parent

def gerar_labirinto_kruskal(width, height):
    """
    Gera uma matriz representando um labirinto com a largura e altura especificadas
    usando o algoritmo de Kruskal.

    Args:
        width (int): A largura do labirinto (em número de células).
        height (int): A altura do labirinto (em número de células).

    Returns:
        numpy.ndarray: Uma matriz 2D onde 0=caminho, 1=parede, 2=início, 3=saída.
    """
    tempo_inicio = time.time()

    CAMINHO = parametros.CAMINHO
    PAREDE = parametros.PAREDE
    INICIO = parametros.INICIO
    FIM = parametros.FIM
    # --- Passo 1: Definir nós e arestas com base na largura e altura ---
    nodes = [(x, y) for y in range(height) for x in range(width)]
    
    # Função aninhada para encontrar vizinhos, agora usa width e height
    def get_neighbors(n):
        return [(n[0]+dx, n[1]+dy) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
                if 0 <= n[0]+dx < width and 0 <= n[1]+dy < height]

    edges = [(node, nbor) for node in nodes for nbor in get_neighbors(node)]
    
    # --- Passo 2: Algoritmo de Kruskal para criar um "spanning tree" ---
    maze_edges = []
    ds = DisjointSet(nodes)

    # --- INÍCIO DA OTIMIZAÇÃO ---
    # 1. Embaralha a lista de arestas uma única vez.
    random.shuffle(edges)
    
    while len(maze_edges) < len(nodes) - 1 and len(edges) > 0:
        # 2. Pega o último elemento da lista embaralhada.
        # Esta operação (pop sem índice) é extremamente rápida (O(1)).
        edge = edges.pop()
        
        # O restante do código permanece idêntico.
        if ds.find(edge[0]) != ds.find(edge[1]):
            ds.union(edge[0], edge[1])
            maze_edges.append(edge)
    # --- FIM DA OTIMIZAÇÃO ---

    # --- Passo 3: Construir a matriz do labirinto a partir das arestas ---
    # Dimensões da matriz em pixels, usando o padrão (altura, largura)
    array_height = height * 2 + 1
    array_width = width * 2 + 1
    
    # Labirinto começa todo como parede (valor 1)
    labirinto_matriz = np.ones((array_height, array_width), dtype=np.uint8)

    # Desenha os caminhos na matriz (valor 0)
    for edge in maze_edges:
        # (linha, coluna) == (y, x)
        y1, x1 = edge[0][1], edge[0][0]
        y2, x2 = edge[1][1], edge[1][0]
        
        # Coordenadas em pixels
        px_start_y = 1 + min(y1, y2) * 2
        px_end_y = 1 + max(y1, y2) * 2 + 1
        px_start_x = 1 + min(x1, x2) * 2
        px_end_x = 1 + max(x1, x2) * 2 + 1

        # Desenha os caminhos baseando-se na árvore do labirinto criada anteriormente
        labirinto_matriz[px_start_y:px_end_y, px_start_x:px_end_x] = CAMINHO

    # --- Passo 4: Definir a entrada e a saída ---
    # Entrada (valor 2) na parede superior esquerda
    labirinto_matriz[1, 1] = INICIO

    # Saída (valor 3)
    # A saída estará em um dos dois:
    # 1. na metade da parede direita até a parede inferior 
    # 2. na metade da parede inferior até a parede da direita
    exit_created = False
    if random.randint(0, 1) == 0: # Tenta criar na parede inferior
        possible_exits_x = [x for x in range(int(width/2), width) if labirinto_matriz[array_height - 2, 1 + x * 2] == CAMINHO]
        if possible_exits_x:
            exit_node_x = random.choice(possible_exits_x)
            exit_pixel_x = 1 + exit_node_x * 2
            labirinto_matriz[array_height - 1, exit_pixel_x:exit_pixel_x+1] = FIM
            exit_created = True

    if not exit_created: # Se não conseguiu na inferior, tenta na parede direita
        possible_exits_y = [y for y in range(int(height/2), height) if labirinto_matriz[1 + y * 2, array_width - 2] == CAMINHO]
        if possible_exits_y:
            exit_node_y = random.choice(possible_exits_y)
            exit_pixel_y = 1 + exit_node_y * 2
            labirinto_matriz[exit_pixel_y:exit_pixel_y+1, array_width - 1] = FIM
            exit_created = True

    # Caso extremo: se nenhuma saída for criada (ex: labirinto 1x1), força uma
    if not exit_created:
        labirinto_matriz[-1, -2] = FIM
        
    t_gerar_labirinto = time.time() - tempo_inicio
    print(f"Labirinto gerado em {t_gerar_labirinto} segundos")
    return labirinto_matriz
