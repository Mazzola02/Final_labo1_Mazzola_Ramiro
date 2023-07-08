import pygame
import sys
from constantes import *
from zgui_button import Button

class Form:
    def __init__(self, master_surface, x, y, w, h, color_back, color_border, active):
        self.master_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_back = color_back
        self.color_border = color_border

        self.surface = pygame.Surface((w, h))
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active
        self.x = x
        self.y = y

        if self.color_back is not None:
            self.surface.fill(self.color_back)

    def render(self):
        pass

    def update(self, lista_eventos):
        pass

    def draw(self):
        self.master_surface.blit(self.surface, self.slave_rect)


class FormMenu(Form):
    def __init__(self, master_surface, x, y, w, h, color_back, color_border, active):
        super().__init__(master_surface, x, y, w, h, color_back, color_border, active)

        self.boton1 = Button(master_form=self, x=100, y=50, w=200, h=80, color_back=RED, color_border=GREEN,
                             on_click=self.on_click_boton1, on_click_param="1234", text="MENU", font="Verdana",
                             text_size=30, text_color=GREEN)
        self.boton2 = Button(master_form=self, x=100, y=200, w=100, h=50, color_back=RED, color_border=GREEN,
                             on_click=self.on_click_boton1, on_click_param="88", text="MENU", font="Verdana",
                             text_size=30, text_color=GREEN)
        self.lista_widget = [self.boton1, self.boton2]

    def on_click_boton1(self, parametro):
        print("CLICK", parametro)

    def update(self, lista_eventos):
        for aux_boton in self.lista_widget:
            aux_boton.update(lista_eventos)

    def draw(self):
        self.master_surface.blit(self.surface, self.slave_rect)
        for aux_boton in self.lista_widget:
            aux_boton.draw(self.master_surface)


