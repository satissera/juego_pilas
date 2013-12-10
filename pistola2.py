#! /usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
import pilas
from pilas.comportamientos import Comportamiento
import random


#----------------------------------------------------------------------
pilas.iniciar()
#----------------------------------------------------------------------
#Definimos las teclas a usar
teclas={pilas.simbolos.a:'izquierda', pilas.simbolos.d:'derecha', pilas.simbolos.ESPACIO:'boton'}

#----------------------------------------------------------------------
#creamos el control personalizado
mandos=pilas.control.Control(pilas.escena_actual(),teclas)
tiempo=6
velocidad=6
#----------------------------------------------------------------------
#variables del juego
zombies=[]
fin_de_juego=False
tiempo=6
balassimples = pilas.actores.Bala
#----------------------------------------------------------------------

#la clase del actor


class Tirador(pilas.actores.Actor):

	def __init__(self,x=0, y=0):
		pilas.actores.Actor.__init__(self,x=0,y=-200)
		self.imagen=pilas.imagenes.cargar_grilla("cuchillopistola.png",15)
		self.definir_cuadro(9)
		self.aprender(pilas.habilidades.MoverseConElTeclado)
		self.aprender(pilas.habilidades.SeMantieneEnPantalla)
		self.aprender(pilas.habilidades.MoverseConElTeclado,control=mandos)
		self.aprender(pilas.habilidades.Disparar,
				municion=pilas.actores.proyectil.Bala,
				angulo_salida_disparo=0,
				frecuencia_de_disparo=8,
				offset_disparo=(25,0),
				offset_origen_actor=(-15,47))
		self.balas=0
		self.hacer(Esperando2())
	def definir_cuadro(self,indice):
		self.imagen.definir_cuadro(indice)

		self.radio_de_colision=30
		

	def definir_enemigos(self, grupo, cuando_elimina_enemigo=None):
		self.cuando_elimina_enemigo = cuando_elimina_enemigo
		self.habilidades.Disparar.definir_colision(grupo, self.hacer_explotar_al_enemigo)


	def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
		mi_disparo.eliminar()
		el_enemigo.eliminar()
		if self.cuando_elimina_enemigo:
			self.cuando_elimina_enemigo()	

		


	#----------------------------------------------------------------------
	#esta clase es cuando el personaje no hace nada excepto moverse con la pistola
class Esperando2(Comportamiento):
	def iniciar(self,receptor2):
		self.receptor2=receptor2
		self.receptor2.definir_cuadro(9)

	def actualizar(self):

		if mandos.izquierda:
#modificacion de la velocidad porque si no el actor se mueve muy lentamente (la velocidad es de 6)
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
		else:
			self.receptor2.hacer(Esperando2())

#si toca el boton para disparar 10 veces carga la pistola
		if mandos.boton:
			self.receptor2.hacer(Disparando())
			self.receptor2.balas+=1
			if self.receptor2.balas==10:

				self.receptor2.hacer(cargar())
				self.receptor2.balas=0

#----------------------------------------------------------------------

#clase de cuando el tirador dispara
class Disparando(Comportamiento):

	def iniciar(self,receptor2):
		self.receptor2=receptor2
		self.cuadros=[6,7,7,8,8,9,10,10,10,11,11,11,12,12,13,13,14,14]
		self.paso=9

	def actualizar(self):
		self.avanzar_animacion()		
		if mandos.izquierda:
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
#ponemos aca y no en tirador que aprenda a disparar para que cuando apriete boton dispare un solo tiro
		if not mandos.boton:
			self.receptor2.hacer(Esperando2())

#avanza la animacion
	def avanzar_animacion(self):
		self.paso+=1
		if self.paso>=len(self.cuadros):
			self.paso=9
		self.receptor2.definir_cuadro(self.cuadros[self.paso])	
#----------------------------------------------------------------------
#cuando llegue a 10 balas cargue las balas
class cargar(Comportamiento):
	def iniciar(self,receptor2):

		self.receptor2=receptor2
		self.cuadros=[8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,4,4,4,4,4,5,5,5,5,5,5,5,5,5,6,6,6,6,6,6,6,6,6,6,6,6,7,7,7,7,7,7,7,7,7]
		self.paso=4

	def actualizar(self):
		self.avanzar_animacion()
	
		if mandos.izquierda:
#hacemos que valla hacia la izquierda con la velocidad que ya pusimos
			self.receptor2.x-=velocidad
#hacemos que valla hacia la izquierda con la velocidad que ya pusimos
		elif mandos.derecha:
			self.receptor2.x+=velocidad
#si no se aprieta el boton hace esperando			
		if not mandos.boton:
			self.cuadro=8
			self.receptor2.hacer(Esperando2())

	def avanzar_animacion(self):
		self.paso+=1
		if self.paso>=len(self.cuadros):
			self.paso=8
		self.receptor2.definir_cuadro(self.cuadros[self.paso])

#----------------------------------------------------------------------
#creo un actor que es un zombie (diana para disparar)


class zombie(pilas.actores.Actor):

	def __init__(self):
		pilas.actores.Actor.__init__(self,x=0,y=0)
		self.imagen = pilas.imagenes.cargar('zombie2.png')
		self.radio_de_colision = 200
		self.escala=0.1
		cx = random.randrange(-320, 320)
		self.difx=100
		self.dify=200

	def actualizar(self):
		if self.x > 320:
			self.difx=1 
		if self.x < -320:
			self.difx=0

		if self.difx == 0:
			self.x += 1
		else:
			self.x -= 1
	def eliminar(self):
#cuando el disparo elimina al zombie
		pilas.actores.Explosion(self.x,self.y)
		pilas.actores.Actor.eliminar(self)


#se crean zombies
def salezombie():
	#sale zombie
	enemigo=zombie()
	
	enemigo.aprender(pilas.habilidades.PuedeExplotar)

	
	#añadirlo a la lista de enemigos al nuevo zombie
	zombies.append(enemigo)	

def zombie_destruido(balassimple,enemigo):
	#eliminar el mono alcanzado
	enemigo.eliminar()
	disparo.eliminar()

	#actualizar marcador con un efecto
	puntos.escala=0
	puntos.escala=pilas.interpolar(1,duracion=0.5,tipo="rebote_final")
	puntos.aumentar(1)




juan=Tirador()
pilas.mundo.agregar_tarea(0.5, salezombie())
#juan.definir_enemigos(Tirador.zombies, Tirador.cuando_explota_zombie)
#pilas.escena_actual().colisiones.agregar(balassimple,zombiez,zombie_destruido)
puntos=pilas.actores.Puntaje(x=230,y=200,color=pilas.colores.blanco)
pilas.fondos.Fondo("fondo_juego.png")
pilas.ejecutar()


'''
from pilas.actores import Bomba

class BombaConMovimiento(Bomba):

    def __init__(self, x=0, y=0):
        Bomba.__init__(self, x, y)

    def actualizar(self):
        self.x += 0.5


        if self.x > 320:
            self.x = -320

        if self.y > 240:
            self.y = 0

def cuando_colisionan(balassimples, bomba):
	bomba.explotar

'''

#----------------------------------------------------------------------
'''
if tiempo=10:
	#indica fin del juego y elimina lo que ya no se necesita
global fin_de_juego

zombie.eliminar()

	
fin_de_juego=True
pilas.avisar("GAME OVER")'''

'''bomba_1 = BombaConMovimiento()
bomba_2 = BombaConMovimiento(x=200, y=0)
bomba_3 = BombaConMovimiento(x=0, y=200)

lista_de_bombas = [bomba_1, bomba_2, bomba_3]
pilas.mundo.colisiones.agregar(balassimples,lista_de_bombas,cuando_colisionan)'''




















