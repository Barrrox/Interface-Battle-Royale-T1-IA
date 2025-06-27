from kruskal_labirinto_variavel_gemini import gerar_labirinto_kruskal
from copia_de_interface_gemini import gerar_labirinto



print(gerar_labirinto_kruskal(5,5))

print("-------------------------------")
print("-------------------------------")
print("-------------------------------")

labi = gerar_labirinto(11,11)

for i in labi:
    print(i)
