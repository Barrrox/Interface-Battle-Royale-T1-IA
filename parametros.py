"""
Arquivo para guardar variáveis globais e parâmetros utilizados nos códigos da pasta

"""
from gerador_labirinto import gerar_labirinto_kruskal


# Configurações de imagem
LARGURA_TELA = 1551 
ALTURA_TELA = 801

MARGEM_ESQUERDA = 20

# Configurações do labirinto
LARGURA_LABIRINTO = 100
ALTURA_LABIRINTO = 100
TAMANHO_CELULA = 2

# Valores dos elementos na matriz do labirinto
CAMINHO = 0
PAREDE = 1
INICIO = 2
FIM = 3

# Matriz do labirinto gerada por Kruskal
LABIRINTO_GLOBAL = gerar_labirinto_kruskal(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

# PONTO INICIAL
PONTO_INICIAL = (1,0)

# PONTO FINAL NA PAREDE INFERIOR
for i in range(len(LABIRINTO_GLOBAL)):
    if LABIRINTO_GLOBAL[i][-1] == FIM: # procura nas linhas finais
        PONTO_FINAL = (i, len(LABIRINTO_GLOBAL)-1)
        print(PONTO_FINAL)

# PONTO FINAL NA PAREDE DA DIREITA
for i in range(len(LABIRINTO_GLOBAL[0])):
    if LABIRINTO_GLOBAL[-1][i] == FIM: # procura nas linhas finais
        PONTO_FINAL = (len(LABIRINTO_GLOBAL)-1, i)
        print(PONTO_FINAL)