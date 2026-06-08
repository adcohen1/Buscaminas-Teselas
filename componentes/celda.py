import pygame as pg
import observador as obs
from adminconf import AdminConf

config = AdminConf()


class Celda(obs.Observador):
    """Clase que representa el modelo y lógica de una celda individual."""

    def __init__(self, lado, xpos, ypos, color):
        self.color = color
        self.rect = pg.Rect(xpos, ypos, lado, lado)
        self.minasAdj = 0
        self.celdasAdj = []

        self.esMina = False
        self.estaMarcada = False
        self.estaAbierta = False
        self.estaExplotada = False

    def actualizar(self):
        """Método requerido por la interfaz de Observador."""
        pass

    def contarAdyacentes(self):
        """Método heredado vacío."""
        pass

    def accionar(self):
        """Acción de hacer clic izquierdo (abrir) la celda."""
        if self.estaAbierta:
            return False
        if self.estaMarcada:
            return False
        if self.esMina:
            self.explotar()
            return True
        self.estaAbierta = True

        if self.minasAdj != 0:
            return False

        # Cascada para abrir celdas adyacentes si no hay minas alrededor
        for celda in self.celdasAdj:
            if not celda.estaAbierta:
                celda.accionar()
        return False

    def marcar(self):
        """Acción de marcar con bandera (clic derecho) la celda."""
        if self.estaAbierta:
            return
        self.estaMarcada = not self.estaMarcada

    def explotar(self):
        """Marca la celda como explotada tras activarse una mina."""
        self.estaExplotada = True


class CeldaRenderer:
    """Clase encargada del renderizado visual de una celda en Pygame."""

    _fuentes = {}

    @classmethod
    def obtener_fuente(cls, lado=30):
        """Obtiene la fuente de Pygame escalada según el tamaño de la celda."""
        size = max(8, int(lado * 0.65))
        if size not in cls._fuentes:
            if not pg.font.get_init():
                pg.font.init()
            cls._fuentes[size] = pg.font.SysFont("timesnewroman", size, bold=True)
        return cls._fuentes[size]

    @staticmethod
    def dibujar(superficie, celda: Celda):
        """Dibuja el estado visual actual de la celda en la superficie destino."""
        if celda.estaAbierta:
            color_fondo = config.color_tablero
            if celda.esMina:
                color_fondo = config.color_bomba
            pg.draw.rect(superficie, color_fondo, celda.rect)

            if not celda.esMina and celda.minasAdj > 0:
                fuente = CeldaRenderer.obtener_fuente(celda.rect.width)
                numero = fuente.render(str(celda.minasAdj), True, (255, 255, 255))
                numero_rect = numero.get_rect(center=celda.rect.center)
                superficie.blit(numero, numero_rect)
        elif celda.estaMarcada:
            pg.draw.rect(superficie, (230, 80, 80), celda.rect)
            fuente = CeldaRenderer.obtener_fuente(celda.rect.width)
            bandera = fuente.render("P", True, (255, 255, 255))
            bandera_rect = bandera.get_rect(center=celda.rect.center)
            superficie.blit(bandera, bandera_rect)
        elif celda.estaExplotada:
            pg.draw.rect(superficie, config.color_bomba, celda.rect)
        else:
            pg.draw.rect(superficie, celda.color, celda.rect)


def calcularLado(rp):
    """Calcula el tamaño de celda ideal según el rectángulo contenedor de la ventana."""
    fil = config.filas
    col = config.columnas
    pad = config.padding_tablero
    factor_sep = 0.1

    xlado = (rp.w - 2 * pad) / (col + factor_sep * (col - 1))
    ylado = (rp.h - 2 * pad) / (fil + factor_sep * (fil - 1))

    return int(min(xlado, ylado))
