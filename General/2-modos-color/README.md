# Programa de Filtros de Color para Imágenes BMP

## Descripción General

Este programa permite cargar y manipular imágenes en formato BMP de 24 bits, aplicando diferentes filtros de color mediante procesamiento píxel a píxel. Está desarrollado completamente en Python utilizando solo las librerías estándar `tkinter`, `tk` y `ttk`, sin dependencias externas.

## Características Principales

### ✅ Filtros Implementados

1. **Escala de Grises (Luminancia Ponderada)**
   - Fórmula: `gris = 0.3 * R + 0.59 * G + 0.11 * B`
   - Convierte la imagen a tonos de gris preservando la percepción visual humana

2. **Aislamiento de Canales RGB**
   - **Canal Rojo**: Muestra solo el componente rojo `(R, 0, 0)`
   - **Canal Verde**: Muestra solo el componente verde `(0, G, 0)`
   - **Canal Azul**: Muestra solo el componente azul `(0, 0, B)`

3. **Inversión de Colores**
   - Fórmula: `R' = 255 - R`, `G' = 255 - G`, `B' = 255 - B`
   - Crea un efecto de negativo fotográfico

4. **Restauración de Imagen Original**
   - Permite volver al estado original de la imagen sin filtros

### 🔧 Características Técnicas

- **Formato soportado**: BMP de 24 bits sin compresión
- **Procesamiento**: Píxel a píxel (sin librerías externas)
- **Lectura BMP**: Implementación completa del parser de archivos BMP
- **Interfaz**: Interfaz gráfica intuitiva con tkinter
- **Visualización**: Canvas con barras de desplazamiento para imágenes grandes

## Instalación y Requisitos

### Requisitos del Sistema
- Python 3.6 o superior
- tkinter (incluido en la mayoría de instalaciones de Python)

### Sin Dependencias Externas
El programa no requiere instalación de paquetes adicionales ya que utiliza solo librerías estándar de Python.

## Uso del Programa

### Ejecución
```bash
python filtros_color.py
```

### Interfaz de Usuario

#### Panel de Controles (Izquierda)
1. **📁 Cargar Imagen BMP**: Abre un diálogo para seleccionar archivos BMP
2. **Filtros Disponibles**:
   - **⚫ Escala de Grises**: Aplica conversión a grises
   - **🔴 Canal Rojo**: Aislamiento del canal rojo
   - **🟢 Canal Verde**: Aislamiento del canal verde
   - **🔵 Canal Azul**: Aislamiento del canal azul
   - **🔄 Inversión de Colores**: Aplica inversión de colores
3. **↻ Restaurar Original**: Vuelve a la imagen original
4. **Información de la Imagen**: Muestra datos del archivo cargado

#### Panel de Visualización (Derecha)
- Canvas principal para mostrar la imagen
- Barras de desplazamiento para imágenes grandes
- Barra de estado con información del proceso actual

## Arquitectura del Programa

### Estructura de Clases

#### `FiltrosColor` (Clase Principal)
Maneja toda la funcionalidad del programa:

**Métodos Principales:**
- `configurar_interfaz()`: Configura la interfaz gráfica
- `cargar_imagen()`: Gestiona la carga de archivos BMP
- `leer_archivo_bmp()`: Parser completo de archivos BMP
- `mostrar_imagen()`: Visualización de imágenes en tkinter
- `aplicar_*()`: Métodos para aplicar cada filtro

### Procesamiento de Imágenes BMP

#### Lectura de Archivos BMP
El programa implementa un parser completo de BMP que:

1. **Valida el encabezado del archivo** (14 bytes)
   ```python
   # Verificar firma BMP
   if firma != b'BM':
       return None
   ```

2. **Lee el encabezado de información** (40 bytes)
   - Extrae dimensiones (ancho × alto)
   - Verifica que sea 24 bits por píxel
   - Confirma que no tenga compresión

3. **Procesa los datos de píxeles**
   - Maneja el formato BGR → RGB
   - Gestiona el padding de filas (múltiplos de 4 bytes)
   - Invierte las filas (BMP se almacena volteado)

#### Estructura de Datos
```python
# Formato de almacenamiento interno
imagen_datos = [
    [[R, G, B], [R, G, B], ...],  # Fila 1
    [[R, G, B], [R, G, B], ...],  # Fila 2
    ...
]
```

### Algoritmos de Filtros

#### 1. Escala de Grises
```python
def aplicar_escala_grises(self):
    for fila in self.imagen_original:
        for pixel in fila:
            r, g, b = pixel[0], pixel[1], pixel[2]
            # Luminancia ponderada
            valor_gris = int(0.3 * r + 0.59 * g + 0.11 * b)
            nuevo_pixel = [valor_gris, valor_gris, valor_gris]
```

**¿Por qué estos coeficientes?**
- 0.3 para Rojo: El ojo humano es menos sensible al rojo
- 0.59 para Verde: El ojo es más sensible al verde
- 0.11 para Azul: El ojo es menos sensible al azul

#### 2. Aislamiento de Canales
```python
def aplicar_aislamiento_canal(self, nombre_canal, indice_canal):
    for fila in self.imagen_original:
        for pixel in fila:
            nuevo_pixel = [0, 0, 0]
            nuevo_pixel[indice_canal] = pixel[indice_canal]
```

**Resultado visual:**
- Canal Rojo: Imagen con tonos rojizos
- Canal Verde: Imagen con tonos verdosos
- Canal Azul: Imagen con tonos azulados

#### 3. Inversión de Colores
```python
def aplicar_inversion_colores(self):
    for fila in self.imagen_original:
        for pixel in fila:
            r, g, b = pixel[0], pixel[1], pixel[2]
            r_invertido = 255 - r
            g_invertido = 255 - g
            b_invertido = 255 - b
```

### Visualización con tkinter

#### Conversión a PhotoImage
```python
def convertir_pixeles_a_photoimage(self, datos_pixeles):
    imagen_photo = tk.PhotoImage(width=self.ancho_imagen, height=self.alto_imagen)
    for y, fila in enumerate(datos_pixeles):
        fila_datos = []
        for pixel in fila:
            r, g, b = pixel[0], pixel[1], pixel[2]
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            fila_datos.append(color_hex)
        imagen_photo.put(" ".join(fila_datos), (0, y))
```

## Modificaciones en Tiempo Real

### Para agregar un nuevo filtro:

1. **Crear el método del filtro**:
```python
def aplicar_mi_filtro(self):
    if self.imagen_original is None:
        messagebox.showwarning("Advertencia", "Primero debe cargar una imagen.")
        return

    try:
        self.barra_estado.config(text="Aplicando mi filtro...")
        self.ventana.update()

        imagen_filtrada = []
        for fila in self.imagen_original:
            fila_filtrada = []
            for pixel in fila:
                r, g, b = pixel[0], pixel[1], pixel[2]

                # AQUÍ VA TU ALGORITMO
                nuevo_r = # tu transformación
                nuevo_g = # tu transformación
                nuevo_b = # tu transformación

                fila_filtrada.append([nuevo_r, nuevo_g, nuevo_b])
            imagen_filtrada.append(fila_filtrada)

        self.imagen_actual = imagen_filtrada
        self.mostrar_imagen()
        self.barra_estado.config(text="Mi filtro aplicado")

    except Exception as e:
        messagebox.showerror("Error", f"Error al aplicar mi filtro: {str(e)}")
```

2. **Agregar el botón en la interfaz** (en `crear_panel_controles`):
```python
btn_mi_filtro = ttk.Button(
    frame_controles,
    text="✨ Mi Filtro",
    command=self.aplicar_mi_filtro,
    width=25
)
btn_mi_filtro.pack(pady=2, fill=tk.X)
```

### Ejemplos de filtros adicionales:

#### Filtro Sepia
```python
# En aplicar_mi_filtro():
sepia_r = min(255, int(0.393 * r + 0.769 * g + 0.189 * b))
sepia_g = min(255, int(0.349 * r + 0.686 * g + 0.168 * b))
sepia_b = min(255, int(0.272 * r + 0.534 * g + 0.131 * b))
```

#### Filtro de Brillo
```python
# En aplicar_mi_filtro():
factor_brillo = 50  # Ajustar según necesidad
nuevo_r = max(0, min(255, r + factor_brillo))
nuevo_g = max(0, min(255, g + factor_brillo))
nuevo_b = max(0, min(255, b + factor_brillo))
```

#### Filtro de Contraste
```python
# En aplicar_mi_filtro():
factor_contraste = 1.5  # Ajustar según necesidad
nuevo_r = max(0, min(255, int((r - 128) * factor_contraste + 128)))
nuevo_g = max(0, min(255, int((g - 128) * factor_contraste + 128)))
nuevo_b = max(0, min(255, int((b - 128) * factor_contraste + 128)))
```

## Solución de Problemas

### Errores Comunes

1. **"Solo se admiten imágenes BMP de 24 bits"**
   - Usar un editor de imágenes para convertir a BMP 24 bits
   - Verificar que el archivo no esté comprimido

2. **"El archivo no es un BMP válido"**
   - Verificar la extensión del archivo
   - Asegurar que el archivo no esté corrupto

3. **Imagen no se muestra correctamente**
   - Verificar que el archivo BMP esté en formato estándar
   - Comprobar que las dimensiones sean válidas

### Limitaciones

- Solo soporta archivos BMP de 24 bits sin compresión
- Para imágenes muy grandes, el procesamiento puede ser lento
- La conversión a PhotoImage puede consumir memoria con imágenes grandes

## Estructura de Archivos

```
2-modos-color/
├── filtros_color.py    # Programa principal
├── README.md          # Este archivo de documentación
└── 2do programa.txt   # Especificaciones originales
```

## Conclusión

Este programa demuestra el procesamiento de imágenes a bajo nivel, implementando desde cero la lectura de archivos BMP y la aplicación de filtros píxel a píxel. Es ideal para entender los fundamentos del procesamiento de imágenes y como base para implementar filtros más complejos.

La arquitectura modular permite agregar fácilmente nuevos filtros siguiendo el patrón establecido, mientras que la interfaz intuitiva facilita la experimentación con diferentes efectos visuales.
