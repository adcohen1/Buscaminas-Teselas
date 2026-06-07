from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Tuple
from warnings import deprecated


class Admin(ABC):
    @abstractmethod
    def agregar(self, observer): ...

    @abstractmethod
    def quitar(self, observer): ...

    @abstractmethod
    def notificar(self): ...


class AdminConf(Admin):
    _instancia = None
    _observadores = []

    # celdas
    filas: int
    columnas: int
    bombas: int
    tamaño_celda: int
    separacion_celdas: int

    # pantalla
    ancho_pantalla: int
    alto_pantalla: int

    # tablero
    margen_tablero: int
    padding_tablero: int

    # colores
    color_fondo: Tuple[int, int, int]
    color_celda: Tuple[int, int, int]
    color_bomba: Tuple[int, int, int]
    color_tablero: Tuple[int, int, int]

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        self.leerConf()

    _sin_notificar = {"ancho_pantalla", "alto_pantalla", "tamaño_celda"}

    def __setattr__(self, atributo, valor):
        if getattr(self, atributo, None) != valor:
            super().__setattr__(atributo, valor)
            if atributo not in self._sin_notificar:
                self.cambiarConf()

    def agregar(self, observador):
        self._observadores.append(observador)

    def quitar(self, observador):
        self._observadores.remove(observador)

    def notificar(self):
        for observador in self._observadores:
            observador.actualizar()

    @deprecated("Use leerConf instead")
    def obtenerConf(self, conf: str):
        with open("conf.txt", "r", encoding="utf-8") as a:
            for linea in a:
                key = linea.split("=")[0]
                val = linea.split("=")[1]
                if key == conf:
                    return val
            return None

    @deprecated("Use cambiarConf instead")
    def establecerConf(self, conf, valor, notify=True):
        with open("conf.txt", "r") as a:
            cont = a.read().split("\n")
            new_cont = ""
            for linea in cont:
                if linea.split("=")[0] == conf:
                    new_cont += f"{conf}={valor}\n"
                    continue
                new_cont += linea + "\n"

        with open("conf.txt", "w") as a:
            a.write(new_cont)

        if notify:
            self.notificar()

    def leerConf(self):
        with open("conf.json", "r") as arch:
            dict = json.load(arch)
            self.__dict__.update(dict)

    def cambiarConf(self, notify=True):
        with open("conf.json", "w") as arch:
            json.dump(self.__dict__, arch, indent=4)

        if notify:
            self.notificar()
