from copy import deepcopy


class Minimax:
    """
    Clase para elegir el siguiente movimiento a realizar por la máquina
    con base en el algoritmo minimax.
    """
    __nodos = []
    __listaEspera = []
    __valoresMinimax = []
    __movimientos = []
    __movimiento = [0, 0]

    def __init__(self, tablero: list, nivel: int):
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
        self.__valoresMinimax.clear()
        self.__movimientos.clear()

        casLibres, valorNodo, pc, jugador = self.__contarCasillas(tablero)

        nuevoNodo = {
            "padre": None,
            "profundidad": 0,
            "pc": pc,
            "jugador": jugador,
            "tablero": deepcopy(tablero),
            "casillasLibres": casLibres,
            "valor": valorNodo,
            "posicion": 0
        }

        self.__listaEspera.append(nuevoNodo)

        self.__profundidad(nivel * 2)

        self.__movimiento = self.__movimientos[0]

        self.__nodos.clear()
        self.__valoresMinimax.clear()
        self.__movimientos.clear()

    def __contarCasillas(self, tablero: list):
        "Recorrer el tablero para saber la cantidad de casillas libres"
        conteo = [0, 0, 0, 0, 0, 0]
        posiciones = [[], [], [], [], [], []]

        for i in range(len(tablero)):
            for j in range(len(tablero[0])):
                conteo[tablero[i][j]] += 1
                posiciones[tablero[i][j]] = [i, j]

        return conteo[0], conteo[2] - conteo[4], posiciones[3], posiciones[5]

    def __profundidad(self, profundidad: int):
        """
        Bucle que expande los nodos restantes en la lista de espera
        hasta vaciarla o completar la profundidad.
        """
        while (self.__listaEspera != []):
            self.__expandirNodo(self.__listaEspera.pop(0), profundidad)

    def __expandirNodo(self, nodo: dict, profundidad: int):
        """
        Añadir el nodo a la lista de nodos y crear sus hijos 
        poniéndolos en la lista de espera.
        """
        nodo["posicion"] = len(self.__nodos)

        jugadorTurno, valor = ("pc", 3) if (
            nodo["profundidad"] % 2 == 0) else ("jugador", 5)

        if (nodo["profundidad"] < profundidad):
            self.__nodos.append(nodo)
            self.__valoresMinimax.append(None)
            self.__movimientos.append(None)

            for jugada in self.__evaluarJugadas(nodo, jugadorTurno):
                self.__crearHijo(nodo, jugada, jugadorTurno, valor)

            del nodo["tablero"]
        else:
            self.__evaluarHoja(nodo)
            self.__poda()

    def __evaluarJugadas(self, nodo: dict, jugadorTurno: str):
        "Evaluar todos los posibles movimientos del jugador."

        jugadas = []

        for pos in range(8):
            i = nodo[jugadorTurno][0] + ([1, 2][pos % 2] * pow(-1, pos // 2))
            j = nodo[jugadorTurno][1] + \
                ([1, 2][pos % 2] * 2 % 3) * pow(-1, pos // 4)

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
            aumentoValor += self.__agarrarPoder(jugada[0],
                                                jugada[1], valor, nuevoTablero)

        nuevoTablero[padre[jugadorTurno][0]
                     ][padre[jugadorTurno][1]] = valor - 1
        nuevoTablero[jugada[0]][jugada[1]] = valor

        hijo = {
            "padre": padre["posicion"],
            "profundidad": padre["profundidad"] + 1,
            "pc": padre["pc"][:],
            "jugador": padre["jugador"][:],
            "tablero": nuevoTablero,
            "casillasLibres": padre["casillasLibres"] - aumentoValor,
            "valor": padre["valor"] + (aumentoValor * ((-1) ** (padre["profundidad"])))
        }

        hijo[jugadorTurno] = jugada[:]

        self.__listaEspera.insert(0, hijo)

    def __agarrarPoder(self, i: int, j: int, jugador: int, tablero: list):
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
        casillasAfectadas = 0

        for [di, dj] in direcciones:
            if (di + i < 0 or dj + j < 0):
                continue

            try:
                if (tablero[di + i][dj + j] == 0):
                    tablero[di + i][dj + j] = jugador - 1
                    casillasAfectadas += 1
            except:
                "La posición está fuera del rango de la lista"
                continue

        return casillasAfectadas

    def __evaluarHoja(self, nodo: dict):
        self.__valoresMinimax[nodo["padre"]] = nodo["valor"]
        self.__movimientos[nodo["padre"]] = nodo["pc"]

        while (self.__listaEspera != [] and nodo["padre"] == self.__listaEspera[0]["padre"]):
            hermano = self.__listaEspera.pop(0)
            if (hermano["valor"] < self.__valoresMinimax[nodo["padre"]]):
                self.__valoresMinimax[nodo["padre"]] = hermano["valor"]
                self.__movimientos[nodo["padre"]] = hermano["pc"]

    def __poda(self):
        "Eliminar los nodos que no tengan hijos."
        while (self.__listaEspera != [] and self.__nodos[-1]["posicion"] != self.__listaEspera[0]["padre"]):
            # print("Antes: ", self.__valoresMinimax)
            self.__movimientos.pop()
            self.__subirValor(self.__valoresMinimax.pop(),
                              self.__nodos[-1]["pc"], self.__nodos.pop())
            # print("Después: ", self.__valoresMinimax)

        if (self.__listaEspera != []):
            return

        while (self.__nodos[-1]["padre"] != None):
            self.__movimientos.pop()
            self.__subirValor(self.__valoresMinimax.pop(),
                              self.__nodos[-1]["pc"], self.__nodos.pop())

    def __subirValor(self, val: int, mov: list, nodo: dict):
        "Elegir el valor correspondiente y subirlo a través del árbol."
        if (nodo["padre"] == None):
            return

        exponente = ((-1) ** (nodo["profundidad"] - 1))
        debeSubir = (self.__valoresMinimax[nodo["padre"]] == None) or (
            self.__valoresMinimax[nodo["padre"]] * exponente < val * exponente)

        if (not debeSubir):
            return

        self.__valoresMinimax[nodo["padre"]] = val
        self.__movimientos[nodo["padre"]] = mov

    def __podaAB(self):
        "Usar el algoritmo de poda alfa y beta."

    def getMovimiento(self):
        "Retorna el movimiento que debe realizar la IA."
        return self.__movimiento[:]
