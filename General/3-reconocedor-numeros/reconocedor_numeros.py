"""
==> RECONOCEDOR DE NÚMEROS - VISIÓN POR COMPUTADORA
% Sistema de reconocimiento de dígitos basado en patrones y distancia de Hamming
% Utiliza segmentación de regiones y normalización para identificar números en imágenes BMP

-> Características principales:
- Carga y procesamiento de imágenes BMP de 24 bits
- Conversión a escala de grises y binarización
- Segmentación de regiones conectadas usando BFS
- Normalización de patrones a 10x10 píxeles
- Reconocimiento mediante distancia de Hamming
- Interfaz gráfica con tkinter

% Autor: Olvera Olvera Oliver Jesus
% Unidad de Aprendizaje: Visión por Computadora
% Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os

class ReconocedorNumeros:
    """
    ==> CLASE PRINCIPAL - RECONOCEDOR DE NÚMEROS
    % Clase principal para el reconocimiento de dígitos en imágenes
    % Implementa un sistema basado en patrones y distancia de Hamming
    """

    def __init__(self, root):
        """
        # Inicialización del reconocedor
        % Inicializa la aplicación de reconocimiento de números
        $ root: Ventana principal de tkinter
        """
        # ==> CONFIGURACIÓN DE VENTANA PRINCIPAL
        self.root = root
        self.root.title("Reconocedor de Números - Visión por Computadora")
        self.root.geometry("800x600")

        # ==> VARIABLES DE ESTADO
        # -> Datos de imagen
        self.imagen_original = None      # -> Imagen original cargada
        self.imagen_binaria = None       # -> Imagen binarizada
        self.patrones_entrenados = {}    # -> Patrones de entrenamiento por dígito
        self.regiones_detectadas = []    # -> Regiones detectadas en la imagen

        # -> Configurar la interfaz
        self.configurar_interfaz()

        # -> Entrenar con el dataset al iniciar
        self.entrenar_con_dataset()

    def configurar_interfaz(self):
        """
        # Configuración de interfaz gráfica
        % Configura todos los elementos de la interfaz gráfica
        """
        # ==> FRAME PRINCIPAL
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # -> Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # ==> TÍTULO PRINCIPAL
        titulo = ttk.Label(main_frame, text="Reconocedor de Números",
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # ==> FRAME DE CONTROLES
        controles_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        controles_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # -> Botón cargar imagen
        self.btn_cargar = ttk.Button(controles_frame, text="Cargar Imagen BMP",
                                    command=self.cargar_imagen)
        self.btn_cargar.grid(row=0, column=0, padx=(0, 10))

        # -> Botón limpiar
        self.btn_limpiar = ttk.Button(controles_frame, text="Limpiar",
                                     command=self.limpiar_imagen)
        self.btn_limpiar.grid(row=0, column=1, padx=(0, 10))

        # -> Botón procesar
        self.btn_procesar = ttk.Button(controles_frame, text="Procesar Imagen",
                                      command=self.procesar_imagen, state="disabled")
        self.btn_procesar.grid(row=0, column=2)

        # ==> FRAME DE VISUALIZACIÓN
        imagenes_frame = ttk.LabelFrame(main_frame, text="Visualización", padding="10")
        imagenes_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        imagenes_frame.columnconfigure(0, weight=1)
        imagenes_frame.columnconfigure(1, weight=1)
        imagenes_frame.rowconfigure(0, weight=1)

        # -> Canvas para imagen original
        self.canvas_original = tk.Canvas(imagenes_frame, bg="white", width=350, height=400)
        self.canvas_original.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))

        # -> Canvas para imagen binaria
        self.canvas_binaria = tk.Canvas(imagenes_frame, bg="white", width=350, height=400)
        self.canvas_binaria.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # -> Labels para títulos de las imágenes
        ttk.Label(imagenes_frame, text="Imagen Original").grid(row=1, column=0, pady=(5, 0))
        ttk.Label(imagenes_frame, text="Imagen Binaria").grid(row=1, column=1, pady=(5, 0))

        # ==> BARRA DE ESTADO
        self.status_var = tk.StringVar()
        self.status_var.set("Listo para cargar imagen")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

    def entrenar_con_dataset(self):
        """
        # Entrenamiento con dataset
        % Entrena el sistema con el dataset de números
        % Carga patrones de cada dígito (0-9) desde archivos BMP
        """
        try:
            self.status_var.set("Entrenando con dataset...")
            self.root.update()

            # -> Ruta del dataset
            dataset_path = os.path.join(os.path.dirname(__file__), "Numeros")

            # ==> PROCESAMIENTO DE CARPETAS DE DÍGITOS
            # -> Procesar cada carpeta de dígitos (0-9)
            for digito in range(10):
                carpeta_digito = os.path.join(dataset_path, str(digito))
                if os.path.exists(carpeta_digito):
                    self.patrones_entrenados[digito] = []

                    # -> Procesar cada imagen en la carpeta
                    archivos = [f for f in os.listdir(carpeta_digito) if f.endswith('.bmp')]
                    for archivo in archivos:
                        ruta_imagen = os.path.join(carpeta_digito, archivo)
                        try:
                            # ==> PROCESAMIENTO DE IMAGEN DE ENTRENAMIENTO
                            # -> Cargar y procesar imagen
                            imagen = self.cargar_imagen_bmp(ruta_imagen)
                            if imagen is not None:
                                # -> Convertir a escala de grises y binarizar
                                gris = self.convertir_a_grises(imagen)
                                binaria = self.binarizar(gris)

                                # -> Segmentar regiones
                                regiones = self.segmentar_regiones(binaria)

                                # -> Procesar cada región encontrada
                                for region in regiones:
                                    # -> Normalizar región a 10x10
                                    region_normalizada = self.normalizar_region(region['matriz'])
                                    self.patrones_entrenados[digito].append(region_normalizada)

                        except Exception as e:
                            print(f"Error procesando {ruta_imagen}: {e}")

            # -> Mostrar estadísticas de entrenamiento
            total_patrones = sum(len(patrones) for patrones in self.patrones_entrenados.values())
            self.status_var.set(f"Entrenamiento completado. {total_patrones} patrones cargados.")

        except Exception as e:
            self.status_var.set("Error en entrenamiento")

    def cargar_imagen(self):
        """
        # Carga de imagen BMP
        % Abre un diálogo para seleccionar y cargar una imagen BMP
        % Procesa la imagen para reconocimiento de dígitos
        """
        try:
            # -> Abrir diálogo de selección
            ruta_archivo = filedialog.askopenfilename(
                title="Seleccionar imagen BMP",
                filetypes=[("Archivos BMP", "*.bmp"), ("Todos los archivos", "*.*")]
            )

            if ruta_archivo:
                self.status_var.set("Cargando imagen...")
                self.root.update()

                # -> Cargar imagen BMP
                self.imagen_original = self.cargar_imagen_bmp(ruta_archivo)

                if self.imagen_original is not None:
                    # ==> PROCESAMIENTO DE IMAGEN
                    # -> Convertir a escala de grises
                    imagen_gris = self.convertir_a_grises(self.imagen_original)

                    # -> Binarizar
                    self.imagen_binaria = self.binarizar(imagen_gris)

                    # -> Mostrar imágenes
                    self.mostrar_imagen_original()
                    self.mostrar_imagen_binaria()

                    # -> Habilitar botón de procesar
                    self.btn_procesar.config(state="normal")

                    self.status_var.set(f"Imagen cargada: {os.path.basename(ruta_archivo)}")
                else:
                    self.status_var.set("Error al cargar imagen")

        except Exception as e:
            self.status_var.set("Error al cargar imagen")

    def cargar_imagen_bmp(self, ruta_archivo):
        """
        # Carga de archivo BMP
        % Carga una imagen BMP y retorna una lista de listas de listas (alto x ancho x 3)
        $ ruta_archivo: Ruta al archivo BMP
        % Returns: Matriz de imagen en formato RGB
        """
        try:
            with open(ruta_archivo, 'rb') as f:
                # ==> LECTURA DEL HEADER BMP
                # -> Leer header BMP (54 bytes)
                header = f.read(54)

                # -> Extraer información del header
                ancho = int.from_bytes(header[18:22], byteorder='little')
                alto = int.from_bytes(header[22:26], byteorder='little')
                bits_por_pixel = int.from_bytes(header[28:30], byteorder='little')

                # -> Validar formato
                if bits_por_pixel != 24:
                    raise ValueError("Solo se soportan imágenes BMP de 24 bits")

                # ==> CÁLCULO DE PADDING
                # -> Calcular padding
                padding = (4 - (ancho * 3) % 4) % 4

                # ==> CREACIÓN DE MATRIZ DE IMAGEN
                # -> Crear matriz de imagen como lista de listas
                imagen = []
                for y in range(alto):
                    fila = []
                    for x in range(ancho):
                        fila.append([0, 0, 0])  # -> Inicializar con [R, G, B]
                    imagen.append(fila)

                # ==> LECTURA DE DATOS DE PÍXELES
                # -> Leer datos de píxeles
                for y in range(alto - 1, -1, -1):  # -> BMP se almacena de abajo hacia arriba
                    for x in range(ancho):
                        # -> Leer BGR (BMP usa BGR, no RGB)
                        b = int.from_bytes(f.read(1), byteorder='little')
                        g = int.from_bytes(f.read(1), byteorder='little')
                        r = int.from_bytes(f.read(1), byteorder='little')

                        # -> Convertir a RGB
                        imagen[y][x] = [r, g, b]

                    # -> Saltar padding
                    f.read(padding)

                return imagen

        except Exception as e:
            print(f"Error cargando BMP: {e}")
            return None

    def convertir_a_grises(self, imagen):
        """
        # Conversión a escala de grises
        % Convierte una imagen RGB a escala de grises usando luminancia ponderada
        $ imagen: Matriz de imagen en formato RGB
        % Returns: Matriz de imagen en escala de grises
        """
        alto = len(imagen)
        ancho = len(imagen[0])
        imagen_gris = []

        # -> Fórmula de luminancia ponderada: gris = 0.3*R + 0.59*G + 0.11*B
        for y in range(alto):
            fila_gris = []
            for x in range(ancho):
                r, g, b = imagen[y][x]
                gris = int(0.3 * r + 0.59 * g + 0.11 * b)
                fila_gris.append(gris)
            imagen_gris.append(fila_gris)

        return imagen_gris

    def binarizar(self, imagen_gris):
        """
        # Binarización de imagen
        % Binariza una imagen en escala de grises con umbral 128
        $ imagen_gris: Matriz de imagen en escala de grises
        % Returns: Matriz de imagen binaria (0 o 1)
        """
        alto = len(imagen_gris)
        ancho = len(imagen_gris[0])
        imagen_binaria = []

        # -> Umbral fijo de 128: Gris < 128 → 1 (foreground), Gris ≥ 128 → 0 (background)
        for y in range(alto):
            fila_binaria = []
            for x in range(ancho):
                if imagen_gris[y][x] < 128:
                    fila_binaria.append(1)
                else:
                    fila_binaria.append(0)
            imagen_binaria.append(fila_binaria)

        return imagen_binaria

    def segmentar_regiones(self, imagen_binaria):
        """
        # Segmentación de regiones
        % Segmenta regiones conectadas usando BFS (Búsqueda en Anchura)
        $ imagen_binaria: Matriz de imagen binaria
        % Returns: Lista de regiones detectadas
        """
        alto = len(imagen_binaria)
        ancho = len(imagen_binaria[0])

        # ==> INICIALIZACIÓN DE MATRIZ DE VISITADOS
        # -> Crear matriz de visitados
        visitados = []
        for y in range(alto):
            fila_visitados = []
            for x in range(ancho):
                fila_visitados.append(False)
            visitados.append(fila_visitados)

        regiones = []

        # -> Direcciones para conectividad de 4 vecinos
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # -> arriba, abajo, izquierda, derecha

        # ==> BÚSQUEDA DE REGIONES
        # -> Buscar regiones no visitadas
        for y in range(alto):
            for x in range(ancho):
                # -> Si encontramos un píxel no visitado con valor 1
                if imagen_binaria[y][x] == 1 and not visitados[y][x]:
                    # -> Iniciar BFS para esta región
                    region = self.bfs_region(imagen_binaria, visitados, x, y, direcciones)

                    # -> Filtrar regiones muy pequeñas (menos de 5x5 píxeles)
                    if len(region['pixeles']) >= 25:  # -> 5x5 = 25 píxeles
                        regiones.append(region)

        return regiones

    def bfs_region(self, imagen_binaria, visitados, x_inicial, y_inicial, direcciones):
        """
        # Búsqueda en anchura para regiones
        % Implementa BFS para encontrar todos los píxeles conectados de una región
        $ imagen_binaria: Matriz de imagen binaria
        $ visitados: Matriz de píxeles visitados
        $ x_inicial, y_inicial: Coordenadas iniciales
        $ direcciones: Lista de direcciones de movimiento
        % Returns: Diccionario con información de la región
        """
        alto = len(imagen_binaria)
        ancho = len(imagen_binaria[0])

        # ==> INICIALIZACIÓN DE BFS
        # -> Cola para BFS (usando lista simple en lugar de deque)
        cola = [(x_inicial, y_inicial)]
        visitados[y_inicial][x_inicial] = True

        # -> Información de la región
        pixeles_region = [(x_inicial, y_inicial)]
        min_x, max_x = x_inicial, x_inicial
        min_y, max_y = y_inicial, y_inicial

        # ==> BUCLE PRINCIPAL DE BFS
        while cola:
            # -> Obtener el primer elemento de la cola (FIFO)
            x, y = cola.pop(0)

            # -> Explorar vecinos
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy

                # -> Verificar límites y si es un píxel válido no visitado
                if (0 <= nx < ancho and 0 <= ny < alto and
                    imagen_binaria[ny][nx] == 1 and not visitados[ny][nx]):

                    visitados[ny][nx] = True
                    cola.append((nx, ny))
                    pixeles_region.append((nx, ny))

                    # -> Actualizar límites de la región
                    min_x = min(min_x, nx)
                    max_x = max(max_x, nx)
                    min_y = min(min_y, ny)
                    max_y = max(max_y, ny)

        # ==> CREACIÓN DE MATRIZ DE REGIÓN
        # -> Crear matriz de la región
        ancho_region = max_x - min_x + 1
        alto_region = max_y - min_y + 1
        matriz_region = []

        for y in range(alto_region):
            fila = []
            for x in range(ancho_region):
                fila.append(0)
            matriz_region.append(fila)

        # -> Llenar la matriz con los píxeles de la región
        for x, y in pixeles_region:
            matriz_region[y - min_y][x - min_x] = 1

        return {
            'pixeles': pixeles_region,
            'matriz': matriz_region,
            'limites': (min_x, max_x, min_y, max_y),
            'ancho': ancho_region,
            'alto': alto_region
        }

    def normalizar_region(self, matriz_region):
        """
        # Normalización de región
        % Normaliza una región a 10x10 píxeles usando interpolación bilineal
        $ matriz_region: Matriz de la región a normalizar
        % Returns: Matriz normalizada de 10x10 píxeles
        """
        alto_original = len(matriz_region)
        ancho_original = len(matriz_region[0])

        # -> Matriz normalizada de 10x10
        matriz_normalizada = []
        for y in range(10):
            fila = []
            for x in range(10):
                fila.append(0)
            matriz_normalizada.append(fila)

        # ==> INTERPOLACIÓN BILINEAL
        # -> Normalizar cada píxel
        for y_nuevo in range(10):
            for x_nuevo in range(10):
                # -> Calcular coordenadas en la imagen original
                x_original = (x_nuevo + 0.5) * ancho_original / 10
                y_original = (y_nuevo + 0.5) * alto_original / 10

                # -> Interpolación bilineal
                valor = self.interpolacion_bilineal(matriz_region, x_original, y_original)

                # -> Binarizar con umbral 0.5
                matriz_normalizada[y_nuevo][x_nuevo] = 1 if valor > 0.5 else 0

        return matriz_normalizada

    def interpolacion_bilineal(self, matriz, x, y):
        """
        # Interpolación bilineal
        % Realiza interpolación bilineal en una matriz
        $ matriz: Matriz de entrada
        $ x, y: Coordenadas de interpolación
        % Returns: Valor interpolado
        """
        alto = len(matriz)
        ancho = len(matriz[0])

        # -> Coordenadas enteras
        x0 = int(x)
        y0 = int(y)
        x1 = min(x0 + 1, ancho - 1)
        y1 = min(y0 + 1, alto - 1)

        # -> Factores de interpolación
        fx = x - x0
        fy = y - y0

        # -> Valores de los 4 vecinos
        v00 = matriz[y0][x0]
        v01 = matriz[y0][x1]
        v10 = matriz[y1][x0]
        v11 = matriz[y1][x1]

        # -> Interpolación bilineal
        valor = (v00 * (1 - fx) * (1 - fy) +
                v01 * fx * (1 - fy) +
                v10 * (1 - fx) * fy +
                v11 * fx * fy)

        return valor

    def calcular_distancia_hamming(self, patron1, patron2):
        """
        # Cálculo de distancia de Hamming
        % Calcula la distancia de Hamming entre dos patrones binarios
        $ patron1, patron2: Patrones binarios de 10x10
        % Returns: Distancia de Hamming (número de bits diferentes)
        """
        distancia = 0
        for y in range(10):
            for x in range(10):
                if patron1[y][x] != patron2[y][x]:
                    distancia += 1
        return distancia

    def reconocer_digito(self, patron_normalizado):
        """
        # Reconocimiento de dígito
        % Reconoce un dígito comparando con los patrones entrenados
        $ patron_normalizado: Patrón normalizado de 10x10
        % Returns: (dígito reconocido, confianza)
        """
        mejor_digito = -1
        menor_distancia = float('inf')

        # -> Comparar con todos los patrones entrenados
        for digito, patrones in self.patrones_entrenados.items():
            for patron in patrones:
                distancia = self.calcular_distancia_hamming(patron_normalizado, patron)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    mejor_digito = digito

        # -> Calcular confianza (menor distancia = mayor confianza)
        confianza = max(0, 100 - (menor_distancia * 100 / 100))  # -> Máximo 100 bits diferentes

        return mejor_digito, confianza

    def mostrar_imagen_original(self):
        """
        # Visualización de imagen original
        % Muestra la imagen original en el canvas usando solo tkinter
        """
        if self.imagen_original is not None:
            # -> Limpiar canvas
            self.canvas_original.delete("all")

            # -> Obtener dimensiones
            alto = len(self.imagen_original)
            ancho = len(self.imagen_original[0])
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

            # ==> DIBUJO DE PÍXELES
            # -> Dibujar píxeles escalados
            for y in range(alto):
                for x in range(ancho):
                    r, g, b = self.imagen_original[y][x]
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

    def mostrar_imagen_binaria(self):
        """
        # Visualización de imagen binaria
        % Muestra la imagen binaria en el canvas usando solo tkinter
        """
        if self.imagen_binaria is not None:
            # -> Limpiar canvas
            self.canvas_binaria.delete("all")

            # -> Obtener dimensiones
            alto = len(self.imagen_binaria)
            ancho = len(self.imagen_binaria[0])
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

            # ==> DIBUJO DE PÍXELES BINARIOS
            # -> Dibujar píxeles binarios escalados
            for y in range(alto):
                for x in range(ancho):
                    # -> Color blanco para 0 (background), negro para 1 (foreground)
                    color = "black" if self.imagen_binaria[y][x] == 1 else "white"

                    # -> Coordenadas escaladas
                    x1 = x_offset + int(x * escala)
                    y1 = y_offset + int(y * escala)
                    x2 = x_offset + int((x + 1) * escala)
                    y2 = y_offset + int((y + 1) * escala)

                    # -> Solo dibujar si el píxel es visible
                    if x1 < x2 and y1 < y2:
                        self.canvas_binaria.create_rectangle(x1, y1, x2, y2,
                                                           fill=color, outline="", width=0)

    def mostrar_resultados_reconocimiento(self):
        """
        # Visualización de resultados
        % Muestra los resultados del reconocimiento en el canvas binario
        """
        if not self.regiones_detectadas:
            return

        # -> Obtener dimensiones del canvas
        canvas_width = 350
        canvas_height = 400

        # -> Obtener dimensiones de la imagen binaria
        alto = len(self.imagen_binaria)
        ancho = len(self.imagen_binaria[0])

        # ==> CÁLCULO DE ESCALA
        # -> Calcular escala
        escala_x = canvas_width / ancho
        escala_y = canvas_height / alto
        escala = min(escala_x, escala_y)

        # -> Calcular offset para centrar
        nuevo_ancho = int(ancho * escala)
        nuevo_alto = int(alto * escala)
        x_offset = (canvas_width - nuevo_ancho) // 2
        y_offset = (canvas_height - nuevo_alto) // 2

        # ==> DIBUJO DE RESULTADOS
        # -> Dibujar rectángulos y texto para cada región detectada
        for region in self.regiones_detectadas:
            min_x, max_x, min_y, max_y = region['limites']
            digito = region['digito']
            confianza = region['confianza']

            # -> Coordenadas escaladas para el rectángulo
            x1 = x_offset + int(min_x * escala)
            y1 = y_offset + int(min_y * escala)
            x2 = x_offset + int((max_x + 1) * escala)
            y2 = y_offset + int((max_y + 1) * escala)

            # -> Dibujar rectángulo verde
            self.canvas_binaria.create_rectangle(x1, y1, x2, y2, outline="green", width=10)

            # -> Dibujar texto del dígito en rojo
            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2

            # -> Ajustar posición del texto para evitar que se salga de la ventana
            texto_x = max(10, min(centro_x, canvas_width - 10))
            texto_y = max(15, min(centro_y, canvas_height - 15))

            self.canvas_binaria.create_text(texto_x, texto_y, text=str(digito),
                                          fill="blue", font=("Arial", 16, "bold"))

    def limpiar_imagen(self):
        """
        # Limpieza de imágenes
        % Limpia las imágenes mostradas y reinicia el estado
        """
        # -> Reiniciar variables
        self.imagen_original = None
        self.imagen_binaria = None
        self.regiones_detectadas = []

        # -> Limpiar canvas
        self.canvas_original.delete("all")
        self.canvas_binaria.delete("all")

        # -> Deshabilitar botón de procesar
        self.btn_procesar.config(state="disabled")

        self.status_var.set("Listo para cargar imagen")

    def procesar_imagen(self):
        """
        # Procesamiento de imagen
        % Procesa la imagen para reconocimiento de dígitos
        % Segmenta regiones y aplica reconocimiento
        """
        if self.imagen_binaria is None:
            return

        try:
            self.status_var.set("Procesando imagen...")
            self.root.update()

            # -> Segmentar regiones
            regiones = self.segmentar_regiones(self.imagen_binaria)

            if not regiones:
                self.status_var.set("No se detectaron regiones")
                return

            # ==> RECONOCIMIENTO DE DÍGITOS
            # -> Reconocer dígitos en cada región
            self.regiones_detectadas = []

            for i, region in enumerate(regiones):
                # -> Normalizar región
                region_normalizada = self.normalizar_region(region['matriz'])

                # -> Reconocer dígito
                digito, confianza = self.reconocer_digito(region_normalizada)

                # -> Guardar resultado
                region['digito'] = digito
                region['confianza'] = confianza
                self.regiones_detectadas.append(region)

            # -> Mostrar resultados
            self.mostrar_resultados_reconocimiento()

            # -> Actualizar barra de estado
            self.status_var.set(f"Procesamiento completado. {len(regiones)} regiones detectadas.")

        except Exception as e:
            self.status_var.set("Error en procesamiento")

def main():
    """
    ==> FUNCIÓN PRINCIPAL
    % Función principal que inicia la aplicación de reconocimiento
    """
    # -> Crear ventana principal
    root = tk.Tk()

    # -> Crear aplicación
    app = ReconocedorNumeros(root)

    # -> Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
