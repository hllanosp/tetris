
#!/usr/bin/env python
# coding: utf-8

# Copyright 2015 hllanos <hllanos@pcllanos>

import threading
import json
import pprint
import pieza
import pygame
import sys
import cargas
import Board
import threading
import menu_mejorado
import AgenteIA.Agente_tetrix as AG
import json
from pygame.locals import *
import animacion
import registro_Usuarios

class main:
    """
    Marca el inicio del programa, contiene el metodo run que controla la logica del juego
    """
    #==========================================================================================#
    #==================================== INICIO DEL INIT() ===================================#
    def __init__(self):
        """
        Inicializa las variables necesarias para ejecutar el programa

        VARIABLES

        :resolucion : tamano de la ventana que tendra el juego
        :visor : representa el visor o la ventana del programa
        :area_juego : superficie donde estara el area de juego
        :marcadores: superficie donde estara los marcadores los scores el cronometro y la pieza siguiente
        :timer: variable para controlar los refrescos del pintado de la pantalla

        :pieza_siguiente: sprite que representa la pieza de tetris siguiente
        :pieza_ayuda : pieza que representa la ayuda cuando esta activa la ayuda en el menu de pausa
        :pieza_actual: sprite que representa la pieza que esta cayendo

        :cargas : instancia de la clase cargas utilizada para cargar archivos desde disco
        :marco_bajo: sprite que representa el marco bajo del area de juego
        :marco_der: sprite que representa el marco derecho del area de juego
        :marco_izq: sprite que representa el marco izquierdo del area de juego
        :piezas_muertas: grupo de sprites que representan las piezas muertas en area de juego
        :fondo_juego: fondo principal del menu de juego
        :MiFuente: fuente utilizada en los menus

        time: variable utilizada para representar los minutos en el cronometro
        minutos : variable utilizada para representar los segundos en el cronometro
        game_over: variable que indica si el usuario a perdido
        lineas : numero de lineas completadas en el juego
        nivel : nivel o dificultad en el que se encuentra el juego
        salir_juego: indica si el usuario elige salir del juego en el menu principal
        mejor posicion: coordenada que indica la mejor posicion para una pieza
        giros : cantidad de giros que el agente utiliza para colocar la pieza en la mejor posicion
        """
        pygame.init()
        pygame.font.init()
        self.resolucion = (800, 600)
        self.visor = pygame.display.set_mode(self.resolucion)
        pygame.display.set_caption('Tetris')
        self.area_juego = pygame.Surface((300, 525))
        self.marcadores = pygame.Surface((300, 525))

        self.timer = pygame.time.Clock()
        self.Tablero = Board.Board(10, 20)

    #------------------------------Cargas de sprites y fondos----------------------------------#
        self.cargas = cargas.Cargas()
        self.pieza_siguiente = self.cargas.get_sprite()
        self.pieza_actual = pieza.figura(self.pieza_siguiente, 150, 0)
        self.pieza_siguiente = self.cargas.get_sprite()
        self.pieza_ayuda = pieza.ayuda(self.cargas.get_sprite_help())

    #-------------------------Sprites que representan el marco de juego------------------------#
        self.marco_bajo = self.cargas.get_marco_bajo()
        self.marco_der = self.cargas.get_marco_derecho()
        self.marco_izq = self.cargas.get_marco_izquierdo()
        self.girar = self.cargas.get_girar()
        self.piezas_muertas = pygame.sprite.OrderedUpdates()
        self.fondo_juego = self.cargas.fondo_juego
        self.down = self.cargas.get_down()
        self.caer = self.cargas.sonido_caer

    #-----------------------------------Fuentes y colores--------------------------------------#
        self.MiFuente = self.cargas.font_transform
        self.Fuente_Score = self.cargas.font_score
        self.Fuente_Score2 = self.cargas.font_score2
        self.blanco = (3, 16, 25, 255)

    #-------------------------Variables que indican el estado del juego------------------------#
        self.time = 0
        self.minutos = 0
        self.segundos = 0
        self.tiempo = ""
        self.game_over = False
        self.lineas = 0
        self.nivel = 0
        self.salir_juego = False
        self.mejor_posicion = []
        self.activado = False
        self.giros = 0
        self.movimientoY = 150
        self.llamado_agente = False
        self.visitado = False
        self.ayuda_Activada = False
        self.girada = False
        self.inicio = True

    #==================================== FIN DEL INIT() ======================================#
    #==========================================================================================#

    #==========================================================================================#
    #====================METODOS PARA CONTROLAR LOS MENUS DE JUEGO=============================#

    def Menu(self, opciones, X, Y):
        """

        """
        self.opciones = []
        x = X
        y = Y
        paridad = 1

        self.cursor = menu_mejorado.Cursor(x - 30, y, 30)

        for titulo, funcion in opciones:
            self.opciones.append(menu_mejorado.Opcion(titulo, x - 30, y, paridad, funcion))
            y += 30
            if paridad == 1:
                paridad = -1
            else:
                paridad = 1

        self.seleccionado = 0
        self.total = len(self.opciones)
        self.mantiene_pulsado = False

    def actualizar(self, X):
        """
        Altera el valor de 'self.seleccionado' con los direccionales.

        permite mover el cursor a la opcion seleccionado dentro de un menu
        """

        k = pygame.key.get_pressed()

        if not self.mantiene_pulsado:
            if k[K_UP]:
                self.cargas.get_sonido_cursor().play()
                self.seleccionado -= 1
            elif k[K_DOWN]:
                self.cargas.get_sonido_cursor().play()
                self.seleccionado += 1
            elif k[K_RETURN]:
                # Invoca a la funcion asociada a la opcion.
                self.opciones[self.seleccionado].activar()

        # procura que el cursor estee entre las opciones permitidas
        if self.seleccionado < 0:
            self.seleccionado = 0
        elif self.seleccionado > self.total - 1:
            self.seleccionado = self.total - 1

        self.cursor.seleccionar(self.seleccionado)

        # indica si el usuario mantiene pulsada alguna tecla.
        self.mantiene_pulsado = k[K_UP] or k[K_DOWN] or k[K_RETURN]

        self.cursor.actualizar()

        for o in self.opciones:
            if o == self.opciones[self.seleccionado]:
                o.image = o.imagen_destacada
            else:
                o.image = o.imagen_normal

            o.actualizar(X)

    def imprimir(self, screen):
        """
        Imprime sobre screen o superficie deciada el texto de cada opcion del menu.
        """
        self.cursor.imprimir(screen)
        for opcion in self.opciones:
            opcion.imprimir(screen)

    #------------------------------------------------------------------------------------#

    def menu_general(self, opciones, posX, posY, fondo, id_menu, id_fondo):
        """
        Sirve como modelo para los demas menu del juego

        PARAMETROS
        :opciones: tiene todas las opciones que el menu mostrara
        :posx: posicion del menu
        :posy: altura a la cual se pintara el menu
        :fondo: fondo del menu
        :id:variable que indica el tipo de menu
        """

        salir = False
        pygame.init()
        imagen = pygame.Surface((800, 600))
        imagen.blit(fondo, (0, 0))
        self.Menu(opciones, posX, posY)
        while not salir:
            self.timer.tick()
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()


            self.visor.blit(imagen, (0, 0))
            if id_fondo == 0:
                self.scores()
            self.actualizar(posX + 60)
            self.imprimir(self.visor)
            pygame.display.flip()
            pygame.time.delay(10)

            if id_menu != 0:
                self.pinta_pantalla()

    #------------------------------------------------------------------------------------#

    def menu_pausa(self):
        """
        Representa al menu de pausa

        Se carga la imagen de fondo del menu y las posiciones iniciales donde se ubicara el menu
        se especifican las opciones que tendra el menu donde en cada opcion se especifica la accion a realizar
        luego se envia el fondo, y las opciones hacia el menu_general para que este pueda mostrar el menu
        completo
        """
        posX = 280
        posY = 220
        if self.activado:
            opciones = [
                ("Reanudar", self.juego),
                ("Reiniciar", self.reiniciar),
                ("Desactivar Agente", self.activa_agente),
                ("Ayuda",self.ayuda),
                ("Salir", self.salir_del_programa)
            ]
        else:
            opciones = [
            ("Reanudar", self.juego),
            ("Reiniciar", self.reiniciar),
            ("Activar Agente", self.activa_agente),
            ("Ayuda",self.ayuda),
            ("Salir", self.salir_del_programa)
        ]
        fondo = self.cargas.get_paused()
        #se envia al menu_general para que este muestre el menu en pantalla
        self.menu_general(opciones,posX,posY,fondo,1,1)

    #------------------------------------------------------------------------------------#

    def menu_principal(self):
        """
        Representa al menu Principal al inicio del juego

        Se carga la imagen de fondo del menu y la posicion del  menu
        se especifican las opciones que tendra el menu, donde cada opcion llama a un metodo especifico
        luego estos datos se envian al menu_general que se encarga de mostrar el menu en pantalla
        """
        #------Sonido de fondo------
        if self.inicio:
            pygame.mixer.music.load('sonidos/bjorn__lynne-_rock_force.mid')
            pygame.mixer.music.play(-1)
            self.__init__()
            self.inicio = False
        posX = 300
        posY = 235
        opciones = [
            ("Jugar", self.juego),
            ("Controles", self.mostrar_opciones),
            ("Creditos", self.creditos),
            ("Salir", self.salir_del_programa)
        ]
        fondo = self.cargas.get_menu()
        #se envian el fondo  y la posicion
        self.menu_general(opciones,posX,posY,fondo,0,1)

    #-------------------------------------------------------------------------------------#

    def menu_info(self,id_info):
        posX = 300
        posY = 483
        opciones = [
            ("Volver", self.volver_menu)
        ]
        if id_info == 0:
            fondo = self.cargas.cargando
        else:
            if id_info == 1:
                fondo = self.cargas.credito
        self.menu_general(opciones,posX,posY,fondo,0,1)

    #------------------------------------------------------------------------------------#

    def menu_game_over(self):
        pygame.mixer.music.load('sonidos/game_over.wav')
        pygame.mixer.music.play(-1)
        """
        Representa al menu Principal al inicio del juego

        Se carga la imagen de fondo del menu y la posicion del  menu
        se especifican las opciones que tendra el menu, donde cada opcion llama a un metodo especifico
        luego estos datos se envian al menu_general que se encarga de mostrar el menu
        """
        posX = 507
        posY = 420
        opciones = [
            ("Continuar", self.menu_principal)
        ]
        fondo = self.cargas.marcador
        #se envian el fondo la posicion
        self.menu_general(opciones,posX,posY,fondo,0,0)

    #==========================================================================================#
    #============================ LLAMADO DE LOS MENUS ========================================#

    def volver_menu(self):
        if not self.visitado:
            self.menu_principal()
            self.visitado = True
        else:
            self.visitado = False

    def mostrar_opciones(self):
        self.menu_info(0)

    def creditos(self):
        self.menu_info(1)

    def salir_del_programa(self):
        sys.exit(0)

    def reiniciar(self):
        self.__init__()
        self.timer.tick()
        self.timer.tick()
        self.run()

    def juego(self):
        if self.visitado:
            self.visor.blit(self.cargas.fondo, (0,0))
            self.pausada = False
            self.visitado = False
            self.run()
        else:
            self.visitado = True

    def ayuda(self):
        """
        Controla el estado de la variable ayuda_Activada

        se activa y desactiva al momento de presionar la opcion de "AYUDA" en el menu de pausa
        """
        if not self.ayuda_Activada:
            self.llamarAyuda()
            self.ayuda_Activada = True
        else:
            self.ayuda_Activada = False
        self.run()

    def activa_agente(self):
        """
        Controla la variable de estado activado

        este metodo se activa al activar la opcion "AGENTE" en el menu de pausa
        """
        if not self.activado:
            self.activado = True
        else:
            self.activado = False
        self.run()

    #=================================== FIN DE LOS MENUS =====================================#
    #==========================================================================================#

    #==========================================================================================#
    #============================== COMUNICACION CON EL AGENTE ================================#
    def escritura(self):
        """
        Escribe el estado del juego en el archivo json

        El estado de juego en este contexto es representado por la matriz de juego y la pieza actual
        """
        lector = json.loads(open("json/numero.json").read())
        lector2 = json.loads(open('json/matriz.json').read())
        if(lector2[2] != "l"):
            enviar = self.Tablero.tablero, lector[1], "l"
            with open('json/matriz.json','w') as outfile:
                json.dump(enviar,outfile)

    #------------------------------------------------------------------------------------------#

    def lectura(self):
        """
        Lee del archivo json

        Es la respuesta por parte del agente, contiene la mejor posicion para ubicar la pieza
        tambien contiene la cantidad de giros, y el ancho de la pieza
        """
        my_data = json.loads(open("json/Efector.json").read())
        if(my_data[3] == 'l'):
            self.mejor_posicion = my_data
            my_data[3] = "r"
            with open("json/Efector.json",'w') as outfile:
                json.dump(my_data,outfile)

    #============================ FIN COMUNICACION CON EL AGENTE ==============================#
    #==========================================================================================#

    #==========================================================================================#
    #==================================== METODOS DEL JUEGO ===================================#

    #------------------------------------------------------------------------------------------#

    def login(self):
        """
        registros de usuarios al inicio del juego

        """
        self.usuario = registro_Usuarios.usuario(self.visor)
        self.usuario.ask()
        self.menu_principal()

    #------------------------------------------------------------------------------------------#

    def cronometro(self):
        """
        Calcula y pinta el cronometro en area de marcadores
        """
        self.time += self.timer.get_time() / 10
        if(self.time >= 60):
            self.segundos += 1
            self.time -= 60
        if(self.segundos >= 60):
            self.minutos += 1
            self.segundos = 0
        milisegundos = str(self.time)
        self.tiempo = str(self.minutos) + ":" + str(self.segundos) + ":" + milisegundos[:milisegundos.find(".")+5]
        self.mensaje = self.cargas.font_digital.render(self.tiempo,0,(255, 0, 0, 255))

    #------------------------------------------------------------------------------------------#

    def actualiza_score(self):
        """
        se encarga de actualizar el archivo json score "es llamado desde "GAME-OVER"

        solo cuando el numero de lineas hechas en el juego actual supera al mejor score
        guardado en el archivo
        """
        score = json.loads(open("json/score.json").read())
        if not self.activado:
            score.append((json.loads(open("json/usuario.json").read()),self.lineas,self.tiempo))
        else:
            score.append(("AGENTE",self.lineas,self.tiempo))
        score = sorted(score,key=lambda lineas: lineas[1])
        newScore = []
        for i in reversed(range(len(score))):
            if i != 0:
                newScore.append(score[i])
        with open('json/score.json', 'w') as outfile:
                json.dump(newScore, outfile)

    #------------------------------------------------------------------------------------------#

    def scores(self):
        """
        Pinta en pantalla la informacion de cada usuario (Nombre, tiempo y score)
        """
        score = json.loads(open("json/score.json").read())
        for i in range(len(score)):
            for j in range(3):
                if score[i][1] == self.lineas and score[i][2] == self.tiempo:
                    if str(score[i][0]) != "":
                        score_nombre = self.Fuente_Score2.render(str(score[i][0]), 0, (255, 0, 0, 255))
                    else:
                        score_nombre = self.Fuente_Score2.render("INVITADO", 0, (255, 0, 0, 255))
                    score_tiempo = self.Fuente_Score2.render(str(score[i][2]), 0, (255, 0, 0, 255))
                    score_lineas = self.Fuente_Score2.render(str(score[i][1]), 0, (255, 0, 0, 255))
                else:
                    if str(score[i][0]) != "":
                        score_nombre = self.Fuente_Score.render(str(score[i][0]), 0, (255, 255, 255, 255))
                    else:
                        score_nombre = self.Fuente_Score.render("INVITADO", 0, (255, 255, 255, 255))
                    score_tiempo = self.Fuente_Score.render(str(score[i][2]), 0, (255, 255, 255, 255))
                    score_lineas = self.Fuente_Score.render(str(score[i][1]), 0, (255, 255, 255, 255))
                self.visor.blit(score_nombre,(162,200 + i * 40))
                self.visor.blit(score_tiempo,(422,200 + i * 40))
                self.visor.blit(score_lineas,(574,200 + i * 40))

    #------------------------------------------------------------------------------------------#

    def animacion_agente(self):
        """
        Mueve y gira la pieza cuando el agente esta activado

        se encarga de girar y desplazar la pieza que cae, segun los parametros recibidos por parte
        del agente
        """
        if self.mejor_posicion[2] > self.giros:
            self.pieza_actual.update(K_UP)
            self.giros += 1

        if self.movimientoY > (self.mejor_posicion[1] * 25 + 25):
            self.pieza_actual.update(K_LEFT)
            self.movimientoY -= 25
        else:
            if self.movimientoY < (self.mejor_posicion[1] * 25 + 25):
                self.pieza_actual.update(K_RIGHT)
                self.movimientoY += 25

    #------------------------------------------------------------------------------------------#

    def animacion_linea(self):
        """
        animacion de laser cuando completamos una linea
        """
        if len(self.Tablero.filas_encontradas) > 0:
            for i in range(len(self.Tablero.filas_encontradas)):
                linea = self.Tablero.filas_encontradas[i]+1
                animacionlinea = animacion.animacion(self.cargas.animacion_sheet, 100, linea*25, self.visor)
                self.cargas.get_sonido_linea().play()
                self.cargas.get_sonido_linea().play()
                animacionlinea.draw()
            self.caer.play()
            self.Tablero.filas_encontradas = []

    #------------------------------------------------------------------------------------------#

    def llamarAyuda(self):
        """
        hace una comunicacion entre el juego y el agente cuando la ayuda esta activada en el menu de
        pausa

        """
        self.escritura()
        juego = AG.agente()
        juego.control()
        self.lectura()

    #------------------------------------------------------------------------------------------#

    def inicializa_pieza(self):
        """
        se inicializa una nueva pieza de tetris

        cuando la pieza actual colisiona en la parte inferior del area de juego, esta se inicializa
        de nuevo en la posicion inicial (en la parte de arriba) para que siga desplazandose por el
        area de juego
        """
        self.pieza_actual.rect.top = -25
        self.pieza_actual.image = self.pieza_siguiente
        self.pieza_actual.rect.left = 6 * 25
        self.pieza_ayuda = pieza.ayuda(self.cargas.get_sprite_help())
        self.pieza_siguiente = self.cargas.get_sprite()
        self.pieza_actual.rapido = False
        if self.ayuda_Activada:
            self.llamarAyuda()

    #------------------------------------------------------------------------------------------#

    def GAME_OVER(self):
        """
        cuando el usuario pierde

        se actualizan los score
        y se regresa al inicio del juego
        """

        self.actualiza_score()
        pygame.display.update()
        self.piezas_muertas.empty()
        self.inicio = True
        self.menu_game_over()

    #------------------------------------------------------------------------------------------#

    def pintar_muertas(self):
        """
        pinta sobre el area de juego las piezas muertas 

        """
        self.piezas_muertas.empty()
        I_muerta = self.cargas.get_muerta()
        for i in range(20):
            for j in range(10):
                muertad = pieza.figura(I_muerta, (j * 25) + 25, i * 25)
                if self.Tablero.tablero[i][j] == 2:
                    self.piezas_muertas.add(muertad)

     #-------------------------------------------------------------------------------------------#

    def pintar_ayuda(self):
        """
        Se encara de pintar la pieza temporal que indica al usuario donde colocar la pieza

        sucede solo cuando la opcion de ayuda del menu de pausa esta activa
        cuando se genera una nueva pieza, se le presenta al usuario una pieza temporal que le indica el
        mejor movimiento
        """
        if self.ayuda_Activada:
            if not self.girada:
                for i in range(self.mejor_posicion[2]):
                    if self.mejor_posicion[2] != 0:
                        self.pieza_ayuda.update(pygame.K_UP)
                self.girada = True
            if(self.mejor_posicion[4] == 1):
                self.area_juego.blit(self.pieza_ayuda.image,(self.mejor_posicion[1]*25 + 25,self.mejor_posicion[0]*25))
            if(self.mejor_posicion[4] == 2):
                self.area_juego.blit(self.pieza_ayuda.image,(self.mejor_posicion[1]*25+25,self.mejor_posicion[0]*25 - 25))
            if(self.mejor_posicion[4] == 3):
                self.area_juego.blit(self.pieza_ayuda.image,(self.mejor_posicion[1]*25+25,self.mejor_posicion[0]*25 - 50))
            if(self.mejor_posicion[4] == 4):
                self.area_juego.blit(self.pieza_ayuda.image,(self.mejor_posicion[1]*25+25,self.mejor_posicion[0]*25 - 75))

    #------------------------------------------------------------------------------------------#

    def pinta_pantalla(self):
        """
        pinta la pantalla

        Pinta las distintas superficies del juego
        pinta sobre el visor principal los distintos fondos y las siguientes superficies
        -area de juego(marcos  que delimitan el area de juego)
        -marcadores(score, pieza_siguiente, level)
        -se pintan las distintas piezas de tetris, las que caen y las piezas muertas
        """
        self.visor.blit(self.area_juego, (100, 25))
        self.visor.blit(self.marcadores, (425, 25))
        self.visor.blit(self.score, (495, 170))
        self.visor.blit(self.level, (495, 220))
        self.visor.blit(self.mensaje,(538, 253))
        self.marcadores.blit(self.cargas.get_marcador(), (0, 0))
        self.marcadores.blit(self.pieza_siguiente, (25 * 5, 25 * 15))
        self.area_juego.blit(self.fondo_juego, (0,0))

        #si la opcion ayuda del menu de pausa esta activa se pinta la pieza temporal
        if self.ayuda_Activada:
            self.pintar_ayuda();

        #pinta la pieza que cae y el marco de juego
        self.area_juego.blit(self.pieza_actual.image, self.pieza_actual.rect)
        self.area_juego.blit(self.marco_bajo.image, self.marco_bajo.rect)
        self.area_juego.blit(self.marco_izq.image, self.marco_izq.rect)
        self.area_juego.blit(self.marco_der.image, self.marco_der.rect)

        #pintas las piezas muertas en el area de juego
        self.piezas_muertas.draw(self.area_juego)

    #------------------------------------------------------------------------------------------#

    def Analisador(self, x, y):
        """
        Estampa la pieza que ha colisionado a la matriz de estados.

        Este metodo es la conexion entre la parte grafica y la matriz de estados
        cuando una pieza colisiona con una pieza muerta o con el marco inferior del area de juego
        se actualiza la matriz de estados estampando la pieza muerta, en la matriz

        se analiza la pantalla opteniendo el color de los pixeles.
        Estampa la pieza que ha colisionado a la matriz de estados

        """
        indicex = 1
        indicey = 1
        posX = int(round(x + indicex * 12.5))
        posY = int(round(y + indicey * 12.5))
        while (indicey <= 4):
            while (indicex <= 4):
                try:
                    color_pixel = self.area_juego.get_at((posX + (indicex - 1) * 25, posY + (indicey - 1) * 25))
                    if (color_pixel != self.blanco):
                        self.Tablero.estampar_pieza((y + (indicey - 1) * 25) / 25, (x - 1 + (indicex - 1) * 25) / 25)
                except:
                    a = 0
                indicex = indicex + 1
            indicey = indicey + 1
            indicex = 1

    #------------------------------------------------------------------------------------------#

    def validar_izquierda(self):
        if pygame.sprite.collide_mask(self.pieza_actual, self.marco_izq) or pygame.sprite.spritecollide(
                self.pieza_actual, self.piezas_muertas, False, pygame.sprite.collide_mask):
            self.pieza_actual.update(pygame.K_RIGHT)

    #------------------------------------------------------------------------------------------#

    def validar_derecha(self):
        if pygame.sprite.collide_mask(self.pieza_actual, self.marco_der) or pygame.sprite.spritecollide(
                self.pieza_actual, self.piezas_muertas, False, pygame.sprite.collide_mask):
            self.pieza_actual.update(pygame.K_LEFT)

    #-------------------------------------------------------------------------------------------#

    def esperar_evento(self):
        """Escucha por eventos

        Su trabajo es esperar por un evento y de acuerdo al evento capturado
        realiza una accion especifica

        Descripcion de los eventos:

            K_UP    --  si se presiona la tecla hacia arriba la pieza gira
            K_LEFT  --  la pieza se desplaza hacia la izquierda
            K_RIGHT --  la pieza se desplaza hacia la derecha
            K_DOWN  --  esta tecla siempre ocurrira ya que es la que mueve la pieza hacia abajo

        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    pygame.mixer.music.set_volume(0.5)
                    self.girar.play()
                    pygame.mixer.music.set_volume(1.0)

                    self.pieza_actual.update(pygame.K_UP)
                    if pygame.sprite.collide_mask(self.pieza_actual, self.marco_izq) or pygame.sprite.collide_mask(
                            self.pieza_actual, self.marco_der) or pygame.sprite.collide_mask(self.pieza_actual,
                                                                                             self.marco_bajo) or pygame.sprite.spritecollide(
                            self.pieza_actual, self.piezas_muertas, False, pygame.sprite.collide_mask):
                        self.pieza_actual.image = pygame.transform.rotate(self.pieza_actual.image, -90)

                if event.key == pygame.K_LEFT:
                    self.pieza_actual.update(pygame.K_LEFT)
                    self.validar_izquierda()

                if event.key == pygame.K_RIGHT:
                    self.pieza_actual.update(pygame.K_RIGHT)
                    self.validar_derecha()

                if event.key == pygame.K_SPACE:
                    self.menu_pausa()

                if event.key == pygame.K_DOWN:

                    if self.pieza_actual.rapido == False:
                        self.pieza_actual.rapido = True
                        self.cargas.get_sonido_rapido().play()
                    else:
                        self.pieza_actual.rapido = False

    #------------------------------------------------------------------------------------------
    def agente_activo(self):
        if self.activado:
                if not self.llamado_agente:
                    self.escritura()
                    juego = AG.agente()
                    juego.control()
                    self.lectura()
                    self.llamado_agente = True
                    self.pieza_actual.rapido = True
                    self.cargas.get_sonido_rapido().play()
                self.animacion_agente()



    #================================ FIN METODOS DEL JUEGO ===================================#
    #==========================================================================================#

    #==========================================================================================#
    #==================================== INICIO DEL RUN() ====================================#
    def run(self):
        """
        Define la logica de juego.

        Se actualiza el tablero juego, se maneja los eventos, se controlan los timers, se mueven los sprites
        se detecta colisiones entre la pieza (piezas muertas y con el marco de juego), se actualizan los scores del juego
        y por ultimo se pinta la pantalla

        """
        #ejecutamos el sonido de fondo
        pygame.mixer.music.load('sonidos/bjorn__lynne-_retro_electro.mid')
        pygame.mixer.music.play(-1)

        #ciclo principal de juego
        while self.salir_juego == False and self.game_over == False:
            #inicializa el cronometro
            self.cronometro()
            #se inicializa los scores y el nivel
            self.score = self.MiFuente.render((" SCORE: " + str(self.lineas)), 0, (47, 151, 217, 255))
            self.level = self.MiFuente.render((" LEVEL: " + str(self.nivel)), 0, (47, 151, 217, 255))
            #se capturan los eventos
            self.esperar_evento()
            #se desplaza la pieza actual hacia abajo
            self.pieza_actual.update(pygame.K_DOWN)
            #se pinta la pieza siguiente en el area de marcadores
            self.marcadores.blit(self.pieza_siguiente, (25 * 5, 25 * 15))
            # si la pieza que cae colisiona con los bordes del area de juego o con las piezas muertas
            if pygame.sprite.collide_mask(self.pieza_actual, self.marco_bajo) or pygame.sprite.spritecollide(
                    self.pieza_actual, self.piezas_muertas, False, pygame.sprite.collide_mask):
                self.pieza_actual.rect.top -= 1
                #estampa pieza en el tablero o matriz de estados
                self.Analisador(self.pieza_actual.rect.left, self.pieza_actual.rect.top)
                #busca lineas completas en el tablero
                self.Tablero.lineas_formadas(19)
                self.Tablero.encontrar_linea(19)
                #actualizamos el score las lineas hechas
                self.lineas = (self.Tablero.lineas)
                #se pintan las piezas muertas
                self.pintar_muertas()

                #Sonido pieza muerta
                self.down.play()

                # Inicializa datos para la siguiente pieza
                self.giros = 0
                self.movimientoY = 150
                self.llamado_agente = False
                self.girada = False

                #si la pieza actual colisiona con una muerta se crea una nueva
                self.inicializa_pieza()

                #si el juego termina GAME-OVER
                if pygame.sprite.spritecollide(self.pieza_actual, self.piezas_muertas, False,
                                               pygame.sprite.collide_mask):
                    if self.pieza_actual.rect.top < 2:
                        self.GAME_OVER()
                        break
            #se pintan todos los elementos en el visor de la pantalla
            self.pinta_pantalla()

            #si han completado lineas que corra la animacion
            self.animacion_linea()

            #si el agente esta activado
            self.agente_activo()


            self.timer.tick(60)
            pygame.display.update()
    #==================================== FIN DEL RUN() =======================================#
    #==========================================================================================#

#===========================MARCA EL INICIO DEL JUEGO==============================================#
juego = main()
juego.login()
