# 💣 Buscaminas Dinámico (Pygame)

¡Bienvenido al **Buscaminas Dinámico**! Una implementación interactiva del clásico juego del Buscaminas desarrollada en **Python** utilizando **Pygame**. 

Este proyecto no solo ofrece la jugabilidad clásica, sino que introduce un panel dinámico que te permite cambiar el tamaño del tablero (filas y columnas) en tiempo real mediante hilos secundarios y actualización reactiva de la interfaz.

---

## ✨ Características Principales

- **🎮 Redimensionamiento en Tiempo Real:** Modifica el número de filas y columnas directamente desde la pantalla de juego con botones interactivos. El tablero se adaptará dinámicamente.
- **🔄 Persistencia de Configuración:** Guarda de forma automática el estado de la configuración en un archivo JSON (`conf.json`) para que se mantengan tus preferencias en la siguiente partida.
- **⚡ Arquitectura Reactiva (Observer & Singleton):** Uso de patrones de diseño avanzados para desacoplar el estado de la configuración de la representación visual del juego.
- **🚀 Instalación Rápida:** Incluye scripts autodetectables para facilitar la instalación con `uv` o el gestor de paquetes clásico `pip`.

---

## 🛠️ Arquitectura y Patrones de Diseño

El código está estructurado bajo buenos principios de diseño de software:

*   **Patrón Singleton (`AdminConf` en `adminconf.py`):** Garantiza que exista una única instancia global que controle la configuración del juego, impidiendo inconsistencias al mutar el tamaño o colores del tablero.
*   **Patrón Observer (`Admin` y `Tablero`):** El tablero actúa como observador de la configuración del juego. Cuando cambias las filas o columnas en la interfaz:
    1. Se actualizan las propiedades del administrador.
    2. El administrador notifica a los observadores suscritos.
    3. El tablero recalcula y redibuja las celdas automáticamente.
*   **Multithreading:** Las llamadas para cambiar el tamaño del tablero se ejecutan en hilos separados (`threading.Thread`) para evitar bloqueos del bucle principal y mantener los FPS estables.

---

## 🚀 Instalación y Uso

### Requisitos previos
*   **Python 3.13 o superior** (debido al uso de características modernas como `warnings.deprecated`).

### 1. Instalar dependencias
Simplemente haz doble clic en el archivo ejecutable **[`instalar.bat`](file:///c:/Users/Alfonso/Documents/Buscaminas/instalar.bat)** en la raíz del proyecto. 

> [!TIP]
> Si tienes instalado el gestor de paquetes moderno **`uv`**, el script lo detectará automáticamente y creará el entorno ultrarrápido (`uv sync`). Si no lo tienes, el instalador utilizará la forma clásica creando un entorno virtual `.venv` tradicional con `pip`.

### 2. Ejecutar el Juego
Una vez instaladas las dependencias, activa tu entorno virtual y ejecuta el archivo principal:

**Usando el entorno de `uv` (Recomendado):**
```bash
uv run main.py
```

**Usando el entorno tradicional:**
```bash
.venv\Scripts\python.exe main.py
```

---

## 🕹️ Controles
*   **Clic Izquierdo / Derecho** en el tablero: Revelar celda / Colocar bandera (Buscaminas tradicional).
*   **Botones Inferiores:** Incrementa o decrementa la cantidad de filas y columnas del tablero.
*   **Tecla `ESC` / Cerrar ventana:** Salir del juego.

---

## 📂 Estructura del Proyecto

*   **[`main.py`](file:///c:/Users/Alfonso/Documents/Buscaminas/main.py):** Punto de entrada del juego, maneja el ciclo principal de Pygame e inputs.
*   **[`adminconf.py`](file:///c:/Users/Alfonso/Documents/Buscaminas/adminconf.py):** Administrador de la configuración y lógica de patrones de diseño (Singleton y Observer).
*   **[`tablero.py`](file:///c:/Users/Alfonso/Documents/Buscaminas/tablero.py):** Gestiona la matriz de celdas y su redibujo interactivo.
*   **[`celda.py`](file:///c:/Users/Alfonso/Documents/Buscaminas/celda.py):** Representación individual de cada celda del tablero.
*   **[`boton.py`](file:///c:/Users/Alfonso/Documents/Buscaminas/boton.py):** Componente interactivo para alterar las dimensiones del juego.
*   **[`constantes.py`](file:///c:/Users/Alfonso/Documents/Buscaminas/constantes.py):** Configuración de paleta de colores y variables globales del motor físico.