import pygame
from player import Player
from constantes import *
from auxiliar import Auxiliar
from boss_fire import Fire
import random

class Boss(Player):
    def __init__(self, x, y, frame_rate_ms, move_rate_ms, speed):
        super().__init__(x, y, frame_rate_ms, move_rate_ms, speed)
        charizard_sprite_R = Auxiliar.get_surface_from_sprite_sheet("images\\charizard_sprite.png", 12, 2, True)
        charizard_sprite_L = Auxiliar.get_surface_from_sprite_sheet("images\\charizard_sprite.png", 12, 2)
        # caminar
        self.fly_r = charizard_sprite_L[4:8]
        self.fly_l = charizard_sprite_R[4:8]
        # quieto
        self.dying_r = charizard_sprite_L[14:15]
        self.dying_l = charizard_sprite_R[14:15]
        self.hurt_r = charizard_sprite_L[14:15]
        self.hurt_l = charizard_sprite_R[14:15]
        self.shoot_r = charizard_sprite_R[12:]
        self.shoot_l = charizard_sprite_L[12:]
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.movement_done_x = 0
        self.movement_done_y = 0
        self.speed = speed
        self.speed_y = 2
        self.direction = DERECHA  # DIRECCION POR DEFECTO
        self.direction_y = UP
        # caida
        # animacion
        self.animation = self.fly_r
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image, (400, 400))  # TAMAÑO DEL PERSONAJE(se declara dos veces en el codigo, una para que los rects tomen el valor de la imagen reescalada, y la otra para que se dibuje la imagen reescalada constantemente)
        self.rect = self.image.get_rect()
        # posicion inicial
        self.rect.x = x
        self.rect.y = y
        # tiempo transcurrido
        self.time = 0
        self.time_movement = 0
        self.time_animation = 1
        self.dying_animation_time = 0
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        # hitbox pies
        self.is_dead = False
        self.is_dying = False
        self.been_shoot_sound = pygame.mixer.Sound("SOUNDS\\enemy explosion.ogg")
        self.been_shoot_sound.set_volume(0.5)
        self.sound_on = True
        self.points = 999
        self.boss_bar_width = 994
        self.points_added_to_player = False
        self.rect_hitbox = pygame.Rect(self.rect.x+70, self.rect.y+100,280,200)
        self.fire = Fire(frame_rate_ms=40)
        

    # muriendo
    def die_animation(self):
        direction = self.direction
        if (self.animation != self.dying_r and self.animation != self.dying_l):
            self.frame = 0
            if (direction == IZQUIERDA):
                self.animation = self.dying_l
                self.move_x = 0
                self.move_y = 1
            else:
                self.animation = self.dying_r
                self.move_x = 0
                self.move_y = 1

    def been_shoot(self, bullet):
        retorno = False
        if self.rect_hitbox.colliderect(bullet.rect) and not self.is_dying:
            self.boss_bar_width -= 50
            self.been_shoot_sound.play()
            if self.boss_bar_width <= 1:
                self.is_dying = True
            retorno = True
        return retorno

    def shoot_fire(self):
        if not self.is_shooting and not self.is_hurt:
            if self.direction == DERECHA and self.animation != self.shoot_r:
                self.frame = 0
                self.animation = self.shoot_l
                self.move_x = 0
                self.move_y = 5
                self.is_shooting = True
            elif self.direction == IZQUIERDA and self.animation != self.shoot_l:
                self.frame = 0
                self.animation = self.shoot_r
                self.move_x = 0
                self.move_y = 5
                self.is_shooting = True
        if self.frame >= 5:
            self.frame = 5
            self.fire.update(self.rect.x,self.rect.y,self.direction,self.screen,self.delta)
            


    # CAMINAR
    def auto_walk(self, movement_range_x):
        if not self.is_dying and not self.is_shooting:
            if (self.direction == DERECHA):
                self.animation = self.fly_r
                self.move_x = self.speed
                self.move_y = -5
                self.movement_done_x += abs(self.move_x)
                if self.movement_done_x >= movement_range_x:
                    self.movement_done_x = 0
                    self.direction = IZQUIERDA

            elif (self.direction == IZQUIERDA):
                self.animation = self.fly_l
                self.move_x = -self.speed
                self.move_y = -5
                self.movement_done_x += abs(self.move_x)
                if self.movement_done_x >= movement_range_x:
                    self.movement_done_x = 0
                    self.direction = DERECHA
        if self.rect.x <= 0:
            self.direction = DERECHA
        elif self.rect.x >= ANCHO_VENTANA - self.rect.x:
            self.direction = IZQUIERDA
        if self.time >= 4000:
            self.shoot_fire()
            if self.time >= 8000:
                self.time = 0
                self.is_shooting = False

    # FUNCION MOVER
    def do_movement(self, delta_ms):
        self.time_movement += delta_ms
        if (self.time_movement >= self.move_rate_ms):
            self.time_movement = 0
            self.add_x(self.move_x)
            self.add_y(self.move_y)

    # MOVER RECTANGULOS EN X
    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rect_hitbox.x += delta_x

    # MOVER RECTANGULOS EN Y
    def add_y(self, delta_y):
        self.rect.y += delta_y
        self.rect_hitbox.y += delta_y

    # ANIMACION
    def do_animation(self, delta_ms, bullet):
        self.time_animation += delta_ms
        if (self.time_animation >= self.frame_rate_ms):
            self.time_animation = 0
            self.frame += 1
            if self.frame >= len(self.animation):
                self.frame = 0
            if self.is_dying == True:
                self.die_animation()
                if self.sound_on:
                    self.been_shoot_sound.play()
                self.dying_animation_time += delta_ms
                if self.dying_animation_time >= 500: #TIEMPO QUE TARDA EN COMPLETAR LA ANIMACION DE MUERTE
                    self.is_dead = True
                    self.dying_animation_time = 0
            self.image = self.animation[self.frame]
            # TAMAÑO DEL PERSONAJE
            self.image = pygame.transform.scale(self.image, (400, 400))

    def update(self, delta_ms, bullet):
            self.time += delta_ms
            self.delta = delta_ms
            self.do_movement(delta_ms)
            self.do_animation(delta_ms, bullet)
            self.auto_walk(8000)

    def draw(self, screen):
            self.screen = screen
            if (DEBUG):
                hitbox = self.image.get_rect()
                hitbox.topleft = (self.rect.x, self.rect.y)
                pygame.draw.rect(screen, GREEN, hitbox, 2)
                pygame.draw.rect(screen, PURPLE, self.rect_hitbox,2)
            pygame.draw.rect(screen, BLACK, pygame.Rect(460,50,1000,25),4)
            pygame.draw.rect(screen, ORANGE, pygame.Rect(464,54,self.boss_bar_width,17))
            screen.blit(self.image, self.rect)
