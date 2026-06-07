from pygame import Surface
from pygame.sprite import Sprite

import observador as obs
from adminconf import AdminConf

config = AdminConf()


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
