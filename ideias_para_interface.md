# Ideias para plotagem dos labirintos na interface

# ideia 3

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

