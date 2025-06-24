# README

Repositório para a interface da competição de algoritmos de busca em um labirinto. Trabalho 1 da disciplina de IA do curso de Ciência da Computação de Cascavel.

Autores: Matheus Barros, Pedro Lucas

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

# TO DO

[] Alterar o código da interface para receber corretamente a matriz descrita em ideias_para_interface.md

