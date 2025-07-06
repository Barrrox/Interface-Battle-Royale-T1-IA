# README

Repositório para a interface da competição de algoritmos de busca em um labirinto. Trabalho 1 da disciplina de IA do curso de Ciência da Computação de Cascavel.

Autores: Matheus Barros, Pedro Lucas

Apoio: Silva, Lora, Roberto, Hermes, Andre

# Explicação dos arquivos desse repositório

### interface.py 

É a "main", o código que deve ser executado para computar os algoritmos e mostrar a animação.

### parametros.py

Guarda variáveis globais e parâmetros utilizados em todos os códigos

### gerador_labirinto.py

Tem o algoritmo de Kruskal para gerar labirinto

### algoritmos_teste.py

guarda 3 algoritmos para fins de testes

### caminho_final.py

Contém um algoritmo separado dos outros que serve apenas para gerar o caminho final

# Decisões de projeto:

1. Cada grupo deve criar uma função que recebe como parâmetro o labirinto e retornar um histórico(lista do python) do percurso feito pelo seu algoritmo (será explicado mais a frente nesse documento).
2. Posição inicial e final: O começo será fixo na posição (1,1) mas a saída do labirinto será aleatóriazada em uma posição adjacente às paredes limitadoras de labirinto do quarto quadrante (canto inferior direito). Se temos um labirinto i x j, o fim pode estar entre [int(i/2), j - 1] e [i-2, j-1] ou [int(j/2), i - 1] e [j-2, i-1]
3. Tamanhos dos labirintos: 
    L1: 71x71 (pedro/roberto)
    L2: 21x21 (hermes/rafael)
    L3: em aberto (andre/barros)
4. Gerador de labirinto (decisões de Pedro, Barros e Silva):
    1. Utilizaremos o algoritmo de Kruskal.
    2. Na matriz do labirinto: 
        1. Caminho = 0
        2. Parede = 1
        3. Ponto de início = 2
        4. Ponto de fim = 3
5. O labirinto pode ter tamanho variável.
6. Analisar celulas também conta como um passo 
7. O labirinto terá paredes para delimitação.
8. Interface e animação
    1. Será utilizada a biblioteca Pygame
    2. A animação será produzida após a execução dos algoritmos

# Descrição do histórico

O histórico é uma lista do python. Cada elemento da lista deve ser uma tupla (x,y) que indica a posição analisada pelo algoritmo naquela iteração. Ao final, o histórico deve conter todas as células visitadas/analisadas naquele algoritmo e não apenas o caminho final.
Essa matriz é necessária para a animação do labirinto.

