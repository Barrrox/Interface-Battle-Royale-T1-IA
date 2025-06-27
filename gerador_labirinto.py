"""
Código redesenhado pelo gemini para implementar a função gerar_labirinto_kruskal(width, height)
que cria e retorna um labrinto em forma de matriz, seguindo o algoritmo de Kruskal

"""

from PIL import Image
import random
import numpy as np


CAMINHO = 0
PAREDE = 1
INICIO = 2
FIM = 3


# --- Parâmetros de Geração ---
# Você pode alterar estes valores.
CELL_THICKNESS = 1  # Espessura de uma célula de caminho
WALL_THICKNESS = 1  # Espessura de uma parede

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

    while len(maze_edges) < len(nodes) - 1 and len(edges) > 0:
        edge = edges.pop(random.randint(0, len(edges) - 1))
        if ds.find(edge[0]) != ds.find(edge[1]):
            ds.union(edge[0], edge[1])
            maze_edges.append(edge)

    # --- Passo 3: Construir a matriz do labirinto a partir das arestas ---
    # Dimensões da matriz em pixels, usando o padrão (altura, largura)
    array_height = height * (CELL_THICKNESS + WALL_THICKNESS) + WALL_THICKNESS
    array_width = width * (CELL_THICKNESS + WALL_THICKNESS) + WALL_THICKNESS
    
    # Labirinto começa todo como parede (valor 1)
    labirinto_matriz = np.ones((array_height, array_width), dtype=np.uint8)

    # Desenha os caminhos na matriz (valor 0)
    for edge in maze_edges:
        # Usa a convenção (linha, coluna) == (y, x)
        y1, x1 = edge[0][1], edge[0][0]
        y2, x2 = edge[1][1], edge[1][0]
        
        # Coordenadas em pixels
        px_start_y = WALL_THICKNESS + min(y1, y2) * (CELL_THICKNESS + WALL_THICKNESS)
        px_end_y = WALL_THICKNESS + max(y1, y2) * (CELL_THICKNESS + WALL_THICKNESS) + CELL_THICKNESS
        px_start_x = WALL_THICKNESS + min(x1, x2) * (CELL_THICKNESS + WALL_THICKNESS)
        px_end_x = WALL_THICKNESS + max(x1, x2) * (CELL_THICKNESS + WALL_THICKNESS) + CELL_THICKNESS

        labirinto_matriz[px_start_y:px_end_y, px_start_x:px_end_x] = CAMINHO

    # --- Passo 4: Definir a entrada e a saída ---
    # Entrada (valor 2) na parede superior esquerda
    labirinto_matriz[WALL_THICKNESS:WALL_THICKNESS+CELL_THICKNESS, 1] = INICIO

    # Saída (valor 3) - lógica aprimorada e corrigida
    exit_created = False
    if random.randint(0, 1) == 0: # Tenta criar na parede inferior
        possible_exits_x = [x for x in range(width) if labirinto_matriz[array_height - 2, WALL_THICKNESS + x * (CELL_THICKNESS + WALL_THICKNESS)] == CAMINHO]
        if possible_exits_x:
            exit_node_x = random.choice(possible_exits_x)
            exit_pixel_x = WALL_THICKNESS + exit_node_x * (CELL_THICKNESS + WALL_THICKNESS)
            labirinto_matriz[array_height - 2, exit_pixel_x:exit_pixel_x+CELL_THICKNESS] = FIM
            exit_created = True

    if not exit_created: # Se não conseguiu na inferior, tenta na parede direita
        possible_exits_y = [y for y in range(height) if labirinto_matriz[WALL_THICKNESS + y * (CELL_THICKNESS + WALL_THICKNESS), array_width - 2] == CAMINHO]
        if possible_exits_y:
            exit_node_y = random.choice(possible_exits_y)
            exit_pixel_y = WALL_THICKNESS + exit_node_y * (CELL_THICKNESS + WALL_THICKNESS)
            labirinto_matriz[exit_pixel_y:exit_pixel_y+CELL_THICKNESS, array_width - 2] = FIM
            exit_created = True

    # Caso extremo: se nenhuma saída for criada (ex: labirinto 1x1), força uma
    if not exit_created:
        labirinto_matriz[-1, -1-CELL_THICKNESS:-1] = FIM
        
    return labirinto_matriz

# --- Exemplo de Uso ---
if __name__ == "__main__":

    meu_labirinto = gerar_labirinto_kruskal(20, 20)

    print(f"Matriz do labirinto gerado (dimensões: {meu_labirinto.shape}):")
    # print(meu_labirinto) # Descomente para ver a matriz no console

    # --- Para visualizar a imagem (requer Pillow/PIL) ---
    # Converte a matriz para uma imagem em escala de cinza para visualização
    # 0 (caminho) = branco, 1 (parede) = preto, 2 (inicio) e 3 (fim) = cinza
    imagem_array = np.copy(meu_labirinto)
    imagem_array[imagem_array == CAMINHO] = 255 # Paredes
    imagem_array[imagem_array == PAREDE] = 0 # Paredes
    imagem_array[imagem_array == INICIO] = 120 # Entrada
    imagem_array[imagem_array == FIM] = 120 # Saída
    
    im = Image.fromarray(imagem_array)
    im.show()

    # ## Salvar o labirinto (inclua a extensão!)
    # try:
    #     im.save("meu_labirinto.png")
    #     print("Labirinto salvo como 'meu_labirinto.png'")
    # except Exception as e:
    #     print(f"Não foi possível salvar a imagem: {e}")