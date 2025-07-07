"""
Interface para animar os 3 algoritmos de busca

Alterações feitas por Barros e Pedro
"""


import pygame
import threading
import time
import parametros
# Supondo que estes arquivos existam e funcionem como discutido anteriormente
from algoritmos_teste import *
from caminho_final import *
import numpy as np


# --- 1. CONFIGURAÇÕES GERAIS E CORES ---
LARGURA_TELA = parametros.LARGURA_TELA
ALTURA_TELA = parametros.ALTURA_TELA
pygame.init()
pygame.font.init()

# Configurações da tela
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Battle Royale de algoritmos de busca")


# Configurações do labirinto
LARGURA_LABIRINTO_TELA = (LARGURA_TELA // 3)
TAMANHO_CELULA = parametros.TAMANHO_CELULA
MARGEM_ESQUERDA = parametros.MARGEM_ESQUERDA

# Cores
COR_FUNDO = (0, 0, 0) # Preto
COR_PAREDE = (100, 30, 19) # Marrom
COR_CAMINHO = (255, 255, 255) # Branco
COR_VISITADA = (173, 216, 230) # Azul claro
COR_POS_ATUAL = (0, 255, 0) # Verde
COR_FINAL = (255, 215, 0) # Dourado (Para o caminho final)
COR_TEXTO = (255, 255, 255) # Branco
COR_BOTAO = (0, 100, 0)
COR_BOTAO_HOVER = (0, 150, 0)
COR_BOTAO_PAUSA = (180, 0, 0)
COR_BOTAO_PAUSA_HOVER = (230, 0, 0)


### NOVO: Cores específicas para os marcadores de início e fim ###
COR_INICIO = (0, 255, 255)   # Ciano
COR_DESTINO = (255, 0, 255)  # Magenta

# Fonte para texto
fonte_padrao = pygame.font.SysFont('Consolas', 20)
fonte_titulo = pygame.font.SysFont('Consolas', 24, bold=True)
fonte_status = pygame.font.SysFont('Consolas', 40, bold=True)


# --- 2. GERAÇÃO E ESTRUTURA DO LABIRINTO ---

# Definindo manualmente
LARGURA_LABIRINTO = parametros.LARGURA_LABIRINTO
ALTURA_LABIRINTO = parametros.ALTURA_LABIRINTO
LABIRINTO_GLOBAL = parametros.LABIRINTO_GLOBAL


# --- 3. DEFININDO PONTO INICIAL E FINAL ---

PONTO_INICIAL = parametros.PONTO_INICIAL
PONTO_FINAL = parametros.PONTO_FINAL


# --- 4. LÓGICA DE THREADING E EXECUÇÃO ---
resultados = {}

def executar_algoritmo(func_algoritmo, nome, labirinto, caminho_final):
    """Função alvo da thread: executa um algoritmo e mede o tempo."""
    print(f"Thread '{nome}' iniciada.")
    tempo_inicial = time.perf_counter()
    historico = func_algoritmo(labirinto)
    tempo_final = time.perf_counter()

    tempo = tempo_final - tempo_inicial

    # numero de celulas visitadas
    n_celulas_visitadas = len(historico)

    # O multplicador é um número x que multiplica a pontuação.
    # Ele serve apenas para que os números de pontuação tenham valores 
    # parecidos entre cada rodada, independente do tamanho do labirinto.
    # O valor multiplica todos os algoritmos sem mudar, então não vai impactar no
    # ranking dos algoritmos.

    multiplicador = 1000000/2.7**np.sqrt(LARGURA_LABIRINTO+ALTURA_LABIRINTO)

    # Se quiser que o multplicador não interfira, descomente a linha abaixo
    # multiplicador = 1

    # Quanto menor, melhor
    pontuacao = int(tempo*n_celulas_visitadas*multiplicador)

    resultados[nome] = {
        "historico": historico,
        "tempo": tempo,
        "numero de celulas visitadas": n_celulas_visitadas,
        "caminho_final": caminho_final,
        "pontuacao": pontuacao
    }

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
    # ### MODIFICADO: Adicionado o estado "PAUSADO"
    estado_app = "AGUARDANDO"  # AGUARDANDO -> COMPUTANDO -> ANIMANDO -> PAUSADO -> FINALIZADO

    algoritmos = {
        "DFS": algoritmo_dfs,
        "BFS": algoritmo_bfs,
        "DEAD END FILL": algoritmo_dead_end_filling
    }
    threads = []

    indice_animacao = 0
    tempo_animacao = 0
    velocidade_animacao = parametros.VELOCIDADE_ANIMACAO # segundos por passo (velocidade ajustada para melhor visualização)

    botao_start_rect = pygame.Rect(LARGURA_TELA / 2 - 100, ALTURA_TELA / 2 - 25, 200, 50)
    # ### NOVO: Definição mais centralizada e maior para o botão de pausa
    botao_pause_rect = pygame.Rect(LARGURA_TELA / 2 - 75, 15, 150, 40)

    print(LABIRINTO_GLOBAL)
    caminho_final = algoritmo_dead_end_filling(LABIRINTO_GLOBAL)

    while running:
        # ### MODIFICADO: Loop de eventos para lidar com o estado de PAUSA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if estado_app == "AGUARDANDO" and botao_start_rect.collidepoint(event.pos):
                    estado_app = "COMPUTANDO"
                    print("--- Iniciando Computação ---")
                    # Criar e iniciar as threads
                    for nome, func in algoritmos.items():
                        thread = threading.Thread(target=executar_algoritmo, args=(func, nome, LABIRINTO_GLOBAL, caminho_final))
                        threads.append(thread)
                        thread.start()
                
                # ### NOVO: Lógica para pausar/retomar a animação
                # Verifica se o clique foi no botão de pausa e se o estado é apropriado
                elif estado_app in ["ANIMANDO", "PAUSADO"] and botao_pause_rect.collidepoint(event.pos):
                    if estado_app == "ANIMANDO":
                        estado_app = "PAUSADO"
                        print("--- Animação Pausada ---")
                    else: # estado_app é "PAUSADO"
                        estado_app = "ANIMANDO"
                        print("--- Animação Retomada ---")


        # Lógica de atualização de estado
        if estado_app == "COMPUTANDO":
            # Verifica se todas as threads terminaram
            if not any(t.is_alive() for t in threads):
                print("--- Computação Finalizada ---")
                estado_app = "ANIMANDO"

        # ### MODIFICADO: A lógica de animação SÓ avança se o estado for "ANIMANDO"
        elif estado_app == "ANIMANDO":
            tempo_animacao += clock.get_time() / 1000.0
            if tempo_animacao > velocidade_animacao:
                indice_animacao += 1
                tempo_animacao = 0

            # Verifica se todas as animações terminaram
            # Adicionado um tratamento de erro para caso um histórico esteja vazio
            if resultados:
                max_len = max((len(res["historico"]) for res in resultados.values() if res["historico"]), default=0)
                if max_len > 0 and indice_animacao >= max_len:
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

        # ### Estados de desenho. Pause desenha o mesmo frame mas não avança
        elif estado_app in ["ANIMANDO", "PAUSADO", "FINALIZADO"]:
            offsets_x = [0, LARGURA_LABIRINTO_TELA, LARGURA_LABIRINTO_TELA * 2]

            for i, nome in enumerate(algoritmos.keys()):
                offset_x = offsets_x[i] + MARGEM_ESQUERDA
                offset_y = 165 # Espaço para o título e botão de pausa

                # Desenha o título e o tempo de execução
                titulo_surf = fonte_titulo.render(nome, True, COR_TEXTO)
                screen.blit(titulo_surf, (offset_x, 65))

                tempo = resultados[nome]['tempo']
                tempo_surf = fonte_padrao.render(f"Tempo: {tempo:.4f}s", True, COR_TEXTO)
                screen.blit(tempo_surf, (offset_x, 65 + 25))

                n_cell_visitadas = resultados[nome]['numero de celulas visitadas']
                tempo_surf = fonte_padrao.render(f"Celulas visitadas: {n_cell_visitadas}", True, COR_TEXTO)
                screen.blit(tempo_surf, (offset_x, 65 + 25 + 25))

                pontuacao = resultados[nome]['pontuacao']
                tempo_surf = fonte_padrao.render(f"Pontuação: {pontuacao}", True, COR_TEXTO)
                screen.blit(tempo_surf, (offset_x, 65 + 25 + 25 + 25))

                # Desenha o labirinto base
                desenhar_labirinto(screen, LABIRINTO_GLOBAL, offset_x, offset_y)

                # Desenha os passos do algoritmo
                historico_atual = resultados[nome]["historico"]
                if historico_atual: # Garante que o histórico não está vazio
                    passo_atual = min(indice_animacao, len(historico_atual) - 1)

                    caminho_final = []
                    if estado_app == "FINALIZADO":
                        caminho_final = resultados[nome]["caminho_final"]

                    desenhar_passos(screen, historico_atual[:passo_atual], offset_x, offset_y, PONTO_INICIAL, PONTO_FINAL, caminho_final)
        
            mouse_pos = pygame.mouse.get_pos()

            if estado_app == "PAUSADO":
                # Desenha uma camada semi-transparente sobre toda a tela
                overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 50)) # Preto com alpha
                screen.blit(overlay, (0, 0))
                
                # Desenha o texto "PAUSADO" no centro
                texto_pausa_surf = fonte_status.render("PAUSADO", True, COR_TEXTO)
                texto_pausa_rect = texto_pausa_surf.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2))
                screen.blit(texto_pausa_surf, texto_pausa_rect)

            # O botão é desenhado em ambos os estados (ANIMANDO e PAUSADO)
            if estado_app in ["ANIMANDO", "PAUSADO"]:
                cor_botao_atual = COR_BOTAO_PAUSA_HOVER if botao_pause_rect.collidepoint(mouse_pos) else COR_BOTAO_PAUSA
                pygame.draw.rect(screen, cor_botao_atual, botao_pause_rect)
                
                texto_botao = "RETOMAR" if estado_app == "PAUSADO" else "PAUSAR"
                botao_texto_surf = fonte_titulo.render(texto_botao, True, COR_TEXTO)
                botao_texto_rect = botao_texto_surf.get_rect(center=botao_pause_rect.center)
                screen.blit(botao_texto_surf, botao_texto_rect)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()