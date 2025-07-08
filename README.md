# Sistema de Visión por Computadora

Un sistema completo de visión por computadora desarrollado en Python con interfaz gráfica, que incluye diferentes módulos para procesamiento de imágenes y reconocimiento de patrones.

## 📋 Características

- **Interfaz Principal**: Sistema centralizado con menú visual para acceder a todos los módulos
- **Círculo y Línea**: Generador de formas geométricas usando algoritmos de Bresenham y Midpoint Circle
- **Filtros de Color**: Procesamiento de imágenes BMP con diferentes filtros de color
- **Reconocedor de Números**: Sistema de reconocimiento de dígitos en imágenes
- **Reconocedor con Perceptron**: Reconocimiento de dígitos usando redes neuronales tipo Perceptron

## 🚀 Instalación

1. Clona este repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd computer-vision
```

2. Asegúrate de tener Python 3.7+ instalado

3. Instala las dependencias necesarias:
```bash
pip install tkinter numpy opencv-python PIL
```

## 💻 Uso

### Ejecutar la aplicación principal

```bash
python main_display.py
```

Esto abrirá la interfaz principal donde podrás acceder a todos los módulos disponibles.

### Ejecutar módulos individuales

También puedes ejecutar cada módulo por separado:

```bash
# Círculo y línea
python General/1-circulo-y-linea/main.py

# Filtros de color
python General/2-modos-color/filtros_color.py

# Reconocedor de números
python General/3-reconocedor-numeros/reconocedor_numeros.py

# Reconocedor con perceptron
python General/3-reconocedor-perceptron/reconocedor_numeros_perc.py
```

## 📁 Estructura del Proyecto

```
.
├── main_display.py                     # Interfaz principal del sistema
├── General/
│   ├── 1-circulo-y-linea/             # Módulo de generación de formas
│   ├── 2-modos-color/                 # Módulo de filtros de color
│   ├── 3-reconocedor-numeros/         # Reconocimiento básico de dígitos
│   ├── 3-reconocedor-perceptron/      # Reconocimiento con perceptron
│   ├── 4-generador-imagenes/          # Generador de imágenes
│   └── 4-generador-imagenes-d/        # Generador de imágenes alternativo
└── README.md
```

## 🔧 Requisitos del Sistema

- Python 3.7 o superior
- Tkinter (incluido con Python)

## 📚 Módulos Disponibles

### 1. Círculo y Línea
Implementa algoritmos clásicos de computer graphics para dibujar formas geométricas básicas.

### 2. Filtros de Color
Procesamiento de imágenes con diferentes filtros y transformaciones de color.

### 3. Reconocedor de Números
Sistema de reconocimiento de dígitos manuscritos usando técnicas de visión por computadora.

### 4. Reconocedor con Perceptron
Versión avanzada del reconocedor que utiliza redes neuronales tipo perceptron.

## 🤝 Contribuciones

Este es un proyecto académico. Las sugerencias y mejoras son bienvenidas.

## 📄 Licencia

Proyecto académico para fines educativos.
