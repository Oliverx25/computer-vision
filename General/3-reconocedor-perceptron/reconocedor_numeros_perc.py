"""
==> RECONOCEDOR DE NÚMEROS - PERCEPTRÓN MULTICAPA
% Sistema de reconocimiento de dígitos basado en perceptrón multicapa
% Implementa backpropagation para entrenamiento automático de patrones
% Autor: Olvera Olvera Oliver Jesus
% Unidad de Aprendizaje: Visión por Computadora
% Versión: 1.0
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
import random
import math

class Perceptron:
    """
    ==> CLASE PERCEPTRÓN MULTICAPA
    % Implementación de un perceptrón multicapa para reconocimiento de dígitos
    % Incluye forward pass, backward pass y entrenamiento con backpropagation
    """

    def __init__(self, capas):
        """
        # Inicialización del perceptrón
        % Inicializa el perceptrón con la arquitectura especificada
        $ capas: Lista con el número de neuronas en cada capa
        """
        # ==> CONFIGURACIÓN DE ARQUITECTURA
        self.capas = capas
        self.pesos = []
        self.bias = []

        # -> Inicializar pesos y bias
        self.inicializar_pesos()

    def inicializar_pesos(self):
        """
        # Inicialización de pesos y bias
        % Inicializa los pesos y bias de forma aleatoria usando inicialización de Xavier
        """
        for i in range(len(self.capas) - 1):
            # ==> CÁLCULO DE LÍMITES DE INICIALIZACIÓN
            # -> Inicialización de Xavier para mejor convergencia
            limite = math.sqrt(2.0 / self.capas[i])

            # ==> CREACIÓN DE MATRIZ DE PESOS
            # -> Crear matriz de pesos
            # -> Para multiplicar: entrada (neuronas_entrada) * pesos (neuronas_entrada x neuronas_salida)
            w = []
            for fila in range(self.capas[i]):  # -> neuronas_capa_actual
                fila_pesos = []
                for col in range(self.capas[i + 1]):  # -> neuronas_capa_siguiente
                    fila_pesos.append(random.uniform(-limite, limite))
                w.append(fila_pesos)
            self.pesos.append(w)

            # ==> CREACIÓN DE VECTOR DE BIAS
            # -> Bias: vector de tamaño (neuronas_capa_siguiente,)
            b = []
            for j in range(self.capas[i + 1]):
                b.append(random.uniform(-0.1, 0.1))
            self.bias.append(b)

            print(f"Pesos capa {i}: {len(w)}x{len(w[0])} (de {self.capas[i]} a {self.capas[i+1]})")

    def sigmoid(self, x):
        """
        # Función de activación sigmoid
        % Función de activación sigmoid con límites para evitar overflow
        $ x: Valor de entrada
        % Returns: Valor de activación entre 0 y 1
        """
        # -> Limitar x para evitar overflow
        x = max(-500, min(500, x))
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivada(self, x):
        """
        # Derivada de función sigmoid
        % Calcula la derivada de la función sigmoid
        $ x: Valor de activación
        % Returns: Derivada de la función sigmoid
        """
        return x * (1 - x)

    def multiplicar_matrices(self, a, b):
        """
        # Multiplicación de matrices
        % Multiplica dos matrices (a * b)
        $ a, b: Matrices a multiplicar
        % Returns: Matriz resultado de la multiplicación
        """
        filas_a = len(a)
        cols_a = len(a[0])
        cols_b = len(b[0])

        resultado = []
        for i in range(filas_a):
            fila = []
            for j in range(cols_b):
                suma = 0
                for k in range(cols_a):
                    suma += a[i][k] * b[k][j]
                fila.append(suma)
            resultado.append(fila)

        return resultado

    def multiplicar_matriz_vector(self, matriz, vector):
        """
        # Multiplicación matriz por vector
        % Multiplica una matriz por un vector (matriz * vector)
        $ matriz: Matriz de entrada
        $ vector: Vector de entrada
        % Returns: Vector resultado
        """
        filas = len(matriz)
        cols = len(matriz[0])

        # -> Verificar que las dimensiones sean compatibles
        if len(vector) != cols:
            print(f"Error: matriz {filas}x{cols} no puede multiplicar vector de {len(vector)} elementos")
            return [0.0] * filas

        resultado = []
        for i in range(filas):
            suma = 0
            for j in range(cols):
                suma += matriz[i][j] * vector[j]
            resultado.append(suma)

        return resultado

    def multiplicar_vector_matriz(self, vector, matriz):
        """
        # Multiplicación vector por matriz
        % Multiplica un vector por una matriz (vector * matriz)
        $ vector: Vector de entrada
        $ matriz: Matriz de entrada
        % Returns: Vector resultado
        """
        filas = len(matriz)
        cols = len(matriz[0])

        # -> Verificar que las dimensiones sean compatibles
        if len(vector) != filas:
            print(f"Error: vector de {len(vector)} elementos no puede multiplicar matriz {filas}x{cols}")
            return [0.0] * cols

        resultado = []
        for j in range(cols):
            suma = 0
            for i in range(filas):
                suma += vector[i] * matriz[i][j]
            resultado.append(suma)

        return resultado

    def sumar_vectores(self, v1, v2):
        """
        # Suma de vectores
        % Suma dos vectores elemento por elemento
        $ v1, v2: Vectores a sumar
        % Returns: Vector resultado de la suma
        """
        return [v1[i] + v2[i] for i in range(len(v1))]

    def multiplicar_vectores(self, v1, v2):
        """
        # Multiplicación de vectores
        % Multiplica dos vectores elemento por elemento
        $ v1, v2: Vectores a multiplicar
        % Returns: Vector resultado de la multiplicación
        """
        return [v1[i] * v2[i] for i in range(len(v1))]

    def transponer_matriz(self, matriz):
        """
        # Transposición de matriz
        % Transpone una matriz
        $ matriz: Matriz a transponer
        % Returns: Matriz transpuesta
        """
        filas = len(matriz)
        cols = len(matriz[0])

        transpuesta = []
        for j in range(cols):
            fila = []
            for i in range(filas):
                fila.append(matriz[i][j])
            transpuesta.append(fila)

        return transpuesta

    def outer_product(self, v1, v2):
        """
        # Producto exterior
        % Producto exterior de dos vectores (v1 * v2^T)
        $ v1, v2: Vectores para el producto exterior
        % Returns: Matriz resultado del producto exterior
        """
        resultado = []
        for i in range(len(v1)):
            fila = []
            for j in range(len(v2)):
                fila.append(v1[i] * v2[j])
            resultado.append(fila)
        return resultado

    def forward(self, entrada):
        """
        # Propagación hacia adelante
        % Realiza la propagación hacia adelante en la red neuronal
        $ entrada: Vector de entrada
        % Returns: Vector de salida de la red
        """
        self.activaciones = [entrada]
        self.z_values = []

        for i in range(len(self.pesos)):
            # -> Debug: mostrar dimensiones
            print(f"Forward capa {i}: entrada={len(self.activaciones[-1])}, pesos={len(self.pesos[i])}x{len(self.pesos[i][0])}")

            # ==> CÁLCULO DE ACTIVACIÓN
            # -> Calcular z = a * W + b
            # -> Para la primera capa: entrada es un vector, pesos[i] es matriz (neuronas_entrada x neuronas_salida)
            # -> Necesitamos: vector * matriz = vector_resultado
            z = self.multiplicar_vector_matriz(self.activaciones[-1], self.pesos[i])
            z = self.sumar_vectores(z, self.bias[i])
            self.z_values.append(z)

            # -> Calcular activación
            a = [self.sigmoid(val) for val in z]
            self.activaciones.append(a)

        return self.activaciones[-1]

    def backward(self, entrada, salida_deseada, tasa_aprendizaje=0.1):
        """
        # Propagación hacia atrás
        % Realiza la propagación hacia atrás (backpropagation)
        $ entrada: Vector de entrada
        $ salida_deseada: Vector de salida deseada
        $ tasa_aprendizaje: Tasa de aprendizaje
        """
        # ==> CÁLCULO DE ERROR DE SALIDA
        # -> Calcular error de salida
        error = [salida_deseada[i] - self.activaciones[-1][i] for i in range(len(salida_deseada))]
        delta = self.multiplicar_vectores(error, [self.sigmoid_derivada(a) for a in self.activaciones[-1]])

        # -> Lista para almacenar los deltas de cada capa
        deltas = [delta]

        # ==> CÁLCULO DE DELTAS PARA CAPAS OCULTAS
        # -> Calcular deltas para capas ocultas
        for i in range(len(self.pesos) - 1, 0, -1):
            delta_anterior = deltas[0]
            pesos_transpuestos = self.transponer_matriz(self.pesos[i])
            print(f"Backward capa {i}: pesos_transpuestos={len(pesos_transpuestos)}x{len(pesos_transpuestos[0])}, delta_anterior={len(delta_anterior)}")
            # -> pesos_transpuestos: [neurona_salida][neurona_entrada]
            # -> delta_anterior: [neurona_salida]
            # -> resultado: [neurona_entrada]
            delta_propagado = self.multiplicar_vector_matriz(delta_anterior, pesos_transpuestos)
            print(f"  delta_propagado: {len(delta_propagado)}")
            # -> Multiplicar por derivada de sigmoid
            delta = self.multiplicar_vectores(delta_propagado,
                                            [self.sigmoid_derivada(a) for a in self.activaciones[i]])
            deltas.insert(0, delta)

        # ==> ACTUALIZACIÓN DE PESOS Y BIAS
        # -> Actualizar pesos y bias
        for i in range(len(self.pesos)):
            # -> Actualizar pesos: W += tasa_aprendizaje * activación * delta^T
            delta_outer = self.outer_product(self.activaciones[i], deltas[i])
            for fila in range(len(self.pesos[i])):
                for col in range(len(self.pesos[i][0])):
                    self.pesos[i][fila][col] += tasa_aprendizaje * delta_outer[fila][col]

            # -> Actualizar bias: b += tasa_aprendizaje * delta
            for j in range(len(self.bias[i])):
                self.bias[i][j] += tasa_aprendizaje * deltas[i][j]

    def entrenar(self, datos_entrenamiento, epocas=100, tasa_aprendizaje=0.1):
        """
        # Entrenamiento del perceptrón
        % Entrena el perceptrón con los datos proporcionados
        $ datos_entrenamiento: Lista de tuplas (entrada, salida_deseada)
        $ epocas: Número de épocas de entrenamiento
        $ tasa_aprendizaje: Tasa de aprendizaje
        """
        print(f"Iniciando entrenamiento con {len(datos_entrenamiento)} patrones")

        for epoca in range(epocas):
            error_total = 0
            patrones_procesados = 0

            for entrada, salida_deseada in datos_entrenamiento:
                try:
                    # ==> VALIDACIÓN DE DATOS
                    # -> Verificar que los datos sean válidos
                    if len(entrada) != self.capas[0]:
                        print(f"Error: entrada tiene {len(entrada)} elementos, esperaba {self.capas[0]}")
                        continue

                    if len(salida_deseada) != self.capas[-1]:
                        print(f"Error: salida tiene {len(salida_deseada)} elementos, esperaba {self.capas[-1]}")
                        continue

                    # ==> FORWARD Y BACKWARD PASS
                    # -> Forward pass (propagación hacia adelante)
                    salida = self.forward(entrada)

                    # -> Verificar que la salida sea válida
                    if len(salida) != len(salida_deseada):
                        print(f"Error: salida del forward tiene {len(salida)} elementos, esperaba {len(salida_deseada)}")
                        continue

                    # ==> BACKPROPAGATION - CLAVE PARA EL APRENDIZAJE
                    # -> Backward pass (propagación hacia atrás)
                    # -> SIN ESTA LÍNEA, los pesos nunca se actualizarían correctamente
                    self.backward(entrada, salida_deseada, tasa_aprendizaje)

                    # ==> CÁLCULO DE ERROR
                    # -> Calcular error
                    error = sum((salida_deseada[i] - salida[i]) ** 2 for i in range(len(salida))) / len(salida)
                    error_total += error
                    patrones_procesados += 1

                except Exception as e:
                    print(f"Error procesando patrón en época {epoca}: {e}")
                    continue

            # -> Mostrar progreso cada 10 épocas
            if epoca % 10 == 0 and patrones_procesados > 0:
                error_promedio = error_total / patrones_procesados
                print(f"Época {epoca}, Error promedio: {error_promedio:.6f}, Patrones procesados: {patrones_procesados}")

        print("Entrenamiento completado")

    def predecir(self, entrada):
        """
        # Predicción con perceptrón
        % Realiza una predicción con el perceptrón entrenado
        $ entrada: Vector de entrada
        % Returns: Vector de salida de la predicción
        """
        try:
            salida = self.forward(entrada)
            return salida
        except Exception as e:
            print(f"Error en predicción: {e}")
            return [0.0] * self.capas[-1]

class ReconocedorNumeros:
    """
    ==> CLASE PRINCIPAL - RECONOCEDOR CON PERCEPTRÓN
    % Clase principal para el reconocimiento de dígitos usando perceptrón multicapa
    % Integra procesamiento de imágenes con red neuronal para reconocimiento automático
    """

    def __init__(self, root):
        """
        # Inicialización del reconocedor con perceptrón
        % Inicializa la aplicación de reconocimiento de números con perceptrón
        $ root: Ventana principal de tkinter
        """
        # ==> CONFIGURACIÓN DE VENTANA PRINCIPAL
        self.root = root
        self.root.title("Reconocedor de Números - Perceptrón - Visión por Computadora")
        self.root.geometry("800x600")

        # ==> VARIABLES DE ESTADO
        # -> Datos de imagen
        self.imagen_original = None      # -> Imagen original cargada
        self.imagen_binaria = None       # -> Imagen binarizada
        self.regiones_detectadas = []    # -> Regiones detectadas en la imagen

        # ==> INICIALIZACIÓN DEL PERCEPTRÓN
        # -> Inicializar perceptrón
        # -> Arquitectura: 100 entradas (10x10 píxeles) -> 50 neuronas ocultas -> 10 salidas (dígitos 0-9)
        self.perceptron = Perceptron([100, 50, 10])
        self.entrenado = False

        # -> Configurar la interfaz
        self.configurar_interfaz()

        # -> Entrenar con el dataset al iniciar
        self.entrenar_con_dataset()

        # -> Actualizar información inicial del perceptrón
        self.actualizar_info_perceptron()

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
        titulo = ttk.Label(main_frame, text="Reconocedor de Números - Perceptrón",
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
        self.btn_procesar.grid(row=0, column=2, padx=(0, 10))

        # -> Botón reentrenar
        self.btn_reentrenar = ttk.Button(controles_frame, text="Reentrenar Perceptrón",
                                        command=self.reentrenar_perceptron)
        self.btn_reentrenar.grid(row=0, column=3)

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

        # ==> INFORMACIÓN DEL PERCEPTRÓN
        # -> Información del perceptrón
        self.info_perceptron = tk.StringVar()
        self.info_perceptron.set("Perceptrón: No entrenado")
        info_label = ttk.Label(main_frame, textvariable=self.info_perceptron,
                              font=("Arial", 10, "italic"))
        info_label.grid(row=4, column=0, columnspan=3, pady=(5, 0))

    def actualizar_info_perceptron(self):
        """
        # Actualización de información del perceptrón
        % Actualiza la información mostrada sobre el estado del perceptrón
        """
        if self.entrenado:
            self.info_perceptron.set("Perceptrón: Entrenado ✓ (Arquitectura: 100→50→10)")
        else:
            self.info_perceptron.set("Perceptrón: No entrenado ✗")

    def aplanar_matriz(self, matriz):
        """
        # Aplanamiento de matriz
        % Convierte una matriz 2D en un vector 1D
        $ matriz: Matriz de entrada
        % Returns: Vector aplanado
        """
        vector = []
        for fila in matriz:
            for elemento in fila:
                vector.append(float(elemento))
        return vector

    def crear_vector_entrada(self, patron_normalizado):
        """
        # Creación de vector de entrada
        % Convierte un patrón 10x10 en un vector de entrada de 100 elementos
        $ patron_normalizado: Patrón normalizado de 10x10
        % Returns: Vector de entrada para el perceptrón
        """
        return self.aplanar_matriz(patron_normalizado)

    def crear_vector_salida(self, digito):
        """
        # Creación de vector de salida
        % Crea un vector de salida one-hot para el dígito especificado
        $ digito: Dígito a codificar (0-9)
        % Returns: Vector one-hot de 10 elementos
        """
        vector = [0.0] * 10
        vector[digito] = 1.0
        return vector

    def mostrar_estadisticas_entrenamiento(self, datos_entrenamiento):
        """
        # Estadísticas de entrenamiento
        % Muestra estadísticas del entrenamiento
        $ datos_entrenamiento: Datos de entrenamiento utilizados
        """
        if not datos_entrenamiento:
            return

        # ==> ANÁLISIS DE DATOS
        # -> Contar patrones por dígito
        conteo_digitos = {}
        for entrada, salida in datos_entrenamiento:
            # -> Encontrar el índice del valor máximo (one-hot)
            digito = 0
            max_valor = salida[0]
            for i in range(1, len(salida)):
                if salida[i] > max_valor:
                    max_valor = salida[i]
                    digito = i
            conteo_digitos[digito] = conteo_digitos.get(digito, 0) + 1

        # -> Mostrar estadísticas
        print("\n=== ESTADÍSTICAS DE ENTRENAMIENTO ===")
        print(f"Total de patrones: {len(datos_entrenamiento)}")
        print("Patrones por dígito:")
        for digito in range(10):
            cantidad = conteo_digitos.get(digito, 0)
            print(f"  Dígito {digito}: {cantidad} patrones")
        print("=====================================\n")

    def entrenar_con_dataset(self):
        """
        # Entrenamiento con dataset
        % Entrena el perceptrón con el dataset de números
        % Carga patrones de cada dígito (0-9) desde archivos BMP
        """
        try:
            self.status_var.set("Entrenando perceptrón con dataset...")
            self.root.update()

            # -> Ruta del dataset
            dataset_path = os.path.join(os.path.dirname(__file__), "Numeros")
            print(f"Buscando dataset en: {dataset_path}")

            # ==> PREPARACIÓN DE DATOS DE ENTRENAMIENTO
            # -> Preparar datos de entrenamiento
            datos_entrenamiento = []
            total_imagenes = 0

            # -> Procesar cada carpeta de dígitos (0-9)
            for digito in range(10):
                carpeta_digito = os.path.join(dataset_path, str(digito))
                print(f"Procesando carpeta: {carpeta_digito}")

                if os.path.exists(carpeta_digito):
                    # -> Procesar cada imagen en la carpeta
                    archivos = [f for f in os.listdir(carpeta_digito) if f.endswith('.bmp')]
                    print(f"  Encontrados {len(archivos)} archivos BMP")

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
                                print(f"    {archivo}: {len(regiones)} regiones encontradas")

                                # -> Procesar cada región encontrada
                                for region in regiones:
                                    try:
                                        # -> Normalizar región a 10x10
                                        region_normalizada = self.normalizar_region(region['matriz'])

                                        # -> Crear vector de entrada
                                        entrada = self.crear_vector_entrada(region_normalizada)

                                        # -> Verificar que el vector de entrada tenga 100 elementos
                                        if len(entrada) != 100:
                                            print(f"      Error: vector de entrada tiene {len(entrada)} elementos, esperaba 100")
                                            continue

                                        # -> Crear vector de salida (one-hot)
                                        salida = self.crear_vector_salida(digito)

                                        # -> Verificar que el vector de salida tenga 10 elementos
                                        if len(salida) != 10:
                                            print(f"      Error: vector de salida tiene {len(salida)} elementos, esperaba 10")
                                            continue

                                        # -> Agregar a datos de entrenamiento
                                        datos_entrenamiento.append((entrada, salida))
                                        total_imagenes += 1

                                    except Exception as e:
                                        print(f"      Error procesando región: {e}")
                                        continue

                        except Exception as e:
                            print(f"Error procesando {ruta_imagen}: {e}")
                else:
                    print(f"  Carpeta no encontrada: {carpeta_digito}")

            print(f"Total de patrones recolectados: {len(datos_entrenamiento)}")

            if datos_entrenamiento:
                # ==> VERIFICACIÓN Y ENTRENAMIENTO
                # -> Verificar que los datos sean válidos antes de entrenar
                print("Verificando datos de entrenamiento...")
                entrada_ejemplo = datos_entrenamiento[0][0]
                salida_ejemplo = datos_entrenamiento[0][1]
                print(f"Ejemplo - Entrada: {len(entrada_ejemplo)} elementos, Salida: {len(salida_ejemplo)} elementos")

                # -> Entrenar el perceptrón
                print("Iniciando entrenamiento del perceptrón...")
                self.perceptron.entrenar(datos_entrenamiento, epocas=50, tasa_aprendizaje=0.1)
                self.entrenado = True
                self.status_var.set(f"Entrenamiento completado. {total_imagenes} patrones procesados.")
                self.actualizar_info_perceptron()
                self.mostrar_estadisticas_entrenamiento(datos_entrenamiento)
            else:
                print("No se encontraron datos de entrenamiento válidos")
                self.status_var.set("No se encontraron datos de entrenamiento.")
                self.actualizar_info_perceptron()

        except Exception as e:
            print(f"Error general en entrenamiento: {e}")
            import traceback
            traceback.print_exc()
            self.status_var.set("Error en entrenamiento")
            self.actualizar_info_perceptron()

    def reentrenar_perceptron(self):
        """
        # Reentrenamiento del perceptrón
        % Reentrena el perceptrón con el dataset
        """
        # -> Reinicializar perceptrón
        self.perceptron = Perceptron([100, 50, 10])
        self.entrenado = False
        self.actualizar_info_perceptron()

        # -> Entrenar nuevamente
        self.entrenar_con_dataset()

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

    def reconocer_digito(self, patron_normalizado):
        """
        # Reconocimiento de dígito con perceptrón
        % Reconoce un dígito usando el perceptrón entrenado
        $ patron_normalizado: Patrón normalizado de 10x10
        % Returns: (dígito reconocido, confianza)
        """
        if not self.entrenado:
            return -1, 0

        # -> Crear vector de entrada para el perceptrón
        entrada = self.crear_vector_entrada(patron_normalizado)

        # -> Predecir usando el perceptrón
        salida = self.perceptron.predecir(entrada)

        # ==> ANÁLISIS DE SALIDA
        # -> Obtener el dígito con mayor probabilidad
        digito_predicho = 0
        max_probabilidad = salida[0]
        for i in range(1, len(salida)):
            if salida[i] > max_probabilidad:
                max_probabilidad = salida[i]
                digito_predicho = i

        # -> Calcular confianza basada en la probabilidad máxima
        confianza = float(max_probabilidad * 100)

        return digito_predicho, confianza

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
        % Incluye rectángulos de colores según la confianza y dígitos reconocidos
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

            # ==> COLORES SEGÚN CONFIANZA
            # -> Color del rectángulo basado en la confianza
            if confianza > 80:
                color_rectangulo = "green"
            elif confianza > 60:
                color_rectangulo = "orange"
            else:
                color_rectangulo = "red"

            # -> Dibujar rectángulo
            self.canvas_binaria.create_rectangle(x1, y1, x2, y2,
                                               outline=color_rectangulo, width=8)

            # -> Dibujar solo el número predicho
            centro_x = (x1 + x2) // 2
            centro_y = (y1 + y2) // 2
            texto_x = max(10, min(centro_x, canvas_width - 10))
            texto_y = max(15, min(centro_y, canvas_height - 15))
            self.canvas_binaria.create_text(texto_x, texto_y, text=str(digito),
                                           fill="blue", font=("Arial", 16, "bold"),
                                           justify=tk.CENTER)

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
        self.actualizar_info_perceptron()

    def procesar_imagen(self):
        """
        # Procesamiento de imagen
        % Procesa la imagen para reconocimiento de dígitos usando el perceptrón
        % Segmenta regiones y aplica reconocimiento automático
        """
        if self.imagen_binaria is None:
            return

        if not self.entrenado:
            return

        try:
            self.status_var.set("Procesando imagen...")
            self.root.update()

            # -> Segmentar regiones
            regiones = self.segmentar_regiones(self.imagen_binaria)

            if not regiones:
                self.status_var.set("No se detectaron regiones")
                return

            # ==> RECONOCIMIENTO CON PERCEPTRÓN
            # -> Reconocer dígitos en cada región
            self.regiones_detectadas = []

            for i, region in enumerate(regiones):
                # -> Normalizar región
                region_normalizada = self.normalizar_region(region['matriz'])

                # -> Reconocer dígito usando el perceptrón
                digito_predicho, confianza = self.reconocer_digito(region_normalizada)

                # -> Guardar resultado
                region['digito'] = digito_predicho
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
    % Función principal que inicia la aplicación de reconocimiento con perceptrón
    """
    # -> Crear ventana principal
    root = tk.Tk()

    # -> Crear aplicación
    app = ReconocedorNumeros(root)

    # -> Iniciar bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()
