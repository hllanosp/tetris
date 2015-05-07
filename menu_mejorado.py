#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pruebajson.py
#  
#  Copyright 2015 hllanos <hllanos@pcllanos>

#  
import cargas
import random
import pygame
from pygame.locals import *


class Opcion:
    """
    Representa una opcion en 
    """
    def __init__(self, titulo, x, y, paridad, funcion_asignada):
        """
        inicializa todos los valores a utilizar en la partes de menu

        param
        cargas           -- intancia de cargas de todos los metodos del juego
        fuente1          -- fuente utilizada para titulos
        fuente2          -- fuente utilizada para titulos
        imagen_normal    -- redendiza el titulo normal
        imagen_destacada -- redendiza el titulos principales
        image            -- almacena el titulo
        rect.x           -- coordenada en x del menu
        rect.y           -- coordenada en y del menu
        rect             -- dibuja el rectangulo del titulo
        funcion_asignada --
        x                --
        """
        self.cargas = cargas.Cargas()
        self.fuente1 = pygame.font.Font('fonts/transformers_movie.ttf', 20)
        self.fuente2 = pygame.font.Font('fonts/transformers_movie.ttf', 30)
        self.imagen_normal = self.fuente1.render(titulo, 2, (233, 249, 255))
        self.imagen_destacada = self.fuente2.render(titulo, 1, (58,140, 191))
        self.image = self.imagen_normal
        self.rect = self.image.get_rect()
        self.rect.x = 500 * paridad
        self.rect.y = y
        self.funcion_asignada = funcion_asignada
        self.x = float(self.rect.x)

    def actualizar(self,X):
        destino_x = X
        self.x += (destino_x - self.x) / 5.0
        self.rect.x = int(self.x)

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)

    def destacar(self, estado):
        if estado:
            self.image = self.imagen_destacada

        else:
            self.image = self.imagen_normal

    def activar(self):
        self.funcion_asignada()


class Cursor:
    def __init__(self, x, y, dy):
        self.image = pygame.image.load('images/cursor.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x+60
        self.y_inicial = y-5
        self.dy = dy
        self.y = 0
        self.seleccionar(0)

    def actualizar(self):
        self.y += (self.to_y - self.y) / 10.0
        self.rect.y = int(self.y)

    def seleccionar(self, indice):
        self.to_y = self.y_inicial + indice * self.dy

    def imprimir(self, screen):
        screen.blit(self.image, self.rect)
