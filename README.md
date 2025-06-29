# README

Repositório para a interface da competição de algoritmos de busca em um labirinto. Trabalho 1 da disciplina de IA do curso de Ciência da Computação de Cascavel.

Autores: Matheus Barros, Pedro Lucas

Apoio: Silva, Lora, Hermes, Roberto

# Explicação dos arquivos desse repositório

### interface.py 
"é a main", ou seja, o que deve ser executado para computar os algoritmos e mostrar a animação.

### parametros.py

Guarda variáveis globais e parâmetros utilizados em todos os códigos

### gerador_labirinto.py

Tem a função para gerar labirinto

### algoritmos_teste.py

guarda 3 algoritmos de teste para usar enquanto a interface foi implementada

# Decisões de projeto:

1. Cada algoritmo é uma biblioteca e a interface é a main. Cada grupo deve criar uma função que recebe como parâmetro o labirinto. 
2. Os algoritmos não podem analisar ou andar na diagonal.
3. O começo será fixo na posição (1,1) mas a saída do labirinto será aleatóriazada m uma posição adjacente às paredes limitadoras de labirinto do quarto quadrante (canto inferior direito). Se temos um labirinto i x j, o fim pode estar entre [int(i/2), j - 2] e [i-2, j-2] ou [int(j/2), i - 2] e [j-2, i-2]

4. Tamanhos dos labirintos: 
    L1: 71x71 (pedro/roberto)
    L2: 21x21 (hermes/rafael)
    L3: em aberto (andre/barros)
5. Gerador de labirinto (decisões de Pedro, Barros e Silva):
    1. Utilizaremos o algoritmo de Kruskal.
    2. Na matriz do labirinto: 
        1. Caminho = 0
        2. Parede = 1
        3. Ponto de início = 2
        4. Ponto de fim = 3
6. O labirinto deve ser quadrado.
7. O labirinto terá paredes para delimitação.
8. Interface
    1. Utilizar Pygame

# O que cada algoritmo deve retornar?

Cada algoritmo deve retornar uma matriz com n iterações. Cada iteração deve conter um array com m tuplas. A primeira tupla (matriz[i][0]) deve conter a posição atual do algoritmo. As m - 1 tuplas seguintes devem conter as celulas visitadas pelo algoritmo naquela iteração.
Essa matriz é necessária para a plotagem do labirinto e não vai influenciar na execução do código.

matriz = [
    [(0,0),(0,1),(1,0)], # i = 0
    [(0,1),(1,1),(0,2)], # i = 1
    [(1,1),(2,1),(1,2)], # i = 2
    [(2,1)],             # i = 3, beco sem saída, voltar a (1,1)
    [(1,2),(1,2)], # i = 4
    [(2,2)]              # i = 5, fim
]

# TO DO

[ ] Alterar o código da interface para receber corretamente a matriz que cada algoritmo deve retornar
[ ] Implementar contador de casas visitadas
[ ] Alterar o código para excluir o 2*i + 1 na criação do labirinto
[X] Adicionar Pause
