"""
Implementa o algoritmo de dead end filling que retornará o percurso final para o labirinto


"""

def algoritmo_dead_end_filling(labirinto):
    """
    Resolve um labirinto usando o algoritmo Dead End Filling.

    Este algoritmo funciona em duas fases:
    1.  Preenchimento: Identifica e preenche todos os "becos sem saída" do 
        labirinto, marcando-os como paredes. Um beco sem saída é um caminho
        que tem apenas uma entrada/saída. Este processo é repetido até que
        não haja mais becos sem saída a serem preenchidos. O ponto inicial
        e final não são preenchidos.
    2.  Busca do Caminho: Após o preenchimento, o labirinto conterá apenas
        os caminhos que levam à solução (e possíveis ciclos). Uma busca 
        simples é realizada no labirinto simplificado para encontrar o 
        caminho do início ao fim.

    O histórico retornado contém apenas as posições do caminho final,
    conforme solicitado.
    """

    inicio = (1,1)

    altura_labirinto = len(labirinto)
    largura_labirinto = len(labirinto[0])
    
    for i in range(altura_labirinto):
        if labirinto[i][-1] == 3:
            fim = (i, largura_labirinto - 1)

    for i in range(largura_labirinto):
        if labirinto[-1][i] == 3:
            fim = (altura_labirinto - 1, i)

    print(fim)
    
    # Cria uma cópia mutável do labirinto para não alterar o original
    labirinto_copia = [list(linha) for linha in labirinto]
    altura = len(labirinto_copia)
    largura = len(labirinto_copia[0])
    
    # --- FASE 1: PREENCHIMENTO DOS BECOS SEM SAÍDA ---
    
    dead_ends = []
    
    # Identifica os becos sem saída iniciais
    for y in range(altura):
        for x in range(largura):
            # Ignora paredes, o ponto de início e o ponto final
            if labirinto_copia[y][x] == 1 or (y, x) == inicio or (y, x) == fim:
                continue

            vizinhos_livres = 0
            vizinhos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
            for vy, vx in vizinhos:
                if 0 <= vy < altura and 0 <= vx < largura and labirinto_copia[vy][vx] != 1:
                    vizinhos_livres += 1
            
            if vizinhos_livres == 1:
                dead_ends.append((y, x))

    # Preenche os becos sem saída iterativamente
    while dead_ends:
        y, x = dead_ends.pop(0)
        
        # Marca o beco sem saída como uma parede
        labirinto_copia[y][x] = 1
        
        # Verifica se o preenchimento criou novos becos sem saída nos vizinhos
        vizinhos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        for vy, vx in vizinhos:
            if 0 <= vy < altura and 0 <= vx < largura and labirinto_copia[vy][vx] != 1 and (vy, vx) != inicio and (vy, vx) != fim:
                
                novos_vizinhos_livres = 0
                vizinhos_do_vizinho = [(vy - 1, vx), (vy + 1, vx), (vy, vx - 1), (vy, vx + 1)]
                for vvy, vvx in vizinhos_do_vizinho:
                     if 0 <= vvy < altura and 0 <= vvx < largura and labirinto_copia[vvy][vvx] != 1:
                        novos_vizinhos_livres += 1
                
                if novos_vizinhos_livres == 1:
                    if (vy, vx) not in dead_ends:
                        dead_ends.append((vy, vx))

    # --- FASE 2: BUSCA DO CAMINHO NO LABIRINTO SIMPLIFICADO ---
    
    # Como o labirinto foi simplificado, basta seguir o único caminho possível.
    # Usaremos uma busca simples para traçar esse caminho.
    historico = []
    
    # A fila agora só precisa da posição atual e do caminho percorrido
    fila = [(inicio, [inicio])] 
    visitados = {inicio}
    
    while fila:
        pos_atual, caminho_parcial = fila.pop(0)
        
        if pos_atual == fim:
            # Caminho encontrado, retorna o histórico (que é o próprio caminho)
            historico = caminho_parcial
            return historico
            
        (y, x) = pos_atual
        vizinhos = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
        
        for vizinho in vizinhos:
            if 0 <= vizinho[0] < altura and 0 <= vizinho[1] < largura and labirinto_copia[vizinho[0]][vizinho[1]] != 1 and vizinho not in visitados:
                visitados.add(vizinho)
                novo_caminho = caminho_parcial + [vizinho]
                fila.append((vizinho, novo_caminho))

    print("Falha Dead-end-filling")
    # Se não encontrar caminho (improvável se houver solução)
    return []


labirinto = [   [1, 1, 1, 1, 1, 1, 1],
                [1, 2, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1, 0, 1],
                [1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 3, 1, 1, 1]]

algoritmo_dead_end_filling(labirinto)