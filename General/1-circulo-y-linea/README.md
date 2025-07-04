# ==> CÍRCULO Y LÍNEA - GENERADOR DE FORMAS GEOMÉTRICAS

## ==> 📋 DESCRIPCIÓN DEL PROYECTO

% El programa **Círculo y Línea** es una aplicación gráfica interactiva que genera y muestra formas geométricas básicas (líneas y círculos) utilizando algoritmos clásicos de computación gráfica. La aplicación simula píxeles de baja resolución para crear un efecto visual retro mientras demuestra la implementación de los algoritmos de Bresenham para líneas y Midpoint Circle para círculos.

### -> Características principales:
- ✨ Generación aleatoria de 1-5 líneas y 1-5 círculos
- 🎨 Colores aleatorios para cada figura
- 🔄 Interfaz interactiva con botones de control
- 📐 Implementación de algoritmos gráficos clásicos
- 🎯 Simulación de píxeles grandes (8x8) para efecto retro
- 🏗️ Arquitectura modular y extensible

## ==> 🚀 INSTALACIÓN Y EJECUCIÓN

### -> Requisitos del Sistema
- **Python 3.6 o superior**
- **tkinter** (incluido por defecto en la mayoría de instalaciones de Python)

### -> Instrucciones de Instalación

1. **Clona o descarga el proyecto:**
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd circulo-y-linea
   ```

2. **Verifica que Python esté instalado:**
   ```bash
   python --version
   # o
   python3 --version
   ```

3. **Ejecuta el programa:**
   ```bash
   python main.py
   # o
   python3 main.py
   ```

## ==> 🎮 USO DEL PROGRAMA

### -> Interfaz de Usuario

La aplicación presenta una interfaz sencilla con los siguientes elementos:

1. **Canvas Principal (750x500 píxeles):** Área de dibujo donde aparecen las figuras
2. **Botón "Generar Nuevas Figuras":** Crea una nueva configuración aleatoria
3. **Botón "Limpiar Canvas":** Borra todas las figuras del área de dibujo
4. **Etiqueta Informativa:** Muestra el estado actual y número de figuras generadas

### -> Controles Básicos

- **Generar Figuras:** Haz clic en "Generar Nuevas Figuras" para crear líneas y círculos aleatorios
- **Limpiar:** Usa "Limpiar Canvas" para borrar todo y empezar de nuevo
- **Cerrar:** Cierra la ventana para salir del programa

## ==> 🔧 ESTRUCTURA DEL CÓDIGO

### -> Archivos Principales

```
circulo-y-linea/
├── main.py          # -> Programa principal con interfaz gráfica
├── algorithms.py    # -> Algoritmos de Bresenham y Midpoint Circle
├── config.py        # -> Configuraciones y constantes
└── README.md        # -> Esta documentación
```

### -> Arquitectura del Programa

#### 1. `main.py` - Programa Principal
```python
class CirculoYLinea:
    def __init__(self):           # -> Inicialización
    def setup_gui(self):          # -> Configuración de interfaz
    def draw_pixel(self, x, y):   # -> Dibuja píxeles grandes
    def generate_shapes(self):    # -> Genera figuras aleatorias
    def generate_random_line(self): # -> Crea líneas usando Bresenham
    def generate_random_circle(self): # -> Crea círculos usando Midpoint
```

#### 2. `algorithms.py` - Algoritmos Gráficos
```python
class BresenhamLine:
    def get_puntos_linea(self, x1, y1, x2, y2):  # -> Algoritmo de Bresenham

class MidpointCircle:
    def get_puntos_circulo(self, cx, cy, radius): # -> Algoritmo de Midpoint Circle
```

#### 3. `config.py` - Configuración
```python
class Config:
    # -> Dimensiones de ventana y canvas
    # -> Rangos de generación de figuras
    # -> Colores disponibles
    # -> Utilidades de validación
```

## ==> 🧮 ALGORITMOS IMPLEMENTADOS

### -> Algoritmo de Bresenham para Líneas

% El algoritmo de Bresenham es utilizado para dibujar líneas sin aliasing, calculando eficientemente qué píxeles deben ser activados.

**Principio de funcionamiento:**
1. Calcula las diferencias en X e Y entre los puntos inicial y final
2. Usa un error acumulativo para decidir cuándo moverse en cada eje
3. Genera todos los puntos de la línea de forma incremental

**Ventajas:**
- No usa operaciones de punto flotante
- Muy eficiente computacionalmente
- Produce líneas sin gaps

### -> Algoritmo de Midpoint Circle

% El algoritmo de Midpoint Circle dibuja círculos utilizando la simetría de 8 puntos para calcular solo un octavo del círculo.

**Principio de funcionamiento:**
1. Comienza en el punto (0, radio)
2. Usa una función de decisión para determinar el siguiente píxel
3. Aprovecha la simetría para dibujar 8 puntos simultáneamente

**Ventajas:**
- Evita operaciones trigonométricas costosas
- Solo usa aritmética entera
- Genera círculos perfectamente simétricos

## ==> ⚙️ CONFIGURACIÓN Y PERSONALIZACIÓN

### -> Modificar Parámetros Básicos

Edita el archivo `config.py` para personalizar el comportamiento:

```python
# -> Cambiar rango de figuras generadas
MIN_LINES = 1      # -> Nueva cantidad mínima de líneas
MAX_LINES = 8      # -> Nueva cantidad máxima de líneas

MIN_CIRCLES = 1    # -> Nueva cantidad mínima de círculos
MAX_CIRCLES = 8    # -> Nueva cantidad máxima de círculos

# -> Modificar tamaño de píxeles simulados
PIXEL_SIZE = 6     # -> Píxeles más pequeños para mayor detalle
PIXEL_SIZE = 12    # -> Píxeles más grandes para efecto más retro
```

### -> Agregar Nuevos Colores

```python
# -> En config.py, agregar colores a las listas
LINE_COLORS = [
    "#FF0000",  # -> Rojo
    "#00FF00",  # -> Verde
    "#YOUR_NEW_COLOR",  # -> Tu nuevo color
]
```

### -> Cambiar Dimensiones del Canvas

```python
# -> Modificar en config.py
CANVAS_WIDTH = 800   # -> Nuevo ancho
CANVAS_HEIGHT = 600  # -> Nueva altura

# -> Recalcular grilla automáticamente
GRID_WIDTH = CANVAS_WIDTH // PIXEL_SIZE
GRID_HEIGHT = CANVAS_HEIGHT // PIXEL_SIZE
```

## ==> 🛠️ MODIFICACIONES AVANZADAS

### -> Agregar Nuevas Formas

1. **Crear algoritmo en `algorithms.py`:**
```python
class TriangleAlgorithm:
    def get_triangle_points(self, x1, y1, x2, y2, x3, y3):
        # -> Implementar algoritmo para triángulos
        pass
```

2. **Integrar en `main.py`:**
```python
def generate_random_triangle(self):
    # -> Generar triángulo aleatorio
    triangle_algorithm = TriangleAlgorithm()
    points = triangle_algorithm.get_triangle_points(x1, y1, x2, y2, x3, y3)
    # -> Dibujar puntos
```

### -> Agregar Modo de Depuración

Activa el modo debug en `config.py`:
```python
DEBUG_MODE = True
SHOW_GRID = True
SHOW_COORDINATES = True
```

### -> Exportar Imágenes

Agregar funcionalidad para guardar el canvas:
```python
def save_canvas(self):
    # -> Implementar guardado como imagen
    pass
```

## ==> 🐛 RESOLUCIÓN DE PROBLEMAS

### -> Problemas Comunes

1. **Error: "No module named 'tkinter'"**
   - **Solución:** Instala tkinter con `sudo apt-get install python3-tk` (Linux) o reinstala Python con soporte completo

2. **Las figuras se salen del canvas**
   - **Causa:** Validación de límites incorrecta
   - **Solución:** Verifica las funciones de validación en `config.py`

3. **Rendimiento lento con muchas figuras**
   - **Solución:** Reduce el número máximo de figuras o aumenta `PIXEL_SIZE`

4. **Colores no se muestran correctamente**
   - **Solución:** Verifica que los códigos de color estén en formato hexadecimal válido

### -> Debugging

Para activar información de depuración:
```python
# -> En main.py, al inicio del programa
from config import Config
Config.print_config_info()  # -> Imprime configuración actual
```

## ==> 📚 CONCEPTOS TEÓRICOS

### -> Algoritmo de Bresenham
- **Inventor:** Jack Elton Bresenham (1965)
- **Propósito:** Dibujo eficiente de líneas en grillas discretas
- **Aplicaciones:** Gráficos por computadora, CAD, rasterización

### -> Algoritmo de Midpoint Circle
- **Base teórica:** Algoritmo de punto medio
- **Ventaja principal:** Evita cálculos de punto flotante
- **Aplicaciones:** Gráficos 2D, interfaces de usuario, videojuegos

### -> Rasterización
- **Definición:** Conversión de gráficos vectoriales a formato raster (píxeles)
- **Importancia:** Base de los gráficos por computadora modernos
- **Técnicas:** Antialiasing, subpixel rendering, filtrado

## ==> 🎯 EJERCICIOS SUGERIDOS

### -> Nivel Básico
1. Cambiar los colores por defecto de las figuras
2. Modificar el rango de círculos generados (1-3 en lugar de 1-5)
3. Aumentar el tamaño de los píxeles simulados

### -> Nivel Intermedio
1. Agregar un contador de figuras en pantalla
2. Implementar un botón para generar solo líneas o solo círculos
3. Agregar validación para evitar que los círculos se salgan del canvas

### -> Nivel Avanzado
1. Implementar el algoritmo de Wu para líneas con antialiasing
2. Agregar soporte para elipses usando el algoritmo de Midpoint
3. Crear un modo de animación que genere figuras automáticamente
4. Implementar guardado/carga de configuraciones

## ==> 🤝 CONTRIBUCIONES

Para contribuir al proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad: `git checkout -b nueva-funcionalidad`
3. Realiza tus cambios siguiendo las convenciones del código
4. Prueba tus modificaciones
5. Envía un pull request con descripción detallada

## ==> 📄 LICENCIA

Este proyecto está bajo la Licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

## ==> 👨‍💻 AUTOR

**[Tu Nombre]**
- Curso: Visión por Computadora
- Institución: [Tu Institución]
- Fecha: 2024

---

**¡Experimenta con el código y crea tus propias variaciones!** 🎨✨
