import pygame
from player import Player
from constantes import *
from auxiliar import Auxiliar

class Enemy(Player):
    def __init__(self, x, y, frame_rate_ms, move_rate_ms, speed):
        super().__init__(x, y, frame_rate_ms, move_rate_ms, speed)
        gastly_sprite_L = Auxiliar.get_surface_from_sprite_sheet("images\\gastly_sprite.png", 9, 2)
        gastly_sprite_R = Auxiliar.get_surface_from_sprite_sheet("images\\gastly_sprite.png", 9, 2, True)
        # caminar
        self.walk_r = gastly_sprite_R[:9]
        self.walk_l = gastly_sprite_L[:9]
        # quieto
        self.dying_r = gastly_sprite_R[9:18]
        self.dying_l = gastly_sprite_L[9:18]
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.movement_done_x = 0
        self.movement_done_y = 0
        self.speed = speed
        self.speed_y = 1
        self.direction = DERECHA  # DIRECCION POR DEFECTO
        self.direction_y = UP
        # caida
        # animacion
        self.animation = self.walk_r
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image, (100, 100))  # TAMAÑO DEL PERSONAJE(se declara dos veces en el codigo, una para que los rects tomen el valor de la imagen reescalada, y la otra para que se dibuje la imagen reescalada constantemente)
        self.rect = self.image.get_rect()
        # posicion inicial
        self.rect.x = x
        self.rect.y = y
        # tiempo transcurrido
        self.time = 0
        self.time_movement = 0
        self.time_animation = 0
        self.dying_animation_time = 0
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        # hitbox pies
        self.is_dead = False
        self.is_dying = False
        self.been_shoot_sound = pygame.mixer.Sound("SOUNDS\\enemy explosion.ogg")
        self.been_shoot_sound.set_volume(0.5)
        self.points = 50
        self.points_added_to_player = False
        self.rect_hitbox = pygame.Rect(self.rect.x+30, self.rect.y+30,self.rect.w/2+40,self.rect.h/2+40)

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
            self.is_dying = True
            retorno = True
        return retorno

    # CAMINAR
    def auto_walk(self, x=0, y=0, movement_range_x=200, movement_range_y=10):
        if not self.is_dying:
            if (self.direction == DERECHA):
                self.animation = self.walk_r
                self.move_x = self.speed
                self.movement_done_x += abs(self.move_x)
                if self.movement_done_x >= movement_range_x:
                    self.movement_done_x = 0
                    self.direction = IZQUIERDA

            elif (self.direction == IZQUIERDA):
                self.animation = self.walk_l
                self.move_x = -self.speed
                self.movement_done_x += abs(self.move_x)
                if self.movement_done_x >= movement_range_x:
                    self.movement_done_x = 0
                    self.direction = DERECHA

            if (self.direction_y == UP):
                self.move_y = self.speed_y
                self.movement_done_y += abs(self.move_y)
                if self.movement_done_y >= movement_range_y:
                    self.movement_done_y = 0
                    self.direction_y = DOWN
            elif (self.direction_y == DOWN):
                self.move_y = -self.speed_y
                self.movement_done_y += abs(self.move_y)
                if self.movement_done_y >= movement_range_y:
                    self.movement_done_y = 0
                    self.direction_y = UP

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
                self.been_shoot_sound.play()
                self.dying_animation_time += delta_ms
                if self.dying_animation_time >= 150: #TIEMPO QUE TARDA EN COMPLETAR LA ANIMACION DE MUERTE
                    self.is_dead = True
                    self.dying_animation_time = 0
            self.image = self.animation[self.frame]
            # TAMAÑO DEL PERSONAJE
            self.image = pygame.transform.scale(self.image, (150, 150))

    def update(self, delta_ms, bullet):
            self.do_movement(delta_ms)
            self.do_animation(delta_ms, bullet)

    def draw(self, screen):
            if (DEBUG):
                hitbox = self.image.get_rect()
                hitbox.topleft = (self.rect.x, self.rect.y)
                pygame.draw.rect(screen, GREEN, hitbox, 2)
                pygame.draw.rect(screen, PURPLE, self.rect_hitbox,2)
            screen.blit(self.image, self.rect)
