import pygame
from constantes import *
from auxiliar import Auxiliar


class Bullet:
    def __init__(self,frame_rate_ms, move_rate_ms) -> None:
        bullet_sprite_r = Auxiliar.get_surface_from_sprite_sheet(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\bullet2.png", 3, 1,True) 
        bullet_sprite_l = Auxiliar.get_surface_from_sprite_sheet(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\bullet2.png", 3, 1,)
        self.bullet_r = bullet_sprite_r[:]
        self.bullet_l = bullet_sprite_l[:]
        self.bullet_state = "ready"
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.movement_done_x = 0
        self.movement_done_y = 0
        self.direction_y = UP
        self.direction = None
        self.animation = self.bullet_r
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image,BULLET_SIZE)#TAMAÑO DEL PERSONAJE(se declara dos veces en el codigo, una para que los rects tomen el valor de la imagen reescalada, y la otra para que se dibuje la imagen reescalada constantemente)
        self.rect = self.image.get_rect()
        #tiempo transcurrido
        self.time = 0
        self.time_movement = 0
        self.time_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        self.fire_sound = pygame.mixer.Sound(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\SOUNDS\shoot.wav")

    #FUNCION MOVER
    def do_movement(self, delta_ms):
        self.time_movement += delta_ms
        if (self.time_movement >= self.move_rate_ms):
            self.time_movement = 0
            self.add_x(self.move_x)
            self.add_y(self.move_y)

    #MOVER RECTANGULOS EN X
    def add_x(self,delta_x):
        self.rect.x += delta_x
    #MOVER RECTANGULOS EN Y
    def add_y(self,delta_y):
        self.rect.y += delta_y
    #ANIMACION
    def do_animation(self,delta_ms):
        self.time_animation += delta_ms
        if (self.time_animation >= self.frame_rate_ms):
            self.time_animation = 0
            self.frame += 1
            if self.frame >= len(self.animation):
                self.frame = 0
            self.image = self.animation[self.frame]
            #TAMAÑO DEL PERSONAJE
            self.image = pygame.transform.scale(self.image,BULLET_SIZE)

    def update(self, delta_ms):
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
        
    def draw(self, screen):
        if self.bullet_state == "fire":
            if(DEBUG):
                hitbox = self.image.get_rect()
                hitbox.topleft = (self.rect.x, self.rect.y)
                pygame.draw.rect(screen,GREEN, hitbox, 2)
            screen.blit(self.image, self.rect)
            
    def fire_bullet(self, speed, player_x, player_y, direction,delta_ms ,movement_range_x=600):
        if self.bullet_state == "ready":
            self.rect.x = player_x + 120
            self.rect.y = player_y +100
            self.movement_done_x = 0
            self.movement_done_y = 0
            self.direction_y = UP
            if direction == DERECHA:
                self.animation = self.bullet_r
                self.move_x = speed
            elif direction == IZQUIERDA:
                self.animation = self.bullet_l
                self.move_x = -speed
            self.fire_sound.play()
            self.bullet_state = "fire"

        if self.bullet_state == "fire":
            self.add_x(self.move_x)
            self.add_y(self.move_y)
            self.movement_done_x += abs(self.move_x)
            if self.movement_done_x >= movement_range_x:
                self.bullet_state = "ready"






        
