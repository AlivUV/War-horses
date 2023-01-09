from copy import deepcopy
import random

class Tablero:
  """
  Clase que simula el tablero de juego.
  """
  __jugador = []
  __ia = []
  __tablero = []

  def __init__ (self):
    """
    Constructor del tablero.
    """
    self.__tablero = [0 for i in range(8)]
    self.__tablero = [self.__tablero[:] for i in range(8)]

    self.__crearPoderes()
    self.__crearJugadores()

    for fila in self.__tablero:
      print(fila)


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


  def moverJugador(self, i: int, j: int):
    """
    Mover la ficha del jugador a las nuevas coordenadas
    pintando la casilla en la cual se encontraba.
    """
    self.__tablero[i][j] = self.__tablero[self.__jugador[0]][self.__jugador[1]]
    self.__tablero[self.__jugador[0]][self.__jugador[1]] -= 1

    self.__jugador = [i, j]


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

    return jugadas