import time

from pygame import Rect, sprite

import celda
import observador as obs
import random as ran
from adminconf import AdminConf

config = AdminConf()


class Tablero(obs.Observador):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.rect = Rect((0, 0), (1000, 1000))
        self.color = config.color_tablero
        self.celdas = sprite.Group()
        self.celdas_mat = []

    def actualizar(self):
        self.calcularTamaño()
        self.calcularCeldas()

    def calcularTamaño(self):
        margen = config.margen_tablero

        self.width = config.ancho_pantalla - 2 * margen
        self.height = 0.7 * config.alto_pantalla - 2 * margen

        self.rect = Rect((0, 0), (self.width, self.height))
        self.rect.center = (config.ancho_pantalla / 2, config.alto_pantalla / 2)

    def calcularCeldas(self):
        self.celdas.empty()
        self.celdas_mat = []
        lado = celda.calcularLado(self.rect)

        fil = config.filas
        col = config.columnas
        sep = config.separacion_celdas
        pad = config.padding_tablero
        color = config.color_celda
        config.tamaño_celda = lado
        config.cambiarConf(notify=False)

        yspace = config.alto_pantalla / 2 - (pad + sep + fil * (lado + sep)) / 2
        xspace = config.ancho_pantalla / 2 - (pad + sep + col * (lado + sep)) / 2

        for i in range(fil):
            fila_celdas = []
            for j in range(col):
                xpos = xspace + pad + j * (lado + sep)
                ypos = yspace + pad + i * (lado + sep)
                cel = celda.Celda(lado, xpos, ypos, color)

                x = xpos + lado / 2
                y = ypos + lado / 2
                cel.rect.center = (x, y)

                time.sleep(0.0001)

                self.celdas.add(cel)
                fila_celdas.append(cel)
            self.celdas_mat.append(fila_celdas)
        self.minar()
        self.crearAdyacentes()

    def minar(self):
        sprites = self.celdas.sprites()
        ran.shuffle(sprites)

        for i in range(config.bombas):
            sprites[i].esMina = True

    def crearAdyacentes(self):
        filas = len(self.celdas_mat)
        cols = len(self.celdas_mat[0])

        for i in range(filas):
            for j in range(cols):
                celda_actual = self.celdas_mat[i][j]
                celda_actual.celdasAdj = []

                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if df == 0 and dc == 0:
                            continue
                        ni, nj = i + df, j + dc
                        if 0 <= ni < filas and 0 <= nj < cols:
                            vecino = self.celdas_mat[ni][nj]
                            celda_actual.celdasAdj.append(vecino)

                celda_actual.minasAdj = sum(
                    [1 for celda in celda_actual.celdasAdj if celda.esMina]
                )

    def dibujar(self, superficie):
        superficie.fill(self.color, self.rect)
        self.celdas.draw(superficie)
