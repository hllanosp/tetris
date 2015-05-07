# -*- coding: utf-8 -*-
import pygame, pygame.font, pygame.event, pygame.draw, string, cargas, sys, json
from pygame.locals import *


class usuario:
    def __init__(self, visor):
        self.screen = visor
        self.cargas = cargas.Cargas()

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                pass

    def display_box(self, message):
        "Print a message in a box in the middle of the screen"
        fontobject = self.cargas.font_score
        felicitacion = self.cargas.font_felicitacion
        self.screen.blit(self.cargas.menu, (0, 0))
        #self.screen.blit(felicitacion.render("BIENVENIDO", 1, (67, 168, 253, 255)), (280, 250))
        #self.screen.blit(fontobject.render("Como te dicen:",1,(128, 182, 220, 255)), (250, 300))
        self.screen.blit(self.cargas.textbox,(0,0))
        if len(message) != 0:
            self.screen.blit(fontobject.render(message, 0, (255, 255, 255, 255)),
                             (307, 300))
        pygame.display.flip()

    def ask(self):
        "ask(question) -> answer"
        question = ""
        pygame.font.init()
        current_string = []
        str = ""
        self.display_box(question + ": " + str.join(current_string))
        while 1:
            inkey = self.get_key()
            try:
                if inkey == K_BACKSPACE:
                    current_string = current_string[0:-1]
                elif inkey == K_RETURN or chr(inkey) == ' ':
                    with open('json/usuario.json','w') as outfile:
                        json.dump(str.join(current_string),outfile)
                    break
                elif inkey <= 127:
                    if len(current_string) < 10:
                        current_string.append(chr(inkey).upper())
                self.display_box(question + ": " + str.join(current_string))
            except:
                ''''''
        return str.join(current_string)

'''
visor = pygame.display.set_mode((800, 600))
juego = usuario(visor)
juego.ask()
'''