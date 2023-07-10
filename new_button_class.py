import pygame

class Button():
    def __init__(self, x, y, image_path, sound_flag=True,double_size=False):
        self.image = pygame.image.load(image_path).convert_alpha()
        if double_size:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))  # Duplica el tamaño del botón
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False
        self.click_sound = pygame.mixer.Sound(r"c:\Users\Ramiro\Desktop\interface\click.ogg")
        if not sound_flag:
            self.click_sound.set_volume(0)

    def update(self, screen):
        self.draw(screen)
        if not self.active and self.been_clicked():
            self.click_sound.play()
            self.active = True
            return True
        elif self.active and not self.been_clicked():
            self.active = False
        return False

    def been_clicked(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
