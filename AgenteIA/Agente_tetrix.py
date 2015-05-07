# coding=utf-8
__author__ = 'Grupo Tetris'

import random
import json
import pydoc
#import epydoc

class agente:
    """ Este Agente Inteligente que es capaz de resolver una jugada de
    	Tetris utilizando un enfoque heuristico, siendo capaz de Tomar una pieza (Tetrimonio) Examinar las posiciones disponibles en el tablero y enviar la mejor posición donde ubicar la pieza.

	    Las características del ambiente son:
		Parcialmente Observable: Puesto que solo se conoce del ambiente el tablero y			El nombre de la pieza, no se considera la posición de la  Pieza en juego.
		Secuencial: Ya que cada jugada depende del  estado anterior del tablero.
		Dinámico: Cambia sin que agente actué.
		Mono agente: Solo un agente puede controlar el ambiente a la vez
		Continuo: pueden generarse infinitos estados en el ambiente.
		Determinista: El ambiente cambia como el agente espera.

		Arquitectura del Agente
		Agente deliberativo: Toma la mejor decisión basándose en una serie de cálculos
		Lógicos a las posibles posiciones.

		Propiedades:
		El Agente es
		Racional,
		Autónomo
		Persistente
		Taxonomía:
		El Agente simula un Personaje Virtual

    """

    def __init__(self):
        """constructor del Agente inteligente
        Propiedades:
        Tablero : Es un lista que contiene el estado actual del tablero del ambiente
        Nombre : Contiene el nombre del Tetrimonio actula en el ambiente
        Tetrimino :  Contiene un lista que representa a  un tetrimonio y todos sus posibles movimientos
        Tamaño : contiene las dimensiones del tablero un vez que es instanciado el agente
        Ancho : representa la cantidad de celdas horizontales que contiene el ambiente en una fila
        Alto : La cantidad de celdas verticas que tiene el ambiente en una columna
        Pesos : es un Vector que representa la prioridad que se le da a cada parametro de una posiblidad
                estan asignados con respecto a las distintas pruebas realizadas
                en el sigiente orden:
                Profundidad : 100
                Ancho de la ultima linea de un tetrimino: 25 dandole prioridad asi a la forma Horizontas de lso tetriminos
                Area: 24 Detemina el area total que tiene un trtrimonio en esa pocicion en el tablero
                Lineas : 30 la prioridad al completar lineas
                Huecos sobre : 20 cantidad de huecos que quedan una linas bajo en esa posicion
                huecos debajo :40 cantidad d ehuecos ajo la fila x
        Profundidades: es una lista Contiena  Tuplas ( X,Y ) dodne "X" es la fila y "Y" la columna de las putos disponible
        Posibilidades: Contien una lista de tuplas con todas las posible pociciones  de de Form ( X, Y, Z ) y un vector  las caracteristicas de esa posicion
        Clasificador: contiende  el conjunto de  producto punto del vector de pesos con el vector de caracteristicas para cada posicion       
        Conujunto piezas: Es una lista donde estan representados todos los valores de los tetriminos y sus respectivas rotaciones 
        get_Conjunto pieza : Establece todos los valores de tetrimino a la lista de piezas.
        """
        self.Tablero  = []
        self.Tablero_simulado  = []


        self.Nombres = []
        self.nombre=""

        self.Tetrimino = []
        self.Tetrimino_siguinte = []

        self.lector = json.loads(open('json/dimensiones.json').read())
        self.ancho = self.lector[0]
        self.alto = self.lector[1]
        self.pesos = [100, 25, 24, 30,20,40]
        self.profundidades = []
        self.posibilidades = []
        self.clasificador = []

        self.Conjunto_Tetriminos = []
        self.set_Conjunto_Tetriminos()
        self.muestra=[]
        self.mayor=[]
    def set_Conjunto_Tetriminos(self):
        """Este metodo define cada una de las Tetrimonio usados en el Juego"""

        elementoT1 = [[1, 0, 0, 0],
                      [1, 1, 0, 0],
                      [1, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoT2 = [[1, 1, 1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoT3 = [[0, 1, 0, 0],
                      [1, 1, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0]]

        elementoT4 = [[0, 1, 0, 0],
                      [1, 1, 1, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        T = [elementoT2, elementoT3, elementoT4, elementoT1, 'T']

        elementol1 = [[1, 0, 0, 0],
                      [1, 0, 0, 0],
                      [1, 0, 0, 0],
                      [1, 0, 0, 0]]

        elementol2 = [[1, 1, 1, 1],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        i = [elementol1, elementol2, 'i']

        elementoc1 = [[1, 1, 0, 0],
                      [1, 1, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        cu = [elementoc1, 'cu']

        elementoL1 = [[1, 1, 0, 0],
                      [1, 0, 0, 0],
                      [1, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoL2 = [[1, 1, 1, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoL3 = [[0, 1, 0, 0],
                      [0, 1, 0, 0],
                      [1, 1, 0, 0],
                      [0, 0, 0, 0]]

        elementoL4 = [[1, 0, 0, 0],
                      [1, 1, 1, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        LD = [elementoL1, elementoL2, elementoL3, elementoL4, 'LD']

        elementoL5 = [[1, 1, 0, 0],
                      [0, 1, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0]]

        elementoL6 = [[0, 0, 1, 0],
                      [1, 1, 1, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoL7 = [[1, 0, 0, 0],
                      [1, 0, 0, 0],
                      [1, 1, 0, 0],
                      [0, 0, 0, 0]]

        elementoL8 = [[1, 1, 1, 0],
                      [1, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        LI = [elementoL5, elementoL6, elementoL7, elementoL8, 'LI']

        elementoZ1 = [[0, 1, 1, 0],
                      [1, 1, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoZ2 = [[1, 0, 0, 0],
                      [1, 1, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 0]]

        ZD = [elementoZ2, elementoZ1, 'ZD']

        elementoZ3 = [[0, 1, 0, 0],
                      [1, 1, 0, 0],
                      [1, 0, 0, 0],
                      [0, 0, 0, 0]]

        elementoZ4 = [[1, 1, 0, 0],
                      [0, 1, 1, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]

        ZI = [elementoZ3, elementoZ4, 'ZI']
        self.Conjunto_Tetriminos = [ZD, i, cu, T, ZI, LI, LD]

    def sensor(self):
        """Realiza la lectura de un archivo Json
           Datos obtine un Json como una lista con el sigueinte formato:
           [ [Tablero],[nombre_tetrimino],[Lectura/escritura]
           self.Tablero=Establece el valor de la Lectura al Tablero
           self.nombre= estable el nombre del tetrimino
           le lectura solo realiza si el ambiente establece que hay nueva informacion
           y una vez leida se envia un w de respuesta

        """
        Datos = json.loads(open("json/matriz.json").read())
        datos_tetrimino= json.loads(open("json/numero.json").read())


        if (Datos[2] == "l"):
            self.Tablero  = Datos[0]
            self.nombre = Datos[1]


            self.Nombres.append(self.nombre)
            self.Nombres.append(datos_tetrimino[0])

            Datos[2] = "r"
            with open("json/matriz.json", "w") as outfile:
                json.dump(Datos, outfile)

    def get_profundidad(self):
        """ Determina todas la profundidades disponible en el tablero

            Zumacero= contiene todos los ceros posible de cada iteracion
            Listo = detemrina que se encontor el primer 1

        """
        zumacero = 0
        listo = 0
        for i in range(self.ancho):
            for j in range(self.alto):
                if self.Tablero [j][i] == 0:
                    zumacero += 1
                else:
                    listo = 1
                    break
            if listo == 1:
                self.profundidades.append((zumacero - 1, i))
                zumacero = 0
            if j == self.alto - 1:
                self.profundidades.append((self.alto - 1, i))
                zumacero = 0

    def get_dimensiones_pieza(self, rotacion):
        """Retorna una tupla con las dimenciones de de ancho y alto de la pieza

         Parámetros:
         R -- Rotacion del tetrimino

         Retorna:
          Tubla ( F,C ) con el alto y ancho de un tetrimonio

        """
        ancho = 0
        alto = 0

        for filas in range(4):
            for columnas in range(4):
                if self.Tetrimino[rotacion][filas][columnas] == 1:
                    if ancho <= columnas:
                        ancho = columnas

                    if alto <= filas:
                        alto = filas

        return (alto + 1, ancho + 1)


    def clasificador_ganador(self):
        """Este metodo realiza el producto punto entre el vector de pesos y el vector de caracterisitica  y los almacena en una lista"""

        for coordenada in range(len(self.posibilidades)):
            self.clasificador.append((coordenada, self.producto_punto(self.posibilidades[coordenada][1], self.pesos)))
        sorted(self.clasificador)

    def set_pieza(self, nombre):
        """Este Metodo establece el Valor de la Pieza
         o tetrimonio actual partiendo del Nombre recibido como parametro
         :param
         nombre -- el nombre recibido por el sensor
         """


        self.nombre=nombre


        for i in range(len(self.Conjunto_Tetriminos)):
            if nombre == self.Conjunto_Tetriminos[i][len(self.Conjunto_Tetriminos[i]) - 1]:
                self.Tetrimino = self.Conjunto_Tetriminos[i]
                break




    def get_calculos_posiciones(self):
        """Determina todas la posibles soluciones apartir de la espacio mas profundo, area de la pieza y la posible lineas a deshacer

        variables:
            indices : es un tupla que contiene las dimencines de cada rotacion
            que se utilizara como parametro para deliminar el area a examinar del ambiente
            X : posicion de la fila  en a la i-nesima profundidad
            Y : posicion d ela columna en  i-nesima profundidad
            F : Dimencion fila
            C : Dimension Clumna
            Colicion_derecha =toma una tupla   si  en esa profundidad el tetrimino puede ser colocada y uno si colisiona  las linea sy el area
            Colicion_Iz= toma una tupla   si  en esa profundidad el tetrimino puede ser colocada
                    y uno si colisiona  las linea sy el area pero se envia como parametor y-1
                    para tomar un set una posicion a la izquierda
            Colicion_L= toma una tupla   si  en esa profundidad el tetrimino puede ser colocada
                    y uno si colisiona  las linea sy el area pero se envia como parametor y-2
                    para tomar un set dos posicion a la izquierda  para ciertas piezas
            Ultima_linea: determina la cuantas celdas hay la parte inferir dle tetrimonio
            Espacios debajo : Contiene los huecos que hay bajo el set de comparacion



        """

        for rotacion in range(len(self.Tetrimino) - 1):


            indices = self.get_dimensiones_pieza(rotacion)

            for coordenada in range(len(self.profundidades)):


                X=self.profundidades[coordenada][0]
                Y=self.profundidades[coordenada][1]
                F=indices[0]
                C=indices[1]

                # DETERMINA SI ES UNA SOLUCCION POSIBLE
                #para todas
                self.Caracteristicas(rotacion, X,Y, F,C,"DER")
                #solo para la tetrimino derecho
                if self.nombre=="LI" or self.nombre=="LD":
                    self.Caracteristicas(rotacion, X,Y - 2, F, C,"LD-2")
                 #solo para la tetrimino derecho
                if self.nombre=="LI":
                    self.Caracteristicas(rotacion, X+1,Y - 2, F, C,"LI-2")

                #movimiento a la izquierda
                if (self.nombre == "LI" and rotacion == 0) \
                    or (self.nombre == "cu") \
                    or (self.nombre == "ZI" and rotacion == 1) \
                    or (self.nombre == "ZD" and rotacion == 0) \
                    or (self.nombre == "T" and (rotacion == 0 or rotacion == 3) ):
                    self.Caracteristicas(rotacion, X,Y - 1, F, C,"IZQ")



                #comparaciones topes superiores Z y T derecho
                if  (self.nombre == "ZD") \
                    or (self.nombre == "T" and (rotacion == 0 or rotacion == 1) ):
                    self.Caracteristicas(rotacion, X+1,Y, F, C,"SZTD")

                #comparacion topes Z y T Izquierdo

                if (self.nombre == "ZD" ) \
                    or (self.nombre == "T" and (rotacion == 0 or rotacion == 3) ):
                    self.Caracteristicas(rotacion, X+1,Y - 1, F, C,"IZQ")




                #comparaciones topes izquierdos
                if (self.nombre == "LD" and rotacion == 0) :

                    self.Caracteristicas(rotacion,X+2,Y-1,F,C,"SLDI")
                    self.Caracteristicas(rotacion,X+2,Y+1,F,C,"SLDD")
                    self.Caracteristicas(rotacion,X+2,Y,F,C,"SLD")

                #comparaciones topes derechos
                if (self.nombre == "LI" and rotacion == 0) :

                    self.Caracteristicas(rotacion,X+2,Y-1,F,C,"SLID")
                    self.Caracteristicas(rotacion,X+2,Y+1,F,C,"SLID")
                    self.Caracteristicas(rotacion,X+2,Y,F,C,"SLID")

                #comparaciones topes  Z y T izquierdos
                if (self.nombre == "ZD" and rotacion == 7)\
                    or (self.nombre == "T" and (rotacion == 0 or rotacion == 3) ):


                    self.Caracteristicas(rotacion,X+1,Y-1,F,C,"SZTI")


                #comparaciones topes  Z y T izquierdos
                if (self.nombre == "ZI" and rotacion == 0)\
                    or (self.nombre == "T" and (rotacion == 0 or rotacion == 1) ):


                    self.Caracteristicas(rotacion,X+1,Y+1,F,C,"SZTD")




    #METODS UTILIZADOS PARA DETERMINAR LAS CARACTERISITICAS DE CADA POSICION
    def Caracteristicas(self, R, X, Y, F, C,N):
        """     X : posicion de la fila  en a la i-nesima profundidad
            Y : posicion d ela columna en  i-nesima profundidad
            F : Dimencion fila
            C : Dimension Columna"""

        coliciono = 0
        area = 0
        lineas = 0
        huecos=0
        bloqueo=0
        ultima=0
        espacios=0

        try:

            for i in range(F):
                for j in range(C):
                    if self.Tetrimino[R][i][j] + self.Tablero [(X - F) + i + 1][Y + j] > 2:
                        coliciono = 1
                        break
                    else:
                        if self.Tetrimino[R][i][j] + self.Tablero [(X - F) + i + 1][Y + j] >= 1:
                            area += 1

                if coliciono == 1:
                    break

            lineas = self.get_lineas(X, R, F, C)




        except:

            coliciono = 1

        if Y < 0:
            coliciono =1

        if  coliciono ==0:
            huecos=self.get_huecos(X,Y,R,F,C)
            bloqueo=self.bloqueoPorObstaculo(R,X,Y,F,C,N)
            ultima=self.get_cantidad_fila_pieza(R,F,C)
            espacios=self.agujeros_columnas(X+1,Y,C)



        if bloqueo==1:
            coliciono=1

        if coliciono==0:
             self.posibilidades.append(((X, Y, R), ( X,ultima, area, lineas, 10/(huecos+10),10-espacios, N,F,C)))




    def get_lineas(self, X, R, F, C):
        """Detemina  la cantidad de lineas de complet aun tetrimino """
        lineas = 0

        for i in range(F):

            if self.get_espacios(X - i) == self.get_cantidad_fila_pieza(R, F - i, C):
                lineas += 1
        return lineas

    def get_huecos(self, X,Y, R, F, C):
        """retorma la cantidad de huecos segun una posicion especifica"""
        Ultima_lineas = self.get_cantidad_fila_pieza(R, F, C)
        espacios= self.agujeros_columnas(X,Y, C)
        huecos=espacios-Ultima_lineas
        return huecos


    def producto_punto(self, valores, pesos):
        """realiza el producto punto entre dos vectores"""
        return sum(valor * pesos for valor, pesos in zip(valores, pesos))



    def control(self):
        """Ejecuta todas las Operaciones del Agente"""
        self.sensor()
        self.comparador=[]
        for i in range(2):
            self.get_profundidad()

            self.set_pieza(self.Nombres[i])

            self.get_calculos_posiciones()

            self.clasificador_ganador()


            self.comparador.append(self.get_posicion_ganadora())

            self.profundidades = []
            self.posibilidades = []
            self.clasificador = []

        if self.comparador[0][0][0]>self.comparador[1][0][0] and self.comparador[0][1]>self.comparador[1][1]:

            self.set_pieza(self.Nombres[0])
            self.efector(self.comparador[0][0])
            for i in range(len(self.clasificador)):
               print("peso", self.posibilidades[i], self.clasificador[i])
        else :

              self.set_pieza(self.Nombres[0])
              self.get_profundidad()
              self.get_calculos_posiciones()
              self.clasificador_ganador()

              for i in self.clasificador:
                if i[0]==self.comparador[0][0][0]:
                    e=1
                    #parea eliminar las posubilidades del anteriro

              for i in range(len(self.clasificador)):
                  print("peso", self.posibilidades[i], self.clasificador[i])


              ganador=self.get_posicion_ganadora()
              self.efector(ganador[0])



    """NUEVOS METODOS PARA MEJORAR LOS CALCULOS DEL AGENTE INTELIGENTE"""

    def get_espacios(self, X):
        """Este metodo detemrian la cantidad de Espacios en cada Linea de la Matriz """
        espacios = 0

        for j in range(self.ancho):
            if self.Tablero [X][j] == 0:
                espacios += 1

        return espacios

    def efector(self, ganador):

        """despues de encontrar la mejor posicion envia la cordenada y la rotacion atravez de socket
           en formato revision
        """

        lector = json.loads(open('json/Efector.json').read())
        dimensiones = self.get_dimensiones_pieza(ganador[2])
        if (lector[3] != "l"):
            datos = ganador[0], ganador[1], ganador[2], "l", dimensiones[0]
            with open('json/Efector.json', 'w') as outfile:
                json.dump(datos, outfile)

    def get_posicion_ganadora(self):
        """Obtiene la posicion y la rotacion con la mayor prioridad"""

        mayor_peso = 0
        indice_ganador = 0

        for i in range(len(self.clasificador)):

            if self.clasificador[i][1] > mayor_peso:
                mayor_peso = self.clasificador[i][1]
                indice_ganador = i


        return self.posibilidades[indice_ganador][0],mayor_peso

    def bloqueoPorObstaculo(self,R,X,Y,F,C,N):
        """Este metodo elimina las posiblidad en las que el ambiente no puede ejecutar correctamente """
        try:
            colisiono=0
            #iterar c cantidad de veces
            for j in range(C):
                # identificar el indice de la cuulmna
                indice=self.altura_columna_pieza(R,j,F,C)

                for i in range(X-indice+1):

                    if(self.Tablero [i][Y+j] != 0):
                        colisiono=1
                        break

        except:
            colisiono=1
        return colisiono

    def altura_columna_pieza(self,R,J,F,C):

        # Retorna el ensimo tama;o de una pieza
        indice= 0
        for i in range(F):
            if self.Tetrimino[R][i][J] == 1:
                indice =  i
                break
        return F-indice




    #FUNCIONES ADISIONALES

    def iniciarmapa(self, N):
        """Este metodo asigna valor iniciales a la matriz pudiendo crear dificultas """
        for i in range(self.alto):
            self.Tablero .append([])
            for j in range(self.ancho):
                self.Tablero [i].append([])

        for i in range(self.alto):
            for j in range(self.ancho):
                self.Tablero [i][j] = 0

        for i in reversed(range(5, self.alto)):
            for j in range(self.ancho):
                self.Tablero [i][j] = random.randint(0, N)


    def get_imprimir_tablero(self):
        """permite visualizar los valores del tablero """
        print ('matriz')
        print("         0 1 2 3 4 5 6 7 8 9 " )
        for i in range(self.alto):
            print("( " + str(i) + " )" ,(self.Tablero [i]))


    def nuevas_Profundidas(self):
        """ calcula todos los posibles posisicioens basandose en la primeras profundidades """

        for i in range(len(self.profundidades)-1):
            if(self.profundidades[i+1][0] < self.profundidades[i][0]):
                dif = self.profundidades[i][0] - self.profundidades[i+1][0]
                for j in range(dif):
                    self.nProfundidades.append((self.profundidades[i][0] - j,self.profundidades[i][1]))

        for i in range(len(self.nProfundidades)):
            self.profundidades.append(self.nProfundidades[i])

    def Guardar_matriz(self):

        """Guarda el ultimo estado d ela matriz en un archivo Json
        """
        datos = [self.Tablero , "r"]
        with open('matriz.json', 'w') as outfile:
            json.dump(datos, outfile)

        return 0



    def agujeros_columnas(self, X, Y, C):
        """Este metodo detemrian la cantidad de Espacios en cada Linea de la Matriz """
        espacios_debajo = 0

        try:
            for j in range(C):
                if self.Tablero [X][Y + j] == 0:
                    espacios_debajo += 1
        except:
            return espacios_debajo
        return espacios_debajo

    def espacios_piezas(self, X, Y,F, C):
        """Este metodo detemrian la cantidad de Espacios en cada Linea de la Matriz """
        espacios_debajo = 0

        try:
            for j in range(C):
                if self.Tablero [X][Y + j] == 0:
                    espacios_debajo += 1
        except:
            return espacios_debajo
        return espacios_debajo

    def get_espacios_columnas_todas(self, X, Y, C):
        """Este metodo determinar  cantidad de Espacios en cada Linea de la Matriz """
        espacios_debajo = 0

        try:
            for i in range(self.alto - X):
                for j in range(C):
                    if self.Tablero [X + i + 1][Y + j] == 0:
                        espacios_debajo += 1

        except:
            espacios_debajo += 1
            return espacios_debajo
        return espacios_debajo


    def get_cantidad_fila_pieza(self, R, F, C):
        """ Determinana la cantidad de lineas en  un pieza """
        ocupa = 0
        for j in range(C):
            if self.Tetrimino[R][F - 1][j] == 1:
                ocupa += 1
        return ocupa

    def get_ultima_fila_pieza(self, R, F):
        """Determina el espacion entre la ultima fila del tetrimino"""
        ocupa = 0
        for j in range(F):
            if self.Tetrimino[R][F - 1][j] == 1:
                ocupa += 1
        return ocupa





    def set_cambios_tablero(self, coordenada):
        """Estable los cambios en el tablero """
        dimemciones = self.get_dimensiones_pieza(coordenada[1])

        for fila in range(dimemciones[0]):

            for columna in range(dimemciones[1]):

                try:
                    self.Tablero [coordenada[0][0] - fila][coordenada[0][1] + columna] = \
                        self.Tetrimino[coordenada[1]][dimemciones[0] - fila - 1][columna]

                except:
                    print("grave error")









