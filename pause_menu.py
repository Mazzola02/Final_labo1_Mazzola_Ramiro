import pygame
from new_button_class import Button

class PauseMenu():
    def __init__(self, x, y):
        self.image_main = pygame.image.load(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\pause_menu.png").convert_alpha()
        self.image_main = pygame.transform.scale(self.image_main, (708, 448))
        self.image_settings = pygame.image.load(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\settings pause menu.png").convert_alpha()
        self.image_settings = pygame.transform.scale(self.image_settings, (708, 448))
        self.rect = self.image_main.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = "main pause"
        self.resume_button = Button(1029, 389, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\resume_boton.png",True,True)
        self.settings_button = Button(1029, 513, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\settings_boton.png",True,True)
        self.quit_button = Button(1029, 636, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\quit_boton.png",True,True)
        self.sound_checkmark = Button(718, 472, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\checkmark.png",False,True)
        self.disabled_sound_checkmark = Button(718, 472, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\empty_checkmark.png",False,True)
        self.sound_on = True
        self.music_checkmark = Button(718, 552, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\checkmark.png",False,True)
        self.disabled_music_checkmark = Button(718, 552, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\empty_checkmark.png",False,True)
        self.music_on = True
        self.done_button = Button(672, 638, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\done_boton.png",True,True)


    def draw(self, screen):
        if self.state == "main pause":
            screen.blit(self.image_main, self.rect)
            if self.resume_button.update(screen):
                self.state = "running"
            if self.settings_button.update(screen):
                self.state = "settings"
            if self.quit_button.update(screen):
                self.state = "main menu"

        elif self.state == "settings":
            screen.blit(self.image_settings, self.rect)
            # Efectos de sonido
            if self.sound_on:
                if self.sound_checkmark.update(screen):
                    self.sound_on = False
            if not self.sound_on:
                if self.disabled_sound_checkmark.update(screen):
                    self.sound_on = True
            # Música
            if self.music_on:
                if self.music_checkmark.update(screen):
                    self.music_on = False
            if not self.music_on:
                if self.disabled_music_checkmark.update(screen):
                    self.music_on = True
            if self.done_button.update(screen):
                self.state = "main pause"
        return self.state
