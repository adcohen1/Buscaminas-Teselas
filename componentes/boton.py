import pygame as pg


class Boton:
    """Clase que representa el modelo y estado de un botón (Lógica de negocios)."""

    def __init__(
        self,
        w,
        h,
        x,
        y,
        texto="",
        color_base=(71, 85, 105),
        color_hover=(100, 116, 139),
        color_texto=(255, 255, 255),
        tam_fuente=24,
    ):
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.texto = texto
        self.tam_fuente = tam_fuente
        # Usamos Rect de Pygame para el manejo lógico de colisiones y posición
        self.rect = pg.Rect(x, y, w, h)
        self.hovered = False
        self.focused = False

    @property
    def color(self):
        """Mantiene compatibilidad con lecturas directas del color base (ej. en main.py)."""
        return self.color_base

    def check_hover(self, pos):
        """Determina si la posición dada (cursor) colisiona con el botón."""
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered


class BotonRenderer:
    """Clase encargada de dibujar los botones en una superficie de Pygame."""

    _fuentes = {}

    @classmethod
    def obtener_fuente(cls, size=24):
        """Carga perezosa y caché de la fuente de los botones."""
        if size not in cls._fuentes:
            if not pg.font.get_init():
                pg.font.init()
            cls._fuentes[size] = pg.font.SysFont("Arial", size, bold=True)
        return cls._fuentes[size]

    @staticmethod
    def dibujar(superficie, boton: Boton):
        """Dibuja el botón y su texto directamente sobre la superficie dada."""
        # Decidir color basado en hover o focus
        color_actual = boton.color_base
        if boton.hovered or boton.focused:
            color_actual = boton.color_hover

        # Dibujar rectángulo redondeado
        pg.draw.rect(superficie, color_actual, boton.rect, border_radius=10)

        # Dibujar contorno si está enfocado o bajo el mouse (hovered)
        if boton.focused:
            pg.draw.rect(
                superficie, (255, 255, 255), boton.rect, width=3, border_radius=10
            )
        elif boton.hovered:
            pg.draw.rect(
                superficie, (241, 245, 249), boton.rect, width=1, border_radius=10
            )

        # Renderizar y centrar texto
        if boton.texto:
            fuente = BotonRenderer.obtener_fuente(boton.tam_fuente)
            text_surf = fuente.render(boton.texto, True, boton.color_texto)
            text_rect = text_surf.get_rect(center=boton.rect.center)
            superficie.blit(text_surf, text_rect)
