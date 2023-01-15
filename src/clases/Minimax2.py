from copy import deepcopy

class Minimax:
  """
  Clase para elegir el siguiente movimiento a realizar por la máquina
  con base en el algoritmo minimax.
  """
  __nodos = []
  __listaEspera = []
  __valoresMinimax = []
  __movimiento = []


  def __init__ (self, tablero: list, nivel: int, pc: tuple, jugador: tuple):
    """
    Función que da inicio al algoritmo minimax.

    Args:
      tablero (list[list[int]]): Tablero de juego.
      nivel (int): Cantidad de jugadas propias futuras que evaluará el algoritmo. 
      pc (tuple[int]): _description_
      jugador (tuple[int]): _description_
    """
    self.__nodos.clear()
    self.__listaEspera.clear()

    casLibres, valorNodo =self.__contarCasillas(tablero)

    nuevoNodo = {
      "padre": None,
      "posicion": 0,
      "profundidad": 0,
      "tablero": tablero,
      "pc": pc,
      "jugador": jugador,
      "valor": valorNodo,
      "casillasLibres": casLibres
    }

    self.__listaEspera.append(nuevoNodo)

    self.__amplitud(nivel * 2)

    self.__minimax()

    print(self.__nodos[0]["pc"])
    print(self.__movimiento)


  def __amplitud(self, profundidad):
    """
    Bucle que expande los nodos restantes en la lista de espera
    hasta vaciarla o completar la profundidad.
    """
    while (self.__listaEspera != []):
      self.__expandirNodo(self.__listaEspera.pop(0), profundidad)

    for i in range(profundidad + 1):
      for nodo in self.__nodos:
        if (nodo["profundidad"] == i):
          print("padre: {}, posicion: {}, profundidad: {}, pc: {}, jugador: {}, valor: {}.".format(
            nodo["padre"], 
            nodo["posicion"], 
            nodo["profundidad"], 
            nodo["pc"], 
            nodo["jugador"], 
            nodo["valor"]
          ))

    for fila in (self.__nodos[-4]["tablero"]):
      print(fila)


  def __expandirNodo(self, nodo, profundidad):
    """
    Añadir el nodo a la lista de nodos y crear sus hijos 
    poniéndolos en la lista de espera.
    """
    nodo["posicion"] = len(self.__nodos)

    jugadorTurno, valor = ("pc", 3) if (nodo["profundidad"] % 2 == 0) else ("jugador", 5)

    self.__nodos.append(nodo)

    if (nodo["profundidad"] < profundidad):
      for jugada in self.__evaluarJugadas(nodo, jugadorTurno):
        self.__crearHijo(nodo, jugada, jugadorTurno, valor)
    else:
      self.__valoresMinimax.append(nodo)


  def __evaluarJugadas(self, nodo: dict, jugadorTurno: str):
    "Evaluar todos los posibles movimientos del jugador."

    jugadas = []

    for pos in range(8):
      i = nodo[jugadorTurno][0] + ([1, 2][pos % 2] * pow(-1, pos // 2))
      j = nodo[jugadorTurno][1] + ([1, 2][pos % 2] * 2 % 3) * pow(-1, pos // 4)

      if (i < 0 or j < 0):
        "La posición está fuera del rango de la lista"
        continue

      try:
        if (nodo["tablero"][i][j] < 2):
          jugadas.append([i, j])

      except:
        "La posición está fuera del rango de la lista"
        continue

    if (len(jugadas) == 0):
      jugadas = [nodo[jugadorTurno]]

    return jugadas


  def __crearHijo(self, padre: dict, jugada: list, jugadorTurno: str, valor: int):
    "Crear un nuevo nodo y añadirlo a la lista de espera."
    aumentoValor = 0 if (padre[jugadorTurno] == jugada) else 1

    nuevoTablero = deepcopy(padre["tablero"])

    if (nuevoTablero[jugada[0]][jugada[1]] == 1):
      nuevoTablero[jugada[0] - 1][jugada[1]] = valor - 1
      nuevoTablero[jugada[0]][jugada[1] - 1] = valor - 1
      nuevoTablero[jugada[0] + 1][jugada[1]] = valor - 1
      nuevoTablero[jugada[0]][jugada[1] + 1] = valor - 1

      aumentoValor += 4

    nuevoTablero[padre[jugadorTurno][0]][padre[jugadorTurno][1]] = valor - 1
    nuevoTablero[jugada[0]][jugada[1]] = valor

    hijo = {
      "padre": padre["posicion"],
      "profundidad": padre["profundidad"] + 1,
      "pc": padre["pc"][:],
      "jugador": padre["jugador"][:],
      "tablero": nuevoTablero,
      "valor": padre["valor"] + (aumentoValor * ((-1) ** (padre["profundidad"]))),
      "casillasLibres": padre["casillasLibres"] - aumentoValor
    }

    hijo[jugadorTurno] = jugada[:]

    self.__listaEspera.append(hijo)


  def __contarCasillas(self, tablero: list):
    conteo = [0, 0, 0, 0, 0, 0]
    for fila in tablero:
      for casilla in fila:
        conteo[casilla] += 1

    return conteo[0], conteo[2] - conteo[4]


  def __minimax(self):
    "Encuentra la mejor jugada utilizando el algoritmo minimax."
    listaMinimax = [None for i in range(len(self.__nodos))]
    movimientos = listaMinimax[:]

    for nodo in self.__valoresMinimax:
      self.__evaluarValores(listaMinimax, movimientos, nodo["valor"], nodo["pc"], nodo)

    self.__movimiento = movimientos[0][:]


  def __evaluarValores(self, listaMinimax: list, listaMovimientos: list, val: int, mov: list, nodo: dict):
    "Elegir el valor correspondiente y subirlo a través del árbol."
    exponente = ((-1) ** (nodo["profundidad"]))
    esMayor = (listaMinimax[nodo["posicion"]] == None) or (listaMinimax[nodo["posicion"]] * exponente < val * exponente)

    if (esMayor):
      listaMinimax[nodo["posicion"]] = val
      listaMovimientos[nodo["posicion"]] = mov

      if (nodo["padre"] != None):
        self.__evaluarValores(listaMinimax, listaMovimientos, val, nodo["pc"], self.__nodos[nodo["padre"]])


  def getMovimiento(self):
    "Retorna el movimiento que debe realizar la IA."
    return self.__movimiento[:]