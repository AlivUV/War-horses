from src.clases.Tablero import Tablero

tablero = Tablero(3)

puntajes = [0, 0]

while (not tablero.juegoTerminado()):
  tablero.moverIA()

  tablero.imprimirTablero()

  puntajes = tablero.getPuntos()

  print("IA: {}, jugador: {}.".format(puntajes[0], puntajes[1]))

  jugadas = tablero.evaluarJugadas()

  if(jugadas == []):
    continue

  for i in range(len(jugadas)):
    print("{}. {}".format(i, jugadas[i]))

  jugada = int(input("Escriba el número de la jugada que desea realizar: "))

  tablero.moverJugador(jugadas[jugada][0], jugadas[jugada][1])


puntajes = tablero.getPuntos()

print()
print("IA: {}, jugador: {}.".format(puntajes[0], puntajes[1]))

if (tablero.getPuntos()[0] > tablero.getPuntos()[1]):
  print("Ganó la IA.")
else:
  print("Ganó el jugador.")