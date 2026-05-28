from pygame import Surface
from pygame.sprite import Sprite


class Boton(Sprite):
    def __init__(self, w, h, x, y, texto=''):
        super().__init__()
        self.image = Surface((w, h))
        self.color = (200, 200, 200)
        self.image.fill(self.color)
        self.image.convert()

        self.texto = texto
        self.rect = self.image.get_rect()
        self.rect.center = (x + w / 2, y + h / 2)

    def dibujar(self, superficie):
        # self.draw(superficie)
        self.image.fill(self.color)
