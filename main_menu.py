import pygame
from new_button_class import Button

class MainMenu():
    def __init__(self):
        self.image_main = pygame.image.load(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\Main menu.png").convert_alpha()
        self.image_select_level = pygame.image.load(r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\Level_Menu.png").convert_alpha()
        self.rect = self.image_main.get_rect()
        self.state = "main menu"
        self.play_button = Button(164, 200, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\play_button.png")
        self.score_button = Button(164, 480, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\score_button.png")
        self.quit_button = Button(164, 770, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\bigQuitButton.png")
        self.level1_button = Button(1233, 155, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\level1_button.png")
        self.level2_button = Button(1233, 379, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\level2_button.png")
        self.level3_button = Button(1233, 603, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\level3_button.png")
        self.back_button = Button(1233, 827, r"C:\Users\Ramiro\Documents\JUEGO_RAMIRO_labo1\images\Menu\BigBackButton.png")
    
    def draw(self, screen):
        
        if self.state == "main menu":
            self.state="main menu"
            screen.blit(self.image_main, self.rect)
            if self.play_button.update(screen):
                self.state = "select level"
            if self.score_button.update(screen):
                self.state = "score"
            if self.quit_button.update(screen):
                pygame.quit()
        elif self.state == "select level":
            screen.blit(self.image_select_level, self.rect)
            if self.level1_button.update(screen):
                self.state = "running"
            if self.level2_button.update(screen):
                pass
            if self.level3_button.update(screen):
                pass
            if self.back_button.update(screen):
                self.state = "main menu"
        return self.state
