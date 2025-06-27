"""
Arquivo para guardar variáveis globais e parâmetros utilizados nos códigos da pasta

"""
from gerador_labirinto import gerar_labirinto_kruskal


# Configurações de imagem
LARGURA_TELA = 1290  # Múltiplo de 3 para divisão exata
ALTURA_TELA = 821

MARGEM_ESQUERDA = 20

# Configurações do labirinto
LARGURA_LABIRINTO = 5
ALTURA_LABIRINTO = 5
TAMANHO_CELULA = 5

CAMINHO = 0
PAREDE = 1
INICIO = 2
FIM = 3

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