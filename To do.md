# TO DO

- [X] Alterar o código da interface para receber corretamente a matriz-historico que cada algoritmo deve retornar
- [X] Alterar a parte da matriz-historico para não retornar o historico completo na ultima iteração
    - [X] Por que não ta funcionando mesmo que a posição atual passe pelo fim?
    - [X] bem na vdd o alg de teste não precisa chegar ao fim, ent tanto faz...
    - [X] A n, esquece eu tava verificando um labirinto local em vez do global
- [ ] Implementar contador de casas visitadas
- [num vai dar] ~~Alterar o código para excluir o 2*i + 1 na criação do labirinto~~
- [X] Adicionar Pause
- [ ] Medir diferença de tempo entre os algoritmos com a utilização da matriz-historico e os algoritmos limpos (para fins de testes)
- [ ] Verificador de percurso:
    1. Verifica cada historico analisando para cada posição atual (x,y) se a proxima está entre as posições alcançaveis (x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)
    2. Se alguma célula for pulada, o percurso não é válido.