import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import math
import os

class GeneradorImagenesSinteticas:
    def __init__(self):
        # ==> CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
        self.ventana = tk.Tk()
        self.ventana.title("Generador de Imágenes Sintéticas - Texturas")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg='#2c3e50')

        # $ Variables de estado de la aplicación
        self.imagen_original = None
        self.datos_imagen_original = None
        self.dimensiones_imagen = None
        self.parches_extraidos = []
        self.modelo_transicion = {}
        self.imagen_generada = None
        self.numero_iteraciones = 20  # $ Número de iteraciones por defecto

        # ==> CONFIGURACIÓN DE LA INTERFAZ
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # # Configuración del marco principal
        marco_principal = tk.Frame(self.ventana, bg='#2c3e50')
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # -> Título principal
        titulo = tk.Label(marco_principal,
                         text="Generador de Imágenes Sintéticas",
                         font=('Arial', 18, 'bold'),
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=(0, 20))

        # -> Marco de controles
        marco_controles = tk.Frame(marco_principal, bg='#34495e', relief=tk.RAISED, bd=2)
        marco_controles.pack(fill=tk.X, pady=(0, 20))

        # # Botones de control
        self.boton_cargar = tk.Button(marco_controles,
                                     text="Cargar Imagen BMP",
                                     command=self.cargar_imagen_bmp,
                                     bg='#3498db', fg='white',
                                     font=('Arial', 12, 'bold'),
                                     relief=tk.RAISED, bd=3)
        self.boton_cargar.pack(side=tk.LEFT, padx=10, pady=10)

        # # Control de iteraciones
        marco_iteraciones = tk.Frame(marco_controles, bg='#34495e')
        marco_iteraciones.pack(side=tk.LEFT, padx=10, pady=10)

        etiqueta_iteraciones = tk.Label(marco_iteraciones,
                                      text="Iteraciones:",
                                      font=('Arial', 10, 'bold'),
                                      bg='#34495e', fg='white')
        etiqueta_iteraciones.pack(side=tk.LEFT, padx=(0, 5))

        self.entrada_iteraciones = tk.Entry(marco_iteraciones,
                                          width=5,
                                          font=('Arial', 10),
                                          bg='white', fg='black')
        self.entrada_iteraciones.insert(0, "20")
        self.entrada_iteraciones.pack(side=tk.LEFT, padx=(0, 10))

        self.boton_generar = tk.Button(marco_controles,
                                      text="Generar Imagen Sintética",
                                      command=self.generar_imagen_sintetica,
                                      bg='#e74c3c', fg='white',
                                      font=('Arial', 12, 'bold'),
                                      relief=tk.RAISED, bd=3,
                                      state=tk.DISABLED)
        self.boton_generar.pack(side=tk.LEFT, padx=10, pady=10)

        # -> Marco de visualización
        marco_visualizacion = tk.Frame(marco_principal, bg='#34495e')
        marco_visualizacion.pack(fill=tk.BOTH, expand=True)

        # # Marco para imagen original
        marco_original = tk.Frame(marco_visualizacion, bg='#34495e')
        marco_original.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        etiqueta_original = tk.Label(marco_original,
                                   text="Imagen Original",
                                   font=('Arial', 14, 'bold'),
                                   bg='#34495e', fg='white')
        etiqueta_original.pack(pady=(0, 10))

        self.canvas_original = tk.Canvas(marco_original, bg='#2c3e50',
                                       relief=tk.SUNKEN, bd=2)
        self.canvas_original.pack(fill=tk.BOTH, expand=True)

        # # Marco para imagen generada
        marco_generada = tk.Frame(marco_visualizacion, bg='#34495e')
        marco_generada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        etiqueta_generada = tk.Label(marco_generada,
                                   text="Imagen Generada",
                                   font=('Arial', 14, 'bold'),
                                   bg='#34495e', fg='white')
        etiqueta_generada.pack(pady=(0, 10))

        self.canvas_generada = tk.Canvas(marco_generada, bg='#2c3e50',
                                       relief=tk.SUNKEN, bd=2)
        self.canvas_generada.pack(fill=tk.BOTH, expand=True)

        # -> Barra de estado
        self.barra_estado = tk.Label(marco_principal,
                                   text="Listo para cargar imagen BMP",
                                   font=('Arial', 10),
                                   bg='#2c3e50', fg='#ecf0f1')
        self.barra_estado.pack(pady=(10, 0))

    # ==> SECCIÓN 1: CARGA Y VALIDACIÓN DE IMAGEN BMP
    def cargar_imagen_bmp(self):
        # # Selección de archivo
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar imagen BMP",
            filetypes=[("Archivos BMP", "*.bmp"), ("Todos los archivos", "*.*")]
        )

        if not ruta_archivo:
            return

        try:
            # # Lectura del encabezado BMP
            with open(ruta_archivo, 'rb') as archivo:
                firma = archivo.read(2)
                if firma != b'BM':
                    raise ValueError("No es un archivo BMP válido")

                # $ Lectura de información del encabezado
                tamano_archivo = int.from_bytes(archivo.read(4), byteorder='little')
                reservado = int.from_bytes(archivo.read(4), byteorder='little')
                offset_datos = int.from_bytes(archivo.read(4), byteorder='little')

                # $ Información del encabezado DIB
                tamano_dib = int.from_bytes(archivo.read(4), byteorder='little')
                ancho = int.from_bytes(archivo.read(4), byteorder='little')
                alto = int.from_bytes(archivo.read(4), byteorder='little')
                planos = int.from_bytes(archivo.read(2), byteorder='little')
                bits_por_pixel = int.from_bytes(archivo.read(2), byteorder='little')

                if bits_por_pixel != 24:
                    raise ValueError("Solo se admiten imágenes BMP de 24 bits")

                if ancho > 10000 or alto > 10000:
                    raise ValueError("Dimensiones demasiado grandes (máximo 10000x10000)")

                # $ Cálculo de padding
                bytes_por_fila = ancho * 3
                padding_por_fila = (4 - (bytes_por_fila % 4)) % 4

                # # Lectura de datos de píxeles
                archivo.seek(offset_datos)
                datos_pixeles = []

                # $ BMP se almacena de abajo hacia arriba, leemos secuencialmente
                for fila in range(alto):  # $ Leer secuencialmente todas las filas
                    fila_datos = []
                    for columna in range(ancho):
                        # $ Lectura en orden BGR (BMP almacena BGR)
                        azul = int.from_bytes(archivo.read(1), byteorder='little')
                        verde = int.from_bytes(archivo.read(1), byteorder='little')
                        rojo = int.from_bytes(archivo.read(1), byteorder='little')
                        fila_datos.append([rojo, verde, azul])
                    # $ Saltar padding
                    archivo.read(padding_por_fila)
                    datos_pixeles.append(fila_datos)

                # * Almacenamiento de datos
                # ! INVERTIR LA LISTA porque BMP almacena de abajo hacia arriba
                self.datos_imagen_original = datos_pixeles[::-1]
                self.dimensiones_imagen = (ancho, alto)

                # # Actualizar interfaz
                self.mostrar_imagen_original()
                self.boton_generar.config(state=tk.NORMAL)
                self.barra_estado.config(text=f"Imagen cargada: {ancho}x{alto} píxeles")

        except Exception as error:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(error)}")
            self.barra_estado.config(text="Error al cargar imagen")

    def mostrar_imagen_original(self):
        # # Mostrar imagen original usando análisis por filas
        if self.datos_imagen_original:
            # -> Limpiar canvas
            self.canvas_original.delete("all")

            # -> Obtener dimensiones
            alto = len(self.datos_imagen_original)
            ancho = len(self.datos_imagen_original[0])
            canvas_width = 350
            canvas_height = 400

            # ==> CÁLCULO DE ESCALA
            # -> Calcular escala para ajustar a la ventana
            escala_x = canvas_width / ancho
            escala_y = canvas_height / alto
            escala = min(escala_x, escala_y)

            # -> Calcular nuevas dimensiones
            nuevo_ancho = int(ancho * escala)
            nuevo_alto = int(alto * escala)

            # -> Calcular posición centrada
            x_offset = (canvas_width - nuevo_ancho) // 2
            y_offset = (canvas_height - nuevo_alto) // 2

            # ==> DIBUJO DE PÍXELES POR FILAS
            # -> Dibujar píxeles escalados
            for y in range(alto):
                for x in range(ancho):
                    r, g, b = self.datos_imagen_original[y][x]
                    color = f"#{r:02x}{g:02x}{b:02x}"

                    # -> Coordenadas escaladas
                    x1 = x_offset + int(x * escala)
                    y1 = y_offset + int(y * escala)
                    x2 = x_offset + int((x + 1) * escala)
                    y2 = y_offset + int((y + 1) * escala)

                    # -> Solo dibujar si el píxel es visible
                    if x1 < x2 and y1 < y2:
                        self.canvas_original.create_rectangle(x1, y1, x2, y2,
                                                           fill=color, outline="", width=0)

    # ==> SECCIÓN 2: EXTRACCIÓN DE PARCHES (MATRIZ EVOLUTIVA - FASE 1)
    def extraer_parches_aleatorios(self):
        # # Configuración del generador Mersenne Twister
        random.seed(42)  # $ Semilla fija para reproducibilidad

        ancho, alto = self.dimensiones_imagen
        parches = []

        # $ Calcular total de parches posibles
        total_parches = (ancho - 4) * (alto - 4)  # $ Parches 5x5
        parches_a_extraer = max(1, total_parches // 50)  # ! 2% de los parches para optimización

        # # Extracción aleatoria de parches
        parches_extraidos = 0
        intentos_maximos = total_parches * 2

        while parches_extraidos < parches_a_extraer and intentos_maximos > 0:
            # $ Selección aleatoria de coordenadas centrales
            x_centro = random.randint(2, ancho - 3)
            y_centro = random.randint(2, alto - 3)

            # # Extraer parche 5x5
            parche = []
            for dy in range(-2, 3):
                fila_parche = []
                for dx in range(-2, 3):
                    x = x_centro + dx
                    y = y_centro + dy
                    r, g, b = self.datos_imagen_original[y][x]
                    # $ Cuantización de colores para reducir complejidad con valores multiplos enteros de 32
                    r_cuantizado = (r // 32) * 32
                    g_cuantizado = (g // 32) * 32
                    b_cuantizado = (b // 32) * 32
                    fila_parche.append([r_cuantizado, g_cuantizado, b_cuantizado])
                parche.append(fila_parche)

            # $ Verificar que el parche no esté duplicado
            parche_tupla = tuple(tuple(fila) for fila in parche)
            if parche_tupla not in [p['datos'] for p in parches]:
                parches.append({
                    'datos': parche_tupla,
                    'centro_x': x_centro,
                    'centro_y': y_centro
                })
                parches_extraidos += 1

            intentos_maximos -= 1

        self.parches_extraidos = parches
        return parches

    # ==> SECCIÓN 3: CÁLCULO DE PROBABILIDADES DE TRANSICIÓN (RESPALDO)
    def calcular_modelo_transicion(self):
        # # Análisis de transiciones de color entre píxeles vecinos
        ancho, alto = self.dimensiones_imagen
        transiciones = {}

        # $ Direcciones: arriba, abajo, izquierda, derecha
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for y in range(1, alto - 1):
            for x in range(1, ancho - 1):
                color_actual = tuple(self.datos_imagen_original[y][x])

                for dx, dy in direcciones:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < ancho and 0 <= ny < alto:
                        color_vecino = tuple(self.datos_imagen_original[ny][nx])

                        # $ Crear clave de transición
                        clave = (color_actual, color_vecino)
                        transiciones[clave] = transiciones.get(clave, 0) + 1

        # $ Normalización y distribución acumulada
        total_transiciones = sum(transiciones.values())
        if total_transiciones > 0:
            probabilidades = {}
            acumulado = 0.0

            for transicion, cuenta in transiciones.items():
                probabilidad = cuenta / total_transiciones
                acumulado += probabilidad
                probabilidades[transicion] = acumulado

            self.modelo_transicion = probabilidades
        else:
            self.modelo_transicion = {}

    # ==> SECCIÓN 4: SÍNTESIS DE IMAGEN (MATRIZ EVOLUTIVA - FASE 2)
    def generar_imagen_sintetica(self):
        if not self.datos_imagen_original:
            messagebox.showwarning("Advertencia", "Primero debe cargar una imagen BMP")
            return

        # # Obtener número de iteraciones del usuario
        try:
            self.numero_iteraciones = int(self.entrada_iteraciones.get())
            if self.numero_iteraciones < 1 or self.numero_iteraciones > 100:
                messagebox.showwarning("Advertencia", "El número de iteraciones debe estar entre 1 y 100")
                return
        except ValueError:
            messagebox.showwarning("Advertencia", "El número de iteraciones debe ser un número entero")
            return

        # # Fase 1: Extracción de parches
        self.barra_estado.config(text="Extrayendo parches de la imagen original...")
        self.ventana.update()
        parches = self.extraer_parches_aleatorios()

        # # Fase 2: Cálculo del modelo de transición (respaldo)
        self.barra_estado.config(text="Calculando modelo de transición...")
        self.ventana.update()
        self.calcular_modelo_transicion()

        # # Fase 3: Inicialización de la imagen generada
        self.barra_estado.config(text="Inicializando imagen con ruido gaussiano...")
        self.ventana.update()
        imagen_generada = self.inicializar_imagen_con_ruido()

        # # Fase 4: Iteraciones de refinamiento (MATRIZ EVOLUTIVA)
        self.barra_estado.config(text=f"Aplicando refinamiento evolutivo ({self.numero_iteraciones} iteraciones)...")
        self.ventana.update()
        imagen_final = self.aplicar_refinamiento_evolutivo(imagen_generada, parches)

        # # Fase 5: Mostrar imagen generada
        self.imagen_generada = imagen_final
        self.mostrar_imagen_generada()

        self.barra_estado.config(text=f"Imagen sintética generada exitosamente ({self.numero_iteraciones} iteraciones)")

    def inicializar_imagen_con_ruido(self):
        # # Crear imagen base copiando la original
        ancho, alto = self.dimensiones_imagen
        imagen_ruido = []

        for y in range(alto):
            fila_ruido = []
            for x in range(ancho):
                # $ Obtener color original
                r_orig, g_orig, b_orig = self.datos_imagen_original[y][x]

                # $ Aplicar ruido gaussiano (media=0, σ=5)
                ruido_r = int(random.gauss(0, 5))
                ruido_g = int(random.gauss(0, 5))
                ruido_b = int(random.gauss(0, 5))

                # $ Calcular nuevo color con ruido
                r_nuevo = max(0, min(255, r_orig + ruido_r))
                g_nuevo = max(0, min(255, g_orig + ruido_g))
                b_nuevo = max(0, min(255, b_orig + ruido_b))

                fila_ruido.append([r_nuevo, g_nuevo, b_nuevo])
            imagen_ruido.append(fila_ruido)

        return imagen_ruido

    # ==> SECCIÓN 5: REFINAMIENTO EVOLUTIVO (MATRIZ EVOLUTIVA - FASE 3)
    def aplicar_refinamiento_evolutivo(self, imagen_inicial, parches):
        # # Configuración del proceso evolutivo
        ancho, alto = self.dimensiones_imagen
        imagen_actual = [fila[:] for fila in imagen_inicial]  # $ Copia profunda

        # # Iteraciones de refinamiento
        for iteracion in range(self.numero_iteraciones):
            self.barra_estado.config(text=f"Refinamiento evolutivo: iteración {iteracion + 1}/{self.numero_iteraciones}")
            self.ventana.update()

            # $ Procesar cada píxel (excepto bordes)
            for y in range(2, alto - 2):
                for x in range(2, ancho - 2):
                    # # Extraer parche 5x5 centrado en el píxel actual
                    parche_actual = self.extraer_parche_5x5(imagen_actual, x, y)

                    # # Encontrar el parche más similar (OPTIMIZADO: solo 100 parches aleatorios)
                    mejor_parche = self.encontrar_parche_mas_similar(parche_actual, parches, muestra_aleatoria=100)

                    if mejor_parche:
                        # $ Obtener color del centro del mejor parche
                        color_centro = self.obtener_color_centro_parche(mejor_parche)
                        imagen_actual[y][x] = color_centro

            # $ Actualizar visualización después de cada iteración completada
            self.imagen_generada = imagen_actual
            self.mostrar_imagen_generada()
            self.ventana.update()

        return imagen_actual

    def extraer_parche_5x5(self, imagen, x_centro, y_centro):
        # # Extraer parche 5x5 centrado en (x_centro, y_centro)
        parche = []
        for dy in range(-2, 3):
            fila_parche = []
            for dx in range(-2, 3):
                x = x_centro + dx
                y = y_centro + dy
                r, g, b = imagen[y][x]
                # $ Cuantización para comparación
                r_cuantizado = (r // 32) * 32
                g_cuantizado = (g // 32) * 32
                b_cuantizado = (b // 32) * 32
                fila_parche.append([r_cuantizado, g_cuantizado, b_cuantizado])
            parche.append(fila_parche)
        return parche

    def encontrar_parche_mas_similar(self, parche_actual, parches_originales, muestra_aleatoria=100):
        # # Calcular distancia euclidiana al cuadrado
        mejor_parche = None
        menor_distancia = float('inf')

        # OPTIMIZACIÓN: comparar solo con una muestra aleatoria de parches
        if len(parches_originales) > muestra_aleatoria:
            muestra = random.sample(parches_originales, muestra_aleatoria)
        else:
            muestra = parches_originales

        for parche_original in muestra:
            distancia = self.calcular_distancia_parches(parche_actual, parche_original['datos'])
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_parche = parche_original

        return mejor_parche

    def calcular_distancia_parches(self, parche1, parche2):
        # # Distancia euclidiana al cuadrado entre parches
        distancia_total = 0
        for y in range(5):
            for x in range(5):
                r1, g1, b1 = parche1[y][x]
                r2, g2, b2 = parche2[y][x]

                # $ Distancia euclidiana al cuadrado
                dr = (r1 - r2) ** 2
                dg = (g1 - g2) ** 2
                db = (b1 - b2) ** 2

                distancia_total += dr + dg + db

        return distancia_total

    def obtener_color_centro_parche(self, parche_original):
        # # Obtener color del centro del parche original
        centro_x = parche_original['centro_x']
        centro_y = parche_original['centro_y']
        return self.datos_imagen_original[centro_y][centro_x]

    def mostrar_imagen_generada(self):
        # # Mostrar imagen generada usando análisis por filas
        if self.imagen_generada:
            # -> Limpiar canvas
            self.canvas_generada.delete("all")

            # -> Obtener dimensiones
            alto = len(self.imagen_generada)
            ancho = len(self.imagen_generada[0])
            canvas_width = 350
            canvas_height = 400

            # ==> CÁLCULO DE ESCALA
            # -> Calcular escala para ajustar a la ventana
            escala_x = canvas_width / ancho
            escala_y = canvas_height / alto
            escala = min(escala_x, escala_y)

            # -> Calcular nuevas dimensiones
            nuevo_ancho = int(ancho * escala)
            nuevo_alto = int(alto * escala)

            # -> Calcular posición centrada
            x_offset = (canvas_width - nuevo_ancho) // 2
            y_offset = (canvas_height - nuevo_alto) // 2

            # ==> DIBUJO DE PÍXELES POR FILAS
            # -> Dibujar píxeles escalados
            for y in range(alto):
                for x in range(ancho):
                    r, g, b = self.imagen_generada[y][x]
                    color = f"#{r:02x}{g:02x}{b:02x}"

                    # -> Coordenadas escaladas
                    x1 = x_offset + int(x * escala)
                    y1 = y_offset + int(y * escala)
                    x2 = x_offset + int((x + 1) * escala)
                    y2 = y_offset + int((y + 1) * escala)

                    # -> Solo dibujar si el píxel es visible
                    if x1 < x2 and y1 < y2:
                        self.canvas_generada.create_rectangle(x1, y1, x2, y2,
                                                           fill=color, outline="", width=0)

    def ejecutar(self):
        # # Iniciar la aplicación
        self.ventana.mainloop()

# ==> PUNTO DE ENTRADA PRINCIPAL
if __name__ == "__main__":
    # # Crear y ejecutar la aplicación
    app = GeneradorImagenesSinteticas()
    app.ejecutar()
