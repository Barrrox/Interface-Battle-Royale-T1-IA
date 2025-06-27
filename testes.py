"""
Código para fins de testes

Feito por Barros

"""


from gerador_labirinto import gerar_labirinto_kruskal
from interface import gerar_labirinto



print(gerar_labirinto_kruskal(5,5))

print("-------------------------------")
print("-------------------------------")
print("-------------------------------")

labi = gerar_labirinto(11,11)

for i in labi:
    print(i)
