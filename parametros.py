"""
Arquivo para guardar variáveis globais e parâmetros utilizados nos códigos da pasta

"""
from gerador_labirinto import gerar_labirinto_kruskal


# Configurações de imagem
LARGURA_TELA = 1551 
ALTURA_TELA = 801

MARGEM_ESQUERDA = 20

# Configurações do labirinto

# Os valores de altura e largura serão duplicados e incrementados em 1.
# Ex: se a LARGURA_LABIRINTO = 10, então o labirinto terá tamanho 10*2 + 1 = 21
# (Eu (Barros) tentei deixar o valor daqui ser diretamente o tamanho do labirinto mas num deu nao)
LARGURA_LABIRINTO = 217
ALTURA_LABIRINTO = 604
TAMANHO_CELULA = 1

# Valores dos elementos na matriz do labirinto
CAMINHO = 0
PAREDE = 1
INICIO = 2
FIM = 3

# Matriz do labirinto gerada por Kruskal
LABIRINTO_GLOBAL = gerar_labirinto_kruskal(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

# PONTO INICIAL
PONTO_INICIAL = (1,1)

# PONTO FINAL NA PAREDE INFERIOR
for i in range(len(LABIRINTO_GLOBAL)):
    if LABIRINTO_GLOBAL[i][-1] == FIM: # procura nas linhas finais
        PONTO_FINAL = (i, len(LABIRINTO_GLOBAL[0])-1)

# PONTO FINAL NA PAREDE DA DIREITA
for i in range(len(LABIRINTO_GLOBAL[0])):
    if LABIRINTO_GLOBAL[-1][i] == FIM: # procura nas linhas finais
        PONTO_FINAL = (len(LABIRINTO_GLOBAL)-1, i)

# Animação 
VELOCIDADE_ANIMACAO = 0.0001 # (quanto menor, mais rápido)