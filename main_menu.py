import pygame
from new_button_class import Button

class MainMenu():
    def __init__(self):
        self.image_main = pygame.image.load("images\\Menu\\Main menu.png").convert_alpha()
        self.image_select_level = pygame.image.load("images\\Menu\\Level_Menu.png").convert_alpha()
        self.image_game_over = pygame.image.load("images\\Menu\\Game Over Screen.png").convert_alpha()
        self.image_level_completed = pygame.image.load("images\\Menu\\Level complete Screen.png").convert_alpha()
        self.rect = self.image_main.get_rect()
        self.state = "main menu"
        self.play_button = Button(164, 200, "images\\Menu\\play_button.png")
        self.score_button = Button(164, 480, "images\\Menu\\score_button.png")
        self.quit_button = Button(164, 770, "images\\Menu\\bigQuitButton.png")
        self.level1_button = Button(1233, 155, "images\\Menu\\level1_button.png")
        self.level2_button = Button(1233, 379, "images\\Menu\\level2_button.png")
        self.level3_button = Button(1233, 603, "images\\Menu\\level3_button.png")
        self.back_button = Button(1233, 827, "images\\Menu\\BigBackButton.png")
        self.backToMenu_button = Button(1395, 827, "images\\Menu\\backToMenu_button.png")
        self.restart_button = Button(1395, 575, "images\\Menu\\restart_button.png")
        self.continue_button = Button(1095, 805, "images\\Menu\\continue_button.png")
        self.game_over_music = pygame.mixer.Sound("SOUNDS\\GameOver.wav")
        self.level_completed_music = pygame.mixer.Sound("SOUNDS\\win music.wav")
    
    def draw(self, screen):
        if self.state == "main menu":
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
                self.level_selected = 1
            if self.level2_button.update(screen):
                self.state = "running"
                self.level_selected = 2
            if self.level3_button.update(screen):
                self.state = "running"
                self.level_selected = 3
            if self.back_button.update(screen):
                self.state = "main menu"
        elif self.state == "game over":
            screen.blit(self.image_game_over, self.rect)
            if self.restart_button.update(screen):
                self.state = "running"
                self.game_over_music.stop()
            if self.backToMenu_button.update(screen):
                self.state = "main menu"
                self.game_over_music.stop()
        elif self.state == "level complete":
            screen.blit(self.image_level_completed, self.rect)
            if self.continue_button.update(screen):
                self.state = "running"
                self.level_selected += 1
                if self.level_selected > 3:
                    self.state = "main menu"
                self.level_completed_music.stop()
        return self.state
