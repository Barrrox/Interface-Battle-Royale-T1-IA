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

#Caminho = 0
#Parede = 1
#PontoDePartida = 2
#PontoDeChegada = 3
#Andado = 4

# Função para encontrar o fim do labirinto (utilizado pela Heurística do Manhattan)
def encontrarFim(Labirinto, MaxLinha, MaxColuna):
    # O final do labirinto sempre estará do meio para o fim
    # Otimizamos a busca da cordenada final para começar a partir do meio do labirinto
    l = int(round(MaxLinha / 2, 0)) # metade das linhas
    c = int(round(MaxColuna / 2, 0)) # metade das colunas

    # Loop for para achar o final do labirinto começando do meio para o fim
    for i in range(l, MaxLinha):
      for j in range(c, MaxColuna):
        if Labirinto[i][j] == 3: # Encontrou "3" no labirinto, ou seja, a saída
          return (i, j) # Retorna a coordenada de saída do labirinto (Linha, Coluna)

# Função auxiliar para executar a heurística do Manhattan
# Se baseia em calcular qual é a distância do início para o fim, ignorando paredes ou células visitadas
def PreManhattan(max_linhas, max_colunas, destino):
    Fy, Fx = destino
    # Retorna uma matriz das distâncias do início para o fim para evitar chamar a função repetidas vezes
    return [[abs(y - Fy) + abs(x - Fx) # Calcula a distância (posição atual - destino)
             for x in range(max_colunas)] # Loop para posições da coluna
             for y in range(max_linhas)] # Loop para posições da linha

# Algoritimo de execução do DFS
def DFS(Labirinto):
    Historico = [] # Vetor para guardar o histórico de posições visitadas pelo DFS. EX: [(1,1), (1,2), (1,3)...]
    Pilha = [] # Pilha para armazenar possíveis posições a serem acessadas pelo DFS, ou seja, caminhos possíveis são empilhados e desempilhados conforme a necessidade
    # Apenas nomes para melhor identificar os métodos que envolvem a manipulação da pilha, ou seja, push para (Pilha.append) e pop para (Pilha.pop)
    push = Pilha.append
    pop = Pilha.pop

    MaxLinha = len(Labirinto) # Total de linhas do labirinto
    MaxColuna = len(Labirinto[0]) # Total de colunas do labirinto

    # Vetores auxiliares que utilizamos para melhor se movimentar dentro do labirinto
    # São utilizados em conjunto, assim podemos otimizar toda a busca e deixar tanto o DFS quanto o Manhattan mais organizados
    # Ex: ir para baixo = DirecaoLinha[0] + DirecaoColuna[0]
    # Ex: ir para direita = DirecaoLinha[1] + DirecaoColuna[1]
    # Ex: ir para esquerda = DirecaoLinha[2] + DirecaoColuna[2]
    # Ex: ir para cima = DirecaoLinha[3] + DirecaoColuna[3]
    DirecaoLinha = [1, 0, 0, -1]
    DirecaoColuna = [0, 1, -1, 0]

    Final = encontrarFim(Labirinto, MaxLinha, MaxColuna) # Chama a função para encontrar o final do labirinto, contém as posições de x e y em forma de tupla
    H = PreManhattan(MaxLinha, MaxColuna, Final) # Chama a função auxiliar do Manhattan e aloca todos as distâncias em uma matriz H, para evitar buscas repetitivas

    Historico.append((1, 1)) # Acrescentamos a primeira posição (1,1) na pilha de histórico, pois sempre será acessada, é a posição inicial do labirinto

    # Como as posições para a direita e para baixo são as únicas possíveis no começo do labirinto, já calculamos qual caminho percorrer para evitar que o mesmo seja processado pelo loop e gere mais tempo de execução
    Baixo = -1 # Acrescentamos -1 par evitar possíveis erros caso o seu respectivo if não seja acessado
    if Labirinto[2][1] not in (1, 4): # Verifica se o caminho para a baixo é valido, ou seja, não é parede ou já foi percorrido
        Baixo = H[2][1] # Acrescenta para a variável "Baixo" a respectiva distância até o final do labirinto, contida em H

    # Mesmo método para a visita acima descrita, porém para a direita
    Direita = -1
    if Labirinto[1][2] not in (1, 4):
        Direita= H[1][2]

    # Empilha primeiro a direção com heurística MAIOR
    if Baixo >= Direita: # Caso a distância para direita seja menor. Pilha = (coordenada baixo),(coordenada direita)
        if Baixo >= 0: # Verifica se o baixo é maior do que 0, ou seja, para evitar o caso do baixo = -1
          push((2, 1)) # Acrescentamos na pilha a posição para a baixo
        if Direita >= 0: # Faz a mesma verificação, porém para a direita, para evitar direita = -1
          push((1, 2)) # Acrescentamos na pilha a posição para a direita
    else: # Caso a distância para baixo seja menor. Pilha = (coordenada direita),(coordenada baixo)
        push((1, 2)) # Acrescentamos na pilha a posição para a direita
        if Baixo >= 0: # Verificação para evitar -1
          push((2, 1)) # Acrescentamos na pilha a posição para a baixo

    while len(Pilha) > 0: # Loop para enquanto a pilha não estiver vazia, ou seja, ainda tem coordenadas válidas para acessar
        LinhaAtual, ColunaAtual = pop() # Retiramos da pilha as coordenadas de linha e coluna que estão presentes no topo
        Historico.append((LinhaAtual, ColunaAtual)) # Acrescentamos no histórico como coordenadas visitadas
        Labirinto[LinhaAtual][ColunaAtual] = 4 # Marcamos a coordenada como visitada na matriz de labirinto, ou seja, = 4

        # Matriz auxiliar para calcular a heurística de Manhattan, onde calcula todos os os possíveis vizinhos da posição atual
        # Os vizinhos são armazenados da seguinte maneira: Baixo, Direita, Esquerda, Cima
        Vizinhos = [] # Priorizamos Baixo e Direita na frente pois é para onde o final do labirinto está

        # DFS (4 direções)
        for IndiceDirecao in range(4): # Loop para verificar as 4 direções que podem ser visitadas (baixo, cima, direita, esquerda)
            LinhaAdjacente = LinhaAtual + DirecaoLinha[IndiceDirecao] # Calculo da linha adjacente com o auxilio do vetor de DirecaoLinha
            ColunaAdjacente = ColunaAtual + DirecaoColuna[IndiceDirecao]# Calculo da coluna adjacente com o auxilio do vetor de DirecaoColuna

            # Verifica se a coordenada de linha e coluna adjacentes são parede ou já foram visitadas, ou seja, = 1 ou = 4
            if Labirinto[LinhaAdjacente][ColunaAdjacente] in (1, 4):
                continue # Caso seja verdade, apenas pula para o próximo vizinho

            # Verifica se as coordenadas analisadas já são as respetivas coordenadas finais do labirinto
            if (LinhaAdjacente, ColunaAdjacente) == Final:
              # Acrescenta a coordenada no vetor de histórico de posições visitadas e retorna o mesmo
              Historico.append((LinhaAdjacente, ColunaAdjacente))
              return (Historico)

            # Acrescenta ao vetor de vizinhos a distância presente na matriz H, além do indice de direção para saber qual é a direção que tal linha e coluna é percorrido
            Vizinhos.append((H[LinhaAdjacente][ColunaAdjacente], IndiceDirecao, LinhaAdjacente, ColunaAdjacente))

        # Ordemos o vetor para que a maior distância fique primeiro, e em caso de empate, ordenamos com base no Indice de Direção, ou seja, para que priorize os vizinhos que vão para baixo e direita respectivamente
        Vizinhos.sort(key=lambda t: (-t[0], t[1]))

        # Acrescenta à pilha todos os vizinhos possíveis, com base em sua ordem anteriormente calculada com a heurística Manhattan
        for _, IndiceDirecao, LinhaAdjacente, ColunaAdjacente in Vizinhos:
          push((LinhaAdjacente, ColunaAdjacente)) # Vai para a pilha primeiro os vizinhos com maior distância, para que os com menor distância fiquem no topo, e assim sejam escolhidos primeiro