"""
Código cópia criado a partir do arquivo interface_gemini.py

Alterações feitas por Barros e Pedro


"""


import pygame
import threading
import time
import random
# Supondo que estes arquivos existam e funcionem como discutido anteriormente
from kruskal_labirinto_variavel_gemini import gerar_labirinto_kruskal
from algoritmos_interface_gemini import *


# --- 1. CONFIGURAÇÕES GERAIS E CORES ---
pygame.init()
pygame.font.init()

# Configurações da tela
LARGURA_TELA = 1290  # Múltiplo de 3 para divisão exata
ALTURA_TELA = 821
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Battle Royale de algoritmos de busca")



# Configurações do labirinto
LARGURA_LABIRINTO_TELA = (LARGURA_TELA // 3)
TAMANHO_CELULA = 5
MARGEM = 20  # Margem dentro de cada área de labirinto

# Cores
COR_FUNDO = (0, 0, 0) # Preto
COR_PAREDE = (139, 69, 19) # Marrom
COR_CAMINHO = (255, 255, 255) # Branco
COR_VISITADA = (173, 216, 230) # Azul claro
COR_POS_ATUAL = (0, 255, 0) # Verde
COR_FINAL = (255, 215, 0) # Dourado (Para o caminho final)
COR_TEXTO = (255, 255, 255) # Branco
COR_BOTAO = (0, 100, 0)
COR_BOTAO_HOVER = (0, 150, 0)

### NOVO: Cores específicas para os marcadores de início e fim ###
COR_INICIO = (0, 255, 255)    # Ciano
COR_DESTINO = (255, 0, 255)  # Magenta

# Fonte para texto
fonte_padrao = pygame.font.SysFont('Consolas', 20)
fonte_titulo = pygame.font.SysFont('Consolas', 24, bold=True)
fonte_status = pygame.font.SysFont('Consolas', 30)


# --- 2. GERAÇÃO E ESTRUTURA DO LABIRINTO ---

# Definindo manualmente
LARGURA_LABIRINTO = 40
ALTURA_LABIRINTO = 60
LABIRINTO_GLOBAL = gerar_labirinto_kruskal(LARGURA_LABIRINTO, ALTURA_LABIRINTO)

PONTO_INICIAL = (1,1)

# Nota: Recomendo usar a versão mais robusta para encontrar o ponto final
# ou defini-lo estaticamente, como discutido anteriormente.
for i in range(len(LABIRINTO_GLOBAL)):
    if LABIRINTO_GLOBAL[i][-2] == 3: # procura nas linhas finais
        PONTO_FINAL = (i, len(LABIRINTO_GLOBAL)-2)
        print(PONTO_FINAL)

for i in range(len(LABIRINTO_GLOBAL[0])):
    if LABIRINTO_GLOBAL[-2][i] == 3: # procura nas linhas finais
        PONTO_FINAL = (len(LABIRINTO_GLOBAL)-2, i)
        print(PONTO_FINAL)


# --- 4. LÓGICA DE THREADING E EXECUÇÃO ---
resultados = {}

def executar_algoritmo(func_algoritmo, nome, labirinto, inicio, fim):
    """Função alvo da thread: executa um algoritmo e mede o tempo."""
    print(f"Thread '{nome}' iniciada.")
    tempo_inicial = time.perf_counter()
    matriz_historico = func_algoritmo(labirinto, inicio, fim)
    tempo_final = time.perf_counter()
    
    resultados[nome] = {
        "historico": matriz_historico,
        "tempo": tempo_final - tempo_inicial,
        "caminho_final": []
    }
    # Se o caminho foi encontrado, a última entrada do histórico tem o caminho
    if matriz_historico and matriz_historico[-1][0] == fim:
        resultados[nome]["caminho_final"] = matriz_historico[-1][1:]

    print(f"Thread '{nome}' finalizada em {resultados[nome]['tempo']:.4f}s.")


# --- 5. LÓGICA DE DESENHO (PLOTAGEM) ---
def desenhar_labirinto(surface, labirinto, offset_x, offset_y):
    """Desenha o estado estático do labirinto (paredes e caminhos)."""
    for y, linha in enumerate(labirinto):
        for x, celula in enumerate(linha):
            # Desenha a saída (célula 3) com a cor do destino para ser visível desde o início
            if celula == 3:
                 cor = COR_DESTINO
            # Mantém a lógica anterior para paredes e caminhos
            elif celula == 1:
                cor = COR_PAREDE
            else:
                cor = COR_CAMINHO
            pygame.draw.rect(surface, cor, (offset_x + x * TAMANHO_CELULA, offset_y + y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

### MODIFICADO: A função agora aceita `inicio` e `fim` como parâmetros ###
def desenhar_passos(surface, iteracao_historico, offset_x, offset_y, inicio, fim, caminho_final=[]):
    """Desenha o estado dinâmico (passos do algoritmo) sobre o labirinto."""
    if not iteracao_historico:
        return

    # Pinta as células visitadas
    celulas_visitadas = iteracao_historico[1:]
    for y, x in celulas_visitadas:
        pygame.draw.rect(surface, COR_VISITADA, (offset_x + x * TAMANHO_CELULA, offset_y + y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    ### NOVO: Desenha marcadores para o início e o fim ###
    # Eles são desenhados depois das células visitadas, mas antes do caminho final e da posição atual,
    # para que fiquem sempre visíveis como referência.
    iy, ix = inicio
    pygame.draw.rect(surface, COR_INICIO, (offset_x + ix * TAMANHO_CELULA, offset_y + iy * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
    
    fy, fx = fim
    pygame.draw.rect(surface, COR_DESTINO, (offset_x + fx * TAMANHO_CELULA, offset_y + fy * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    # Se a animação acabou, pinta o caminho final (cor Dourada)
    if caminho_final:
        for y, x in caminho_final:
            pygame.draw.rect(surface, COR_FINAL, (offset_x + x * TAMANHO_CELULA, offset_y + y * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

    # Pinta a posição atual por cima de tudo (cor Verde)
    pos_atual = iteracao_historico[0]
    py, px = pos_atual
    pygame.draw.rect(surface, COR_POS_ATUAL, (offset_x + px * TAMANHO_CELULA, offset_y + py * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))


# --- 6. LOOP PRINCIPAL DO JOGO ---
def main():
    clock = pygame.time.Clock()
    running = True
    estado_app = "AGUARDANDO"  # AGUARDANDO -> COMPUTANDO -> ANIMANDO -> FINALIZADO
    
    algoritmos = {
        "DFS": algoritmo_dfs,
        "BFS": algoritmo_bfs,
        "STUB": algoritmo_stub
    }
    threads = []
    
    indice_animacao = 0
    tempo_animacao = 0
    velocidade_animacao = 0.00002 # segundos por passo

    botao_start_rect = pygame.Rect(LARGURA_TELA / 2 - 100, ALTURA_TELA / 2 - 25, 200, 50)

    while running:
        # Tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and estado_app == "AGUARDANDO":
                if botao_start_rect.collidepoint(event.pos):
                    estado_app = "COMPUTANDO"
                    print("--- Iniciando Computação ---")
                    # Criar e iniciar as threads
                    for nome, func in algoritmos.items():
                        thread = threading.Thread(target=executar_algoritmo, args=(func, nome, LABIRINTO_GLOBAL, PONTO_INICIAL, PONTO_FINAL))
                        threads.append(thread)
                        thread.start()

        # Lógica de atualização de estado
        if estado_app == "COMPUTANDO":
            # Verifica se todas as threads terminaram
            if not any(t.is_alive() for t in threads):
                print("--- Computação Finalizada ---")
                estado_app = "ANIMANDO"
        
        elif estado_app == "ANIMANDO":
            tempo_animacao += clock.get_time() / 1000.0
            if tempo_animacao > velocidade_animacao:
                indice_animacao += 1
                tempo_animacao = 0
            
            # Verifica se todas as animações terminaram
            # Adicionado um tratamento de erro para caso um histórico esteja vazio
            if resultados:
                max_len = max(len(res["historico"]) for res in resultados.values() if res["historico"])
                if indice_animacao >= max_len:
                    estado_app = "FINALIZADO"
                    indice_animacao = max_len -1 # Trava no último frame

        # Lógica de desenho
        screen.fill(COR_FUNDO)

        if estado_app == "AGUARDANDO":
            texto_surf = fonte_status.render("Clique para Iniciar", True, COR_TEXTO)
            texto_rect = texto_surf.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 50))
            
            mouse_pos = pygame.mouse.get_pos()
            cor_botao_atual = COR_BOTAO_HOVER if botao_start_rect.collidepoint(mouse_pos) else COR_BOTAO
            
            pygame.draw.rect(screen, cor_botao_atual, botao_start_rect)
            botao_texto_surf = fonte_titulo.render("START", True, COR_TEXTO)
            botao_texto_rect = botao_texto_surf.get_rect(center=botao_start_rect.center)
            screen.blit(texto_surf, texto_rect)
            screen.blit(botao_texto_surf, botao_texto_rect)
        
        elif estado_app == "COMPUTANDO":
            texto_surf = fonte_status.render("Calculando rotas...", True, COR_TEXTO)
            texto_rect = texto_surf.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2))
            screen.blit(texto_surf, texto_rect)

        elif estado_app == "ANIMANDO" or estado_app == "FINALIZADO":
            offsets_x = [0, LARGURA_LABIRINTO_TELA, LARGURA_LABIRINTO_TELA * 2]
            
            for i, nome in enumerate(algoritmos.keys()):
                offset_x = offsets_x[i] + MARGEM
                offset_y = MARGEM + (ALTURA_TELA/2 - (ALTURA_TELA/2 - (ALTURA_LABIRINTO*2.5))) # Espaço para o título

                # Desenha o título e o tempo de execução
                titulo_surf = fonte_titulo.render(nome, True, COR_TEXTO)
                screen.blit(titulo_surf, (offset_x, MARGEM))
                
                tempo = resultados[nome]['tempo']
                tempo_surf = fonte_padrao.render(f"Tempo: {tempo:.4f}s", True, COR_TEXTO)
                screen.blit(tempo_surf, (offset_x, MARGEM + 25))

                # Desenha o labirinto base
                desenhar_labirinto(screen, LABIRINTO_GLOBAL, offset_x, offset_y)
                
                # Desenha os passos do algoritmo
                historico_atual = resultados[nome]["historico"]
                if historico_atual: # Garante que o histórico não está vazio
                    passo_atual = min(indice_animacao, len(historico_atual) - 1)
                    
                    caminho_final = []
                    if estado_app == "FINALIZADO":
                        caminho_final = resultados[nome]["caminho_final"]

                    ### MODIFICADO: Passa PONTO_INICIAL e PONTO_FINAL para a função de desenho ###
                    desenhar_passos(screen, historico_atual[passo_atual], offset_x, offset_y, PONTO_INICIAL, PONTO_FINAL, caminho_final)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()