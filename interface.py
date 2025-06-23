# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 #delta time, possibilita escolher quantidade de frames


# Gerar o labirinto

# Desenhar o labirinto

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")



    # Pseudocodigo

    # MAIN():
        # Criar 3 Treads

        # Thread 1:
            # Rodar algoritmo 1
        
        # Thread 2:
            # Rodar algoritmo 2

        # Thread 3:
            # Rodar algoritmo 3







    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000 # NÃO MUDAR

pygame.quit()