import pygame
import sys
from constantes import*
from player import Player
from enemigo import Enemy
from boss import Boss
from plataforma import Platform
from botin import Loot 
from lives import Lives
from trap import Trap
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
just_opened = True
# constantes
pause_menu = PauseMenu(x=606,y=316)
main_menu = MainMenu()
pause_sound = pygame.mixer.Sound("SOUNDS\\pause.wav")
font = pygame.font.Font("images\\fonts\\PressStart2P-Regular.ttf", 36)
level1_points = 0

while True:
    delta_ms = clock.tick(FPS)
    if game_menu:
        if just_opened == True:
            main_menu.menu_music.play()
            just_opened = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        game_state = main_menu.draw(screen)
        pygame.display.flip()
        if game_state == "running":
            game_menu = False
            game_running = True
            # Nivel seleccionado
            with open("LEVELS DATA\data_level_{}.json".format(str(main_menu.level_selected))) as json_file:
                data = json.load(json_file)
                level_music = pygame.mixer.Sound(data['level_music'])
                imagen_fondo = pygame.image.load(data['imagen_fondo']).convert_alpha()
                imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))
                level_points = data["level_points"]
            # Cargar Nivel
            player_1 = Player(x=0, y=820, frame_rate_ms=50, move_rate_ms=45, speed=17)
            player_1.points = 0
            seconds = 60
            delta_ms = 0
            level_music.play(1)
            level_music.set_volume(0.1)
            enemy_list = []
            if not main_menu.level_selected == 3:
                for enemy_data in data['enemy_list']:
                    x = enemy_data['x']
                    y = enemy_data['y']
                    frame_rate_ms = enemy_data['frame_rate_ms']
                    move_rate_ms = enemy_data['move_rate_ms']
                    speed = enemy_data['speed']
                    range_x = enemy_data["range_x"]
                    enemy = Enemy(x, y, frame_rate_ms, move_rate_ms, speed,range_x)
                    enemy_list.append(enemy)
            traps_list=[]
            if not main_menu.level_selected == 3:
                for traps_data in data['trap_list']:
                    x = traps_data['x']
                    y = traps_data['y']
                    range_x = traps_data['range_x']
                    range_y = traps_data['range_y']
                    speed = traps_data['speed']
                    trap = Trap(x, y, range_x, range_y, speed)
                    traps_list.append(trap)

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
            boss_list = []
            if main_menu.level_selected == 3:
                for boss_data in data['boss_list']:
                    x = boss_data['x']
                    y = boss_data['y']
                    frame_rate_ms = boss_data['frame_rate_ms']
                    move_rate_ms = boss_data['move_rate_ms']
                    speed = boss_data['speed']
                    boss = Boss(x, y, frame_rate_ms, move_rate_ms, speed)
                    boss_list.append(boss)

    elif game_pause:
        level_music.set_volume(0.0)
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
            delta_ms = 0
            main_menu.state = "main menu"
            main_menu.menu_music.play(-1)
        pygame.display.flip()

    elif game_running:
        if not pause_menu.music_on:
            level_music.set_volume(0)
        else:
            level_music.set_volume(0.1)
        if not pause_menu.sound_on:
            player_1.sound_on = False
            player_1.bullet.sound_on = False
            for enemy in enemy_list:
                enemy.sound_on = False
            for fruit in fruit_list:
                fruit.sound_on = False
            for live in lives_list:
                live.sound_on = False
        elif pause_menu.sound_on:
            player_1.sound_on = True
            player_1.bullet.sound_on = True
            for enemy in enemy_list:
                enemy.sound_on = True
            for fruit in fruit_list:
                fruit.sound_on = True
            for live in lives_list:
                live.sound_on = True

        
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
        if(keys[pygame.K_f] and player_1.bullet.bullet_state=="ready"):
            player_1.bullet.fire_bullet(7 ,player_1.rect.x,player_1.rect.y,player_1.direction) #DISPARAR
            player_1.shoot()
        if player_1.bullet.bullet_state == "fire":
            player_1.bullet.fire_bullet(5 ,player_1.rect.x,player_1.rect.y,player_1.direction) #DISPARAR
            for enemy in enemy_list:
                if enemy.been_shoot(player_1.bullet):
                    player_1.bullet.bullet_state = "ready"
            for boss in boss_list:
                if boss.been_shoot(player_1.bullet):
                    player_1.bullet.bullet_state = "ready"
        # ---- HUD ----
        time_hud = font.render("00:{}".format(str(round(seconds)).zfill(2)), True, LIGHT_GRAY)#se redondean los segundos para que no se muestren decimales y se agrega un cero con zfill
        points_hud = font.render("POINTS:{}".format(str(player_1.points).zfill(3)), True, LIGHT_GRAY)
        # Centrar el timepo en pantalla
        time_hud_rect = time_hud.get_rect()  
        points_hud_rect = points_hud.get_rect()
        points_hud_rect.center = (ANCHO_VENTANA -200, 30)
        time_hud_rect.center = (ANCHO_VENTANA // 2, 30)
            
        #LOOT
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

        #ENEMIGOS
        for enemy in enemy_list:
            enemy.auto_walk()
            enemy.update(delta_ms,player_1.bullet)
            enemy.draw(screen)
            if not enemy.is_dying and player_1.rect_hitbox.colliderect(enemy.rect_hitbox):
                player_1.hurt_animation(enemy.direction)
            if player_1.rect_ground_collision.colliderect(enemy.top_hitbox):
                enemy.is_dying = True
                player_1.move_y = -25
                player_1.jump_sound.play()
            else:
                if not enemy.points_added_to_player and enemy.is_dead:
                    player_1.points += enemy.points
                    enemy_list.remove(enemy) 
                    enemy.points_added_to_player = True
        for trap in traps_list:
            trap.update(delta_ms,screen)
            if player_1.rect_hitbox.colliderect(trap.rect_hitbox):
                player_1.hurt_animation(player_1.direction) 
        

        #DIBUJAR PLATAFORMAS
        for plataforma in lista_plataformas: 
            plataforma.draw(screen)
        #BOSS
        for boss in boss_list:
            boss.update(delta_ms,player_1.bullet)
            boss.draw(screen)
            if (not boss.is_dying and player_1.rect_hitbox.colliderect(boss.rect_hitbox)) or (player_1.rect_hitbox.colliderect(boss.fire.rect_hitbox) and boss.is_shooting):
                player_1.hurt_animation(boss.direction)
            else:
                if not boss.points_added_to_player and boss.is_dead:
                    player_1.points += boss.points
                    boss_list.remove(boss)
                    boss.points_added_to_player = True

        player_1.update(delta_ms, lista_plataformas)
        player_1.draw(screen)
        player_1.bullet.draw(screen)
        player_1.bullet.update(delta_ms)
        screen.blit(time_hud, time_hud_rect)
        screen.blit(points_hud, points_hud_rect)

        if seconds <= 0 or player_1.lives == 0:
            level_music.stop()
            game_menu = True
            game_pause = False
            game_running= False
            main_menu.state = "game over"
            main_menu.game_over_music.play()
        if player_1.points >= level_points:
            level_music.stop()
            game_menu = True
            game_pause = False
            game_running= False
            main_menu.state = "level complete"
            
            if main_menu.level_selected == 1:
                main_menu.level_completed_music.play()
                level1_points = player_1.points
            elif main_menu.level_selected == 2:
                main_menu.level_completed_music.play()
                level2_points = player_1.points
            elif main_menu.level_selected >= 3:
                level3_points = player_1.points
                main_menu.game_completed_music.play()
                main_menu.total_score = level1_points + level2_points + level3_points
                datos_score = str("Player1: {}".format(main_menu.total_score))
                with open("SCORE.txt", "a") as archivo:
                    archivo.write(datos_score+"\n")
                archivo.close()
                print("dsjdlksjdklasjkldjasl")
            else:
                main_menu.level_completed_music.play()

        pygame.display.flip()
