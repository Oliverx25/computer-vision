"""
==> CONFIGURACIÓN DEL PROGRAMA
% Contiene todas las constantes y parámetros configurables del programa Círculo y Línea
% Centraliza la configuración para facilitar modificaciones
% Autor: Olvera Olvera Oliver Jesus
% Unidad de Aprendizaje: Visión por Computadora
"""

class Config:
    """
    ==> CLASE DE CONFIGURACIÓN CENTRALIZADA
    % Maneja todos los parámetros configurables del programa
    % Incluye dimensiones, colores y rangos de generación
    """

    # ==> DIMENSIONES DE LA VENTANA
    # -> Dimensiones de la ventana principal en píxeles
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 650

    # ==> DIMENSIONES DEL CANVAS
    # -> Dimensiones del canvas en el que se dibujan las formas
    CANVAS_WIDTH = 750
    CANVAS_HEIGHT = 500

    # ==> CONFIGURACIÓN DE PÍXELES
    # -> Tamaño de cada "píxel" simulado dentro del canvas
    PIXEL_SIZE = 1

    # ==> DIMENSIONES DE LA GRILLA LÓGICA
    # -> Dimensiones de la grilla lógica (basada en píxeles simulados)
    GRID_WIDTH = CANVAS_WIDTH // PIXEL_SIZE   # -> 750 píxeles
    GRID_HEIGHT = CANVAS_HEIGHT // PIXEL_SIZE  # -> 500 píxeles

    # ==> RANGOS DE GENERACIÓN
    # -> Rango de líneas a generar aleatoriamente
    MIN_LINES = 1
    MAX_LINES = 5

    # -> Rango de círculos a generar aleatoriamente
    MIN_CIRCLES = 1
    MAX_CIRCLES = 5

    # ==> CONFIGURACIÓN DE RADIOS
    # -> Rango de radios para círculos generados
    MIN_RADIUS = 3
    MAX_RADIUS = 15

    # ==> PALETA DE COLORES
    # -> Colores para líneas (gama de rojos y naranjas)
    LINE_COLORS = [
        "#B22222",  # -> Rojo ladrillo
        "#DC143C",  # -> Rojo carmesí
        "#FF0000",  # -> Rojo puro
        "#FF4500",  # -> Naranja rojizo
        "#FF8C00",  # -> Naranja oscuro
        "#FFD700",  # -> Amarillo dorado
    ]

    # -> Colores para círculos (gama de verdes)
    CIRCLE_COLORS = [
        "#008000",  # -> Verde puro
        "#006400",  # -> Verde oscuro
        "#228B22",  # -> Verde bosque
        "#32CD32",  # -> Verde lima
        "#90EE90",  # -> Verde claro
        "#98FB98",  # -> Verde pálido
    ]
