from __future__ import annotations
from abc import ABC, abstractmethod


class Observador(ABC):
    @abstractmethod
    def actualizar(self): ...
