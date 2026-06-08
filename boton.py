import pygame as pg
from pygame import Surface
from pygame.sprite import Sprite

_fuentes_boton = {}

def obtener_fuente_boton(size=24):
    if size not in _fuentes_boton:
        if not pg.font.get_init():
            pg.font.init()
        _fuentes_boton[size] = pg.font.SysFont("Arial", size, bold=True)
    return _fuentes_boton[size]


class Boton(Sprite):
    def __init__(self, w, h, x, y, texto='', color_base=(71, 85, 105), color_hover=(100, 116, 139), color_texto=(255, 255, 255), tam_fuente=24):
        super().__init__()
        self.image = Surface((w, h), pg.SRCALPHA)
        self.color = color_base
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.texto = texto
        self.tam_fuente = tam_fuente
        self.rect = self.image.get_rect()
        # Maintain compatibility with center initialization:
        self.rect.center = (x + w / 2, y + h / 2)
        self.hovered = False
        self.focused = False

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered

    def dibujar(self, superficie):
        self.image.fill((0, 0, 0, 0))  # Clear with transparency
        
        # Decide color based on hover or focus
        color_actual = self.color_base
        if self.hovered or self.focused:
            color_actual = self.color_hover
            
        # Draw rounded rectangle
        pg.draw.rect(self.image, color_actual, (0, 0, self.rect.w, self.rect.h), border_radius=10)
        
        # If focused or hovered, draw outline
        if self.focused:
            pg.draw.rect(self.image, (255, 255, 255), (0, 0, self.rect.w, self.rect.h), width=3, border_radius=10)
        elif self.hovered:
            pg.draw.rect(self.image, (241, 245, 249), (0, 0, self.rect.w, self.rect.h), width=1, border_radius=10)
        
        # Render text
        if self.texto:
            fuente = obtener_fuente_boton(self.tam_fuente)
            text_surf = fuente.render(self.texto, True, self.color_texto)
            text_rect = text_surf.get_rect(center=(self.rect.w // 2, self.rect.h // 2))
            self.image.blit(text_surf, text_rect)
            
        superficie.blit(self.image, self.rect)

