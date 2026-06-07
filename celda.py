from pygame import Surface, font
from pygame.sprite import Sprite

import observador as obs
from adminconf import AdminConf

config = AdminConf()
_fuente = None


def obtener_fuente():
    global _fuente
    if _fuente is None:
        if not font.get_init():
            font.init()
        _fuente = font.SysFont("Arial", 30)
    return _fuente


class Celda(obs.Observador, Sprite):
    def __init__(self, lado, xpos, ypos, color):
        super().__init__()

        self.color = color
        self.image = Surface((lado, lado))
        self.image.fill(self.color)
        self.image.convert()

        self.rect = self.image.get_rect()
        self.minasAdj = 0
        self.celdasAdj = []

        self.esMina = False
        self.estaMarcada = False
        self.estaAbierta = False

    def actualizar(self): ...

    def contarAdyacentes(self): ...

    def accionar(self):
        if self.esMina:
            self.explotar()
            return
        self.estaAbierta = True
        self.image.fill(config.color_tablero)
        if self.minasAdj > 0:
            numero = obtener_fuente().render(str(self.minasAdj), True, (255, 255, 255))
            numero_rect = numero.get_rect(center=(self.image.get_width() // 2, self.image.get_height() // 2))
            self.image.blit(numero, numero_rect)
        else:
            # Si es 0, no dibujamos número
            pass
        if self.minasAdj != 0:
            return
        for celda in self.celdasAdj:
            if not celda.estaAbierta:
                celda.accionar()

    def marcar(self):
        if self.estaMarcada:
            self.estaMarcada = False
            return
        self.estaMarcada = True

    def explotar(self):
        self.image.fill(config.color_bomba)


def calcularLado(rp):
    # rp: rectangulo padre

    fil = config.filas
    col = config.columnas
    sep = config.separacion_celdas
    pad = config.padding_tablero

    xlado = (rp.w - sep * (col - 1) - 2 * pad) / col
    ylado = (rp.h - sep * (fil - 1) - 2 * pad) / fil

    return int(min(xlado, ylado))
