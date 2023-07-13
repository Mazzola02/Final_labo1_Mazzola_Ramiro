import pygame
from constantes import *
from auxiliar import Auxiliar


class Fire:
    def __init__(self,frame_rate_ms) -> None:
        fire_sprite_r = Auxiliar.get_surface_from_sprite_sheet("images\\fire_sprite.png", 6, 3) 
        fire_sprite_l = Auxiliar.get_surface_from_sprite_sheet("images\\fire_sprite.png", 6, 3,True)
        self.bullet_r = fire_sprite_r[:]
        self.bullet_l = fire_sprite_l[:]
        self.frame = 0
        self.move_x = 0
        self.move_y = 0
        self.direction = None
        self.animation = self.bullet_r
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image,(400,400))#TAMAÑO DEL PERSONAJE(se declara dos veces en el codigo, una para que los rects tomen el valor de la imagen reescalada, y la otra para que se dibuje la imagen reescalada constantemente)
        self.rect = self.image.get_rect()
        #tiempo transcurrido
        self.time_animation = 0
        self.frame_rate_ms = frame_rate_ms
        self.fire_sound = pygame.mixer.Sound("SOUNDS\\Fire.aif")
        self.sound_on = True
        self.rect_hitbox = pygame.Rect(self.rect.x+50, self.rect.y+30,self.rect.w/2,self.rect.h/2+40)
        self.fire_rect_w = 300

    #ANIMACION
    def do_animation(self,delta_ms):
        self.time_animation += delta_ms
        if (self.time_animation >= self.frame_rate_ms):
            self.time_animation = 0
            if self.sound_on and self.frame == 0:
                self.fire_sound.play()
            self.frame += 1
            if self.frame >= len(self.animation):
                self.frame = 0
            self.image = self.animation[self.frame]
            #TAMAÑO DEL PERSONAJE
            self.image = pygame.transform.scale(self.image,(400,400))

    def fire_bullet(self, boss_x, boss_y, direction):
            if direction == DERECHA:
                self.rect.x = boss_x + 370
                self.rect.y = boss_y +18
                self.rect_hitbox = pygame.Rect(self.rect.x, self.rect.y+120,self.fire_rect_w,100)
                self.animation = self.bullet_r
            elif direction == IZQUIERDA:
                self.rect.x = boss_x - 370
                self.rect.y = boss_y +18
                self.rect_hitbox = pygame.Rect(self.rect.x+100, self.rect.y+120,self.fire_rect_w,100)
                self.animation = self.bullet_l

    def update(self,boss_x,boss_y,direction,screen,delta_ms):
        self.fire_bullet(boss_x,boss_y,direction)
        self.do_animation(delta_ms)
        if self.frame == 0:
            self.fire_rect_w = 112
        elif self.frame == 1:
            self.fire_rect_w = 140
        elif self.frame == 2:
            self.fire_rect_w = 206
        elif self.frame == 3:
            self.fire_rect_w = 276
        elif self.frame == 4:
            self.fire_rect_w = 338
        elif self.frame == 5:
            self.fire_rect_w = 370
        elif self.frame == 6:
            self.fire_rect_w = 380
        elif self.frame == 7:
            self.fire_rect_w = 380
        elif self.frame == 8:
            self.fire_rect_w = 380
        elif self.frame == 9:
            self.fire_rect_w = 380
        elif self.frame == 10:
            self.fire_rect_w = 380
        elif self.frame == 11:
            self.fire_rect_w = 380
        elif self.frame == 12:
            self.fire_rect_w = 380
        elif self.frame == 13:
            self.fire_rect_w = 300
        elif self.frame == 14:
            self.fire_rect_w = 200
        elif self.frame == 15:
            self.fire_rect_w = 100
        elif self.frame == 16:
            self.fire_rect_w = 0
        elif self.frame == 17:
            self.fire_rect_w = 0
        self.draw(screen)


    def draw(self, screen):
            if(DEBUG):
                hitbox = self.image.get_rect()
                hitbox.topleft = (self.rect.x, self.rect.y)
                pygame.draw.rect(screen,GREEN, hitbox, 2)
                pygame.draw.rect(screen, ORANGE, self.rect_hitbox,2)
            screen.blit(self.image, self.rect)








        
         