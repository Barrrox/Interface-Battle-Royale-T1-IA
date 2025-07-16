import time
import numpy as np
from algoritmos_teste import *
from caminho_final import aEstrela_perfeito



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
    CAMINHO = 0
    PAREDE = 1
    INICIO = 2
    FIM = 3
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
        
    return labirinto_matriz

def executar_algoritmo(func_algoritmo, labirinto):
    """Função alvo da thread: executa um algoritmo e mede o tempo."""
    tempo_inicial = time.perf_counter()
    historico = func_algoritmo(labirinto)
    tempo_final = time.perf_counter()

    espaco = len(historico)

    tempo = tempo_final - tempo_inicial

    return tempo, espaco

# DEFINE ALTURA E LARGURA

largura = 10
altura = 20

labirintos_por_iteracao = 1

algoritmos = {
    "bfs" : algoritmo_bfs,
    "dfs" : algoritmo_dfs,
    # "def" : algoritmo_dead_end_filling
}

# Cria um dicionario em que:
# 1. Cada chave é o nome do algoritmo
# 2. Cada valor terá mais um dicionario dentro, que contem a pontuacao media
resultados = {
    nome : {
    "pontuacao_media" : 0,
    "tempo execucao" : 0,
    "celulas visitadas" : 0
    } for nome in algoritmos
}



pontuacao_final = {
    nome : 0 for nome in algoritmos
}

# # loop para calcular labirintos de um tamanho inicial até um tamanho final,
# # incluindo o tamanho final
# for altura_atual in range(altura_inicial, altura_final + passo, passo):


    # Zerando as variaveis de media
for algoritmo in algoritmos:
    resultados[algoritmo]["pontuacao_media"] = 0
   
    # # loop para calcular quantos labirintos serão gerados para cada tamanho de labirinto
    # for j in range(labirintos_por_iteracao):

#     # gera labirinto
labirinto = gerar_labirinto_kruskal(altura, largura)

# multiplicador = 1000000/2.7**np.sqrt(tamanho_atual+tamanho_atual)

# Calcula para cada algoritmo
for algoritmo in algoritmos:
    # Executa e captura o tempo de exe e o espaco (celulas visitadas)
    tempo, espaco = executar_algoritmo(algoritmos[algoritmo], labirinto)
    resultados[algoritmo]["tempo execucao"] += tempo
    resultados[algoritmo]["celulas visitadas"] += espaco
    resultados[algoritmo]["pontuacao_media"] += (tempo*espaco)/labirintos_por_iteracao # Ja soma dividido para calcular a media 
        
    # Calculando vencedor para o labirinto de tamanho atual    

    # A melhor pontuacao será a mais baixa
    melhor_pontuacao = np.inf # infinito
    vencedor = ""

print(f"\n ----------------- LABIRINTO {largura*2 + 1}x{altura*2 + 1} ----------------- \n")

for algoritmo in resultados:
    # Guarda a pontuacao do algoritmo atual
    t_exe = resultados[algoritmo]["tempo execucao"]
    c_visitadas = resultados[algoritmo]["celulas visitadas"]
    pontuacao_algoritmo = resultados[algoritmo]["pontuacao_media"]
    
    print(f"{algoritmo}:")
    print(f"  Tempo de execução : {t_exe}s")
    print(f"  Celulas visitadas : {c_visitadas}")
    print(f"  Pontuação final   : {pontuacao_algoritmo}\n")

    # Procura o menor valor (melhor pontuaçao)
    if pontuacao_algoritmo < melhor_pontuacao:
        melhor_pontuacao = pontuacao_algoritmo
        vencedor = algoritmo
    
for nome in algoritmos:
    if vencedor == nome:
        pontuacao_final[nome] += 1

    
print(f"\nVENCEDOR: {vencedor} com {melhor_pontuacao}")

print("\n\n ######## NÚMERO DE VITÓRIAS ######## \n ")
for nome in pontuacao_final:
    print(f"{nome} : {pontuacao_final[nome]} vitórias")
