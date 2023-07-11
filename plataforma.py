import pygame
from constantes import*
from auxiliar import Auxiliar

class Platform:
    def __init__(self,x,y,w,h,type=0) -> None:
        self.image = Auxiliar.get_surface_from_sprite_sheet("images\\texturas.jpg",5,5)[type]
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_ground_collision = pygame.Rect(self.rect.x, self.rect.y-1, self.rect.w, 10)
    
    def draw(self, screen):
        if(DEBUG):
            hitbox = self.image.get_rect()
            hitbox.topleft = (self.rect.x, self.rect.y)
            pygame.draw.rect(screen,BLUE, hitbox, 2)
            pygame.draw.rect(screen,GREEN, self.rect_ground_collision)
        screen.blit(self.image, self.rect)