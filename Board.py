#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2015 hllanos <hllanos@pcllanos>

import pprint
import json
import cargas

class Board:
    """
    Inicializa todos lo valores del juego
    parametros
    cargas            -- Instancia todos lo objetos a utilizar en el juego
    board_width       -- ancho de la superficie del juego
    board_hight       -- alto de la superficie del juego
    enviar            -- establece las dimensiones de la surpeficie de juego
    tablero           -- matriz del juego
    iniciarmapa       -- utilizada para la busqueda de filas completas de piezas
    lineas            -- contador
    filas_encontradas -- matriz que guardas todos las lineas completas encontradas
    """
    
    def __init__(self, ancho, alto):
        self.cargas = cargas.Cargas()
        self.board_width = ancho
        self.board_hight = alto
        enviar = self.board_width, self.board_hight
        with open('json/dimensiones.json','w') as outfile:
            json.dump(enviar,outfile)
        self.tablero = []
        self.iniciarmapa()
        self.lineas = 0
        self.filas_encontradas = []

    #----------------------------------------------------------------------------------------#

    def iniciarmapa(self):
        """
        Inicializa el tablero de juego.

        inicializa con cero toda el tablero de juego
        """
        for i in range(self.board_hight):
            self.tablero.append([])
            for j in range(self.board_width):
                self.tablero[i].append([])

        for i in range(self.board_hight):
            for j in range(self.board_width):
                self.tablero[i][j] = 0

    #----------------------------------------------------------------------------------------#

    def encontrar_linea(self, fila):
        """
        Encuentra las filas completadas.

        Mueve el tablero de piezas que se encuentra sobre la linea compleatada una fila hacia abajo, 
        esto lo hace recursivamente luego  aumenta el score de lineas completadas 

        """
        suma = 0
        for j in range(self.board_width):
            suma = suma + self.tablero[fila][j]

        if suma == self.board_width * 2:
            self.lineas += 1
            if fila == 0:
                for j in range(self.board_width):
                    self.tablero[fila][j] = 0

            else:
                for i in reversed(range(fila + 1)):
                    for j in range(self.board_width):
                        if (i != 0):
                            self.tablero[i][j] = self.tablero[i - 1][j]
                        else:
                            self.tablero[i][j] = 0
                self.encontrar_linea(fila)

        elif (fila > 0):
            self.encontrar_linea(fila - 1)

    #----------------------------------------------------------------------------------------#

    def lineas_formadas(self, fila):

        suma = 0
        for j in range(self.board_width):
            suma = suma + self.tablero[fila][j]

        if suma == self.board_width * 2:
            self.filas_encontradas.append(fila)
            if fila == 0:
                ''''''
            else:
                self.lineas_formadas(fila-1)
        elif (fila > 0):
            self.lineas_formadas(fila - 1)

    #----------------------------------------------------------------------------------------#

    def estampar_pieza(self, x, y):
        """
        Estampa una pieza en el tablero

        estampa una pieza de tetris
        cuando una pieza toca la superficie baja o colisiona con una pieza muerta

        parametros:
        x -- coordenada x de la pieza
        y -- coordenada y de la pieza

        """
        try:
            self.tablero[int(x)][int(y)] = 2
        except:
            b = 0



