from src.clases.Minimax2 import Minimax
from src.clases.Tablero import Tablero

'''
Tablero con un posible estado del juego
ejemplificado en el enunciado del proyecto.
'''
tablero = [
  [0, 0, 0, 0, 0, 0, 0, 5],
  [0, 0, 0, 0, 0, 4, 0, 0],
  [0, 0, 2, 1, 0, 0, 4, 0],
  [0, 0, 0, 0, 2, 1, 0, 0],
  [0, 3, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0]
]

Minimax(tablero, 1, (4, 1), (0, 7))

# tablero = Tablero()

# print(tablero.evaluarJugadas())