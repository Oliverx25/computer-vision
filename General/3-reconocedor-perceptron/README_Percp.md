# Reconocedor de Números con Perceptrón Multicapa

## Descripción

Este programa implementa un reconocedor de dígitos utilizando un **perceptrón multicapa** (red neuronal artificial) en lugar del sistema de comparación de patrones original. El perceptrón aprende a reconocer dígitos del 0 al 9 mediante entrenamiento supervisado.

## Arquitectura del Perceptrón

### Estructura de la Red
- **Capa de entrada**: 100 neuronas (10×10 píxeles normalizados)
- **Capa oculta**: 50 neuronas
- **Capa de salida**: 10 neuronas (una por cada dígito 0-9)

### Funciones de Activación
- **Función sigmoid**: `f(x) = 1 / (1 + e^(-x))`
- **Derivada**: `f'(x) = f(x) * (1 - f(x))`

## Algoritmo de Entrenamiento

### Backpropagation
1. **Propagación hacia adelante (Forward Pass)**:
   - Calcula la salida de cada capa usando los pesos actuales
   - Aplica la función sigmoid a las activaciones

2. **Propagación hacia atrás (Backward Pass)**:
   - Calcula el error en la capa de salida
   - Propaga el error hacia las capas anteriores
   - Actualiza pesos y bias usando descenso de gradiente

### Parámetros de Entrenamiento
- **Épocas**: 50 (configurable)
- **Tasa de aprendizaje**: 0.1
- **Inicialización de pesos**: Xavier (para mejor convergencia)

## Flujo de Trabajo

### 1. Preparación de Datos
- Carga imágenes BMP del dataset
- Convierte a escala de grises
- Binariza con umbral 128
- Segmenta regiones conectadas
- Normaliza cada región a 10×10 píxeles

### 2. Entrenamiento
- Convierte patrones 10×10 en vectores de 100 elementos
- Crea vectores one-hot para las etiquetas (0-9)
- Entrena el perceptrón con backpropagation
- Muestra progreso y estadísticas

### 3. Reconocimiento
- Procesa nueva imagen de la misma manera
- Alimenta el patrón normalizado al perceptrón
- Obtiene probabilidades para cada dígito
- Selecciona el dígito con mayor probabilidad

## Características del Sistema

### Interfaz Mejorada
- **Botón "Reentrenar Perceptrón"**: Permite reentrenar la red
- **Indicador de estado**: Muestra si el perceptrón está entrenado
- **Visualización de confianza**: Colores basados en la confianza de predicción
  - Verde: >80% confianza
  - Naranja: 60-80% confianza
  - Rojo: <60% confianza

### Ventajas sobre el Sistema Anterior
1. **Aprendizaje adaptativo**: Mejora con más datos
2. **Generalización**: Puede reconocer variaciones no vistas en entrenamiento
3. **Probabilidades**: Proporciona medidas de confianza más sofisticadas
4. **Escalabilidad**: Fácil de extender para más clases

### Limitaciones
1. **Dependencia de datos**: Requiere dataset de entrenamiento
2. **Tiempo de entrenamiento**: Más lento que comparación directa
3. **Overfitting**: Puede memorizar en lugar de generalizar
4. **Parámetros**: Requiere ajuste de hiperparámetros

## Uso del Programa

1. **Inicio**: El perceptrón se entrena automáticamente al abrir
2. **Cargar imagen**: Selecciona una imagen BMP con dígitos
3. **Procesar**: El perceptrón reconoce los dígitos encontrados
4. **Reentrenar**: Si es necesario, puede reentrenar la red

## Archivos Requeridos

- `reconocedor_numeros.py`: Programa principal
- `Numeros/`: Carpeta con subcarpetas 0-9 conteniendo imágenes BMP de entrenamiento

## Dependencias

- `tkinter`: Interfaz gráfica
- `numpy`: Operaciones matemáticas
- `collections.deque`: Para BFS en segmentación
- `os`: Manejo de archivos
- `random`: Inicialización de pesos

## Notas Técnicas

### Inicialización de Pesos
Se usa la inicialización de Xavier para evitar el problema de desvanecimiento/explosión de gradientes:
```
limite = sqrt(2.0 / numero_neuronas_capa_anterior)
peso = random.uniform(-limite, limite)
```

### Normalización de Datos
Los patrones se normalizan a 10×10 píxeles usando interpolación bilineal para mantener la proporción y calidad de la imagen.

### Función de Pérdida
Se usa el error cuadrático medio (MSE) para medir la diferencia entre predicciones y valores reales durante el entrenamiento.

## ⚡️ ¿Dónde está implementado el perceptrón en el código?

---

### 📂 Archivo: `reconocedor_numeros_perc.py`

#### 🧠 **Toda la lógica del perceptrón está implementada en la clase `Perceptron` (líneas 7 a 74 aprox.)**

```python
class Perceptron:
    """Implementación de un perceptrón multicapa para reconocimiento de dígitos"""
    def __init__(self, capas):
        # Inicializa la arquitectura y llama a inicializar_pesos()
    def inicializar_pesos(self):
        # Inicializa pesos y bias aleatoriamente (Xavier)
    def sigmoid(self, x):
        # Función de activación sigmoid
    def sigmoid_derivada(self, x):
        # Derivada de la sigmoid
    def forward(self, entrada):
        # Propagación hacia adelante
    def backward(self, entrada, salida_deseada, tasa_aprendizaje=0.1):
        # Backpropagation (ajuste de pesos)
    def entrenar(self, datos_entrenamiento, epocas=100, tasa_aprendizaje=0.1):
        # Entrenamiento completo (llama forward y backward)
    def predecir(self, entrada):
        # Predicción de salida
```

- **La clase `Perceptron` es completamente independiente y NO usa librerías externas de machine learning.**
- **Todo el aprendizaje, ajuste de pesos y predicción se hace desde cero usando solo numpy.**

#### 📌 ¿Dónde se usa el perceptrón en el flujo del programa?

- **Inicialización:**
  ```python
  self.perceptron = Perceptron([100, 50, 10])
  ```
  (En el constructor de `ReconocedorNumeros`)

- **Entrenamiento:**
  ```python
  self.perceptron.entrenar(datos_entrenamiento, epocas=50, tasa_aprendizaje=0.1)
  ```
  (En el método `entrenar_con_dataset`)

- **Predicción:**
  ```python
  salida = self.perceptron.predecir(entrada)
  digito_predicho = np.argmax(salida)
  ```
  (En el método `reconocer_digito`)

---

## 🧩 **Resumen de la arquitectura y funciones**

- **`__init__`**: Define la arquitectura (capas) y llama a la inicialización de pesos.
- **`inicializar_pesos`**: Inicializa pesos y bias aleatoriamente (Xavier).
- **`sigmoid` y `sigmoid_derivada`**: Función de activación y su derivada.
- **`forward`**: Propagación hacia adelante (cálculo de activaciones).
- **`backward`**: Backpropagation (ajuste de pesos y bias).
- **`entrenar`**: Entrenamiento completo (llama forward y backward para cada ejemplo).
- **`predecir`**: Propagación hacia adelante para obtener la predicción.

---

## 🏷️ **¿Dónde modificar si quieres cambiar el perceptrón?**
- Cambia la arquitectura (número de capas/neuronas) en la línea de inicialización: `Perceptron([100, 50, 10])`
- Cambia la función de activación o el algoritmo de entrenamiento dentro de la clase `Perceptron`.

---

## 🔎 **Referencia rápida**
- **Clase principal:** `Perceptron` (líneas 7-74 aprox.)
- **Uso en el flujo:** Métodos de la clase `ReconocedorNumeros` (`entrenar_con_dataset`, `reconocer_digito`)
- **No depende de librerías externas de ML**

---
