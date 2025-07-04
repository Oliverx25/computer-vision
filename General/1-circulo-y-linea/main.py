#!/usr/bin/env python3
"""
==> PROGRAMA CÍRCULO Y LÍNEA
% Genera y muestra formas geométricas básicas (líneas y círculos) con algoritmos clásicos
% Autor: Olvera Olvera Oliver Jesus
% Unidad de Aprendizaje: Visión por Computadora
"""

import tkinter as tk
from tkinter import ttk
import random

# ==> IMPORTACIONES
from algorithms import BresenhamLine, MidpointCircle
from config import Config

class CirculoYLinea:
    """
    ==> CLASE PRINCIPAL - CÍRCULO Y LÍNEA
    % Clase principal que maneja la interfaz gráfica y la generación de figuras
    """

    def __init__(self):
        # # Inicialización de componentes principales
        self.config = Config()
        self.setup_gui()
        self.canvas_data = {}  # Almacenamiento de píxeles a dibujar

    def setup_gui(self):
        """
        # Configuración de la interfaz gráfica principal
        % Configura todos los elementos visuales de la aplicación
        """
        # ==> CONFIGURACIÓN DE VENTANA PRINCIPAL
        self.root = tk.Tk()
        self.root.title("Círculo y Línea - Algoritmos Gráficos")
        self.root.geometry(f"{self.config.WINDOW_WIDTH}x{self.config.WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        # ==> FRAME PRINCIPAL
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # -> Título
        title_label = ttk.Label(main_frame, text="Generador de Círculos y Líneas",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # ==> CANVAS DE DIBUJO
        # -> Area de dibujo de figuras
        self.canvas = tk.Canvas(main_frame,
                               width=self.config.CANVAS_WIDTH,
                               height=self.config.CANVAS_HEIGHT,
                               bg="white",
                               border=1,
                               relief="solid")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # ==> BOTONES DE CONTROL
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        # -> Botón de generación
        self.generate_btn = ttk.Button(button_frame, text="Generar Nuevas Figuras",
                                      command=self.generate_shapes)
        self.generate_btn.grid(row=0, column=0, padx=5)

        # -> Botón de limpieza
        self.clear_btn = ttk.Button(button_frame, text="Limpiar Canvas",
                                   command=self.clear_canvas)
        self.clear_btn.grid(row=0, column=1, padx=5)

        # ==> INFORMACIÓN DE ESTADO
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.info_label = ttk.Label(info_frame, text="Presiona 'Generar Nuevas Figuras' para comenzar")
        self.info_label.grid(row=0, column=0)

        # ==> CONFIGURACIÓN DE GRID
        # -> Configuración para redimensionamiento responsivo
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def clear_canvas(self):
        """
        # Limpieza del canvas
        % Limpia el canvas y reinicia los datos almacenados
        """
        self.canvas.delete("all")
        self.canvas_data.clear()
        self.info_label.config(text="Canvas limpiado. Presiona 'Generar Nuevas Figuras' para dibujar.")

    def draw_pixel(self, x, y, color="black"):
        """
        # Dibujo de pixeles
        % Dibuja un 'pixel' en el canvas en las coordenadas especificadas
        $ x, y: Coordenadas en la grilla logica
        $ color: Color del pixel (por defecto negro)
        """
        if 0 <= x < self.config.GRID_WIDTH and 0 <= y < self.config.GRID_HEIGHT:
            # -> Calculo de posicion real en el canvas
            real_x = x * self.config.PIXEL_SIZE
            real_y = y * self.config.PIXEL_SIZE

            # -> Creacion del rectangulo que representa el pixel
            pixel_id = self.canvas.create_rectangle(
                real_x, real_y,
                real_x + self.config.PIXEL_SIZE, real_y + self.config.PIXEL_SIZE,
                fill=color, outline=color
            )

            # -> Almacenamiento en datos del canvas
            self.canvas_data[(x, y)] = {"id": pixel_id, "color": color}

    def generate_shapes(self):
        """
        # Generación de figuras
        % Genera figuras aleatorias (líneas y círculos) en el canvas
        """
        self.clear_canvas()

        # ==> GENERACIÓN DE LÍNEAS
        num_lines = random.randint(self.config.MIN_LINES, self.config.MAX_LINES)
        for _ in range(num_lines):
            self.generate_random_line()

        # ==> GENERACIÓN DE CÍRCULOS
        num_circles = random.randint(self.config.MIN_CIRCLES, self.config.MAX_CIRCLES)
        for _ in range(num_circles):
            self.generate_random_circle()

        # -> Actualización de información de estado
        self.info_label.config(text=f"Generadas: {num_lines} líneas y {num_circles} círculos")

    def generate_random_line(self):
        """
        # Generación de línea aleatoria
        % Genera una línea aleatoria usando el algoritmo de Bresenham
        """
        # -> Generación de puntos aleatorios
        x1 = random.randint(0, self.config.GRID_WIDTH - 1)
        y1 = random.randint(0, self.config.GRID_HEIGHT - 1)
        x2 = random.randint(0, self.config.GRID_WIDTH - 1)
        y2 = random.randint(0, self.config.GRID_HEIGHT - 1)

        # -> Selección de color aleatorio
        color = random.choice(self.config.LINE_COLORS)

        # -> Aplicación del algoritmo de Bresenham
        line_algorithm = BresenhamLine()
        points = line_algorithm.get_puntos_linea(x1, y1, x2, y2)

        # -> Dibujo de todos los puntos de la línea
        for x, y in points:
            self.draw_pixel(x, y, color)

    def generate_random_circle(self):
        """
        # Generación de círculo aleatorio
        % Genera un círculo aleatorio usando el algoritmo de Midpoint Circle
        """
        # -> Cálculo de radio máximo y selección aleatoria
        max_radius = min(self.config.GRID_WIDTH, self.config.GRID_HEIGHT) // 4
        radius = random.randint(self.config.MIN_RADIUS, max_radius)

        # -> Posicionamiento seguro del círculo dentro del canvas
        cx = random.randint(radius, self.config.GRID_WIDTH - radius - 1)
        cy = random.randint(radius, self.config.GRID_HEIGHT - radius - 1)

        # -> Selección de color aleatorio
        color = random.choice(self.config.CIRCLE_COLORS)

        # -> Aplicación del algoritmo de Midpoint Circle
        circle_algorithm = MidpointCircle()
        points = circle_algorithm.get_puntos_circulo(cx, cy, radius)

        # -> Dibujo de todos los puntos del círculo
        for x, y in points:
            self.draw_pixel(x, y, color)

    def run(self):
        """
        # Ejecución de la aplicación
        % Inicia el bucle principal de la interfaz gráfica
        """
        self.root.mainloop()

def main():
    """
    ==> FUNCIÓN PRINCIPAL
    % Punto de entrada principal del programa
    """
    app = CirculoYLinea()
    app.run()

if __name__ == "__main__":
    main()
