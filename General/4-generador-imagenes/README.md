# Generador de Imágenes Sintéticas - Texturas

## 📋 Descripción General

Este proyecto implementa un **generador de imágenes sintéticas** que crea nuevas imágenes preservando las texturas y patrones locales de una imagen BMP original. El sistema utiliza un proceso de **síntesis de texturas basada en parches** y una **matriz evolutiva** que refina la imagen a través de múltiples iteraciones.

## 🎯 Objetivo Principal

Crear una imagen nueva (sintética) a partir de una imagen BMP de 24 bits, preservando sus texturas y patrones locales mediante un proceso de síntesis de texturas basada en parches. Todo se controla desde una interfaz gráfica con botones para cargar y generar la imagen.

## 🔧 Componentes del Sistema

### 1. 🖼 Carga de Imagen BMP
- **Lectura del encabezado**: Lee los primeros 54 bytes del archivo BMP
- **Validación**: Verifica que sea un archivo BMP válido ("BM", 24 bits)
- **Extracción de datos**:
  - Dimensiones de la imagen
  - Datos RGB por píxel, fila por fila
  - Aplicación de padding para alinear cada fila a múltiplos de 4 bytes
- **Validación de límites**: Dimensiones no exceden 10000 x 10000
- **Corrección de orientación**: Las imágenes BMP se almacenan de abajo hacia arriba, se corrige automáticamente

### 2. 🧩 Extracción de Parches (5x5) - **MATRIZ EVOLUTIVA FASE 1**
- **Selección aleatoria**: Extrae el 10% de los posibles parches 5x5
- **Generador Mersenne Twister**: Para aleatoriedad reproducible
- **Cuantización de colores**: Reduce complejidad agrupando colores similares
- **Almacenamiento**: Cada parche contiene los 25 valores RGB cuantizados junto con sus coordenadas centrales

### 3. 🎲 Cálculo de Probabilidades de Transición (Respaldo)
- **Análisis de transiciones**: Cómo cambia el color entre píxeles vecinos
- **Mapa de pares**: Crea un mapa de pares de colores (actual, vecino)
- **Conteo de ocurrencias**: Cuenta las transiciones más frecuentes
- **Distribución acumulada**: Para muestreo probabilístico
- **Uso como respaldo**: Solo si no se puede aplicar el método principal de parches

### 4. 🧪 Síntesis de Imagen - **MATRIZ EVOLUTIVA FASE 2**

#### 4.1 Inicialización
- **Copia de imagen original**: Como base para la generación
- **Ruido gaussiano**: Se aplica a cada canal RGB (media = 0, σ = 5)

#### 4.2 Iteración de Refinamiento (Configurable) - **MATRIZ EVOLUTIVA FASE 3**
Para cada píxel (excepto bordes):
1. **Extracción de parche**: Se toma un parche 5x5 centrado en el píxel actual
2. **Cálculo de distancia**: Distancia euclidiana al cuadrado entre el parche actual y todos los parches originales
3. **Selección del mejor**: Se selecciona el parche más similar (menor distancia)
4. **Asignación de color**: Se toma el color del centro de ese parche original y se asigna al píxel actual

### 5. 🖥️ Interfaz Gráfica
- **Visualización dual**: Muestra la imagen original y la generada lado a lado
- **Escalado uniforme**: Ambas imágenes se escalan para ajustarse al área de visualización
- **Etiquetas informativas**: "Imagen Original" y "Imagen Generada"
- **Actualización en tiempo real**: La imagen generada se actualiza durante el proceso
- **Renderizado por filas**: Implementado mediante análisis píxel por píxel sin librerías externas
- **Control de iteraciones**: Campo de entrada para configurar el número de iteraciones (1-100)

## 🧭 Flujo del Algoritmo

```
[Seleccionar BMP]
        ↓
[Cargar y validar imagen BMP]
        ↓
[Configurar número de iteraciones]
        ↓
[Extraer parches aleatorios (5x5)] ← MATRIZ EVOLUTIVA FASE 1
        ↓
[Calcular modelo de transición de color (opcional)]
        ↓
[Inicializar imagen generada con ruido] ← MATRIZ EVOLUTIVA FASE 2
        ↓
[Iterar N veces: comparar parches, seleccionar mejor, refinar píxel] ← MATRIZ EVOLUTIVA FASE 3
        ↓
[Mostrar imagen original + generada]
```

## 🔬 Concepto de "Matriz Evolutiva"

El sistema implementa una **matriz evolutiva** que evoluciona la imagen a través de tres fases principales:

### Fase 1: Extracción de Conocimiento
- **Análisis de patrones**: Extrae parches representativos de la imagen original
- **Cuantización**: Reduce la complejidad del espacio de colores
- **Base de conocimiento**: Crea una biblioteca de texturas locales

### Fase 2: Inicialización Evolutiva
- **Estado inicial**: Copia la imagen original con ruido gaussiano
- **Preparación**: Prepara la matriz para el proceso evolutivo
- **Condiciones iniciales**: Establece el punto de partida para la evolución

### Fase 3: Refinamiento Evolutivo
- **Iteraciones configurables**: Número de ciclos ajustable por el usuario (1-100)
- **Selección natural**: En cada iteración, cada píxel "evoluciona" hacia el patrón más similar
- **Convergencia**: La imagen converge hacia una versión sintética que preserva las texturas originales

## 📊 Características Técnicas

### Parámetros del Sistema
- **Tamaño de parches**: 5x5 píxeles
- **Porcentaje de extracción**: 10% de los parches posibles
- **Cuantización de colores**: Agrupación en bloques de 32 niveles
- **Número de iteraciones**: Configurable por el usuario (1-100, por defecto 20)
- **Ruido gaussiano**: Media = 0, Desviación estándar = 5

### Limitaciones
- **Formato de entrada**: Solo archivos BMP de 24 bits
- **Dimensiones máximas**: 10000 x 10000 píxeles
- **Memoria**: El procesamiento puede ser intensivo para imágenes grandes
- **Iteraciones**: Máximo 100 para evitar tiempos de procesamiento excesivos

## 🚀 Instalación y Uso

### Requisitos
```bash
# No se requieren librerías externas
# Solo Python 3.7 o superior con tkinter incluido
```

### Ejecución
```bash
python generador_imagenes.py
```

### Instrucciones de Uso
1. **Cargar imagen**: Hacer clic en "Cargar Imagen BMP" y seleccionar un archivo BMP
2. **Configurar iteraciones**: Ajustar el número de iteraciones en el campo de entrada (1-100)
3. **Generar sintética**: Hacer clic en "Generar Imagen Sintética"
4. **Observar proceso**: El sistema mostrará el progreso en la barra de estado
5. **Resultado**: La imagen sintética aparecerá en el panel derecho

## 🔍 Análisis del Código

### Estructura de Comentarios
El código utiliza un sistema de comentarios especializado:
- `// *` - Comentario de finalización de solución
- `// !` - Comentario de correcciones
- `// @` - Comentario de mención
- `// [ ]` - Comentario de pendiente
- `// [x]` - Comentario de realizado
- `// #` - Comentario de sección de funcionalidad
- `// $` - Comentario de parámetros
- `// %` - Comentario de información y ejemplos
- `// ?` - Comentario de pregunta
- `// ==>` - Comentario de seccionamiento
- `// ->` - Comentario de subseccionamiento
- `// +>` - Comentario de seccionamiento a eliminar

### Variables en Español
Todas las variables están declaradas en español para mayor comprensión:
- `imagen_original`, `datos_imagen_original`, `dimensiones_imagen`
- `parches_extraidos`, `modelo_transicion`, `imagen_generada`
- `ancho`, `alto`, `iteracion`, `distancia_total`
- `numero_iteraciones`, `entrada_iteraciones`

## 🎨 Características de la Interfaz

### Diseño Visual
- **Tema oscuro**: Fondo azul oscuro (#2c3e50)
- **Controles destacados**: Botones con colores distintivos
- **Layout responsivo**: Se adapta al tamaño de la ventana
- **Feedback visual**: Barra de estado con información del progreso

### Funcionalidades
- **Carga de archivos**: Selector de archivos BMP
- **Control de iteraciones**: Campo de entrada para configurar el número de iteraciones
- **Visualización dual**: Imagen original y generada
- **Escalado automático**: Las imágenes se ajustan al área disponible
- **Actualización en tiempo real**: Progreso visible durante la generación
- **Renderizado nativo**: Sin dependencias externas, solo tkinter

## 🔬 Algoritmo de Síntesis Detallado

### 1. Análisis de Texturas
```python
# Extracción de parches 5x5 con cuantización
parche = []
for dy in range(-2, 3):
    for dx in range(-2, 3):
        r, g, b = datos_imagen[y + dy][x + dx]
        r_cuantizado = (r // 32) * 32
        g_cuantizado = (g // 32) * 32
        b_cuantizado = (b // 32) * 32
```

### 2. Cálculo de Similitud
```python
# Distancia euclidiana al cuadrado entre parches
distancia_total = 0
for y in range(5):
    for x in range(5):
        dr = (r1 - r2) ** 2
        dg = (g1 - g2) ** 2
        db = (b1 - b2) ** 2
        distancia_total += dr + dg + db
```

### 3. Refinamiento Evolutivo Configurable
```python
# Para cada píxel, encontrar el parche más similar
for iteracion in range(numero_iteraciones):
    for y in range(2, alto - 2):
        for x in range(2, ancho - 2):
            parche_actual = extraer_parche_5x5(imagen_actual, x, y)
            mejor_parche = encontrar_parche_mas_similar(parche_actual, parches)
            color_centro = obtener_color_centro_parche(mejor_parche)
            imagen_actual[y][x] = color_centro
```

### 4. Renderizado por Filas
```python
# Renderizado nativo sin librerías externas
for y in range(alto):
    for x in range(ancho):
        r, g, b = imagen[y][x]
        color = f"#{r:02x}{g:02x}{b:02x}"
        # Dibujar píxel escalado en canvas
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)
```

### 5. Corrección de Orientación BMP
```python
# BMP se almacena de abajo hacia arriba, necesitamos invertir
for fila in range(alto - 1, -1, -1):  # Leer de abajo hacia arriba
    for columna in range(ancho):
        # Procesar píxeles en orden correcto
```

## 📈 Resultados Esperados

### Calidad de Síntesis
- **Preservación de texturas**: Las texturas locales se mantienen
- **Variación natural**: Cada generación produce resultados ligeramente diferentes
- **Convergencia**: Después de N iteraciones, la imagen converge a un estado estable
- **Orientación correcta**: Las imágenes se muestran en la orientación correcta

### Limitaciones
- **Tiempo de procesamiento**: Puede ser lento para imágenes grandes o muchas iteraciones
- **Memoria**: Requiere almacenar múltiples copias de la imagen
- **Calidad**: Depende de la riqueza de texturas en la imagen original

## 🔧 Posibles Mejoras

### Optimizaciones
- **Paralelización**: Procesar múltiples píxeles simultáneamente
- **Estructuras de datos**: Usar árboles k-d para búsqueda más rápida
- **Compresión**: Reducir el uso de memoria

### Funcionalidades Adicionales
- **Múltiples tamaños de parche**: Permitir diferentes tamaños (3x3, 7x7)
- **Control de parámetros**: Ajustar ruido y otros parámetros
- **Exportación**: Guardar la imagen generada
- **Historial**: Mantener un historial de generaciones

## 🆕 Cambios Recientes

### Eliminación de Dependencias Externas
- **Sin PIL/Pillow**: Renderizado implementado nativamente con tkinter
- **Sin struct**: Lectura de bytes implementada con `int.from_bytes()`
- **Análisis por filas**: Renderizado píxel por píxel como en el reconocedor de números

### Correcciones y Mejoras
- **Orientación BMP**: Corregida la lectura de imágenes BMP (de abajo hacia arriba)
- **Control de iteraciones**: Campo de entrada para configurar el número de iteraciones
- **Validación de entrada**: Verificación de que el número de iteraciones esté en rango (1-100)
- **Feedback mejorado**: Barra de estado muestra el número de iteraciones configurado

### Ventajas del Nuevo Sistema
- **Independencia**: No requiere instalación de librerías externas
- **Compatibilidad**: Funciona con cualquier instalación de Python estándar
- **Control total**: Manipulación directa de datos de píxeles
- **Eficiencia**: Menor overhead al no usar librerías intermedias
- **Flexibilidad**: Número de iteraciones configurable por el usuario

## 📝 Conclusión

Este generador de imágenes sintéticas implementa un algoritmo sofisticado de síntesis de texturas que preserva las características locales de la imagen original mientras genera una nueva imagen única. El concepto de "matriz evolutiva" representa el proceso iterativo de refinamiento que evoluciona la imagen hacia un estado que mantiene las texturas originales pero con una estructura única.

El sistema es completamente funcional y proporciona una interfaz gráfica intuitiva para el proceso de generación, haciendo accesible esta técnica avanzada de procesamiento de imágenes a usuarios sin conocimientos técnicos profundos. La implementación nativa sin dependencias externas garantiza máxima compatibilidad y control sobre el proceso de renderizado, mientras que las correcciones recientes aseguran que las imágenes se muestren correctamente y que el usuario tenga control sobre el número de iteraciones del proceso evolutivo.
