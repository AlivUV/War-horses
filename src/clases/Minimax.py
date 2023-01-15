from copy import deepcopy

class Minimax:
  """
  Clase para elegir el siguiente movimiento a realizar por la máquina
  con base en el algoritmo minimax.
  """
  __nodos = []
  __listaEspera = []
  __valoresMinimax = []


  def __init__ (self, tablero: list, profundidad: int, pc: tuple, jugador: tuple):
    """
    Función que da inicio al algoritmo minimax.

    Args:
      tablero (list[list[int]]): Tablero de juego.
      profundidad (int): Profundidad a la que llegará el algoritmo. 
      pc (tuple[int]): _description_
      jugador (tuple[int]): _description_
    """
    self.__nodos.clear()
    self.__listaEspera.clear()

    nuevoNodo = {
      "padre": None,
      "posicion": 0,
      "tablero": tablero,
      "pc": pc,
      "jugador": jugador
    }

    self.__listaEspera.append(nuevoNodo)

    self.__minimax(profundidad)


  def __minimax (self, profundidad):
    """
    Bucle que expande los nodos restantes en la lista de espera
    hasta vaciarla o completar la profundidad.
    """
    while (self.__listaEspera != []):
      self.__expandirNodo(self.__listaEspera.pop(0), profundidad)

    for nodo in self.__valoresMinimax:
      if (nodo["valor"] != None):
        print(nodo)


  def __expandirNodo(self, nodo: dict, profundidad: int):
    """
    Añadir el nodo a la lista de nodos y crear sus hijos 
    poniéndolos en la lista de espera.
    """
    nodo["posicion"] = len(self.__nodos)

    jugadorTurno, valor = ("pc", 3) if (nodo["padre"] == None or nodo["padre"] % 2) else ("jugador", 5)

    if(nodo["posicion"] >= profundidad):
      "Evaluar heurística y podar el árbol de nodos."
      self.__heuristica(nodo)
      self.__podarNodos()
      return

    self.__nodos.append(nodo)
    self.__valoresMinimax.append({
      "padre": self.__encontrarPadre(nodo["posicion"] - 1),
      "posicion": len(self.__valoresMinimax),
      "profundidad": nodo["posicion"],
      "valor": None
    })

    jugadasPosibles = self.__evaluarJugadas(nodo, jugadorTurno)

    for jugada in jugadasPosibles:
      self.__crearHijo(nodo, jugada, jugadorTurno, valor)


  def __evaluarJugadas(self, nodo: dict, jugadorTurno: str):
    "Evaluar todos los posibles movimientos del jugador."
    # jugadorTurno, valor = ("pc", 3) if (nodo["padre"] == None or nodo["padre"] % 2) else ("jugador", 5)

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
    # jugadorTurno = "jugador" if (jugada[0] == 5) else "pc"

    nuevoTablero = deepcopy(padre["tablero"])

    if (nuevoTablero[jugada[0]][jugada[1]] == 1):
      nuevoTablero[jugada[0] - 1][jugada[1]] = valor - 1
      nuevoTablero[jugada[0]][jugada[1] - 1] = valor - 1
      nuevoTablero[jugada[0] + 1][jugada[1]] = valor - 1
      nuevoTablero[jugada[0]][jugada[1] + 1] = valor - 1

    nuevoTablero[padre[jugadorTurno][0]][padre[jugadorTurno][1]] = valor - 1
    nuevoTablero[jugada[0]][jugada[1]] = valor

    hijo = {
      "padre": padre["posicion"],
      "pc": padre["pc"],
      "jugador": padre["jugador"],
      "tablero": nuevoTablero
    }

    hijo[jugadorTurno] = jugada[:]

    self.__listaEspera.insert(0, hijo)


  def __heuristica(self, nodo: dict):
    "Dar una puntuación al estado actual del tablero."
    nuevoValor = 0

    for fila in nodo["tablero"]:
      for casilla in fila:
        if (casilla == 2):
          nuevoValor += 1
        elif (casilla == 4):
          nuevoValor -= 1

      self.__seleccionarValor(nuevoValor, (nodo["posicion"] - 1))


  def __podarNodos(self):
    """
    Eliminar de la lista de nodos aquellos que ya no tengan hijos
    en la lista de espera
    """
    # print("A PODAR.")
    while(self.__listaEspera != [] and self.__listaEspera[0]["padre"] != self.__nodos[-1]["posicion"]):
      pos = self.__nodos.pop()["posicion"]
      # val = self.__valoresMinimax[pos]["valor"]

      # self.__seleccionarValor(val, (pos - 1))


  def __seleccionarValor(self, val: int, pos: int):
    "Elegir el menor o mayor valor según el tipo nodo."
    self.__selecValAux(val, pos, self.__valoresMinimax[-1])


  def __selecValAux(self, val: int, pos: int, nodo):
    esMayor = (nodo["valor"] == None) or (nodo["valor"] * ((-1) ** pos) < val * ((-1) ** pos))

    if (esMayor):
      nodo["valor"] = val

      if(nodo["padre"] != None):
        self.__selecValAux(val, pos - 1, self.__valoresMinimax[nodo["padre"]])


  def __encontrarPadre(self, profundidad: int):
    for i in range(-1, -1 - len(self.__valoresMinimax), -1):
      if (self.__valoresMinimax[i]["profundidad"] == profundidad):
        return len(self.__valoresMinimax) + i