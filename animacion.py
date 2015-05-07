
import pygame
import sys

class animacion(pygame.sprite.Sprite):
	def __init__(self, dibujo, posx, posy, visor):
		pygame.sprite.Sprite.__init__(self)
		self.image = dibujo
		self.visor =  visor
		self.cont = 0
		self.frame_num = 0
		self.frame_ancho = 300
		self.frame_alto = 25
		self.rect = pygame.Rect(posx, posy, self.frame_ancho, self.frame_alto)


	def update(self):
		if self.cont < 12:
			self.frame_num +=1
			self.cont = 0

		else:
			self.cont = 0

	def draw(self):
		contador = 0
		pygame.time.set_timer(pygame.USEREVENT, 20)
		while contador < 23:
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT:
					print('animacion')
					contador +=1
					area_recorte = pygame.Rect(0, self.frame_num *25, self.frame_ancho , self.frame_alto)
					self.visor.blit(self.image, self.rect , area_recorte)
					self.update()
					pygame.display.update()
