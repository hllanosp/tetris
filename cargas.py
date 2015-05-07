#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015 hllanos <hllanos@pcllanos>


import pygame
import pieza
import random
import json


class Cargas:
    def __init__(self):
        """
        carga imagenes y archivos de Disco Duro.
        cuenta con todas las imagenes como ser marcos marcadores etc.

        param:
        Imagenes
        lista_tetris     -- tiene la lista de sprites de figuras
        inicializar_piezas -- inicializa todos los sprites de piezas utilizados en el juego
        game_over        -- imagen que retorna cuando termina el juego
        I_bajo           -- imagen utilizado como marco inferior
        I_marcoderecho   -- imagen utilizado como marco derecho
        I_marcoizquierdo -- imagen utilizado como marco izquierdo
        fondo            -- imagen que dibuja la matriz del juego
        I_muerta         -- imagen que muestra cuando es pieza muerta
        I_marcador       -- imagen que muestra el puntaje del juego
        menu             -- imagen utilizada para rellenar las opciones del juego
        cargando         -- imagen utilizada para la informacion de controles del juego
        paused           -- imagen utilizada cuando es pausado el juego
        fondo_juego      -- imagen que dibuja la matriz en la pantalla del juego

        Sonidos
        girar            -- sonido cuando la pieza realiza un giro
        down             -- sonido cuando se la aplica mayor velocidad
        sonido_lineas    -- sonido cuando se ha eliminado una fila
        sonido_cursor    -- sonido cuando se desplaza en las opciones del juego
        sonido_rapido    -- sonido cuando se le da mayor velocidad al juego

        Fuentes
        font_transform    -- tipo de fuente para titulos
        font_felicitacion -- tipo letra cuando ha superado la puntuacion
        lista_nombres     -- arreglo que guarda cada nombre de cada figura

        """
        pygame.init()
        self.lista_tetris = []
        self.inicializar_piezas()
        self.I_bajo = pygame.image.load('images/columnabaja.png')
        self.I_marcoderecho = pygame.image.load('images/columna_der.png')
        self.I_marcoizquierdo = pygame.image.load('images/columna_izq.png')
        self.fondo = pygame.image.load('images/fondo.png')
        self.I_muerta = pygame.image.load('images/M.png')
        self.I_marcador = pygame.image.load('images/marcador.jpg').convert()
        self.menu = pygame.image.load("images/menu.png")
        self.cargando = pygame.image.load("images/cargando.png")
        self.paused = pygame.image.load("images/paused.jpg").convert()
        self.girar = pygame.mixer.Sound('sonidos/rotate.wav')
        self.down = pygame.mixer.Sound('sonidos/down.wav')
      
        self.fondo_juego = pygame.image.load('images/fondo_juego2.png')
        self.font_transform = pygame.font.Font("fonts/transformers_movie.ttf", 30)
        self.font_felicitacion = pygame.font.Font("fonts/transformers_movie.ttf",50)
        self.font_score = pygame.font.Font("fonts/classhvy.ttf",20)
        self.font_score2 = pygame.font.Font("fonts/classhvy.ttf",25)
        self.credito = pygame.image.load('images/credito.png')
        self.sonido_lineas = pygame.mixer.Sound('sonidos/linea.wav')
        self.sonido_cursor = pygame.mixer.Sound('sonidos/sonido_cursor.wav')
        self.lista_nombres = ['cu', 'i', 'LI', 'LD', 'ZI', 'ZD', 'T']
        self.sonido_rapido = pygame.mixer.Sound('sonidos/velocidad.wav')
        self.animacion_sheet = pygame.image.load('images/a.png')
        self.textbox = pygame.image.load('images/textbox.jpg').convert()
        self.sonido_caer = pygame.mixer.Sound('sonidos/CRASH6.WAV')
        self.marcador = pygame.image.load('images/score.jpg').convert()
        self.font_digital = pygame.font.Font('fonts/digital.ttf',30)
        self.sonido_game = pygame.mixer.Sound('sonidos/game_over.wav')

    def inicializar_piezas(self):
        """
        inicializa los sprites del tetrix.

        crea una lista de sprites
        """
        C_imagen = pygame.image.load("images/cu.png")
        C = pieza.figura(C_imagen, 125, 0)

        CA_imagen = pygame.image.load("images/help's_images/cu.png")
        CA = pieza.ayuda(CA_imagen)

        I_imagen = pygame.image.load("images/i.png")
        I = pieza.figura(I_imagen, 125, 0)

        IA_imagen = pygame.image.load("images/help's_images/i.png")
        IA = pieza.ayuda(IA_imagen)

        LI_imagen = pygame.image.load('images/LI.png')
        LI = pieza.figura(LI_imagen, 125, 0)

        LIA_imagen = pygame.image.load("images/help's_images/LI.png")
        LIA = pieza.ayuda(LIA_imagen)

        LD_imagen = pygame.image.load('images/LD.png')
        LD = pieza.figura(LD_imagen, 125, 0)

        LDA_imagen = pygame.image.load("images/help's_images/LD.png")
        LDA = pieza.ayuda(LDA_imagen)

        ZI_imagen = pygame.image.load('images/ZI.png')
        ZI = pieza.figura(ZI_imagen, 125, 0)

        ZIA_imagen = pygame.image.load("images/help's_images/ZI.png")
        ZIA = pieza.ayuda(ZIA_imagen)

        ZD_imagen = pygame.image.load('images/ZD.png')
        ZD = pieza.figura(ZD_imagen, 125, 0)

        ZDA_imagen = pygame.image.load("images/help's_images/ZD.png")
        ZDA = pieza.ayuda(ZDA_imagen)

        T_imagen = pygame.image.load('images/T.png')
        T = pieza.figura(T_imagen, 125, 0)

        TA_imagen = pygame.image.load("images/help's_images/T.png")
        TA = pieza.ayuda(T_imagen)

        self.lista_tetris = [C_imagen, I_imagen, LI_imagen, LD_imagen, ZI_imagen, ZD_imagen, T_imagen]
        self.lista_ayuda = [CA_imagen, IA_imagen, LIA_imagen, LDA_imagen, ZIA_imagen, ZDA_imagen, TA_imagen]

    def get_sprite(self):
        """
        retorna una pieza aleatoria aleatoria

        """
        numero = random.randint(0, 6)
        lector = json.loads(open('json/numero.json').read())
        lector[1] = lector[0]
        lector[0] = self.lista_nombres[numero]
        lector[2] = numero
        with open('json/numero.json', 'w') as outfile:
            json.dump(lector, outfile)

        return (self.lista_tetris[numero])

    def get_sprite_help(self):
        lector = json.loads(open('json/numero.json').read())
        return(self.lista_ayuda[lector[2]])

    def get_over(self):
        return self.game_over

    def get_marco_bajo(self):
        marco_bajo = pieza.figura(self.I_bajo, 0, 500)
        return marco_bajo

    def get_marco_derecho(self):

        marco_izquierdo = pieza.figura(self.I_marcoderecho, 275, 0)
        return marco_izquierdo

    def get_marco_izquierdo(self):
        marco_derecho = pieza.figura(self.I_marcoizquierdo, 0, 0)
        return marco_derecho

    def get_muerta(self):

        return self.I_muerta

    def get_marcador(self):
        return self.I_marcador

    def get_menu(self):
        return self.menu

    def get_cargando(self):
        return self.cargando

    def get_paused(self):
        return self.paused

    def get_girar(self):
        return self.girar

    def get_down(self):
        return self.down

    def get_sonido_linea(self):
        return self.sonido_lineas


    def get_sonido_cursor(self):
        return self.sonido_cursor

    def get_sonido_rapido(self):
        return self.sonido_rapido
