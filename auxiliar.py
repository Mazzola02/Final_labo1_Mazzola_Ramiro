import pygame
from constantes import *
class Auxiliar:
    @staticmethod
    def get_surface_from_sprite_sheet(path, columnas, filas, flip = False):
        lista = []
        surface_image = pygame.image.load(path).convert_alpha()
        frame_ancho = int(surface_image.get_width() / columnas)
        frame_alto = int(surface_image.get_height() / filas)
        for fila in range(filas):
            for columna in range(columnas):
                x = columna * frame_ancho
                y = fila * frame_alto
                surface_fotograma = surface_image.subsurface((x, y, frame_ancho, frame_alto))
                if flip:
                    surface_fotograma = pygame.transform.flip(surface_fotograma,True,False)
                lista.append(surface_fotograma)
        return lista
