from src.clases.Minimax import Minimax
from copy import deepcopy
import random

class Tablero:
  """
  Clase que simula el tablero de juego.
  """
  __nivel = 1
  __ia = []
  __jugador = []
  __tablero = []
  __puntos = [1, 1]
  __iaTieneMovimientos = True
  __jugadorTieneMovimientos = True

  def __init__ (self, nivel: int):
    """
    Constructor del tablero.
    """
    self.__nivel = nivel

    self.__tablero = [0 for i in range(8)]
    self.__tablero = [self.__tablero[:] for i in range(8)]

    self.__crearPoderes()
    self.__crearJugadores()


  def __crearPoderes(self):
    """
    Crear poderes en tres casillas de manera aleatoria asegurando
    que no se encuentren en casillas contiguas.
    """
    poderesCreados = []
    intento = 0

    while (intento < 3):
      i =random.randint(0, 7)
      j =random.randint(0, 7)
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
    Añadir dos jugadores de manera aleatoria sin ocupar una casilla
    que ya contenga un poder.
    """
    intento = 0
    jugadores = []

    while (intento < 2):
      i =random.randint(0, 7)
      j =random.randint(0, 7)

      if (self.__tablero[i][j] == 0):
        self.__tablero[i][j] = 3 + 2 * intento
        jugadores.append([i, j])
        intento += 1

    self.__ia = jugadores[0]
    self.__jugador = jugadores[1]


  def imprimirTablero (self):
    print("   0  1  2  3  4  5  6  7")
    for i in range(len(self.__tablero)):
      print("{} {}".format(i, self.__tablero[i]))


  def getTablero(self):
    return deepcopy(self.__tablero)


  def getPosJugador(self):
    return self.__jugador[:]


  def getPosIA(self):
    return self.__ia[:]


  def moverIA (self):
    """
    Utilizar el algoritmo minimax para decidir el 
    próximo movimiento de la ia.
    """
    posicionAnterior = self.__ia[:]
    casillasAfectadas = []
    pc = Minimax(self.__tablero, self.__nivel)

    i, j = pc.getMovimiento()[:]

    if (posicionAnterior == [i, j]):
      self.__iaTieneMovimientos = False
      return

    if (self.__tablero[i][j] == 1):
      casillasAfectadas = self.__agarrarPoder(i, j, self.__tablero[self.__ia[0]][self.__ia[1]])

    self.__tablero[i][j] = self.__tablero[self.__ia[0]][self.__ia[1]]
    self.__tablero[self.__ia[0]][self.__ia[1]] -= 1

    self.__ia = [i, j]

    casillasAfectadas.insert(0, [i, j])

    self.__puntos[0] += len(casillasAfectadas)

    return posicionAnterior, casillasAfectadas


  def moverJugador(self, i: int, j: int):
    """
    Mover la ficha del jugador a las nuevas coordenadas
    pintando la casilla en la cual se encontraba.
    """
    posicionAnterior = self.__jugador[:]
    casillasAfectadas = []

    if (self.__tablero[i][j] == 1):
      casillasAfectadas = self.__agarrarPoder(i, j, self.__tablero[self.__jugador[0]][self.__jugador[1]])

    self.__tablero[i][j] = self.__tablero[self.__jugador[0]][self.__jugador[1]]
    self.__tablero[self.__jugador[0]][self.__jugador[1]] -= 1

    self.__jugador = [i, j]

    casillasAfectadas.insert(0, [i, j])

    self.__puntos[1] += len(casillasAfectadas)

    return posicionAnterior, casillasAfectadas


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


  def evaluarJugadas(self):
    """
    Ver las diferentes posibilidades que tiene el jugador
    para mover su ficha. Retorna una lista de parejas [i, j].
    """
    jugadas = []

    for pos in range(8):
      i = self.__jugador[0] + ([1, 2][pos % 2] * pow(-1, pos // 2))
      j = self.__jugador[1] + ([1, 2][pos % 2] * 2 % 3) * pow(-1, pos // 4)

      if (i < 0 or j < 0):
        "La posición está fuera del rango de la lista"
        continue

      try:
        if (self.__tablero[i][j] < 2):
          jugadas.append([i, j])

      except:
        "La posición está fuera del rango de la lista"
        continue

    if (jugadas == []):
      self.__jugadorTieneMovimientos = False
      return jugadas

    return jugadas


  def juegoTerminado(self):
    "Indica si el jugador y la ia ya no tienen movimientos."
    return not (self.__jugadorTieneMovimientos or self.__iaTieneMovimientos)


  def getPuntos(self):
    """
    Retorna una lista con los puntos de la ia en la primera
    posición y los puntos del jugador en la segunda.
    """
    return self.__puntos[:]