#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2015 hllanos <hllanos@pcllanos>

 

import pygame
"""
clase que representa los sprites del juego

contiene las propiedades y el comportamiento de los sprites

propiedades:

image	-- define la imagen del sprite
rect	-- define el rectangulo  y la posicion del sprite
mascara -- propiedad para determinar colision en sprites
left	-- alejamiento del sprite con respecto al marco izquierdo
top		-- altura del sprite con respecto a la altura del marco de juego
rapido	-- velocidad de moviento del sprite
"""

class figura (pygame.sprite.Sprite):
	def __init__(self, dibujo, posx, posy):
		pygame.sprite.Sprite.__init__(self)
		self.image = dibujo
		self.rect = dibujo.get_rect()
		self.mascara = pygame.mask.from_surface(self.image)
		self.rect.left = posx
		self.rect.top = posy
		self.rapido = False
		#self.image.set_colorkey((255,255,255))

	def update(self, tecla):
		if(tecla == pygame.K_UP):
			self.image = pygame.transform.rotate(self.image, -90)
		
		if(tecla == pygame.K_LEFT):
			
				self.rect.move_ip(-25,0)
			
		if(tecla == pygame.K_RIGHT):
			
			self.rect.move_ip(25,0)
		
		if(tecla == pygame.K_DOWN):	
			if self.rapido == False:
				self.rect.move_ip(0,2)
			else:
				self.rect.move_ip(0,5)


class ayuda(pygame.sprite.Sprite):
    def __init__(self, dibujo):
        pygame.sprite.Sprite.__init__(self)
        self.image = dibujo
        self.mascara = pygame.mask.from_surface(self.image)

    def update(self, tecla):
        if (tecla == pygame.K_UP):
            self.image = pygame.transform.rotate(self.image, -90)