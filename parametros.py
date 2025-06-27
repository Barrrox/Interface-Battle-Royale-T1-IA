"""
Arquivo para guardar variáveis globais e parâmetros utilizados nos códigos da pasta

"""

from gerador_labirinto import gerar_labirinto_kruskal

LARGURA_TELA = 1290  # Múltiplo de 3 para divisão exata
ALTURA_TELA = 821

MARGEM_ESQUERDA = 20


LARGURA_LABIRINTO = 60
ALTURA_LABIRINTO = 60

TAMANHO_CELULA = 3


CAMINHO = 0
PAREDE = 1
INICIO = 2
FIM = 3

LABIRINTO_GLOBAL = gerar_labirinto_kruskal(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

PONTO_INICIAL = (1,0)

for i in range(len(LABIRINTO_GLOBAL)):
    if LABIRINTO_GLOBAL[i][-1] == FIM: # procura nas linhas finais
        PONTO_FINAL = (i, len(LABIRINTO_GLOBAL)-1)
        print(PONTO_FINAL)

for i in range(len(LABIRINTO_GLOBAL[0])):
    if LABIRINTO_GLOBAL[-1][i] == FIM: # procura nas linhas finais
        PONTO_FINAL = (len(LABIRINTO_GLOBAL)-1, i)
        print(PONTO_FINAL)