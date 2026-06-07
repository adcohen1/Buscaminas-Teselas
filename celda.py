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
        _fuente = font.SysFont("timesnewroman", 30)
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
            numero = obtener_fuente().render(str(self.minasAdj), True, (255, 255, 255))
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
            fuente = obtener_fuente()
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
    sep = config.separacion_celdas
    pad = config.padding_tablero

    xlado = (rp.w - sep * (col - 1) - 2 * pad) / col
    ylado = (rp.h - sep * (fil - 1) - 2 * pad) / fil

    return int(min(xlado, ylado))
