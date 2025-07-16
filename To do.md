# TO DO

- [X] Alterar o código da interface para receber corretamente a matriz-historico que cada algoritmo deve retornar
- [X] Alterar a parte da matriz-historico para não retornar o historico completo na ultima iteração
    - [X] Por que não ta funcionando mesmo que a posição atual passe pelo fim?
    - [X] bem na vdd o alg de teste não precisa chegar ao fim, ent tanto faz...
    - [X] A n, esquece eu tava verificando um labirinto local em vez do global
- [X] utilizar o dead end fill para desenhar o caminho final por cima dos algoritmos.
- [X] Implementar contador de casas visitadas
- [X] Implementar pontuação
- [num vai dar] ~~Alterar o código para excluir o 2*i + 1 na criação do labirinto~~
- [X] Adicionar Pause
- [deu preguiça] ~~Medir diferença de tempo entre os algoritmos com a utilização da lista-historico e os algoritmos limpos, sem a necessidade de criar o historico (para fins de testes)~~
- [ ] Implementar uma taxa de animação que represente fielmente a velocidade dos algoritmos. Isso pode ser feito com uma normalização. Digamos que o alg1 demore 1.5s e tenha 100 passos e o alg2 demore 3.0s e tenha 90 passos. Assim, normaliza o primeiro para, digamos, 6s onde cada passo terá 6/100s  o segundo algoritmo terminará em 12 segundos onde cada passo terá 12/90s