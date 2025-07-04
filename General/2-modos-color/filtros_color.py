"""
==> PROGRAMA DE FILTROS DE COLOR PARA IMÁGENES BMP
% Autor: Olvera Olvera Oliver Jesus
% Unidad de Aprendizaje: Visión por Computadora
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import struct
import os


class FiltrosColor:
		# ==> Sección de visualización (renderizado)
    def __init__(self, ventana_principal):
        """
        # Inicialización de la aplicación
        % Inicializa la aplicación de filtros de color
        $ ventana_principal: Ventana principal de tkinter
        """
        # ==> CONFIGURACIÓN DE VENTANA PRINCIPAL
        self.ventana = ventana_principal
        self.ventana.title("Filtros de Color - Procesamiento de Imágenes BMP")
        self.ventana.geometry("1000x700")
        self.ventana.resizable(True, True)

        # ==> VARIABLES DE ALMACENAMIENTO DE IMAGEN
        # -> Datos de la imagen
        self.imagen_original = None  # -> Datos originales de la imagen
        self.imagen_actual = None    # -> Imagen actualmente mostrada
        self.ruta_imagen = None      # -> Ruta del archivo de imagen
        self.ancho_imagen = 0        # -> Ancho en píxeles
        self.alto_imagen = 0         # -> Alto en píxeles
        self.imagen_tk = None        # -> Imagen PhotoImage para tkinter

        # -> Configurar la interfaz de usuario
        self.configurar_interfaz()

    def configurar_interfaz(self):
        """
        # Configuración de interfaz de usuario
        % Configura todos los elementos de la interfaz de usuario
        """
        # ==> FRAME PRINCIPAL
        frame_principal = ttk.Frame(self.ventana, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # -> Configurar el grid para que se redimensione
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(1, weight=1)

        # ==> PANELES DE LA INTERFAZ
        # -> Panel de controles (lado izquierdo)
        self.crear_panel_controles(frame_principal)

        # -> Panel de visualización (lado derecho)
        self.crear_panel_visualizacion(frame_principal)

        # -> Barra de estado
        self.crear_barra_estado(frame_principal)

    def crear_panel_controles(self, padre):
        """
        # Creación del panel de controles
        % Crea el panel de controles con botones para los filtros
        $ padre: Widget padre donde se colocará el panel
        """
        # ==> FRAME DE CONTROLES
        frame_controles = ttk.LabelFrame(padre, text="Controles de Filtros", padding="10")
        frame_controles.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # -> Botón para cargar imagen
        btn_cargar = ttk.Button(
            frame_controles,
            text="==> Cargar Imagen BMP",
            command=self.cargar_imagen,
            width=25
        )
        btn_cargar.pack(pady=5, fill=tk.X)

        # -> Separador
        ttk.Separator(frame_controles, orient='horizontal').pack(fill=tk.X, pady=10)

        # ==> BOTONES DE FILTROS
        # -> Etiqueta para filtros
        ttk.Label(frame_controles, text="Filtros Disponibles:", font=("Arial", 10, "bold")).pack(pady=(0, 5))

        # -> Botón para escala de grises
        btn_grises = ttk.Button(
            frame_controles,
            text="-> Escala de Grises",
            command=self.aplicar_escala_grises,
            width=25
        )
        btn_grises.pack(pady=2, fill=tk.X)

        # -> Botones para aislamiento de canales
        btn_canal_rojo = ttk.Button(
            frame_controles,
            text="-> Canal Rojo",
            command=self.aplicar_canal_rojo,
            width=25
        )
        btn_canal_rojo.pack(pady=2, fill=tk.X)

        btn_canal_verde = ttk.Button(
            frame_controles,
            text="-> Canal Verde",
            command=self.aplicar_canal_verde,
            width=25
        )
        btn_canal_verde.pack(pady=2, fill=tk.X)

        btn_canal_azul = ttk.Button(
            frame_controles,
            text="-> Canal Azul",
            command=self.aplicar_canal_azul,
            width=25
        )
        btn_canal_azul.pack(pady=2, fill=tk.X)

        # -> Botón para inversión de colores
        btn_inversion = ttk.Button(
            frame_controles,
            text="-> Inversión de Colores",
            command=self.aplicar_inversion_colores,
            width=25
        )
        btn_inversion.pack(pady=2, fill=tk.X)

        # -> Separador
        ttk.Separator(frame_controles, orient='horizontal').pack(fill=tk.X, pady=10)

        # -> Botón para restaurar imagen original
        btn_restaurar = ttk.Button(
            frame_controles,
            text="<-> Restaurar Original",
            command=self.restaurar_imagen_original,
            width=25
        )
        btn_restaurar.pack(pady=5, fill=tk.X)

        # ==> INFORMACIÓN DE LA IMAGEN
        self.frame_info = ttk.LabelFrame(frame_controles, text="Información de la Imagen", padding="5")
        self.frame_info.pack(fill=tk.X, pady=(10, 0))

        self.etiqueta_info = ttk.Label(self.frame_info, text="No hay imagen cargada")
        self.etiqueta_info.pack()

    def crear_panel_visualizacion(self, padre):
        """
        # Creación del panel de visualización
        % Crea el panel para visualizar la imagen
        $ padre: Widget padre donde se colocará el panel
        """
        # ==> FRAME DE VISUALIZACIÓN
        frame_visualizacion = ttk.LabelFrame(padre, text="Visualización de Imagen", padding="10")
        frame_visualizacion.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_visualizacion.columnconfigure(0, weight=1)
        frame_visualizacion.rowconfigure(0, weight=1)

        # -> Canvas con barras de desplazamiento
        self.canvas = tk.Canvas(frame_visualizacion, bg="white")
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # -> Barras de desplazamiento
        scroll_vertical = ttk.Scrollbar(frame_visualizacion, orient="vertical", command=self.canvas.yview)
        scroll_vertical.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=scroll_vertical.set)

        scroll_horizontal = ttk.Scrollbar(frame_visualizacion, orient="horizontal", command=self.canvas.xview)
        scroll_horizontal.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.canvas.configure(xscrollcommand=scroll_horizontal.set)

    def crear_barra_estado(self, padre):
        """
        # Creación de barra de estado
        % Crea la barra de estado en la parte inferior
        $ padre: Widget padre donde se colocará la barra
        """
        self.barra_estado = ttk.Label(
            padre,
            text="Listo para cargar imagen BMP",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.barra_estado.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def cargar_imagen(self):
        """
        # Carga de imagen BMP
        % Carga una imagen BMP desde el disco y la prepara para procesamiento
        % Solo acepta archivos BMP de 24 bits
        """
        try:
            # -> Abrir diálogo para seleccionar archivo
            ruta_archivo = filedialog.askopenfilename(
                title="Seleccionar imagen BMP",
                filetypes=[("Archivos BMP", "*.bmp"), ("Todos los archivos", "*.*")]
            )

            if not ruta_archivo:
                return

            # -> Verificar que el archivo existe
            if not os.path.exists(ruta_archivo):
                messagebox.showerror("Error", "El archivo seleccionado no existe.")
                return

            # -> Leer y validar el archivo BMP
            datos_imagen = self.leer_bmp(ruta_archivo)

            if datos_imagen is None:
                return

            # ==> ALMACENAMIENTO DE DATOS
            # -> Guardar datos de la imagen
            self.ruta_imagen = ruta_archivo
            self.imagen_original = datos_imagen.copy()
            self.imagen_actual = datos_imagen.copy()

            # -> Mostrar la imagen
            self.mostrar_imagen()

            # -> Actualizar información
            self.actualizar_informacion_imagen()
            self.barra_estado.config(text=f"Imagen cargada: {os.path.basename(ruta_archivo)}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")

    def leer_bmp(self, ruta_archivo):
        """
        # Lectura de archivo BMP
        % Lee un archivo BMP de 24 bits y extrae los datos de píxeles fila por fila
        $ ruta_archivo: Ruta al archivo BMP
        % Retornar: Matriz de píxeles en formato [R, G, B] para implementacion de filtros
        """
        try:
            with open(ruta_archivo, 'rb') as archivo:
                # ==> LECTURA Y VALIDACIÓN DEL HEADER BMP
                # -> Leer header BMP estándar
                header = archivo.read(54)  # -> Header BMP estándar

                if len(header) < 54:
                    raise ValueError("Archivo BMP demasiado pequeño o corrupto")

                # -> Verificar firma BMP
                if header[0:2] != b'BM':
                    raise ValueError("No es un archivo BMP válido (falta firma 'BM')")

                # ==> EXTRACCIÓN DE INFORMACIÓN DEL HEADER
                # -> Leer información del header
                tamano_archivo = struct.unpack('<I', header[2:6])[0]
                offset_datos = struct.unpack('<I', header[10:14])[0]
                tamano_header_info = struct.unpack('<I', header[14:18])[0]
                ancho = struct.unpack('<I', header[18:22])[0]
                alto = struct.unpack('<I', header[22:26])[0]
                planos = struct.unpack('<H', header[26:28])[0]
                bits_por_pixel = struct.unpack('<H', header[28:30])[0]
                compresion = struct.unpack('<I', header[30:34])[0]

                # ==> VALIDACIONES DEL FORMATO
                # -> Validar bits por píxel
                if bits_por_pixel != 24:
                    raise ValueError(f"Solo se soportan imágenes de 24 bits. Este archivo tiene {bits_por_pixel} bits por píxel")

                # -> Validar compresión
                if compresion != 0:
                    raise ValueError(f"Solo se soportan imágenes sin compresión. Este archivo tiene compresión tipo {compresion}")

                # -> Validar planos
                if planos != 1:
                    raise ValueError(f"Número de planos inválido: {planos}")

                # ==> INFORMACIÓN DE DEPURACIÓN
                # -> Información de depuración
                print(f"Información del BMP:")
                print(f"  - Tamaño: {ancho}x{alto} píxeles")
                print(f"  - Bits por píxel: {bits_por_pixel}")
                print(f"  - Tamaño archivo: {tamano_archivo} bytes")
                print(f"  - Offset datos: {offset_datos}")
                print(f"  - Compresión: {compresion}")

                # -> Actualizar información de la imagen
                self.ancho_imagen = ancho
                self.alto_imagen = alto

                # ==> CÁLCULO DE PADDING
                # -> Calcular padding (las filas deben ser múltiplos de 4 bytes)
                bytes_por_fila_sin_padding = ancho * 3
                padding = (4 - (bytes_por_fila_sin_padding % 4)) % 4
                bytes_por_fila_con_padding = bytes_por_fila_sin_padding + padding

                print(f"  - Bytes por fila (sin padding): {bytes_por_fila_sin_padding}")
                print(f"  - Padding: {padding}")
                print(f"  - Bytes por fila (con padding): {bytes_por_fila_con_padding}")

                # ==> LECTURA DE DATOS DE PÍXELES
                # -> Moverse al inicio de los datos de píxeles
                archivo.seek(offset_datos)

                # -> Leer todos los datos de píxeles
                datos_esperados = bytes_por_fila_con_padding * alto
                datos_crudos = archivo.read(datos_esperados)

                if len(datos_crudos) < datos_esperados:
                    print(f"Advertencia: Se esperaban {datos_esperados} bytes, pero solo se leyeron {len(datos_crudos)}")

                # -> Mostrar progreso de lectura
                self.barra_estado.config(text="Procesando datos de píxeles...")
                self.ventana.update_idletasks()

                # ==> CONVERSIÓN DE DATOS CRUDOS
                # -> Convertir datos crudos a matriz de píxeles
                matriz_pixeles = []

                # -> Los BMPs se almacenan desde abajo hacia arriba (fila inferior primero)
                for y in range(alto):
                    # -> Mostrar progreso cada 50 filas
                    if y % 50 == 0:
                        progreso = (y / alto) * 100
                        self.barra_estado.config(text=f"Leyendo fila {y+1}/{alto} ({progreso:.1f}%)")
                        self.ventana.update_idletasks()

                    fila_pixeles = []
                    # -> Calcular la posición de la fila (desde abajo hacia arriba)
                    posicion_fila = (alto - 1 - y) * bytes_por_fila_con_padding

                    for x in range(ancho):
                        # -> Calcular posición del píxel
                        posicion_pixel = posicion_fila + (x * 3)

                        # -> Verificar que no excedamos los datos disponibles
                        if posicion_pixel + 2 >= len(datos_crudos):
                            print(f"Error: Posición de píxel fuera de rango en ({x}, {y})")
                            # -> Usar píxel negro como fallback
                            fila_pixeles.append([0, 0, 0])
                            continue

                        # -> BMP almacena en formato BGR, convertir a RGB
                        b = datos_crudos[posicion_pixel]
                        g = datos_crudos[posicion_pixel + 1]
                        r = datos_crudos[posicion_pixel + 2]

                        fila_pixeles.append([r, g, b])

                    matriz_pixeles.append(fila_pixeles)

                print(f"Imagen BMP leída exitosamente: {len(matriz_pixeles)} filas x {len(matriz_pixeles[0]) if matriz_pixeles else 0} columnas")
                self.barra_estado.config(text=f"BMP cargado: {ancho}x{alto} píxeles")

                return matriz_pixeles

        except FileNotFoundError:
            raise FileNotFoundError(f"El archivo {ruta_archivo} no fue encontrado")
        except struct.error as e:
            raise ValueError(f"Error al leer el header del BMP: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al leer BMP: {str(e)}")

    def convertir_pixeles_a_photoimage(self, datos_pixeles):
        """
        # Conversión de píxeles a PhotoImage
        % Convierte una matriz de píxeles RGB a un objeto PhotoImage de tkinter
        % Utiliza método fila por fila para máxima compatibilidad
        $ datos_pixeles: Matriz de píxeles en formato [R, G, B]
        % Returns: Objeto PhotoImage de tkinter
        """
        try:
            # -> Crear PhotoImage
            imagen_photo = tk.PhotoImage(width=self.ancho_imagen, height=self.alto_imagen)

            # ==> CONVERSIÓN FILA POR FILA
            # -> Convertir píxeles fila por fila
            for y, fila in enumerate(datos_pixeles):
                # -> Mostrar progreso cada 10 filas
                if y % 10 == 0:
                    progreso = (y / self.alto_imagen) * 100
                    self.barra_estado.config(text=f"Renderizando imagen... {progreso:.1f}%")
                    self.ventana.update_idletasks()

                # -> Convertir la fila completa
                fila_colores = []
                for pixel in fila:
                    r, g, b = max(0, min(255, pixel[0])), max(0, min(255, pixel[1])), max(0, min(255, pixel[2]))
                    # -> Convertir RGB a formato hexadecimal (#RRGGBB)
                    color_hex = f"#{r:02x}{g:02x}{b:02x}"
                    fila_colores.append(color_hex)

                # -> Establecer la fila completa de píxeles
                if fila_colores:  # -> Solo si hay datos
                    imagen_photo.put("{" + " ".join(fila_colores) + "}", (0, y))

            return imagen_photo

        except Exception as e:
            messagebox.showerror("Error", f"Error al convertir píxeles: {str(e)}")
            return None

    def mostrar_imagen(self):
        """
        # Visualización de imagen
        % Convierte los datos de píxeles a PhotoImage y la muestra en el canvas
        % Versión mejorada con mejor feedback y manejo de errores
        """
        if self.imagen_actual is None:
            return

        try:
            # -> Mostrar mensaje de progreso
            self.barra_estado.config(text="Preparando visualización de imagen...")
            self.ventana.update_idletasks()

            # -> Verificar que tenemos datos válidos
            if not self.imagen_actual or len(self.imagen_actual) == 0:
                messagebox.showerror("Error", "No hay datos de imagen válidos para mostrar.")
                return

            # -> Convertir datos de píxeles a PhotoImage
            self.imagen_tk = self.convertir_pixeles_a_photoimage(self.imagen_actual)

            if self.imagen_tk is None:
                messagebox.showerror("Error", "No se pudo crear la imagen para visualización.")
                return

            # ==> ACTUALIZACIÓN DEL CANVAS
            # -> Limpiar canvas y mostrar imagen
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagen_tk)

            # -> Actualizar región de scroll
            self.canvas.configure(scrollregion=(0, 0, self.ancho_imagen, self.alto_imagen))

            # -> Mensaje de éxito
            self.barra_estado.config(text="Imagen mostrada correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar la imagen: {str(e)}")
            print(f"Error detallado: {e}")  # -> Para debugging

    def aplicar_escala_grises(self):
        """
        # Filtro de escala de grises
        % Aplica el filtro de escala de grises usando luminancia ponderada
        % Fórmula: gris = 0.3 * R + 0.59 * G + 0.11 * B
        """
        if self.imagen_original is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar una imagen.")
            return

        try:
            self.barra_estado.config(text="Aplicando filtro de escala de grises...")
            self.ventana.update()

            # -> Crear nueva imagen para el resultado
            imagen_grises = []

            # ==> PROCESAMIENTO PÍXEL A PÍXEL
            # -> Procesar cada píxel
            for fila in self.imagen_original:
                fila_grises = []
                for pixel in fila:
                    r, g, b = pixel[0], pixel[1], pixel[2]

                    # -> Aplicar fórmula de luminancia ponderada
                    valor_gris = int(0.3 * r + 0.59 * g + 0.11 * b)

                    # -> Asegurar que el valor esté en el rango válido (0-255)
                    valor_gris = max(0, min(255, valor_gris))

                    # -> Crear píxel gris (R=G=B=valor_gris)
                    fila_grises.append([valor_gris, valor_gris, valor_gris])

                imagen_grises.append(fila_grises)

            # -> Actualizar imagen actual y mostrar
            self.imagen_actual = imagen_grises
            self.mostrar_imagen()

            self.barra_estado.config(text="Filtro de escala de grises aplicado")

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar escala de grises: {str(e)}")

    def aplicar_canal_rojo(self):
        """
        # Filtro de canal rojo
        % Aplica el filtro de aislamiento del canal rojo
        % Mantiene solo el componente rojo: (R, 0, 0)
        """
        self.aplicar_aislamiento_canal('rojo', 0)

    def aplicar_canal_verde(self):
        """
        # Filtro de canal verde
        % Aplica el filtro de aislamiento del canal verde
        % Mantiene solo el componente verde: (0, G, 0)
        """
        self.aplicar_aislamiento_canal('verde', 1)

    def aplicar_canal_azul(self):
        """
        # Filtro de canal azul
        % Aplica el filtro de aislamiento del canal azul
        % Mantiene solo el componente azul: (0, 0, B)
        """
        self.aplicar_aislamiento_canal('azul', 2)

    def aplicar_aislamiento_canal(self, nombre_canal, indice_canal):
        """
        # Aislamiento de canal específico
        % Aplica el aislamiento de un canal específico de color
        $ nombre_canal: Nombre del canal para mostrar en mensajes
        $ indice_canal: Índice del canal (0=rojo, 1=verde, 2=azul)
        """
        if self.imagen_original is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar una imagen.")
            return

        try:
            self.barra_estado.config(text=f"Aplicando filtro de canal {nombre_canal}...")
            self.ventana.update()

            # -> Crear nueva imagen para el resultado
            imagen_canal = []

            # ==> PROCESAMIENTO DE CANAL
            # -> Procesar cada píxel
            for fila in self.imagen_original:
                fila_canal = []
                for pixel in fila:
                    # -> Crear nuevo píxel con solo el canal seleccionado
                    nuevo_pixel = [0, 0, 0]
                    nuevo_pixel[indice_canal] = pixel[indice_canal]
                    fila_canal.append(nuevo_pixel)

                imagen_canal.append(fila_canal)

            # -> Actualizar imagen actual y mostrar
            self.imagen_actual = imagen_canal
            self.mostrar_imagen()

            self.barra_estado.config(text=f"Filtro de canal {nombre_canal} aplicado")

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro de canal {nombre_canal}: {str(e)}")

    def aplicar_inversion_colores(self):
        """
        # Filtro de inversión de colores
        % Aplica el filtro de inversión de colores
        % Fórmula: R' = 255 - R, G' = 255 - G, B' = 255 - B
        """
        if self.imagen_original is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar una imagen.")
            return

        try:
            self.barra_estado.config(text="Aplicando inversión de colores...")
            self.ventana.update()

            # -> Crear nueva imagen para el resultado
            imagen_invertida = []

            # ==> PROCESAMIENTO DE INVERSIÓN
            # -> Procesar cada píxel
            for fila in self.imagen_original:
                fila_invertida = []
                for pixel in fila:
                    r, g, b = pixel[0], pixel[1], pixel[2]

                    # -> Aplicar inversión de colores
                    r_invertido = 255 - r
                    g_invertido = 255 - g
                    b_invertido = 255 - b

                    fila_invertida.append([r_invertido, g_invertido, b_invertido])

                imagen_invertida.append(fila_invertida)

            # -> Actualizar imagen actual y mostrar
            self.imagen_actual = imagen_invertida
            self.mostrar_imagen()

            self.barra_estado.config(text="Inversión de colores aplicada")

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar inversión de colores: {str(e)}")

    def restaurar_imagen_original(self):
        """
        # Restauración de imagen original
        % Restaura la imagen a su estado original, sin filtros aplicados
        """
        if self.imagen_original is None:
            messagebox.showwarning("Advertencia", "No hay imagen original para restaurar.")
            return

        try:
            # -> Restaurar imagen original
            self.imagen_actual = self.imagen_original.copy()
            self.mostrar_imagen()

            self.barra_estado.config(text="Imagen original restaurada")

        except Exception as e:
            messagebox.showerror("Error", f"Error al restaurar imagen original: {str(e)}")

    def actualizar_informacion_imagen(self):
        """
        # Actualización de información de imagen
        % Actualiza la información mostrada sobre la imagen actual
        """
        if self.imagen_original is None:
            self.etiqueta_info.config(text="No hay imagen cargada")
            return

        nombre_archivo = os.path.basename(self.ruta_imagen) if self.ruta_imagen else "Desconocido"
        texto_info = f"""Archivo: {nombre_archivo}
Dimensiones: {self.ancho_imagen} x {self.alto_imagen} píxeles
Formato: BMP 24 bits
Píxeles totales: {self.ancho_imagen * self.alto_imagen:,}"""

        self.etiqueta_info.config(text=texto_info)


def main():
    """
    ==> FUNCIÓN PRINCIPAL
    % Función principal que inicia la aplicación
    """
    # -> Crear ventana principal
    ventana_principal = tk.Tk()

    # -> Crear aplicación
    aplicacion = FiltrosColor(ventana_principal)

    # -> Iniciar bucle principal de la interfaz
    ventana_principal.mainloop()


if __name__ == "__main__":
    main()
