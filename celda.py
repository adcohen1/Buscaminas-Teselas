from pygame import Surface, font
from pygame.sprite import Sprite

import observador as obs
from adminconf import AdminConf

config = AdminConf()
_fuentes = {}

def obtener_fuente(lado=30):
    size = max(8, int(lado * 0.65))
    if size not in _fuentes:
        if not font.get_init():
            font.init()
        _fuentes[size] = font.SysFont("timesnewroman", size, bold=True)
    return _fuentes[size]


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
        self.estaExplotada = False

    def actualizar(self): ...

    def contarAdyacentes(self): ...

    def accionar(self):
        if self.estaAbierta:
            return False
        if self.estaMarcada:
            return False
        if self.esMina:
            self.explotar()
            return True
        self.estaAbierta = True
        self.image.fill(config.color_tablero)
        if self.minasAdj > 0:
            numero = obtener_fuente(config.tamaño_celda).render(str(self.minasAdj), True, (255, 255, 255))
            numero_rect = numero.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() // 2)
            )
            self.image.blit(numero, numero_rect)
        else:
            # Si es 0, no dibujamos número
            pass
        if self.minasAdj != 0:
            return False
        for celda in self.celdasAdj:
            if not celda.estaAbierta:
                celda.accionar()
        return False

    def marcar(self):
        if self.estaAbierta:
            return
        if self.estaMarcada:
            self.estaMarcada = False
            self.image.fill(self.color)
        else:
            self.estaMarcada = True
            self.image.fill((230, 80, 80))
            fuente = obtener_fuente(config.tamaño_celda)
            bandera = fuente.render("P", True, (255, 255, 255))
            bandera_rect = bandera.get_rect(
                center=(self.image.get_width() // 2, self.image.get_height() // 2)
            )
            self.image.blit(bandera, bandera_rect)

    def explotar(self):
        self.estaExplotada = True
        self.image.fill(config.color_bomba)


def calcularLado(rp):
    # rp: rectangulo padre

    fil = config.filas
    col = config.columnas
    pad = config.padding_tablero
    factor_sep = 0.1

    xlado = (rp.w - 2 * pad) / (col + factor_sep * (col - 1))
    ylado = (rp.h - 2 * pad) / (fil + factor_sep * (fil - 1))

    return int(min(xlado, ylado))
