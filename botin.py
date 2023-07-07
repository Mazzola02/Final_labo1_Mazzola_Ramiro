import pygame
from constantes import *
from auxiliar import Auxiliar

class Loot:
    def __init__(self, x, y,points, frame_rate_ms=40):
        self.fruit_animation = Auxiliar.get_surface_from_sprite_sheet(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Wumpa Fruit.png", 14, 1)
        self.picked_up_sound = pygame.mixer.Sound(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\SOUNDS\coin.ogg")
        self.frame = 0
        # animacion
        self.animation = self.fruit_animation
        self.image = self.animation[self.frame]
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
        self.points = points
        self.is_been_picked_up = False
        self.points_added = False

    def is_picked_up(self,player_rect):
        if self.rect.colliderect(player_rect):
            if not self.is_been_picked_up: 
                self.is_been_picked_up = True
                self.picked_up_sound.play()

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

    def update(self, delta_ms,player_rect):
        self.do_animation(delta_ms)
        self.is_picked_up(player_rect)

    def draw(self, screen):
        if (DEBUG):
            hitbox = self.image.get_rect()
            hitbox.topleft = (self.rect.x, self.rect.y)
            pygame.draw.rect(screen, GREEN, hitbox, 2)

        screen.blit(self.image, self.rect)
