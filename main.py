import pygame
import sys
from constantes import*
from player import Player
from enemigo import Enemy
from plataforma import Platform
from bullet import Bullet
from botin import Loot
from lives import Lives
from pause_menu import PauseMenu
from main_menu import MainMenu
import json


screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA)) 
pygame.init()
clock = pygame.time.Clock()             
#game variables
game_pause = False
game_state = "main menu"
game_menu = True
game_running = False

# constantes
pause_menu = PauseMenu(x=606,y=316)
main_menu = MainMenu()
pause_sound = pygame.mixer.Sound("SOUNDS\\pause.wav")

bullet = Bullet(frame_rate_ms=100, move_rate_ms=10)
font = pygame.font.Font("images\\fonts\\PressStart2P-Regular.ttf", 36)

while True:
    print(clock)
    if game_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        game_state = main_menu.draw(screen)
        pygame.display.flip()

        if game_state == "running":
            game_menu = False
            game_running = True
            # Nivel seleccionado
            with open("LEVELS DATA\data_level_{}.json".format(main_menu.level_selected)) as json_file:
                data = json.load(json_file)
                level_music = pygame.mixer.Sound(data['level_music'])
                imagen_fondo = pygame.image.load(data['imagen_fondo']).convert_alpha()
            # Cargar Nivel
            player_1 = Player(x=0, y=700, frame_rate_ms=50, move_rate_ms=45, speed=17) 
            player_1.points = 0
            seconds = 60
            enemy_list = []
            level_music.play(1)
            for enemy_data in data['enemy_list']:
                x = enemy_data['x']
                y = enemy_data['y']
                frame_rate_ms = enemy_data['frame_rate_ms']
                move_rate_ms = enemy_data['move_rate_ms']
                speed = enemy_data['speed']
                enemy = Enemy(x, y, frame_rate_ms, move_rate_ms, speed)
                enemy_list.append(enemy)

            lista_plataformas=[]
            for platforms_data in data['platforms']:
                x = platforms_data["x"]
                y = platforms_data["y"]
                w = platforms_data["w"]
                h = platforms_data["h"]
                type = platforms_data["type"]
                plataforma = Platform(x,y,w,h,type)
                lista_plataformas.append(plataforma)

            lives_list = []
            for lives_data in data['lives_list']:
                x = lives_data["x"]
                y = lives_data["y"]
                live = Lives(x,y)
                lives_list.append(live)

            fruit_list = []
            for fruit_data in data['fruit_list']:
                x = fruit_data["x"]
                y = fruit_data["y"]
                points = fruit_data["points"]
                fruit = Loot(x,y,points)
                fruit_list.append(fruit)

    elif game_pause:
        level_music.set_volume(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        game_state = pause_menu.draw(screen)

        if game_state == "running":
            game_pause = False
            game_running = True
        elif game_state == "main menu":
            game_menu = True
            game_pause = False
            game_running= False
            main_menu.state = "main menu"
        pygame.display.flip()

    elif game_running:
        if not pause_menu.music_on:
            level_music.set_volume(0)
        else:
            level_music.set_volume(0.3)
        delta_ms = clock.tick(FPS)
        seconds -= (delta_ms / 1000)
        screen.blit(imagen_fondo,imagen_fondo.get_rect())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN: #PRESIONAR TECLA
                if event.key == pygame.K_DELETE:
                    pygame.quit()
                if event.key == pygame.K_ESCAPE:
                    game_pause = True
                    game_running = False
                    pause_sound.play()
                    pause_menu.state = "main pause"
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