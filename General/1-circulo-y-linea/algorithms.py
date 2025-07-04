"""
==> ALGORITMOS GRÁFICOS
% Implementa los algoritmos clásicos de Bresenham y Midpoint Circle para dibujo de líneas y círculos
% Autor: Olvera Olvera Olive Jesus
% Unidad de Aprendizaje: Visión por Computadora
"""

class BresenhamLine:
    """
    ==> ALGORITMO DE BRESENHAM PARA LÍNEAS
    % Implementa el algoritmo de Bresenham para dibujo eficiente de líneas
    % Optimizado para evitar operaciones de punto flotante
    """

    def get_puntos_linea(self, x1, y1, x2, y2):
        """
        # Cálculo de puntos de línea
        % Calcula todos los puntos de una línea usando el algoritmo de Bresenham
        $ x1, y1: Coordenadas del punto inicial
        $ x2, y2: Coordenadas del punto final
        % Returns: Lista de tuplas (x, y) con todos los puntos de la línea
        """
        puntos = []

        # ==> CÁLCULO DE DIFERENCIAS
        # -> Distancia absoluta en el eje X
        distancia_x = abs(x2 - x1)
        # -> Distancia absoluta en el eje Y
        distancia_y = abs(y2 - y1)

        # ==> DETERMINACIÓN DE DIRECCIÓN
        # -> Sentido de movimiento en X (1: derecha, -1: izquierda)
        sentido_x = 1 if x1 < x2 else -1
        # -> Sentido de movimiento en Y (1: abajo, -1: arriba)
        sentido_y = 1 if y1 < y2 else -1

        # ==> INICIALIZACIÓN DE ERROR
        # -> Error inicial basado en la diferencia entre distancias
        error = distancia_x - distancia_y

        # -> Coordenadas actuales (comenzando en el punto inicial)
        x, y = x1, y1

        # ==> BUCLE PRINCIPAL DEL ALGORITMO
        while True:
            # -> Agregar punto actual a la lista
            puntos.append((x, y))

            # -> Verificar si llegamos al punto final
            if x == x2 and y == y2:
                break

            # ==> CÁLCULO DE ERROR DUPLICADO
            # -> Multiplicación por 2 para evitar divisiones
            error_duplicado = 2 * error

            # ==> DECISIÓN DE MOVIMIENTO EN X
            # -> Si el error es mayor que -distancia_y, moverse en X
            if error_duplicado > -distancia_y:
                error -= distancia_y
                x += sentido_x

            # ==> DECISIÓN DE MOVIMIENTO EN Y
            # -> Si el error es menor que distancia_x, moverse en Y
            if error_duplicado < distancia_x:
                error += distancia_x
                y += sentido_y

        # -> Retorno de todos los puntos calculados
        return puntos


class MidpointCircle:
    """
    ==> ALGORITMO MIDPOINT CIRCLE
    % Implementa el algoritmo de Midpoint Circle para dibujo eficiente de círculos
    % Utiliza simetría de octantes para optimizar el cálculo
    """

    def get_puntos_circulo(self, centro_x, centro_y, radio):
        """
        # Cálculo de puntos de círculo
        % Calcula todos los puntos de un círculo usando el algoritmo de Midpoint Circle
        $ centro_x, centro_y: Coordenadas del centro del círculo
        $ radio: Radio del círculo
        % Returns: Lista de tuplas (x, y) con todos los puntos del círculo
        """
        puntos = []

        # ==> INICIALIZACIÓN DE VARIABLES
        # -> Punto inicial en el primer octante
        x = 0
        y = radio

        # -> Decisión inicial (error del punto medio)
        decision_inicial = 1 - radio

        # -> Agregar puntos iniciales en las 8 direcciones
        self._agregar_puntos_circulo(puntos, centro_x, centro_y, x, y)

        # ==> BUCLE PRINCIPAL DEL ALGORITMO
        # -> Mientras x < y (recorrer solo el primer octante)
        while x < y:
            x += 1

            # ==> EVALUACIÓN DE LA DECISIÓN
            if decision_inicial < 0:
                # -> Punto medio está dentro del círculo
                # -> Moverse solo en X
                decision_inicial += 2 * x + 1
            else:
                # -> Punto medio está fuera del círculo
                # -> Moverse en X e Y
                y -= 1
                decision_inicial += 2 * (x - y) + 1

            # -> Agregar puntos simétricos en las 8 direcciones
            self._agregar_puntos_circulo(puntos, centro_x, centro_y, x, y)

        return puntos

    def _agregar_puntos_circulo(self, puntos, centro_x, centro_y, x, y):
        """
        # Agregado de puntos simétricos
        % Agrega puntos en las 8 direcciones simétricas del círculo
        $ puntos: Lista donde agregar los puntos
        $ centro_x, centro_y: Centro del círculo
        $ x, y: Coordenadas relativas al centro
        """
        # ==> PUNTOS SIMÉTRICOS EN 8 DIRECCIONES
        puntos_simetricos = [
            (centro_x + x, centro_y + y),  # -> Octante 1 (arriba derecha superior)
            (centro_x - x, centro_y + y),  # -> Octante 2 (arriba izquierda superior)
            (centro_x + x, centro_y - y),  # -> Octante 3 (abajo derecha superior)
            (centro_x - x, centro_y - y),  # -> Octante 4 (abajo izquierda superior)
            (centro_x + y, centro_y + x),  # -> Octante 5 (arriba derecha inferior)
            (centro_x - y, centro_y + x),  # -> Octante 6 (arriba izquierda inferior)
            (centro_x + y, centro_y - x),  # -> Octante 7 (abajo derecha inferior)
            (centro_x - y, centro_y - x),  # -> Octante 8 (abajo izquierda inferior)
        ]

        # -> Agregar puntos únicos para evitar duplicados
        for punto in puntos_simetricos:
            if punto not in puntos:
                puntos.append(punto)


class LineUtils:
    """
    ==> UTILIDADES PARA LÍNEAS
    % Clase de utilidades adicionales para manejo y cálculos de líneas
    """

    @staticmethod
    def calculate_line_length(x1, y1, x2, y2):
        """
        # Cálculo de longitud de línea
        % Calcula la longitud euclidiana de una línea
        $ x1, y1, x2, y2: Coordenadas de los puntos extremos
        % Returns: Longitud de la línea
        """
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    @staticmethod
    def get_line_angle(x1, y1, x2, y2):
        """
        # Cálculo de ángulo de línea
        % Calcula el ángulo de una línea en radianes
        $ x1, y1, x2, y2: Coordenadas de los puntos extremos
        % Returns: Ángulo en radianes
        """
        import math
        return math.atan2(y2 - y1, x2 - x1)


class CircleUtils:
    """
    ==> UTILIDADES PARA CÍRCULOS
    % Clase de utilidades adicionales para manejo y cálculos de círculos
    """

    @staticmethod
    def calculate_circle_area(radius):
        """
        # Cálculo de área de círculo
        % Calcula el área de un círculo dado su radio
        $ radius: Radio del círculo
        % Returns: Área del círculo
        """
        import math
        return math.pi * radius ** 2

    @staticmethod
    def calculate_circle_circumference(radius):
        """
        # Cálculo de circunferencia
        % Calcula la circunferencia de un círculo dado su radio
        $ radius: Radio del círculo
        % Returns: Circunferencia del círculo
        """
        import math
        return 2 * math.pi * radius

    @staticmethod
    def point_in_circle(px, py, cx, cy, radius):
        """
        # Verificación de punto en círculo
        % Verifica si un punto está dentro de un círculo
        $ px, py: Coordenadas del punto a verificar
        $ cx, cy: Coordenadas del centro del círculo
        $ radius: Radio del círculo
        % Returns: True si el punto está dentro del círculo, False en caso contrario
        """
        distance_squared = (px - cx) ** 2 + (py - cy) ** 2
        return distance_squared <= radius ** 2
