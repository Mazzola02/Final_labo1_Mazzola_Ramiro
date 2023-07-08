import pygame

class Button():
    def __init__(self,x,y,image_path) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image=pygame.transform.scale(self.image,(242,94))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        self.click_sound = pygame.mixer.Sound(r"c:\Users\Ramiro\Desktop\interface\click.ogg")

    def been_clicked(self):
        self.clicked = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.click_sound.play()
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.clicked
        
    def update(self,screen):
        retorno = False
        self.draw(screen)
        if self.been_clicked():
            retorno = True
        return retorno
    def draw(self,screen):
        screen.blit(self.image,self.rect)