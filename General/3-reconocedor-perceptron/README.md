# Reconocedor de Números - Visión por Computadora

## Descripción General

Este programa implementa un sistema completo de reconocimiento de dígitos (0-9) utilizando técnicas de visión por computadora. El sistema puede cargar imágenes BMP de 24 bits, procesarlas y reconocer dígitos escritos a mano o impresos. **Todas las operaciones de procesamiento de imágenes se implementan manualmente sin usar librerías externas.**

## Características Principales

### 1. Carga y Visualización de Imagen
- **Formato soportado**: BMP de 24 bits (RGB)
- **Lectura**: Los píxeles se almacenan en un arreglo con valores RGB
- **Visualización**: Se renderiza en una ventana de 800x600 píxeles con escalado proporcional
- **Implementación**: Lectura manual del formato BMP sin librerías externas

### 2. Binarización
- **Conversión a escala de grises**: Se aplica la fórmula de luminancia ponderada:
  ```
  Gris = 0.3 × R + 0.59 × G + 0.11 × B
  ```
- **Umbral binario fijo**: 128
  - Gris < 128 → 1 (foreground / posible dígito)
  - Gris ≥ 128 → 0 (background)
- **Salida**: Matriz binaria 2D con valores 0 y 1
- **Implementación**: Algoritmo manual sin librerías de procesamiento

### 3. Entrenamiento con Dataset
- **Dataset**: Carpeta "Numeros" con 10 subcarpetas (0-9)
- **Cada subcarpeta**: Contiene múltiples imágenes BMP del dígito correspondiente
- **Proceso automático**: Al iniciar el programa, se cargan y procesan todas las imágenes del dataset
- **Segmentación**: Cada imagen del dataset se segmenta para extraer patrones individuales

### 4. Segmentación de Regiones
- **Algoritmo**: Búsqueda en anchura (BFS) implementado manualmente
- **Criterio**: Identifica regiones conectadas de píxeles con valor 1 (negros)
- **Conectividad**: 4 direcciones (arriba, abajo, izquierda, derecha)
- **Filtrado**: Se descartan regiones menores a 5x5 píxeles
- **Salida**: Matriz binaria de cada región con sus límites

### 5. Normalización
- **Reescalado**: Cada región se normaliza a matriz de 10x10 píxeles
- **Método**: Interpolación bilineal sobre la región original
- **Umbralización**: Se binariza con umbral 0.5 → valores 0 o 1
- **Objetivo**: Estandarizar entrada para comparación

### 6. Reconocimiento de Dígitos
- **Base de datos**: Patrones binarios 10x10 extraídos del dataset
- **Comparación**: Distancia de Hamming entre patrones
- **Selección**: Patrón con menor distancia como predicción
- **Confianza**: Calculada basada en la similitud

### 7. Visualización de Resultados
- **Imagen mostrada**: Versión binarizada (foreground negro, background blanco)
- **Rectángulos**: Dibujados en verde alrededor de cada región detectada
- **Texto**: Dígito reconocido mostrado en rojo, centrado sobre cada región
- **Ajuste automático**: Para evitar que los textos se salgan de la ventana

### 8. Interfaz de Usuario

#### Controles Disponibles:
- **Cargar Imagen BMP**: Permite seleccionar y cargar una imagen BMP
- **Limpiar**: Borra la imagen cargada y reinicia la interfaz
- **Procesar Imagen**: Realiza el reconocimiento completo de dígitos

#### Visualización:
- **Panel izquierdo**: Muestra la imagen original cargada
- **Panel derecho**: Muestra la imagen binarizada con resultados del reconocimiento
- **Barra de estado**: Informa sobre el estado actual del programa
- **Renderizado**: Implementado manualmente usando solo tkinter

## Estructura del Proyecto

```
3-reconocedor-numeros/
├── reconocedor_numeros.py    # Programa principal
├── README.md                 # Este archivo
└── Numeros/                  # Dataset de entrenamiento
    ├── 0/                    # Imágenes del dígito 0
    ├── 1/                    # Imágenes del dígito 1
    ├── 2/                    # Imágenes del dígito 2
    ├── 3/                    # Imágenes del dígito 3
    ├── 4/                    # Imágenes del dígito 4
    ├── 5/                    # Imágenes del dígito 5
    ├── 6/                    # Imágenes del dígito 6
    ├── 7/                    # Imágenes del dígito 7
    ├── 8/                    # Imágenes del dígito 8
    └── 9/                    # Imágenes del dígito 9
```

## Requisitos del Sistema

### Dependencias:
- **Python 3.7+**
- **tkinter** (incluido con Python)
- **numpy** para operaciones matemáticas básicas

### Instalación de dependencias:
```bash
pip install numpy
```

**Nota**: Ya no se requiere PIL/Pillow, ya que todas las operaciones de procesamiento de imágenes se implementan manualmente.

## Uso del Programa

### 1. Ejecutar el Programa
```bash
python reconocedor_numeros.py
```

### 2. Flujo de Trabajo
1. **Inicio**: El programa se inicia y automáticamente entrena con el dataset
2. **Cargar imagen**: Hacer clic en "Cargar Imagen BMP" y seleccionar una imagen
3. **Visualización**: La imagen original y binarizada se muestran en los paneles
4. **Procesamiento**: Hacer clic en "Procesar Imagen" para reconocer dígitos
5. **Resultados**: Los dígitos detectados se muestran con rectángulos verdes y texto rojo
6. **Limpieza**: Usar "Limpiar" para reiniciar y cargar una nueva imagen

### 3. Formato de Imagen Requerido
- **Tipo**: Archivo BMP
- **Profundidad de color**: 24 bits (RGB)
- **Contenido**: Imágenes que contengan dígitos escritos o impresos
- **Fondo**: Preferiblemente claro para mejor binarización

## Funciones Técnicas Implementadas

### Procesamiento de Imágenes (Implementación Manual)
- **`cargar_imagen_bmp()`**: Lee archivos BMP manualmente sin librerías externas
- **`convertir_a_grises()`**: Implementa luminancia ponderada manualmente
- **`binarizar()`**: Aplica umbral manualmente sin librerías de procesamiento

### Segmentación y Análisis
- **`segmentar_regiones()`**: Detecta regiones conectadas usando BFS
- **`bfs_region()`**: Implementa búsqueda en anchura para segmentación
- **`normalizar_region()`**: Normaliza regiones a 10x10 usando interpolación bilineal
- **`interpolacion_bilineal()`**: Realiza interpolación bilineal manualmente

### Reconocimiento
- **`calcular_distancia_hamming()`**: Calcula distancia de Hamming entre patrones
- **`reconocer_digito()`**: Reconoce dígitos comparando con patrones entrenados
- **`entrenar_con_dataset()`**: Carga y procesa todas las imágenes del dataset

### Interfaz Gráfica
- **`configurar_interfaz()`**: Crea todos los elementos de la interfaz
- **`mostrar_imagen_original()`**: Renderiza la imagen original usando solo tkinter
- **`mostrar_imagen_binaria()`**: Renderiza la imagen binaria usando solo tkinter
- **`mostrar_resultados_reconocimiento()`**: Muestra resultados con rectángulos y texto

## Algoritmos Implementados Manualmente

### 1. Luminancia Ponderada (Escala de Grises)
```python
# Fórmula implementada manualmente
gris = 0.3 * R + 0.59 * G + 0.11 * B
```

### 2. Binarización con Umbral
```python
# Algoritmo implementado manualmente
if gris < 128:
    pixel = 1  # Foreground
else:
    pixel = 0  # Background
```

### 3. BFS (Búsqueda en Anchura)
```python
# Implementación manual para segmentación de regiones
cola = deque([(x_inicial, y_inicial)])
while cola:
    x, y = cola.popleft()
    # Explorar vecinos en 4 direcciones
```

### 4. Interpolación Bilineal
```python
# Normalización de regiones a 10x10
valor = (v00 * (1-fx) * (1-fy) + v01 * fx * (1-fy) +
         v10 * (1-fx) * fy + v11 * fx * fy)
```

### 5. Distancia de Hamming
```python
# Comparación de patrones binarios
for y in range(10):
    for x in range(10):
        if patron1[y, x] != patron2[y, x]:
            distancia += 1
```

### 6. Renderizado de Imágenes
- **Escalado proporcional**: Calculado manualmente
- **Centrado**: Implementado manualmente
- **Dibujo de píxeles**: Usando solo tkinter Canvas

## Proceso de Reconocimiento Completo

### 1. **Entrenamiento**
- Carga todas las imágenes del dataset
- Segmenta cada imagen para extraer dígitos individuales
- Normaliza cada dígito a 10x10 píxeles
- Almacena patrones para cada dígito (0-9)

### 2. **Procesamiento de Nueva Imagen**
- Convierte imagen a escala de grises
- Binariza con umbral 128
- Segmenta regiones usando BFS
- Filtra regiones muy pequeñas (< 5x5)

### 3. **Reconocimiento**
- Normaliza cada región a 10x10
- Calcula distancia de Hamming con todos los patrones entrenados
- Selecciona el dígito con menor distancia
- Calcula nivel de confianza

### 4. **Visualización**
- Muestra imagen binarizada
- Dibuja rectángulos verdes alrededor de regiones detectadas
- Muestra dígitos reconocidos en rojo
- Ajusta posición de texto automáticamente

## Modificaciones y Personalización

### Ajustar Umbral de Binarización
```python
# En la función binarizar()
if imagen_gris[y, x] < 128:  # Cambiar este valor según la imagen
    imagen_binaria[y, x] = 1
else:
    imagen_binaria[y, x] = 0
```

### Modificar Filtro de Ruido
```python
# En la función segmentar_regiones()
if len(region['pixeles']) >= 25:  # Cambiar 25 para ajustar filtro
    regiones.append(region)
```

### Ajustar Tamaño de Normalización
```python
# En la función normalizar_region()
matriz_normalizada = np.zeros((10, 10), dtype=np.uint8)  # Cambiar tamaño
```

### Modificar Tamaño de Ventana
```python
# En __init__()
self.root.geometry("800x600")  # Cambiar dimensiones
```

### Agregar Nuevos Patrones
- Colocar nuevas imágenes BMP en las carpetas correspondientes del dataset
- Reiniciar el programa para recargar los patrones

## Ventajas de la Implementación Manual

### 1. **Sin Dependencias Externas**
- No requiere librerías de procesamiento de imágenes
- Solo usa numpy para operaciones matemáticas básicas
- Más fácil de distribuir y ejecutar

### 2. **Control Total**
- Implementación personalizada de algoritmos
- Fácil de modificar y optimizar
- Comprensión completa del proceso

### 3. **Educativo**
- Demuestra cómo funcionan los algoritmos internamente
- Ideal para aprendizaje de visión por computadora
- Código transparente y comprensible

### 4. **Reconocimiento Robusto**
- Usa múltiples patrones por dígito del dataset
- Comparación exhaustiva con todos los patrones
- Filtrado de ruido automático

## Solución de Problemas

### Error al Cargar Imagen
- Verificar que el archivo sea BMP de 24 bits
- Comprobar que la ruta del archivo sea válida
- Revisar permisos de lectura del archivo

### Imagen Binarizada Incorrecta
- Ajustar el umbral en la función `binarizar()`
- Verificar que la imagen tenga buen contraste
- Considerar preprocesamiento adicional

### No Se Detectan Regiones
- Verificar que la imagen contenga dígitos claros
- Ajustar el filtro de ruido (tamaño mínimo de región)
- Revisar la binarización

### Reconocimiento Incorrecto
- Verificar que el dataset contenga patrones variados
- Ajustar el umbral de normalización (0.5)
- Considerar agregar más patrones al dataset

### Problemas de Rendimiento
- Reducir el tamaño de las imágenes del dataset
- Optimizar el procesamiento de patrones
- Considerar optimizaciones en los bucles de procesamiento

## Notas de Desarrollo

- El programa está diseñado para ser modular y fácil de modificar
- Cada función tiene una responsabilidad específica
- Los comentarios en el código explican la lógica implementada
- La interfaz se puede personalizar fácilmente modificando `configurar_interfaz()`
- **Todas las operaciones de procesamiento de imágenes son manuales**
- **El reconocimiento usa el dataset completo para mayor precisión**

## Autor y Licencia

Desarrollado para el curso de Visión por Computadora en ESCOM.
