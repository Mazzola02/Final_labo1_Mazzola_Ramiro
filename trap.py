import pygame
from constantes import *
from auxiliar import Auxiliar

class Trap:
    def __init__(self, x, y, range_x=0,range_y=0,speed=5, frame_rate_ms=20, move_rate_ms=20):
        saw_sprite = Auxiliar.get_surface_from_sprite_sheet("images\\sawblade .png", 2, 1)
        self.saw_sprite = saw_sprite[:]
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.movement_done_x = 0
        self.movement_done_y = 0
        self.range_x = range_x
        self.range_y = range_y
        self.speed = speed
        self.speed_y = 5
        self.direction = DERECHA  # DIRECCION POR DEFECTO
        self.direction_y = UP
        # caida
        # animacion
        self.animation = self.saw_sprite
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
        self.rect_hitbox = pygame.Rect(self.rect.x+30, self.rect.y+30,self.rect.w/2+40,self.rect.h/2+40)

    # CAMINAR
    def auto_walk(self,movement_range_x=0, movement_range_y=0):
            if (self.direction == DERECHA):
                self.animation = self.saw_sprite
                self.move_x = self.speed
                self.movement_done_x += abs(self.move_x)
                if self.movement_done_x >= self.range_x:
                    self.movement_done_x = 0
                    self.direction = IZQUIERDA

            elif (self.direction == IZQUIERDA):
                self.animation = self.saw_sprite
                self.move_x = -self.speed
                self.movement_done_x += abs(self.move_x)
                if self.movement_done_x >= self.range_x:
                    self.movement_done_x = 0
                    self.direction = DERECHA
            if self.range_y != 0:
                if (self.direction_y == UP):
                    self.move_y = self.speed_y
                    self.movement_done_y += abs(self.move_y)
                    if self.movement_done_y >= self.range_y:
                        self.movement_done_y = 0
                        self.direction_y = DOWN

                elif (self.direction_y == DOWN):
                    self.move_y = -self.speed_y
                    self.movement_done_y += abs(self.move_y)
                    if self.movement_done_y >= self.range_y:
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
    def do_animation(self, delta_ms):
        self.time_animation += delta_ms
        if (self.time_animation >= self.frame_rate_ms):
            self.time_animation = 0
            self.frame += 1
            if self.frame >= len(self.animation):
                self.frame = 0
            self.image = self.animation[self.frame]
            # TAMAÑO DEL PERSONAJE
            self.image = pygame.transform.scale(self.image, (100, 100))

    def update(self, delta_ms, screen):
            self.auto_walk(self.range_x)
            self.do_movement(delta_ms)
            self.do_animation(delta_ms)
            self.draw(screen)

    def draw(self, screen):
            if (DEBUG):
                hitbox = self.image.get_rect()
                hitbox.topleft = (self.rect.x, self.rect.y)
                pygame.draw.rect(screen, GREEN, hitbox, 2)
                pygame.draw.rect(screen, PURPLE, self.rect_hitbox,2)
            screen.blit(self.image, self.rect)
