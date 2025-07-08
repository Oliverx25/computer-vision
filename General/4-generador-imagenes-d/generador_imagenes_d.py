import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import math
import os

class GeneradorImagenesSinteticas:
    def __init__(self):
        # ==> CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
        self.ventana = tk.Tk()
        self.ventana.title("Generador de Imágenes Sintéticas - Fusión de Texturas")
        self.ventana.geometry("1400x800")
        self.ventana.configure(bg='#2c3e50')

        # $ Variables de estado de la aplicación
        self.imagen_original_1 = None
        self.datos_imagen_original_1 = None
        self.dimensiones_imagen_1 = None

        self.imagen_original_2 = None
        self.datos_imagen_original_2 = None
        self.dimensiones_imagen_2 = None

        self.parches_extraidos_1 = []
        self.parches_extraidos_2 = []
        self.imagen_generada = None
        self.numero_iteraciones = 20  # $ Número de iteraciones por defecto
        self.factor_fusion = 0.5  # $ Factor de fusión (50% cada imagen)

        # ==> CONFIGURACIÓN DE LA INTERFAZ
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # # Configuración del marco principal
        marco_principal = tk.Frame(self.ventana, bg='#2c3e50')
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # -> Título principal
        titulo = tk.Label(marco_principal,
                         text="Generador de Imágenes Sintéticas - Fusión de Dos Texturas",
                         font=('Arial', 18, 'bold'),
                         bg='#2c3e50', fg='white')
        titulo.pack(pady=(0, 20))

        # -> Marco de controles
        marco_controles = tk.Frame(marco_principal, bg='#34495e', relief=tk.RAISED, bd=2)
        marco_controles.pack(fill=tk.X, pady=(0, 20))

        # # Botones de carga
        self.boton_cargar_1 = tk.Button(marco_controles,
                                       text="Cargar Imagen BMP #1",
                                       command=lambda: self.cargar_imagen_bmp(1),
                                       bg='#3498db', fg='white',
                                       font=('Arial', 10, 'bold'),
                                       relief=tk.RAISED, bd=3)
        self.boton_cargar_1.pack(side=tk.LEFT, padx=5, pady=10)

        self.boton_cargar_2 = tk.Button(marco_controles,
                                       text="Cargar Imagen BMP #2",
                                       command=lambda: self.cargar_imagen_bmp(2),
                                       bg='#9b59b6', fg='white',
                                       font=('Arial', 10, 'bold'),
                                       relief=tk.RAISED, bd=3)
        self.boton_cargar_2.pack(side=tk.LEFT, padx=5, pady=10)

        # # Control de factor de fusión
        marco_fusion = tk.Frame(marco_controles, bg='#34495e')
        marco_fusion.pack(side=tk.LEFT, padx=10, pady=10)

        etiqueta_fusion = tk.Label(marco_fusion,
                                  text="Fusión (Img1:Img2):",
                                  font=('Arial', 10, 'bold'),
                                  bg='#34495e', fg='white')
        etiqueta_fusion.pack(side=tk.LEFT, padx=(0, 5))

        self.entrada_fusion = tk.Entry(marco_fusion,
                                      width=5,
                                      font=('Arial', 10),
                                      bg='white', fg='black')
        self.entrada_fusion.insert(0, "0.5")
        self.entrada_fusion.pack(side=tk.LEFT, padx=(0, 10))

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
                                      text="Generar Fusión Sintética",
                                      command=self.generar_imagen_fusionada,
                                      bg='#e74c3c', fg='white',
                                      font=('Arial', 12, 'bold'),
                                      relief=tk.RAISED, bd=3,
                                      state=tk.DISABLED)
        self.boton_generar.pack(side=tk.LEFT, padx=10, pady=10)

        # -> Marco de visualización (3 columnas)
        marco_visualizacion = tk.Frame(marco_principal, bg='#34495e')
        marco_visualizacion.pack(fill=tk.BOTH, expand=True)

        # # Marco para imagen original 1
        marco_original_1 = tk.Frame(marco_visualizacion, bg='#34495e')
        marco_original_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        etiqueta_original_1 = tk.Label(marco_original_1,
                                     text="Imagen Original #1",
                                     font=('Arial', 12, 'bold'),
                                     bg='#34495e', fg='#3498db')
        etiqueta_original_1.pack(pady=(0, 10))

        self.canvas_original_1 = tk.Canvas(marco_original_1, bg='#2c3e50',
                                         relief=tk.SUNKEN, bd=2)
        self.canvas_original_1.pack(fill=tk.BOTH, expand=True)

        # # Marco para imagen original 2
        marco_original_2 = tk.Frame(marco_visualizacion, bg='#34495e')
        marco_original_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        etiqueta_original_2 = tk.Label(marco_original_2,
                                     text="Imagen Original #2",
                                     font=('Arial', 12, 'bold'),
                                     bg='#34495e', fg='#9b59b6')
        etiqueta_original_2.pack(pady=(0, 10))

        self.canvas_original_2 = tk.Canvas(marco_original_2, bg='#2c3e50',
                                         relief=tk.SUNKEN, bd=2)
        self.canvas_original_2.pack(fill=tk.BOTH, expand=True)

        # # Marco para imagen fusionada
        marco_fusionada = tk.Frame(marco_visualizacion, bg='#34495e')
        marco_fusionada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        etiqueta_fusionada = tk.Label(marco_fusionada,
                                    text="Imagen Fusionada",
                                    font=('Arial', 12, 'bold'),
                                    bg='#34495e', fg='#e74c3c')
        etiqueta_fusionada.pack(pady=(0, 10))

        self.canvas_fusionada = tk.Canvas(marco_fusionada, bg='#2c3e50',
                                        relief=tk.SUNKEN, bd=2)
        self.canvas_fusionada.pack(fill=tk.BOTH, expand=True)

        # -> Barra de estado
        self.barra_estado = tk.Label(marco_principal,
                                   text="Listo para cargar dos imágenes BMP",
                                   font=('Arial', 10),
                                   bg='#2c3e50', fg='#ecf0f1')
        self.barra_estado.pack(pady=(10, 0))

    # ==> SECCIÓN 1: CARGA Y VALIDACIÓN DE IMAGEN BMP (MODIFICADA PARA DOS IMÁGENES)
    def cargar_imagen_bmp(self, numero_imagen):
        # # Selección de archivo
        ruta_archivo = filedialog.askopenfilename(
            title=f"Seleccionar imagen BMP #{numero_imagen}",
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
                for fila in range(alto):
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

                # * Almacenamiento de datos según la imagen
                datos_invertidos = datos_pixeles[::-1]

                if numero_imagen == 1:
                    self.datos_imagen_original_1 = datos_invertidos
                    self.dimensiones_imagen_1 = (ancho, alto)
                    self.mostrar_imagen_original(1)
                    self.barra_estado.config(text=f"Imagen #1 cargada: {ancho}x{alto} píxeles")
                else:
                    self.datos_imagen_original_2 = datos_invertidos
                    self.dimensiones_imagen_2 = (ancho, alto)
                    self.mostrar_imagen_original(2)
                    self.barra_estado.config(text=f"Imagen #2 cargada: {ancho}x{alto} píxeles")

                # # Verificar si ambas imágenes están cargadas
                if self.datos_imagen_original_1 and self.datos_imagen_original_2:
                    self.boton_generar.config(state=tk.NORMAL)
                    self.barra_estado.config(text="Ambas imágenes cargadas - Listo para fusionar")

        except Exception as error:
            messagebox.showerror("Error", f"Error al cargar la imagen #{numero_imagen}: {str(error)}")
            self.barra_estado.config(text=f"Error al cargar imagen #{numero_imagen}")

    def mostrar_imagen_original(self, numero_imagen):
        # # Seleccionar datos y canvas según la imagen
        if numero_imagen == 1:
            datos_imagen = self.datos_imagen_original_1
            canvas = self.canvas_original_1
        else:
            datos_imagen = self.datos_imagen_original_2
            canvas = self.canvas_original_2

        if datos_imagen:
            # -> Limpiar canvas
            canvas.delete("all")

            # -> Obtener dimensiones
            alto = len(datos_imagen)
            ancho = len(datos_imagen[0])
            canvas_width = 300
            canvas_height = 350

            # ==> CÁLCULO DE ESCALA
            escala_x = canvas_width / ancho
            escala_y = canvas_height / alto
            escala = min(escala_x, escala_y)

            # -> Calcular nuevas dimensiones y posición centrada
            nuevo_ancho = int(ancho * escala)
            nuevo_alto = int(alto * escala)
            x_offset = (canvas_width - nuevo_ancho) // 2
            y_offset = (canvas_height - nuevo_alto) // 2

            # ==> DIBUJO DE PÍXELES POR FILAS
            for y in range(alto):
                for x in range(ancho):
                    r, g, b = datos_imagen[y][x]
                    color = f"#{r:02x}{g:02x}{b:02x}"

                    # -> Coordenadas escaladas
                    x1 = x_offset + int(x * escala)
                    y1 = y_offset + int(y * escala)
                    x2 = x_offset + int((x + 1) * escala)
                    y2 = y_offset + int((y + 1) * escala)

                    if x1 < x2 and y1 < y2:
                        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

    # ==> SECCIÓN 2: EXTRACCIÓN DE PARCHES (MATRIZ EVOLUTIVA - FASE 1) - MODIFICADA PARA DOS IMÁGENES
    def extraer_parches_aleatorios(self, numero_imagen):
        # # Configuración del generador Mersenne Twister
        random.seed(42 + numero_imagen)  # $ Semilla diferente para cada imagen

        # $ Seleccionar datos según la imagen
        if numero_imagen == 1:
            datos_imagen = self.datos_imagen_original_1
            dimensiones = self.dimensiones_imagen_1
        else:
            datos_imagen = self.datos_imagen_original_2
            dimensiones = self.dimensiones_imagen_2

        ancho, alto = dimensiones
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
                    r, g, b = datos_imagen[y][x]
                    # $ Cuantización de colores para reducir complejidad
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
                    'centro_y': y_centro,
                    'imagen_origen': numero_imagen
                })
                parches_extraidos += 1

            intentos_maximos -= 1

        # $ Almacenar parches según la imagen
        if numero_imagen == 1:
            self.parches_extraidos_1 = parches
        else:
            self.parches_extraidos_2 = parches

        return parches

    # ==> SECCIÓN 3: SÍNTESIS DE FUSIÓN (NUEVA FUNCIÓN PRINCIPAL)
    def generar_imagen_fusionada(self):
        if not self.datos_imagen_original_1 or not self.datos_imagen_original_2:
            messagebox.showwarning("Advertencia", "Debe cargar ambas imágenes BMP primero")
            return

        # # Validar parámetros del usuario
        try:
            self.numero_iteraciones = int(self.entrada_iteraciones.get())
            if self.numero_iteraciones < 1 or self.numero_iteraciones > 100:
                messagebox.showwarning("Advertencia", "El número de iteraciones debe estar entre 1 y 100")
                return

            self.factor_fusion = float(self.entrada_fusion.get())
            if self.factor_fusion < 0.0 or self.factor_fusion > 1.0:
                messagebox.showwarning("Advertencia", "El factor de fusión debe estar entre 0.0 y 1.0")
                return
        except ValueError:
            messagebox.showwarning("Advertencia", "Valores inválidos en los parámetros")
            return

        # # Reescalar automáticamente las imágenes a dimensiones compatibles
        self.barra_estado.config(text="Reescalando imágenes para compatibilidad...")
        self.ventana.update()
        ancho_fusion, alto_fusion = self.calcular_dimensiones_fusion()

        # $ Reescalar ambas imágenes a las dimensiones de fusión
        imagen_1_reescalada = self.reescalar_imagen(self.datos_imagen_original_1, self.dimensiones_imagen_1, (ancho_fusion, alto_fusion))
        imagen_2_reescalada = self.reescalar_imagen(self.datos_imagen_original_2, self.dimensiones_imagen_2, (ancho_fusion, alto_fusion))

        # $ Almacenar temporalmente las imágenes reescaladas
        datos_orig_1 = self.datos_imagen_original_1
        datos_orig_2 = self.datos_imagen_original_2
        self.datos_imagen_original_1 = imagen_1_reescalada
        self.datos_imagen_original_2 = imagen_2_reescalada

        # # Fase 1: Extracción de parches de ambas imágenes reescaladas
        self.barra_estado.config(text="Extrayendo parches de la imagen #1 reescalada...")
        self.ventana.update()
        parches_1 = self.extraer_parches_aleatorios_fusion(1, ancho_fusion, alto_fusion)

        self.barra_estado.config(text="Extrayendo parches de la imagen #2 reescalada...")
        self.ventana.update()
        parches_2 = self.extraer_parches_aleatorios_fusion(2, ancho_fusion, alto_fusion)

        # # Combinar parches según el factor de fusión
        parches_combinados = self.combinar_parches(parches_1, parches_2)

        # # Fase 2: Inicialización de la imagen fusionada con ruido híbrido
        self.barra_estado.config(text="Inicializando imagen fusionada con texturas híbridas...")
        self.ventana.update()
        imagen_inicial = self.inicializar_imagen_fusion_hibrida(ancho_fusion, alto_fusion)

        # # Fase 3: Iteraciones de refinamiento evolutivo
        self.barra_estado.config(text=f"Aplicando refinamiento evolutivo de fusión ({self.numero_iteraciones} iteraciones)...")
        self.ventana.update()
        imagen_final = self.aplicar_refinamiento_fusion(imagen_inicial, parches_combinados, ancho_fusion, alto_fusion)

        # # Restaurar imágenes originales
        self.datos_imagen_original_1 = datos_orig_1
        self.datos_imagen_original_2 = datos_orig_2

        # # Fase 4: Mostrar imagen fusionada
        self.imagen_generada = imagen_final
        self.mostrar_imagen_fusionada()

        self.barra_estado.config(text=f"Imagen fusionada generada exitosamente ({self.numero_iteraciones} iteraciones) - {ancho_fusion}x{alto_fusion}")

    def calcular_dimensiones_fusion(self):
        # # Calcular dimensiones óptimas para la fusión
        ancho_1, alto_1 = self.dimensiones_imagen_1
        ancho_2, alto_2 = self.dimensiones_imagen_2

        # $ Estrategia: Usar la dimensión promedio para mejor calidad
        ancho_fusion = (ancho_1 + ancho_2) // 2
        alto_fusion = (alto_1 + alto_2) // 2

        # $ Asegurar dimensiones mínimas para parches 5x5
        ancho_fusion = max(ancho_fusion, 50)
        alto_fusion = max(alto_fusion, 50)

        # $ Limitar dimensiones máximas para performance
        ancho_fusion = min(ancho_fusion, 800)
        alto_fusion = min(alto_fusion, 800)

        return ancho_fusion, alto_fusion

    def reescalar_imagen(self, imagen_original, dimensiones_originales, nuevas_dimensiones):
        # # Reescalar imagen usando interpolación bilineal
        ancho_orig, alto_orig = dimensiones_originales
        ancho_nuevo, alto_nuevo = nuevas_dimensiones

        # $ Si las dimensiones son iguales, no reescalar
        if ancho_orig == ancho_nuevo and alto_orig == alto_nuevo:
            return imagen_original

        imagen_reescalada = []

        # $ Calcular factores de escala
        factor_x = ancho_orig / ancho_nuevo
        factor_y = alto_orig / alto_nuevo

        for y_nuevo in range(alto_nuevo):
            fila_nueva = []
            for x_nuevo in range(ancho_nuevo):
                # $ Mapear coordenadas nuevas a originales
                x_orig = x_nuevo * factor_x
                y_orig = y_nuevo * factor_y

                # $ Interpolación bilineal
                color_interpolado = self.interpolar_bilineal(imagen_original, x_orig, y_orig, ancho_orig, alto_orig)
                fila_nueva.append(color_interpolado)

            imagen_reescalada.append(fila_nueva)

        return imagen_reescalada

    def interpolar_bilineal(self, imagen, x, y, ancho, alto):
        # # Interpolación bilineal para reescalado suave
        x1 = int(x)
        y1 = int(y)
        x2 = min(x1 + 1, ancho - 1)
        y2 = min(y1 + 1, alto - 1)

        # $ Asegurar coordenadas válidas
        x1 = max(0, min(x1, ancho - 1))
        y1 = max(0, min(y1, alto - 1))

        # $ Factores de interpolación
        fx = x - x1
        fy = y - y1

        # $ Obtener píxeles de las esquinas
        p11 = imagen[y1][x1]  # Superior izquierda
        p12 = imagen[y2][x1]  # Inferior izquierda
        p21 = imagen[y1][x2]  # Superior derecha
        p22 = imagen[y2][x2]  # Inferior derecha

        # $ Interpolación para cada canal RGB
        r = int((1-fx)*(1-fy)*p11[0] + fx*(1-fy)*p21[0] + (1-fx)*fy*p12[0] + fx*fy*p22[0])
        g = int((1-fx)*(1-fy)*p11[1] + fx*(1-fy)*p21[1] + (1-fx)*fy*p12[1] + fx*fy*p22[1])
        b = int((1-fx)*(1-fy)*p11[2] + fx*(1-fy)*p21[2] + (1-fx)*fy*p12[2] + fx*fy*p22[2])

        # $ Asegurar valores en rango válido
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        return [r, g, b]

    def extraer_parches_aleatorios_fusion(self, numero_imagen, ancho, alto):
        # # Extracción de parches optimizada para imágenes reescaladas
        random.seed(42 + numero_imagen)  # $ Semilla diferente para cada imagen

        # $ Seleccionar datos según la imagen (ya reescaladas)
        if numero_imagen == 1:
            datos_imagen = self.datos_imagen_original_1
        else:
            datos_imagen = self.datos_imagen_original_2

        parches = []

        # $ Calcular total de parches posibles
        total_parches = (ancho - 4) * (alto - 4)  # $ Parches 5x5
        parches_a_extraer = max(1, total_parches // 30)  # ! Mayor densidad de parches para mejor calidad

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
                    r, g, b = datos_imagen[y][x]
                    # $ Cuantización de colores para reducir complejidad
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
                    'centro_y': y_centro,
                    'imagen_origen': numero_imagen
                })
                parches_extraidos += 1

            intentos_maximos -= 1

        return parches

    def combinar_parches(self, parches_1, parches_2):
        # # Combinar parches según el factor de fusión
        total_parches_1 = int(len(parches_1) * self.factor_fusion)
        total_parches_2 = int(len(parches_2) * (1.0 - self.factor_fusion))

        # $ Tomar muestra de cada conjunto de parches
        muestra_1 = random.sample(parches_1, min(total_parches_1, len(parches_1)))
        muestra_2 = random.sample(parches_2, min(total_parches_2, len(parches_2)))

        # $ Combinar y mezclar aleatoriamente
        parches_combinados = muestra_1 + muestra_2
        random.shuffle(parches_combinados)

        return parches_combinados

    def inicializar_imagen_fusion_hibrida(self, ancho, alto):
        # # Crear imagen inicial fusionando muestras de ambas imágenes con ruido
        imagen_fusion = []

        for y in range(alto):
            fila_fusion = []
            for x in range(ancho):
                # $ Decidir aleatoriamente de qué imagen tomar el píxel base
                if random.random() < self.factor_fusion:
                    # $ Tomar de imagen 1
                    r_base, g_base, b_base = self.datos_imagen_original_1[y][x]
                else:
                    # $ Tomar de imagen 2
                    r_base, g_base, b_base = self.datos_imagen_original_2[y][x]

                # $ Aplicar ruido gaussiano para forzar el proceso evolutivo
                ruido_r = int(random.gauss(0, 8))  # $ Ruido ligeramente mayor para más diversidad
                ruido_g = int(random.gauss(0, 8))
                ruido_b = int(random.gauss(0, 8))

                # $ Calcular nuevo color con ruido
                r_nuevo = max(0, min(255, r_base + ruido_r))
                g_nuevo = max(0, min(255, g_base + ruido_g))
                b_nuevo = max(0, min(255, b_base + ruido_b))

                fila_fusion.append([r_nuevo, g_nuevo, b_nuevo])
            imagen_fusion.append(fila_fusion)

        return imagen_fusion

    def aplicar_refinamiento_fusion(self, imagen_inicial, parches_combinados, ancho, alto):
        # # Configuración del proceso evolutivo para fusión
        imagen_actual = [fila[:] for fila in imagen_inicial]  # $ Copia profunda

        # # Iteraciones de refinamiento
        for iteracion in range(self.numero_iteraciones):
            self.barra_estado.config(text=f"Refinamiento fusión: iteración {iteracion + 1}/{self.numero_iteraciones}")
            self.ventana.update()

            # $ Procesar cada píxel (excepto bordes)
            for y in range(2, alto - 2):
                for x in range(2, ancho - 2):
                    # # Extraer parche 5x5 centrado en el píxel actual
                    parche_actual = self.extraer_parche_5x5_fusion(imagen_actual, x, y)

                    # # Encontrar el parche más similar de la colección combinada
                    mejor_parche = self.encontrar_parche_mas_similar_fusion(parche_actual, parches_combinados)

                    if mejor_parche:
                        # $ Obtener color del centro del mejor parche
                        color_centro = self.obtener_color_centro_parche_fusion(mejor_parche)
                        imagen_actual[y][x] = color_centro

            # $ Actualizar visualización cada iteración para ver el progreso en tiempo real
            self.imagen_generada = imagen_actual
            self.mostrar_imagen_fusionada()
            self.ventana.update()

        return imagen_actual

    def extraer_parche_5x5_fusion(self, imagen, x_centro, y_centro):
        # # Extraer parche 5x5 para proceso de fusión
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

    def encontrar_parche_mas_similar_fusion(self, parche_actual, parches_combinados):
        # # Encontrar parche más similar de la colección fusionada
        mejor_parche = None
        menor_distancia = float('inf')

        # $ Muestra optimizada para performance
        muestra_aleatoria = min(150, len(parches_combinados))
        if len(parches_combinados) > muestra_aleatoria:
            muestra = random.sample(parches_combinados, muestra_aleatoria)
        else:
            muestra = parches_combinados

        for parche_original in muestra:
            distancia = self.calcular_distancia_parches_fusion(parche_actual, parche_original['datos'])
            if distancia < menor_distancia:
                menor_distancia = distancia
                mejor_parche = parche_original

        return mejor_parche

    def calcular_distancia_parches_fusion(self, parche1, parche2):
        # # Distancia euclidiana optimizada para fusión
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

    def obtener_color_centro_parche_fusion(self, parche_original):
        # # Obtener color del centro según la imagen de origen
        centro_x = parche_original['centro_x']
        centro_y = parche_original['centro_y']
        imagen_origen = parche_original['imagen_origen']

        if imagen_origen == 1:
            return self.datos_imagen_original_1[centro_y][centro_x]
        else:
            return self.datos_imagen_original_2[centro_y][centro_x]

    def mostrar_imagen_fusionada(self):
        # # Mostrar imagen fusionada
        if self.imagen_generada:
            # -> Limpiar canvas
            self.canvas_fusionada.delete("all")

            # -> Obtener dimensiones
            alto = len(self.imagen_generada)
            ancho = len(self.imagen_generada[0])
            canvas_width = 300
            canvas_height = 350

            # ==> CÁLCULO DE ESCALA
            escala_x = canvas_width / ancho
            escala_y = canvas_height / alto
            escala = min(escala_x, escala_y)

            # -> Calcular nuevas dimensiones y posición centrada
            nuevo_ancho = int(ancho * escala)
            nuevo_alto = int(alto * escala)
            x_offset = (canvas_width - nuevo_ancho) // 2
            y_offset = (canvas_height - nuevo_alto) // 2

            # ==> DIBUJO DE PÍXELES POR FILAS
            for y in range(alto):
                for x in range(ancho):
                    r, g, b = self.imagen_generada[y][x]
                    color = f"#{r:02x}{g:02x}{b:02x}"

                    # -> Coordenadas escaladas
                    x1 = x_offset + int(x * escala)
                    y1 = y_offset + int(y * escala)
                    x2 = x_offset + int((x + 1) * escala)
                    y2 = y_offset + int((y + 1) * escala)

                    if x1 < x2 and y1 < y2:
                        self.canvas_fusionada.create_rectangle(x1, y1, x2, y2, fill=color, outline="", width=0)

    def ejecutar(self):
        # # Iniciar la aplicación
        self.ventana.mainloop()

# ==> PUNTO DE ENTRADA PRINCIPAL
if __name__ == "__main__":
    # # Crear y ejecutar la aplicación
    app = GeneradorImagenesSinteticas()
    app.ejecutar()
