import pygame
import sys
from constantes import *
from zgui_form import FormMenu

screen = pygame.display.set_mode((1200, 800))
pygame.init()
clock = pygame.time.Clock() 

form_menu = FormMenu(master_surface=screen, x=100, y=200, w=500, h=500, color_back=BLUE, color_border=PURPLE, active=True)
form_menu2 = FormMenu(master_surface=screen, x=400, y=200, w=500, h=500, color_back=GRAY, color_border=PURPLE, active=True)

while True:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # PRESIONAR TECLA
            if event.key == pygame.K_DELETE:
                pygame.quit()

    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    if form_menu.active:
        form_menu.update(lista_eventos)
        form_menu.draw()

    if form_menu2.active:
        form_menu2.update(lista_eventos)
        form_menu2.draw()

    pygame.display.flip()
