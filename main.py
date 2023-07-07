import pygame
import sys
from constantes import*
from player import Player
from enemigo import Enemy
from plataforma import Platform
from bullet import Bullet
from botin import Loot
from lives import Lives
from button_class import Button

screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA)) 
pygame.init()
clock = pygame.time.Clock()
seconds = 60

font = pygame.font.Font(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\fonts\PressStart2P-Regular.ttf", 36)  
imagen_fondo = pygame.image.load(PATH_IMAGE + "locations\\forest\\all.png").convert_alpha()
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA, ALTO_VENTANA))

player_1 = Player(x=0, y=700, frame_rate_ms=50, move_rate_ms=45, speed=17) 
bullet = Bullet(frame_rate_ms=100, move_rate_ms=10)

enemy_1 = Enemy(x=1000, y=400, frame_rate_ms=100, move_rate_ms=40, speed=5)
enemy_2 = Enemy(x=200, y=500, frame_rate_ms=100, move_rate_ms=40, speed=5)
enemy_3 = Enemy(x=900, y=600, frame_rate_ms=100, move_rate_ms=40, speed=5)
enemy_4 = Enemy(x=1000, y=700, frame_rate_ms=100, move_rate_ms=40, speed=5)

plataforma_1 = Platform(x=900,y=650,w=1100,h=110,type=9)
plataforma_2 = Platform(x=950,y=650,w=1100,h=110,type=9)

live_1 = Lives(x=1800,y=780)

fruit_1 = Loot(x=500, y=780,points = 10)
fruit_2 = Loot(x=600, y=780,points = 10)
fruit_3 = Loot(x=700, y=780,points = 10)
fruit_4 = Loot(x=800, y=780,points = 10)
fruit_5 = Loot(x=900, y=780,points = 10)
fruit_6 = Loot(x=1000, y=780,points = 10)
fruit_7 = Loot(x=1100, y=780,points = 10)
fruit_8 = Loot(x=1200, y=780,points = 10)

lista_plataformas = [plataforma_1,plataforma_2]
enemy_list = [enemy_1,enemy_2,enemy_3,enemy_4]
fruit_list= [fruit_1,fruit_2,fruit_3,fruit_4,fruit_5,fruit_6,fruit_7,fruit_8]
lives_list = [live_1]
#BOTONES
close_image = pygame.image.load(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\Buttons\Close.png").convert_alpha()
back_image = pygame.image.load(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\Buttons\Back.png").convert_alpha()

close_button = Button(ANCHO_VENTANA // 2 -50, ALTO_VENTANA // 2 + 100, close_image)
back_button = Button(ANCHO_VENTANA // 2 -350, ALTO_VENTANA // 2, back_image)
  
while True:
    delta_ms = clock.tick(FPS)
    seconds -= (delta_ms / 1000)
    screen.blit(imagen_fondo,imagen_fondo.get_rect())

    close_button.draw(screen)
    back_button.draw(screen)

    for event in pygame.event. get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: #PRESIONAR TECLA
            if event.key == pygame.K_DELETE:
                pygame.quit()
        elif event.type == pygame.KEYUP: #SOLTAR TECLA
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_1.stay() 

    keys = pygame.key.get_pressed()
    if(keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]):
        player_1.walk(IZQUIERDA)
    if(keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]):
        player_1.walk(DERECHA)
    if(keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]):
        player_1.stay() 
    if(not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]):
        player_1.stay()
    if(keys[pygame.K_SPACE]):
        player_1.jump()
    if(keys[pygame.K_f] and bullet.bullet_state=="ready"):
        bullet.fire_bullet(7 ,player_1.rect.x,player_1.rect.y,player_1.direction,delta_ms) #DISPARAR
        player_1.shoot()
    if bullet.bullet_state == "fire":
        bullet.fire_bullet(5 ,player_1.rect.x,player_1.rect.y,player_1.direction,delta_ms) #DISPARAR
        for enemy in enemy_list:
            if enemy.been_shoot(bullet):
                bullet.bullet_state = "ready"
    # ---- HUD ----
    time_hud = font.render("00:{}".format(str(round(seconds)).zfill(2)), True, LIGHT_GRAY)#se redondean los segundos para que no se muestren decimales y se agrega un cero con zfill
    points_hud = font.render("POINTS:{}".format(str(player_1.points).zfill(3)), True, LIGHT_GRAY)
    # Centrar el timepo en pantalla
    time_hud_rect = time_hud.get_rect()  
    points_hud_rect = points_hud.get_rect()
    points_hud_rect.center = (ANCHO_VENTANA -200, 30)
    time_hud_rect.center = (ANCHO_VENTANA // 2, 30)

    #DIBUJAR PLATAFORMAS
    for plataforma in lista_plataformas: 
        plataforma.draw(screen)
        
    #ENEMIGOS
    for enemy in enemy_list:
        enemy.auto_walk(x=0, y=0,movement_range_x=500,movement_range_y=10)
        enemy.update(delta_ms,bullet)
        enemy.draw(screen)
        if not enemy.is_dying and player_1.rect_hitbox.colliderect(enemy.rect_hitbox):
            player_1.hurt_animation(enemy.direction)
        else:
            if not enemy.points_added_to_player and enemy.is_dead:
                player_1.points += enemy.points
                enemy_list.remove(enemy)
                enemy.points_added_to_player = True
    
    for fruit in fruit_list:
        fruit.draw(screen)
        fruit.update(delta_ms,player_1.rect_hitbox)
        if fruit.is_been_picked_up:
            player_1.points += fruit.points
            fruit_list.remove(fruit)
               
    for live in lives_list:
        live.draw(screen)
        live.update(delta_ms,player_1.rect_hitbox)
        if live.is_been_picked_up:
            player_1.lives += 6
            if player_1.lives > 6:
                player_1.lives = 6
            lives_list.remove(live)

    player_1.update(delta_ms, lista_plataformas)
    player_1.draw(screen)

    bullet.update(delta_ms)
    bullet.draw(screen)
    screen.blit(time_hud, time_hud_rect)
    screen.blit(points_hud, points_hud_rect)
    

    pygame.display.flip()