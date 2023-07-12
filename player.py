import pygame
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet

class Player:
    def __init__(self, x, y, frame_rate_ms, move_rate_ms, speed):
        gengar_sprite_L = Auxiliar.get_surface_from_sprite_sheet("images\\gengar-sprite-sheet.png", 12, 6)
        gengar_sprite_R = Auxiliar.get_surface_from_sprite_sheet("images\\gengar-sprite-sheet.png", 12, 6, True)
        
        # Caminar
        self.walk_r = gengar_sprite_R[:8]
        self.walk_l = gengar_sprite_L[:8]
        
        # Quieto
        self.stay_r = gengar_sprite_R[60:72]
        self.stay_l = gengar_sprite_L[60:72]
        
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.speed = speed
        self.direction = DERECHA  # DIRECCION POR DEFECTO
        
        # Caida
        self.gravity = 5
        
        # Salto
        self.is_jumping = False
        self.jump_power = 50
        self.jump_l = gengar_sprite_L[24:29]
        self.jump_r = gengar_sprite_R[24:29]
        self.jump_sound = pygame.mixer.Sound("SOUNDS\\jump player.wav")
        self.hurt_sound = pygame.mixer.Sound("SOUNDS\\hurt.ogg")
        self.sound_on = True
        
        # Disparar
        self.shoot_l = gengar_sprite_L[35:40]
        self.shoot_r = gengar_sprite_R[35:40]
        self.is_shooting = False
        
        #recibir daño
        self.got_hurt_r = gengar_sprite_R[48:50]
        self.got_hurt_l = gengar_sprite_L[48:50]
        self.is_hurt = False
        # Animacion
        self.animation = self.stay_r
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE))  # TAMAÑO DEL PERSONAJE
        self.rect = self.image.get_rect()
        # Posicion inicial
        self.rect.x = x
        self.rect.y = y
        # Tiempo transcurrido
        self.time = 0
        self.time_movement = 0
        self.time_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        #stats
        self.points = 0
        self.lives = 6
        # Hitbox pies
        self.rect_ground_collision = pygame.Rect(self.rect.x + self.rect.w / 4 - 6, self.rect.y + self.rect.h - 33, self.rect.w / 2 + 8, 10)
        # hitbox
        self.rect_hitbox = pygame.Rect(self.rect.x+50, self.rect.y+30,self.rect.w/2,self.rect.h/2+40)
        
    def stay(self):
        if not self.is_shooting:
            direction = self.direction
            if (self.animation != self.stay_r and self.animation != self.stay_l and not self.is_jumping and not self.is_shooting):
                if direction == IZQUIERDA:
                    self.animation = self.stay_l
                    self.move_x = 0
                    self.frame = len(self.stay_l) - 1
                else:
                    self.animation = self.stay_r
                    self.move_x = 0
                    self.frame = len(self.stay_r) - 1
    
    def walk(self, direction, x=0, y=0):
        if not self.is_shooting and not self.is_hurt:
            self.direction = direction
            if (self.direction != direction and self.animation != self.walk_r and self.animation != self.walk_l):
                self.frame = 0
            if direction == DERECHA:
                self.move_x = self.speed
                if not self.is_jumping:
                    self.animation = self.walk_r
            else:
                self.move_x = -self.speed
                if not self.is_jumping:
                    self.animation = self.walk_l
    
    def jump(self):
        if not self.is_shooting and not self.is_hurt:
            if self.direction == DERECHA and not self.is_jumping:
                self.frame = 0
                self.move_y = -self.jump_power
                self.animation = self.jump_r
                self.is_jumping = True
                if self.sound_on:
                    self.jump_sound.play()
            elif self.direction == IZQUIERDA and not self.is_jumping:
                self.frame = 0
                self.move_y = -self.jump_power
                self.animation = self.jump_l
                self.is_jumping = True
                if self.sound_on:
                    self.jump_sound.play()
            
    def shoot(self):
        if not self.is_shooting and not self.is_hurt:
            if self.direction == DERECHA and self.animation != self.shoot_r:
                self.frame = 0
                self.animation = self.shoot_r
                self.is_shooting = True
            elif self.direction == IZQUIERDA and self.animation != self.shoot_l:
                self.frame = 0
                self.animation = self.shoot_l
                self.is_shooting = True

    def hurt_animation(self,enemy_direction):
        if not self.is_hurt:
            self.is_hurt = True
            self.time_hurt = 1000
            if enemy_direction == IZQUIERDA and self.animation != self.got_hurt_r:
                self.frame = 0
                self.animation = self.got_hurt_r
                if self.sound_on:
                    self.hurt_sound.play(1)
                self.move_x = -20
                self.move_y = -15
            elif enemy_direction == DERECHA and self.animation != self.got_hurt_l:
                self.frame = 0
                self.animation = self.got_hurt_l
                if self.sound_on:
                    self.hurt_sound.play(1)
                self.move_x = +20
                self.move_y = -15
            self.lives -= 1
    
    def do_movement(self, delta_ms, lista_plataformas):
        self.time_movement += delta_ms
        if self.time_movement >= self.move_rate_ms:
            self.time_movement = 0
            self.add_x(self.move_x)
            self.add_y(self.move_y)
            if not self.is_on_platform(lista_plataformas):
                self.move_y += self.gravity
                self.is_jumping = True
            else:
                self.move_y = 0
                self.is_jumping = False
                self.is_hurt = False
        # Cambiar de direccion en el aire
        keys = pygame.key.get_pressed()
        if self.is_jumping and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            if keys[pygame.K_LEFT]:
                self.direction = IZQUIERDA
                self.animation = self.jump_l
            elif keys[pygame.K_RIGHT]:
                self.direction = DERECHA
                self.animation = self.jump_r
    
    def is_on_platform(self, lista_plataformas):
        if self.rect.y >= GROUND_LEVEL:
            return True
        else:
            for plataforma in lista_plataformas:
                if self.rect_ground_collision.colliderect(plataforma.rect_ground_collision):
                    return True
            return False
    
    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rect_ground_collision.x += delta_x
        self.rect_hitbox.x += delta_x
    
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_ground_collision.y += delta_y
        self.rect_hitbox.y += delta_y

    
    def do_animation(self, delta_ms):
        self.time_animation += delta_ms
        if self.time_animation >= self.frame_rate_ms:
            self.time_animation = 0
            self.frame += 1
            if self.is_shooting or (self.is_shooting and self.is_jumping):
                if self.frame >= len(self.animation):
                    self.frame = len(self.animation) - 1
                    self.is_shooting = False
            else:
                if self.frame >= len(self.animation):
                    self.frame = 0
            self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE))
    
    def update(self, delta_ms, lista_plataformas):
        self.do_movement(delta_ms, lista_plataformas)
        self.do_animation(delta_ms)
    
    def draw(self, screen):
        if DEBUG:
            hitbox = self.image.get_rect()
            hitbox.topleft = (self.rect.x, self.rect.y)
            pygame.draw.rect(screen, GREEN, hitbox, 2)
            pygame.draw.rect(screen, BLUE, self.rect_ground_collision)
            pygame.draw.rect(screen, ORANGE, self.rect_hitbox,2)
        self.lives_hud = pygame.image.load("images\\HUD\\{}.png".format(self.lives))
        self.lives_hud = pygame.transform.scale(self.lives_hud, (162,51))
        screen.blit(self.lives_hud,self.lives_hud.get_rect())
        screen.blit(self.image, self.rect)
