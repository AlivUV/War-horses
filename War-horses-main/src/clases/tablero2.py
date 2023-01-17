from copy import deepcopy
import random
import pygame
import time
from clases.Minimax import Minimax
import sys
from perdedor import main as perdedor
from ganador import main as ganador

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 255, 255)
DIMENSIONES = (600, 600)
pygame.init()


class Tablero:
    """
    Clase que simula el tablero de juego.
    """
    __jugador = []
    __ia = []
    __tablero = []
    __puntos = [1, 1]
    __nivel = 1
    __turno = 0
    __jugadasEvaluadas = False
    __iaTieneMovimientos = True
    __jugadorTieneMovimientos = True

    def __init__(self, screen, dimension, puntoInicio, nivel: int):
        """
        Constructor del tablero.
        """
        self.__nivel = nivel
        self.__tablero = [0 for i in range(8)]
        self.__tablero = [self.__tablero[:] for i in range(8)]

        self.__crearPoderes()
        self.__crearJugadores()
        self.__dibujarTablero(screen, dimension, puntoInicio, nivel)

    def __dibujarTablero(self, screen, dimension, p_inicio, nivel: int):
        '''
        # Función que dibuja el tablero
        screen: 		referencia del lienzo donde dibujar
        dimension: 		tamaño de los rectangulos
        p_inicio: 		coordenadas del punto de inicio del tablero
        '''
        color = 0

        for i in range(8):
            for j in range(8):
                x = j * dimension + p_inicio[0]
                y = i * dimension + p_inicio[1]+10
                if color % 2 == 0 and self.__tablero[i][j] == 0:
                    pygame.draw.rect(screen, NEGRO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                elif self.__tablero[i][j] == 0 and color % 2 != 0:
                    pygame.draw.rect(screen, NEGRO, pygame.Rect(
                        x, y, dimension, dimension), 1)
                else:
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                color += 1
            color += 1

    def cargarImagenes(self, screen, dimension, posicionx, posiciony, tipo, colorCasilla):
        '''
        #Función que pinta los elementos del juego de acuerdo a la posición 
        aleatoria que le fue asignada a cada uno.
        screen: 		referencia del lienzo donde dibujar
        dimension: 		tamaño de la imagen
        posicionx:      coordenada x de la imagen
        posiciony:      coordenada y de la imagen
        tipo:           define el elemento a pintar en el tablero 
        '''
        if tipo == 5:
            pygame.draw.rect(screen, VERDE, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 0)
            jugador1 = pygame.image.load(
                "./src/imagenes/caballo.png").convert_alpha()
            jugador1 = pygame.transform.scale(jugador1, [dimension, dimension])
            screen.blit(jugador1, (posicionx, posiciony))
        elif tipo == 3:
            pygame.draw.rect(screen, ROJO, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 0)
            jugador1 = pygame.image.load(
                "./src/imagenes/caballo_IA.png").convert_alpha()
            jugador1 = pygame.transform.scale(jugador1, [dimension, dimension])
            screen.blit(jugador1, (posicionx, posiciony))
        elif colorCasilla % 2 != 0 and tipo == 1:
            pygame.draw.rect(screen, BLANCO, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 0)
            pygame.draw.rect(screen, NEGRO, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 1)
            bonus = pygame.image.load(
                "./src/imagenes/bonus.png").convert_alpha()
            bonus = pygame.transform.scale(bonus, [dimension, dimension])
            screen.blit(bonus, (posicionx, posiciony))
        elif tipo == 2:
            pygame.draw.rect(screen, ROJO, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 0)
        else:
            pygame.draw.rect(screen, BLANCO, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 0)
            pygame.draw.rect(screen, NEGRO, pygame.Rect(
                posicionx, posiciony, dimension, dimension), 0)
            bonus = pygame.image.load(
                "./src/imagenes/bonus.png").convert_alpha()
            bonus = pygame.transform.scale(bonus, [dimension, dimension])
            screen.blit(bonus, (posicionx, posiciony))

    def __crearPoderes(self):
        """
        Crea poderes en tres casillas de manera aleatoria asegurando
        que no se encuentren en casillas contiguas.
        """
        poderesCreados = []
        intento = 0

        while (intento < 3):
            i = random.randint(0, 7)
            j = random.randint(0, 7)
            creado = False

            for poder in poderesCreados:
                if (abs(poder[0] - i) < 2 and abs(poder[1] - j) < 2):
                    creado = True
                    break

            if (not creado):
                intento += 1
                self.__tablero[i][j] = 1
                poderesCreados.append([i, j])

    def __crearJugadores(self):
        """
        Añade dos jugadores de manera aleatoria sin ocupar una casilla
        que ya contenga un poder.
        """
        intento = 0
        jugadores = []

        while (intento < 2):
            i = random.randint(0, 7)
            j = random.randint(0, 7)

            if (self.__tablero[i][j] == 0):
                self.__tablero[i][j] = 3 + 2 * intento
                jugadores.append([i, j])
                intento += 1

        self.__ia = jugadores[0]
        self.__jugador = jugadores[1]

    def getTablero(self):
        '''
        Retorna la matriz que representa al tablero.
        '''
        return deepcopy(self.__tablero)

    def getPosJugador(self):
        '''
        Retorna la posición en la que se encuentra el jugador.
        '''
        return self.__jugador[:]

    def getPosIA(self):
        '''
        Retorna la posición en la que se encuentra la IA.
        '''
        return self.__ia[:]

    def getPuntos(self):
        """
        Retorna una lista con los puntos de la ia en la primera
        posición y los puntos del jugador en la segunda.
        """
        return self.__puntos[:]

    def getTurno(self):
        """
        Retorna un número que indica quien es el jugador que debe realizar el movimiento.
        Siendo 0 para la IA y 1 para el jugador.
        """
        return self.__turno

    def getJugadasEvaluadas(self):
        '''
        Retorna el arreglo que contiene todas las jugadas posibles 
        que se pueden realizar de acuerdo a la posición en la que se encuentre el jugador.
        '''
        return self.__jugadasEvaluadas

    def moverIA(self, screen, dimension, p_inicio):
        """
        Utilizar el algoritmo minimax para decidir el
        próximo movimiento de la ia.
        """

        posicionAnterior = self.__ia[:]
        casillasAfectadas = []
        color = 0
        pc = Minimax(self.__tablero, self.__nivel)

        i, j = pc.getMovimiento()[:]

        if (posicionAnterior == [i, j]):
            self.__iaTieneMovimientos = False
            self.__turno = 1
            return

        if (self.__tablero[i][j] == 1):
            casillasAfectadas = self.__agarrarPoder(
                i, j, self.__tablero[self.__ia[0]][self.__ia[1]])

        self.__tablero[i][j] = self.__tablero[self.__ia[0]][self.__ia[1]]
        self.__tablero[self.__ia[0]][self.__ia[1]] -= 1

        self.__ia = [i, j]

        casillasAfectadas.insert(0, [i, j])

        self.__puntos[0] += len(casillasAfectadas)
        screen.fill(BLANCO)

        for i in range(8):
            for j in range(8):
                x = j * dimension + p_inicio[0]
                y = i * dimension + p_inicio[1]+10
                if self.__tablero[i][j] == 0 and color % 2 != 0:
                    pygame.draw.rect(screen, BLANCO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    pygame.draw.rect(screen, NEGRO, pygame.Rect(
                        x, y, dimension, dimension), 1)
                elif self.__tablero[i][j] == 0 and color % 2 == 0:
                    pygame.draw.rect(screen, BLANCO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    pygame.draw.rect(screen, NEGRO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                elif self.__tablero[i][j] == 4:
                    pygame.draw.rect(screen, VERDE, pygame.Rect(
                        x, y, dimension, dimension), 0)
                elif self.__tablero[i][j] == 5:
                    pygame.draw.rect(screen, VERDE, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                elif self.__tablero[i][j] == 1:
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                else:
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                color += 1
            color += 1

        if (self.__jugadorTieneMovimientos == True):
            self.__turno = 1
        return posicionAnterior, casillasAfectadas

    def moverJugador(self, screen, dimension, p_inicio, i: int, j: int):
        """
        Mover la ficha del jugador a las nuevas coordenadas
        pintando la casilla en la cual se encontraba.
        """
        posicionAnterior = self.__jugador[:]
        casillasAfectadas = []
        color = 0
        screen.fill(BLANCO)

        if (self.__tablero[i][j] == 1):
            casillasAfectadas = self.__agarrarPoder(
                i, j, self.__tablero[self.__jugador[0]][self.__jugador[1]])

        self.__tablero[i][j] = self.__tablero[self.__jugador[0]
                                              ][self.__jugador[1]]
        self.__tablero[self.__jugador[0]][self.__jugador[1]] -= 1

        self.__jugador = [i, j]

        casillasAfectadas.insert(0, [i, j])

        self.__puntos[1] += len(casillasAfectadas)

        for i in range(8):
            for j in range(8):
                x = j * dimension + p_inicio[0]
                y = i * dimension + p_inicio[1]+10
                if self.__tablero[i][j] == 0 and color % 2 != 0:
                    pygame.draw.rect(screen, BLANCO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    pygame.draw.rect(screen, NEGRO, pygame.Rect(
                        x, y, dimension, dimension), 1)
                elif self.__tablero[i][j] == 0 and color % 2 == 0:
                    pygame.draw.rect(screen, BLANCO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    pygame.draw.rect(screen, NEGRO, pygame.Rect(
                        x, y, dimension, dimension), 0)
                elif self.__tablero[i][j] == 4:
                    pygame.draw.rect(screen, VERDE, pygame.Rect(
                        x, y, dimension, dimension), 0)
                elif self.__tablero[i][j] == 5:
                    pygame.draw.rect(screen, VERDE, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                elif self.__tablero[i][j] == 1:
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                else:
                    self.cargarImagenes(screen, dimension,
                                        x, y, self.__tablero[i][j], color)
                color += 1
            color += 1

        if (self.__iaTieneMovimientos == True):
            self.__turno = 0
        self.__jugadasEvaluadas = False

    def __agarrarPoder(self, i: int, j: int, jugador: int):
        """
        Pintar las cuatro casillas contiguas a la casilla en que se 
        encontraba el poder.
        Args:
            i (int): Posición i de la casilla en donde se encontraba el poder
            y ahora se encuentra el jugador.
            j (int): Posicion j de la casilla en donde se encontraba el poder
            y ahora se encuentra el jugador.
        """
        direcciones = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        casillasAfectadas = []

        for [di, dj] in direcciones:
            if (di + i < 0 or dj + j < 0):
                continue

            try:
                if (self.__tablero[di + i][dj + j] == 0):
                    self.__tablero[di + i][dj + j] = jugador - 1
                    casillasAfectadas.append([i, j])
            except:
                "La posición está fuera del rango de la lista"
                continue

        return casillasAfectadas

    def evaluarJugadas(self, screen, dimension, p_inicio):
        """
        Ver las diferentes posibilidades que tiene el jugador
        para mover su ficha de acuerdo a la posición en la que se encuentra. 
        Retorna una lista de parejas [i, j].
        """
        jugadas = []
        self.__jugadasEvaluadas = True

        for pos in range(8):
            i = self.__jugador[0] + ([1, 2][pos % 2] * pow(-1, pos // 2))
            j = self.__jugador[1] + ([1, 2][pos % 2] * 2 %
                                     3) * pow(-1, pos // 4)

            if (i < 0 or j < 0):
                "La posición está fuera del rango de la lista"
                continue

            try:
                if (self.__tablero[i][j] < 2):
                    jugadas.append([i, j])

            except:
                "La posición está fuera del rango de la lista"
                continue

        for i in range(len(jugadas)):
            for j in range(1):
                x = jugadas[i][j+1] * dimension + p_inicio[0]
                y = (jugadas[i][j]) * dimension + p_inicio[1]+10
                if self.getTablero()[jugadas[i][j]][jugadas[i][j+1]] == 1:
                    pygame.draw.rect(screen, AZUL, pygame.Rect(
                        x, y, dimension, dimension), 0)
                    bonus = pygame.image.load(
                        "./src/imagenes/bonus.png").convert_alpha()
                    bonus = pygame.transform.scale(
                        bonus, [dimension, dimension])
                    screen.blit(bonus, (x, y))
                else:
                    pygame.draw.rect(screen, AZUL, pygame.Rect(
                        x, y, dimension, dimension), 0)

        if (jugadas == [] and self.__iaTieneMovimientos == True):
            self.__jugadorTieneMovimientos = False
            self.__turno = 0
            return jugadas

        return jugadas

    def juegoTerminado(self):
        '''
        Indica si el jugador y la ia ya no tienen movimientos.
        '''
        return not (self.__jugadorTieneMovimientos or self.__iaTieneMovimientos)

    def jugadaValida(self, jugadas, x: int, y: int):
        '''
        Verifica que la casilla que haya seleccionado el jugador 
        se encuentra dentro de las jugadas validas que puede realizar.
        '''

        jugadaValida = False
        for i in range(len(jugadas)):
            for j in range(1):
                if jugadas[i][j+1] == x and jugadas[i][j] == y:
                    jugadaValida = True
                    break
        return jugadaValida


def ajustarMedidas(tamanio_fuente):
    '''
    Realiza el ajuste del ancho de cada rectángulo para que 
    se pueda adaptar todo el tablero a las dimensiones que se definan para la ventana.
    '''
    if DIMENSIONES[1] < DIMENSIONES[0]:
        ancho = int((DIMENSIONES[1] - (tamanio_fuente * 2)) / 8)
        inicio = ((DIMENSIONES[0] - DIMENSIONES[1]) /
                  2) + tamanio_fuente, tamanio_fuente
    else:
        ancho = int((DIMENSIONES[0] - (tamanio_fuente * 2)) / 8)
        inicio = tamanio_fuente, ((
            DIMENSIONES[1] - DIMENSIONES[0]) / 2) + tamanio_fuente
    return [inicio, ancho]


def obtenerPosicion(mouse, dimension, p_inicio, actual):
    """
    Realiza la conversión de las coordenadas en las que fue 
    presionado el cursor a coordenadas de la matriz que representa el tablero.
    """
    xr, yr = mouse[0], mouse[1]
    for i in range(8):
        for j in range(8):
            x = i * dimension + p_inicio[0]
            y = j * dimension + p_inicio[1]
            if (xr >= x) and (xr <= x + dimension) and (yr >= y) and (yr <= y + dimension):
                actual = [i, j]
    return actual


def fontsize(size):
    fuente = pygame.font.SysFont("Arial", size)
    return fuente


font_default = fontsize(20)

labels = []


class Label:

    ''' CLASS FOR TEXT LABELS ON THE WIN SCREEN SURFACE '''

    def __init__(self, screen, text, x, y, size=20, color="white"):
        if size != 20:
            self.font = fontsize(size)
        else:
            self.font = font_default
        self.image = self.font.render(text, 1, color)
        _, _, w, h = self.image.get_rect()
        self.rect = pygame.Rect(x, y, w, h)
        self.screen = screen
        self.text = text
        labels.append(self)

    def change_text(self, newtext, color="white"):
        self.text = newtext
        self.image = self.font.render(self.text, 1, color)

    def change_font(self, size, color="white"):
        #self.font = pygame.font.SysFont(font, size)
        self.change_text(self.text, color)

    def draw(self):
        self.screen.blit(self.image, (self.rect))


def show_labels():
    for _ in labels:
        _.draw()


def main(nivel: int):
    pygame.init()
    screen = pygame.display.set_mode(DIMENSIONES)
    pygame.display.set_caption("WAR HORSES")
    icono = pygame.image.load("./src/imagenes/icono.jpg")
    pygame.display.set_icon(icono)
    clock = pygame.time.Clock()
    tamanio_fuente = 30
    seleccion = [0, 0]
    puntoInicio, dimension = ajustarMedidas(tamanio_fuente)
    screen.fill(BLANCO)
    puntajeJugador = Label(
        screen, "Tu puntaje:", puntoInicio[0], 0, tamanio_fuente, color="black")
    puntajeIA = Label(
        screen, "Puntaje de la IA:", 300, 0, tamanio_fuente, color="black")
    show_labels()

    tablero = Tablero(screen, dimension, puntoInicio, nivel)
    pygame.display.flip()

    puntajeJugador1 = Label(
        screen, str(tablero.getPuntos()[1]), 170, 0, tamanio_fuente, color="green")
    puntajeIA1 = Label(
        screen, str(tablero.getPuntos()[0]), 500, 0, tamanio_fuente, color="red")
    show_labels()
    pygame.display.flip()

    while not tablero.juegoTerminado():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if tablero.getTurno() == 0:
                tablero.moverIA(screen, dimension, puntoInicio)
                puntajeIA1.change_text(
                    str(tablero.getPuntos()[0]), color="red")
                show_labels()
                pygame.display.flip()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                seleccion = obtenerPosicion(
                    pos, dimension, puntoInicio, seleccion)
                if tablero.getTablero()[seleccion[1]][seleccion[0]] == 5 and tablero.getJugadasEvaluadas() == False and tablero.getTurno() != 0:
                    tablero.evaluarJugadas(screen, dimension, puntoInicio)
                    pygame.display.flip()
                elif (tablero.getTablero()[seleccion[1]][seleccion[0]] == 0 or tablero.getTablero()[seleccion[1]][seleccion[0]] == 1) and tablero.getJugadasEvaluadas() == True and tablero.jugadaValida(tablero.evaluarJugadas(screen, dimension, puntoInicio), seleccion[0], seleccion[1]):
                    tablero.moverJugador(
                        screen, dimension, puntoInicio, seleccion[1], seleccion[0])
                    puntajeJugador1.change_text(
                        str(tablero.getPuntos()[1]), color="green")
                    show_labels()
                    pygame.display.flip()
            clock.tick(60)
    if tablero.getPuntos()[0] > tablero.getPuntos()[1]:
        perdedor()
    else:
        ganador()
    # pygame.quit()
