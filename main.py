import threading as thr

import pygame as pg

import adminconf as ac
import boton as btn
import constantes as c
import tablero as t

pg.init()
conf = ac.AdminConf()

info = pg.display.Info()

conf.ancho_pantalla = info.current_w
conf.alto_pantalla = info.current_h

# lienzo
canva = pg.display.set_mode((conf.ancho_pantalla, conf.alto_pantalla))
bg_color = conf.color_fondo

# texto
fuente = pg.font.SysFont("Arial", 30)


def escribir(string, x, y):
    texto = fuente.render(string, True, (255, 255, 255))
    canva.blit(texto, (x, y))


# Tiempo
reloj = pg.time.Clock()

# control

prueba = "No"

run = True

# items
tablero = t.Tablero()
tablero.actualizar()

bots = btn.Boton(190, 100, 220, 950)
bots2 = btn.Boton(190, 100, conf.ancho_pantalla - 220, 950)
botr = btn.Boton(190, 100, 20, 950)
botr2 = btn.Boton(190, 100, conf.ancho_pantalla - 420, 950)

conf.agregar(tablero)

vals = list(c.dists.values())
counter = len(vals) - 1

while run:
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            run = False
        elif evt.type == pg.KEYUP:
            if evt.key == pg.K_ESCAPE:
                run = False
        elif evt.type == pg.MOUSEBUTTONUP:
            if bots.rect.collidepoint(evt.pos):
                hilo = thr.Thread(
                    target=conf.__setattr__, args=["filas", conf.filas + 1], daemon=True
                )
                hilo.start()
                # conf.filas += 1

            elif bots2.rect.collidepoint(evt.pos):
                hilo = thr.Thread(
                    target=conf.__setattr__,
                    args=["columnas", conf.columnas + 1],
                    daemon=True,
                )
                hilo.start()
                # conf.columnas += 1

            elif botr.rect.collidepoint(evt.pos):
                hilo = thr.Thread(
                    target=conf.__setattr__, args=["filas", conf.filas - 1], daemon=True
                )
                hilo.start()
                # conf.filas -= 1

            elif botr2.rect.collidepoint(evt.pos):
                hilo = thr.Thread(
                    target=conf.__setattr__,
                    args=["columnas", conf.columnas - 1],
                    daemon=True,
                )
                hilo.start()
                # conf.columnas-= 1

    # bot.image.fill(bot.color)
    canva.fill(bg_color)
    tablero.dibujar(canva)

    prueba = str(
        f"filas: {conf.filas} columnas: {conf.columnas}, celdas: {conf.filas * conf.columnas}"
    )
    escribir(f"lado : {conf.tamaño_celda}, {prueba}", 100, 100)
    escribir(f"FPS: {int(reloj.get_fps())}", 100, 140)

    canva.fill(bots.color, bots2.rect)
    canva.fill(bots.color, bots.rect)
    canva.fill(bots.color, botr2.rect)
    canva.fill(bots.color, botr.rect)

    pg.display.flip()
    reloj.tick(c.FPS)

pg.quit()
