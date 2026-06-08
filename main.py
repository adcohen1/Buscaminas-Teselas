import os
import ctypes

import threading as thr
import pygame as pg

import adminconf as ac
import boton as btn
import constantes as c
import tablero as t

# Hacer que la aplicación sea consciente del DPI en Windows para evitar que se cambie la resolución del monitor o se estire
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

os.environ["SDL_VIDEO_CENTERED"] = "1"

pg.init()
conf = ac.AdminConf()

info = pg.display.Info()

conf.ancho_pantalla = int(info.current_w * 2 / 3)
conf.alto_pantalla = int(info.current_h * 2 / 3)

orientacion = "vertical" if conf.ancho_pantalla < conf.alto_pantalla else "horizontal"

# lienzo
canva = pg.display.set_mode((conf.ancho_pantalla, conf.alto_pantalla), pg.RESIZABLE)
bg_color = conf.color_fondo

# texto
fuente = pg.font.SysFont("Arial", 30)


def escribir(string, x, y):
    texto = fuente.render(string, True, (255, 255, 255))
    canva.blit(texto, (x, y))


# Tiempo
reloj = pg.time.Clock()

# control

# prueba = "No"

run = True
r_presionado = False
r_inicio = 0
TIEMPO_REINICIO = 5

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
game_active = False

def run_game(nuevo_juego=True):
    global run, r_presionado, r_inicio, canva, bg_color, tablero, bots, bots2, botr, botr2, game_active
    
    # Asegurar que la pantalla esté configurada y caption esté definido
    canva = pg.display.get_surface()
    if canva is None:
        canva = pg.display.set_mode((conf.ancho_pantalla, conf.alto_pantalla), pg.RESIZABLE)
    pg.display.set_caption("Teselaminas")
    
    bg_color = conf.color_fondo
    
    # Ajustar posición inicial de los botones modificadores de tamaño
    bots.rect.center = (220 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
    bots2.rect.center = (conf.ancho_pantalla - 220 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
    botr.rect.center = (20 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
    botr2.rect.center = (conf.ancho_pantalla - 420 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
    
    if nuevo_juego:
        tablero.actualizar()
        tablero.estado = "JUGANDO"
        game_active = True
    else:
        tablero.reposicionar()
        
    run = True
    r_presionado = False
    r_inicio = 0
    TIEMPO_REINICIO = 5

    while run:
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                return "QUIT"
            elif evt.type == pg.VIDEORESIZE:
                # Actualizar dimensiones en la configuracion
                conf.ancho_pantalla = evt.size[0]
                conf.alto_pantalla = evt.size[1]
                # Solo recrear el lienzo si no está en pantalla completa (NOFRAME)
                es_fullscreen = bool(pg.display.get_surface().get_flags() & pg.NOFRAME)
                if not es_fullscreen:
                    canva = pg.display.set_mode(
                        (conf.ancho_pantalla, conf.alto_pantalla), pg.RESIZABLE
                    )
                # Recalcular el tamaño de las celdas
                tablero.reposicionar()
                # Reposicionar botones modificadores
                bots.rect.center = (220 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
                bots2.rect.center = (conf.ancho_pantalla - 220 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
                botr.rect.center = (20 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
                botr2.rect.center = (conf.ancho_pantalla - 420 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)

            elif evt.type == pg.KEYDOWN:
                if evt.key == pg.K_r and not r_presionado:
                    r_presionado = True
                    r_inicio = pg.time.get_ticks()

            elif evt.type == pg.KEYUP:
                if evt.key == pg.K_ESCAPE:
                    return "MENU"
                elif evt.key == pg.K_r:
                    if tablero.estado != "JUGANDO":
                        # Reinicio inmediato si el juego terminó
                        tablero.actualizar()
                        tablero.estado = "JUGANDO"
                    elif r_presionado:
                        tiempo_mantenido = (pg.time.get_ticks() - r_inicio) / 1000
                        if tiempo_mantenido >= TIEMPO_REINICIO:
                            tablero.actualizar()
                            tablero.estado = "JUGANDO"
                    r_presionado = False

                # Alternar pantalla completa usando NOFRAME
                elif evt.key == pg.K_f:
                    es_fullscreen = bool(pg.display.get_surface().get_flags() & pg.NOFRAME)
                    if not es_fullscreen:
                        conf.ancho_pantalla = info.current_w
                        conf.alto_pantalla = info.current_h
                        canva = pg.display.set_mode(
                            (conf.ancho_pantalla, conf.alto_pantalla), pg.NOFRAME
                        )
                    else:
                        conf.ancho_pantalla = int(info.current_w * 2 / 3)
                        conf.alto_pantalla = int(info.current_h * 2 / 3)
                        x = (info.current_w - conf.ancho_pantalla) // 2
                        y = (info.current_h - conf.alto_pantalla) // 2
                        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"
                        canva = pg.display.set_mode(
                            (conf.ancho_pantalla, conf.alto_pantalla), pg.RESIZABLE
                        )
                    tablero.reposicionar()
                    bots.rect.center = (220 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
                    bots2.rect.center = (conf.ancho_pantalla - 220 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
                    botr.rect.center = (20 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
                    botr2.rect.center = (conf.ancho_pantalla - 420 + 190 / 2, conf.alto_pantalla - 120 + 100 / 2)
            elif evt.type == pg.MOUSEBUTTONUP:
                if bots.rect.collidepoint(evt.pos):
                    hilo = thr.Thread(
                        target=conf.__setattr__, args=["filas", conf.filas + 1], daemon=True
                    )
                    hilo.start()

                elif bots2.rect.collidepoint(evt.pos):
                    hilo = thr.Thread(
                        target=conf.__setattr__,
                        args=["columnas", conf.columnas + 1],
                        daemon=True,
                    )
                    hilo.start()

                elif botr.rect.collidepoint(evt.pos):
                    hilo = thr.Thread(
                        target=conf.__setattr__, args=["filas", conf.filas - 1], daemon=True
                    )
                    hilo.start()

                elif botr2.rect.collidepoint(evt.pos):
                    hilo = thr.Thread(
                        target=conf.__setattr__,
                        args=["columnas", conf.columnas - 1],
                        daemon=True,
                    )
                    hilo.start()

                else:
                    if tablero.estado == "JUGANDO":
                        for celda in tablero.celdas:
                            if celda.rect.collidepoint(evt.pos):
                                if evt.button == 1:  # Clic izquierdo
                                    if not tablero.minas_creadas:
                                        tablero.generar_minas(celda)
                                    if celda.accionar():
                                        tablero.estado = "DERROTA"
                                        tablero.revelar_minas()
                                    elif tablero.verificar_victoria():
                                        tablero.estado = "VICTORIA"
                                elif evt.button == 3:  # Clic derecho
                                    celda.marcar()
                                break

        # bot.image.fill(bot.color)
        canva.fill(bg_color)
        tablero.dibujar(canva)

        # Dibujar HUD
        fuente_hud = pg.font.SysFont("Arial", 36, bold=True)
        
        # Contador de banderas
        if tablero.minas_creadas:
            minas_restantes = tablero.num_bombas_generadas - tablero.contar_banderas()
        else:
            total_celdas = conf.filas * conf.columnas
            minas_restantes = max(1 if conf.bombas > 0 else 0, int(total_celdas * (conf.bombas / 100.0)))

        texto_minas = fuente_hud.render(f"Minas: {minas_restantes}", True, (255, 60, 60))
        rect_minas = texto_minas.get_rect(topleft=(50, 30))
        canva.blit(texto_minas, rect_minas)

        # Temporizador
        tiempo = tablero.get_tiempo()
        minutos = tiempo // 60
        segundos = tiempo % 60
        texto_tiempo = fuente_hud.render(f"Tiempo: {minutos:02d}:{segundos:02d}", True, (240, 240, 240))
        rect_tiempo = texto_tiempo.get_rect(topright=(conf.ancho_pantalla - 50, 30))
        canva.blit(texto_tiempo, rect_tiempo)

        # Dibujar botones de fila/columna en la parte inferior
        canva.fill(bots.color, bots2.rect)
        canva.fill(bots.color, bots.rect)
        canva.fill(bots.color, botr2.rect)
        canva.fill(bots.color, botr.rect)

        # Barra de progreso al mantener R durante el juego
        if r_presionado and tablero.estado == "JUGANDO":
            progreso = min((pg.time.get_ticks() - r_inicio) / 1000 / TIEMPO_REINICIO, 1.0)
            barra_ancho = 300
            barra_alto = 12
            barra_x = (conf.ancho_pantalla - barra_ancho) // 2
            barra_y = 30

            # Fondo de la barra
            pg.draw.rect(
                canva,
                (50, 50, 50),
                (barra_x, barra_y, barra_ancho, barra_alto),
                border_radius=6,
            )
            # Progreso
            color_barra = (80, 200, 120) if progreso < 1.0 else (255, 220, 50)
            pg.draw.rect(
                canva,
                color_barra,
                (barra_x, barra_y, int(barra_ancho * progreso), barra_alto),
                border_radius=6,
            )
            # Texto
            fuente_r = pg.font.SysFont("Arial", 18)
            texto_r = fuente_r.render(
                f"Mantén 'R' para reiniciar ({progreso * 100:.0f}%)", True, (220, 220, 220)
            )
            rect_r = texto_r.get_rect(
                center=(conf.ancho_pantalla // 2, barra_y + barra_alto + 18)
            )
            canva.blit(texto_r, rect_r)

            # Auto-reiniciar si se completó el tiempo mientras se mantiene presionado
            if progreso >= 1.0:
                tablero.actualizar()
                tablero.estado = "JUGANDO"
                r_presionado = False

        if tablero.estado != "JUGANDO":
            overlay = pg.Surface((conf.ancho_pantalla, conf.alto_pantalla), pg.SRCALPHA)
            overlay.fill((15, 23, 42, 200))

            ancho_box = 450
            alto_box = 220
            box_x = (conf.ancho_pantalla - ancho_box) // 2
            box_y = (conf.alto_pantalla - alto_box) // 2
            pg.draw.rect(
                overlay,
                (30, 41, 59, 240),
                (box_x, box_y, ancho_box, alto_box),
                border_radius=15,
            )
            pg.draw.rect(
                overlay,
                (71, 85, 105, 255),
                (box_x, box_y, ancho_box, alto_box),
                width=3,
                border_radius=15,
            )

            fuente_titulo = pg.font.SysFont("Arial", 40, bold=True)
            fuente_sub = pg.font.SysFont("Arial", 22)

            if tablero.estado == "DERROTA":
                texto_titulo = "¡GAME OVER!"
                color_titulo = (239, 68, 68)
            else:
                texto_titulo = "¡VICTORIA!"
                color_titulo = (234, 179, 8)

            render_titulo = fuente_titulo.render(texto_titulo, True, color_titulo)
            render_sub = fuente_sub.render(
                "Presiona 'R' para jugar de nuevo", True, (241, 245, 249)
            )

            rect_titulo = render_titulo.get_rect(
                center=(conf.ancho_pantalla // 2, conf.alto_pantalla // 2 - 30)
            )
            rect_sub = render_sub.get_rect(
                center=(conf.ancho_pantalla // 2, conf.alto_pantalla // 2 + 40)
            )

            overlay.blit(render_titulo, rect_titulo)
            overlay.blit(render_sub, rect_sub)

            canva.blit(overlay, (0, 0))

        pg.display.flip()
        reloj.tick(c.FPS)


if __name__ == "__main__":
    import menu
    menu.main()
