from src.clases.Minimax import Minimax

'''
Tablero con un posible estado del juego
ejemplificado en el enunciado del proyecto.
'''
tablero = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 4],
    [0, 3, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1]
]

print("   0  1  2  3  4  5  6  7")

for i in range(len(tablero)):
    print("{} {}".format(i, tablero[i]))

pc = Minimax(tablero, 3)
