import sys
import pygame as pg
import main as game
from componentes.boton import Boton, BotonRenderer

# Obtener variables de configuración y estado desde el módulo main
conf = game.conf
canva = game.canva
reloj = game.reloj

buttons = []
btn_nuevo = None
btn_continuar = None
btn_config = None
btn_puntuaciones = None
btn_acercade = None
btn_salir = None
btn_volver = None
btn_si = None
btn_no = None


def recreate_buttons():
    global \
        buttons, \
        btn_nuevo, \
        btn_continuar, \
        btn_config, \
        btn_puntuaciones, \
        btn_acercade, \
        btn_salir

    cx = conf.ancho_pantalla // 2
    cy_start = int(conf.alto_pantalla * 0.35)
    w = 320
    h = 55
    gap = 18

    # El botón Continuar está activo solo si hay una partida en progreso
    if game.game_active:
        color_continuar_base = (71, 85, 105)
        color_continuar_hover = (100, 116, 139)
        color_continuar_text = (255, 255, 255)
    else:
        color_continuar_base = (30, 41, 59)
        color_continuar_hover = (30, 41, 59)
        color_continuar_text = (100, 116, 139)

    btn_nuevo = Boton(
        w,
        h,
        cx - w // 2,
        cy_start,
        "Nuevo Juego",
        color_base=(30, 144, 255),
        color_hover=(65, 105, 225),
    )
    btn_continuar = Boton(
        w,
        h,
        cx - w // 2,
        cy_start + (h + gap),
        "Continuar",
        color_base=color_continuar_base,
        color_hover=color_continuar_hover,
        color_texto=color_continuar_text,
    )
    btn_config = Boton(w, h, cx - w // 2, cy_start + 2 * (h + gap), "Configuración")
    btn_puntuaciones = Boton(
        w, h, cx - w // 2, cy_start + 3 * (h + gap), "Puntuaciones"
    )
    btn_acercade = Boton(w, h, cx - w // 2, cy_start + 4 * (h + gap), "Acerca de")
    btn_salir = Boton(
        w,
        h,
        cx - w // 2,
        cy_start + 5 * (h + gap),
        "Salir",
        color_base=(185, 28, 28),
        color_hover=(220, 38, 38),
    )

    buttons = [
        btn_nuevo,
        btn_continuar,
        btn_config,
        btn_puntuaciones,
        btn_acercade,
        btn_salir,
    ]


def main_menu():
    global canva, btn_volver, btn_si, btn_no

    pg.display.set_caption("Teselaminas - Menú Principal")

    # Inicializar botones
    recreate_buttons()

    state = 0  # 0: Menú Principal, 1: WIP Configuración, 2: WIP Puntuaciones
    overlay_exit_open = False
    exit_focus_index = 1  # 0: Sí, 1: No (Focus por defecto en No)

    btn_si = None
    btn_no = None

    running = True
    while running:
        mouse_pos = pg.mouse.get_pos()

        # Actualizar hover de botones
        if overlay_exit_open:
            if btn_si and btn_no:
                btn_si.hovered = False
                btn_no.hovered = False
                btn_si.check_hover(mouse_pos)
                btn_no.check_hover(mouse_pos)
        elif state == 0:
            for b in buttons:
                b.hovered = False
                b.check_hover(mouse_pos)
        else:
            if btn_volver:
                btn_volver.hovered = False
                btn_volver.check_hover(mouse_pos)

        # Bucle de eventos
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                running = False

            elif evt.type == pg.VIDEORESIZE:
                conf.ancho_pantalla = evt.size[0]
                conf.alto_pantalla = evt.size[1]
                canva = pg.display.set_mode(
                    (conf.ancho_pantalla, conf.alto_pantalla), pg.RESIZABLE
                )

                recreate_buttons()
                cx = conf.ancho_pantalla // 2
                btn_volver = Boton(
                    200, 50, cx - 100, int(conf.alto_pantalla * 0.7), "Volver al Menú"
                )

                if overlay_exit_open:
                    cy = conf.alto_pantalla // 2
                    btn_si = Boton(
                        120,
                        45,
                        cx - 140,
                        cy + 20,
                        "Sí",
                        color_base=(185, 28, 28),
                        color_hover=(220, 38, 38),
                    )
                    btn_no = Boton(
                        120,
                        45,
                        cx + 20,
                        cy + 20,
                        "No",
                        color_base=(71, 85, 105),
                        color_hover=(100, 116, 139),
                    )
                    btn_si.focused = exit_focus_index == 0
                    btn_no.focused = exit_focus_index == 1

            elif evt.type == pg.KEYDOWN:
                if overlay_exit_open:
                    if evt.key == pg.K_ESCAPE:
                        overlay_exit_open = False
                    elif evt.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_TAB):
                        exit_focus_index = 1 - exit_focus_index
                        if btn_si and btn_no:
                            btn_si.focused = exit_focus_index == 0
                            btn_no.focused = exit_focus_index == 1
                    elif evt.key in (pg.K_RETURN, pg.K_KP_ENTER, pg.K_SPACE):
                        if exit_focus_index == 0:  # Sí -> Salir
                            pg.quit()
                            sys.exit()
                        else:  # No -> Cerrar overlay
                            overlay_exit_open = False
                else:
                    if evt.key == pg.K_ESCAPE:
                        # Si presionan ESC en el menú principal o WIP screens, abre confirmación de salida
                        if state != 0:
                            state = 0
                            recreate_buttons()
                        else:
                            overlay_exit_open = True
                            exit_focus_index = 1  # Foco en No
                            cx = conf.ancho_pantalla // 2
                            cy = conf.alto_pantalla // 2
                            btn_si = Boton(
                                120,
                                45,
                                cx - 140,
                                cy + 20,
                                "Sí",
                                color_base=(185, 28, 28),
                                color_hover=(220, 38, 38),
                            )
                            btn_no = Boton(
                                120,
                                45,
                                cx + 20,
                                cy + 20,
                                "No",
                                color_base=(71, 85, 105),
                                color_hover=(100, 116, 139),
                            )
                            btn_si.focused = False
                            btn_no.focused = True

            elif evt.type == pg.MOUSEBUTTONUP:
                if evt.button == 1:  # Clic izquierdo
                    if overlay_exit_open:
                        if btn_si and btn_si.rect.collidepoint(evt.pos):
                            pg.quit()
                            sys.exit()
                        elif btn_no and btn_no.rect.collidepoint(evt.pos):
                            overlay_exit_open = False
                    elif state == 0:
                        if btn_nuevo.rect.collidepoint(evt.pos):
                            res = game.run_game(nuevo_juego=True)
                            if res == "QUIT":
                                running = False
                            else:
                                pg.display.set_caption("Teselaminas - Menú Principal")
                                recreate_buttons()
                        elif (
                            btn_continuar.rect.collidepoint(evt.pos)
                            and game.game_active
                        ):
                            res = game.run_game(nuevo_juego=False)
                            if res == "QUIT":
                                running = False
                            else:
                                pg.display.set_caption("Teselaminas - Menú Principal")
                                recreate_buttons()
                        elif btn_config.rect.collidepoint(evt.pos):
                            state = 1
                            cx = conf.ancho_pantalla // 2
                            btn_volver = Boton(
                                200,
                                50,
                                cx - 100,
                                int(conf.alto_pantalla * 0.7),
                                "Volver al Menú",
                            )
                        elif btn_puntuaciones.rect.collidepoint(evt.pos):
                            state = 2
                            cx = conf.ancho_pantalla // 2
                            btn_volver = Boton(
                                200,
                                50,
                                cx - 100,
                                int(conf.alto_pantalla * 0.7),
                                "Volver al Menú",
                            )
                        elif btn_salir.rect.collidepoint(evt.pos):
                            overlay_exit_open = True
                            exit_focus_index = 1
                            cx = conf.ancho_pantalla // 2
                            cy = conf.alto_pantalla // 2
                            btn_si = Boton(
                                120,
                                45,
                                cx - 140,
                                cy + 20,
                                "Sí",
                                color_base=(185, 28, 28),
                                color_hover=(220, 38, 38),
                            )
                            btn_no = Boton(
                                120,
                                45,
                                cx + 20,
                                cy + 20,
                                "No",
                                color_base=(71, 85, 105),
                                color_hover=(100, 116, 139),
                            )
                            btn_si.focused = False
                            btn_no.focused = True
                    else:
                        if btn_volver and btn_volver.rect.collidepoint(evt.pos):
                            state = 0
                            recreate_buttons()

        # Dibujado de la escena
        canva.fill((15, 23, 42))

        if state == 0:
            # Título principal
            fuente_titulo = pg.font.SysFont("Arial", 64, bold=True)
            texto_titulo = fuente_titulo.render("Teselaminas", True, (248, 250, 252))
            rect_titulo = texto_titulo.get_rect(
                center=(conf.ancho_pantalla // 2, int(conf.alto_pantalla * 0.18))
            )

            # Sombra del título
            texto_sombra = fuente_titulo.render("Teselaminas", True, (2, 6, 23))
            rect_sombra = texto_sombra.get_rect(
                center=(
                    conf.ancho_pantalla // 2 + 4,
                    int(conf.alto_pantalla * 0.18) + 4,
                )
            )
            canva.blit(texto_sombra, rect_sombra)
            canva.blit(texto_titulo, rect_titulo)

            # Subtítulo descriptivo
            fuente_sub = pg.font.SysFont("Arial", 20)
            texto_sub = fuente_sub.render(
                "El Buscaminas de Próxima Generación", True, (148, 163, 184)
            )
            rect_sub = texto_sub.get_rect(
                center=(conf.ancho_pantalla // 2, int(conf.alto_pantalla * 0.26))
            )
            canva.blit(texto_sub, rect_sub)

            # Dibujar botones
            for b in buttons:
                BotonRenderer.dibujar(canva, b)

        elif state == 1 or state == 2:
            # Pantalla de Trabajo en Progreso (WIP)
            fuente_wip_tit = pg.font.SysFont("Arial", 48, bold=True)
            wip_title_str = "CONFIGURACIÓN" if state == 1 else "PUNTUACIONES"
            texto_wip_tit = fuente_wip_tit.render(wip_title_str, True, (248, 250, 252))
            rect_wip_tit = texto_wip_tit.get_rect(
                center=(conf.ancho_pantalla // 2, int(conf.alto_pantalla * 0.25))
            )

            texto_wip_tit_som = fuente_wip_tit.render(wip_title_str, True, (2, 6, 23))
            rect_wip_tit_som = texto_wip_tit_som.get_rect(
                center=(
                    conf.ancho_pantalla // 2 + 3,
                    int(conf.alto_pantalla * 0.25) + 3,
                )
            )
            canva.blit(texto_wip_tit_som, rect_wip_tit_som)
            canva.blit(texto_wip_tit, rect_wip_tit)

            # Texto explicativo
            fuente_wip_body = pg.font.SysFont("Arial", 24)
            texto_wip_body = fuente_wip_body.render(
                "TRABAJO EN PROGRESO (WIP)", True, (245, 158, 11)
            )
            rect_wip_body = texto_wip_body.get_rect(
                center=(conf.ancho_pantalla // 2, int(conf.alto_pantalla * 0.4))
            )
            canva.blit(texto_wip_body, rect_wip_body)

            texto_wip_sub = fuente_wip_body.render(
                "Esta sección estará disponible próximamente.", True, (148, 163, 184)
            )
            rect_wip_sub = texto_wip_sub.get_rect(
                center=(conf.ancho_pantalla // 2, int(conf.alto_pantalla * 0.48))
            )
            canva.blit(texto_wip_sub, rect_wip_sub)

            if btn_volver:
                BotonRenderer.dibujar(canva, btn_volver)

        # Dibujar overlay de confirmación de salida
        if overlay_exit_open:
            overlay = pg.Surface((conf.ancho_pantalla, conf.alto_pantalla), pg.SRCALPHA)
            overlay.fill((15, 23, 42, 210))

            ancho_box = 460
            alto_box = 230
            box_x = (conf.ancho_pantalla - ancho_box) // 2
            box_y = (conf.alto_pantalla - alto_box) // 2

            pg.draw.rect(
                overlay,
                (30, 41, 59, 245),
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

            fuente_box = pg.font.SysFont("Arial", 28, bold=True)
            render_msg = fuente_box.render(
                "¿Seguro que deseas salir?", True, (241, 245, 249)
            )
            rect_msg = render_msg.get_rect(
                center=(conf.ancho_pantalla // 2, box_y + 65)
            )
            overlay.blit(render_msg, rect_msg)

            if btn_si and btn_no:
                BotonRenderer.dibujar(overlay, btn_si)
                BotonRenderer.dibujar(overlay, btn_no)

            canva.blit(overlay, (0, 0))

        pg.display.flip()
        reloj.tick(60)


def main():
    try:
        main_menu()
    except SystemExit:
        pass
    except Exception as e:
        print(f"Error en el menú principal: {e}")
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    main()
