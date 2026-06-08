import time
import random as ran
import pygame as pg

import core.observador as obs
from core.adminconf import AdminConf
from componentes.celda import Celda, CeldaRenderer, calcularLado

config = AdminConf()


class Tablero(obs.Observador):
    """Clase que representa la lógica de negocios y estado del tablero de juego."""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.rect = pg.Rect((0, 0), (1000, 1000))
        self.color = config.color_tablero
        self.celdas = []  # Lista estándar para el bucle de colisiones e iteración
        self.celdas_mat = []
        self.estado = "JUGANDO"
        self.minas_creadas = False
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.num_bombas_generadas = 0

    def contar_banderas(self):
        """Cuenta el número de banderas colocadas en el tablero."""
        return sum(1 for fila in self.celdas_mat for cel in fila if cel.estaMarcada)

    def get_tiempo(self):
        """Devuelve el tiempo transcurrido en segundos de la partida."""
        if self.tiempo_inicio is None:
            return 0
        if self.estado != "JUGANDO":
            if self.tiempo_fin is None:
                self.tiempo_fin = time.time()
            return int(self.tiempo_fin - self.tiempo_inicio)
        return int(time.time() - self.tiempo_inicio)

    def revelar_minas(self):
        """Revela la posición de todas las minas en el tablero."""
        for fila in self.celdas_mat:
            for cel in fila:
                if cel.esMina:
                    cel.explotar()

    def verificar_victoria(self):
        """Comprueba si se han abierto todas las celdas seguras."""
        for fila in self.celdas_mat:
            for cel in fila:
                if not cel.esMina and not cel.estaAbierta:
                    return False
        return True

    def actualizar(self):
        """Calcula el tamaño y genera las celdas lógicas."""
        self.calcularTamaño()
        self.calcularCeldas()

    def reposicionar(self):
        """Recalcular dimensiones y coordenadas lógicas de las celdas sin reiniciar."""
        self.calcularTamaño()
        if not self.celdas_mat:
            return

        lado = calcularLado(self.rect)
        fil = config.filas
        col = config.columnas
        sep = int(lado * 0.1)
        pad = config.padding_tablero
        config.tamaño_celda = lado
        config.cambiarConf(notify=False)

        yspace = config.alto_pantalla / 2 - (pad + sep + fil * (lado + sep)) / 2
        xspace = config.ancho_pantalla / 2 - (pad + sep + col * (lado + sep)) / 2

        for i in range(fil):
            for j in range(col):
                cel = self.celdas_mat[i][j]
                xpos = xspace + pad + j * (lado + sep)
                ypos = yspace + pad + i * (lado + sep)

                cel.rect.x = xpos
                cel.rect.y = ypos
                cel.rect.width = lado
                cel.rect.height = lado

    def calcularTamaño(self):
        """Calcula el tamaño del contenedor del tablero centrado en pantalla."""
        margen = config.margen_tablero

        self.width = config.ancho_pantalla - 2 * margen
        self.height = 0.7 * config.alto_pantalla - 2 * margen

        self.rect = pg.Rect((0, 0), (self.width, self.height))
        self.rect.center = (config.ancho_pantalla / 2, config.alto_pantalla / 2)

    def calcularCeldas(self):
        """Crea e inicializa la matriz lógica de celdas."""
        self.celdas.clear()
        self.celdas_mat = []
        lado = calcularLado(self.rect)

        fil = config.filas
        col = config.columnas
        sep = int(lado * 0.1)
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
                cel = Celda(lado, xpos, ypos, color)

                time.sleep(0.0001)

                self.celdas.append(cel)
                fila_celdas.append(cel)
            self.celdas_mat.append(fila_celdas)
        self.crearAdyacentes()
        self.minas_creadas = False
        self.tiempo_inicio = None
        self.tiempo_fin = None

    def generar_minas(self, celda_inicial):
        """Genera minas aleatorias evitando la celda del primer clic y sus vecinas."""
        # 1. Identificar las celdas excluidas
        excluidas = {celda_inicial}
        for vecino in celda_inicial.celdasAdj:
            excluidas.add(vecino)

        # 2. Celdas disponibles para colocar minas
        disponibles = [
            cel for fila in self.celdas_mat for cel in fila if cel not in excluidas
        ]

        # 3. Mezclar y colocar bombas según porcentaje configurado
        total_celdas = config.filas * config.columnas
        num_bombas_deseadas = max(
            1 if config.bombas > 0 else 0, int(total_celdas * (config.bombas / 100.0))
        )
        num_bombas = min(num_bombas_deseadas, len(disponibles))
        ran.shuffle(disponibles)
        for i in range(num_bombas):
            disponibles[i].esMina = True

        # 4. Calcular el número de minas vecinas para cada celda
        for fila in self.celdas_mat:
            for cel in fila:
                cel.minasAdj = sum([1 for vecino in cel.celdasAdj if vecino.esMina])

        self.minas_creadas = True
        self.tiempo_inicio = time.time()
        self.tiempo_fin = None
        self.num_bombas_generadas = num_bombas

    def minar(self):
        """Distribuye minas iniciales sin evitar ninguna celda específica."""
        sprites = list(self.celdas)
        ran.shuffle(sprites)

        total_celdas = config.filas * config.columnas
        num_bombas_deseadas = max(
            1 if config.bombas > 0 else 0, int(total_celdas * (config.bombas / 100.0))
        )
        num_bombas = min(num_bombas_deseadas, len(sprites))

        for i in range(num_bombas):
            sprites[i].esMina = True

    def crearAdyacentes(self):
        """Construye las relaciones de adyacencia de las celdas en el tablero."""
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


class TableroRenderer:
    """Clase encargada de dibujar el tablero de juego y sus celdas en Pygame."""

    @staticmethod
    def dibujar(superficie, tablero: Tablero):
        """Dibuja el fondo del tablero y delega el dibujado de cada celda a CeldaRenderer."""
        superficie.fill(tablero.color, tablero.rect)
        for celda in tablero.celdas:
            CeldaRenderer.dibujar(superficie, celda)
