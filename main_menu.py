import pygame
from button_class import Button
from constantes import*
class MainMenu():
    def __init__(self):
        self.image_main = pygame.image.load("images\\Menu\\Main menu.png").convert_alpha()
        self.image_select_level = pygame.image.load("images\\Menu\\Level_Menu.png").convert_alpha()
        self.image_game_over = pygame.image.load("images\\Menu\\Game Over Screen.png").convert_alpha()
        self.image_level_completed = pygame.image.load("images\\Menu\\Level complete Screen.png").convert_alpha()
        self.image_game_completed = pygame.image.load("images\\Menu\\Game complete Screen.png").convert_alpha()
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
        self.level_completed_music = pygame.mixer.Sound("SOUNDS\\level_complete.wav")
        self.game_completed_music = pygame.mixer.Sound("SOUNDS\\game_completed.wav")
        self.menu_music = pygame.mixer.Sound("SOUNDS\\8BitMenuMusic.wav")
        self.menu_music.set_volume(0.1)
        self.game_over_music.set_volume(0.3)
        self.level1_completed = False 
        self.level2_completed = False
        self.level3_blocked = Button(1233, 603, "images\\Menu\\level3_blocked.png",False)
        self.level2_blocked = Button(1233, 379, "images\\Menu\\level2_blocked.png",False)
        self.blocked_sound = pygame.mixer.Sound("SOUNDS\\denied.wav")
        self.total_score = 0
        self.scoreback_button = Button(1233, 827, "images\\Menu\\BigBackButton.png")
        self.font = pygame.font.Font("images\\fonts\\PressStart2P-Regular.ttf", 36)
        self.scores = self.load_scores()
        self.image_score = pygame.image.load("images\\Menu\\ScoreScreen.png").convert_alpha()

    def load_scores(self):
        scores = []
        with open("SCORE.txt", "r") as archivo:
            lineas = archivo.readlines()
        for linea in lineas:
            puntuacion = linea.strip()
            scores.append(puntuacion)
        return scores
    
    def render_scores(self, screen):
        for i, puntuacion in enumerate(self.scores):
            score = self.font.render(puntuacion, True, (255, 255, 255))
            score_rect = score.get_rect()
            score_rect.center = (ANCHO_VENTANA // 2, 300 + i * 40)
            screen.blit(score, score_rect)
    
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

            if self.level1_completed == False:
                if self.level2_blocked.update(screen):
                    self.blocked_sound.play()
            else:
                if self.level2_button.update(screen):
                    self.state = "running"
                    self.level_selected = 2
            if self.level2_completed == False:
                if self.level3_blocked.update(screen):
                    self.blocked_sound.play()
            else:
                if self.level3_button.update(screen):
                    self.state = "running"
                    self.level_selected = 3
            if self.back_button.update(screen):
                self.state = "main menu"

        elif self.state == "score":
            screen.blit(self.image_score, self.rect)
            self.render_scores(screen)
            if self.scoreback_button.update(screen):
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
            if self.level_selected == 1:
                self.level1_completed = True
                screen.blit(self.image_level_completed, self.rect)
            elif self.level_selected == 2:
                self.level2_completed = True
                screen.blit(self.image_level_completed, self.rect)
            elif self.level_selected == 3:
                screen.blit(self.image_game_completed, self.rect)
            if self.continue_button.update(screen):
                self.state = "running"
                self.level_selected += 1
                if self.level_selected > 3:
                    self.state = "main menu"
                self.level_completed_music.stop()
        if self.state != "main menu" and self.state !="select level" and self.state !="score":
            self.menu_music.stop()
        return self.state
