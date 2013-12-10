#! /usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
import pilas
from pilas.comportamientos import Comportamiento
import random
from pilas.actores import Bomba

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


#la clase del actor
class Tirador(pilas.actores.Actor):
 
	def __init__(self):
		pilas.actores.Actor.__init__(self,x=0,y=-200)
		self.imagen=pilas.imagenes.cargar_grilla("cuchillopistola.png",15)
		self.definir_cuadro(0)
		self.aprender(pilas.habilidades.MoverseConElTeclado)
		self.aprender(pilas.habilidades.SeMantieneEnPantalla)
		self.aprender(pilas.habilidades.MoverseConElTeclado,control=mandos)
		self.balas=0

		self.radio_de_colision=30
		self.hacer(Esperando2())
	def definir_cuadro(self,indice):
		self.imagen.definir_cuadro(indice)




#----------------------------------------------------------------------
#esta clase es cuando el personaje no hace nada excepto moverse con la pistola
class Esperando2(Comportamiento):
	def iniciar(self,receptor2):
		self.receptor2=receptor2
		self.receptor2.definir_cuadro(9)

	def actualizar(self):

		if mandos.izquierda:
#modificacion de la velocidad porque si no el juego es muy lento, la velocidad es de 6
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
		else:
			self.receptor2.hacer(Esperando2())

#si toca el boton para disparar 10 veces carga la pistola
		if pilas.escena_actual().control.boton:
			self.receptor2.hacer(Disparar())
			self.receptor2.balas+=1
			if self.receptor2.balas==10:
				self.receptor2.hacer(cargar())
				self.receptor2.balas=0

#----------------------------------------------------------------------

#clase de cuando el tirador dispara con la pistola
class Disparar(Comportamiento):


#lo del cargador que todavia no me sale

	def iniciar(self,receptor2):
		self.receptor2=receptor2
		self.cuadros=[6,7,7,8,8,9,10,10,10,11,11,11,12,12,13,13,14,14]
		self.paso=9
		self.receptor2.aprender(pilas.habilidades.Disparar)
	def actualizar(self):
		self.avanzar_animacion()

		if mandos.izquierda:
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
			
		if not mandos.boton:
			self.cuadro=9
			self.receptor2.hacer(Esperando2())

#avabza la animacion

			
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
			self.receptor2.x-=velocidad
		elif mandos.derecha:
			self.receptor2.x+=velocidad
			
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
bomba = pilas.actores.Bomba

class zombie(Bomba):

	def __init__(self, x=0, y=0):
		Bomba.__init__(self, x, y)
		self.imagen = pilas.imagenes.cargar('zombie2.png')
		self.escala=0.1
		self.radio_de_colision=30

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

#----------------------------------------------------------------------

zombies=[]
fin_de_juego=False

#se crean zombies
def salezombie():
	#sale zombie
	enemigo=zombie()
	
	enemigo.aprender(pilas.habilidades.PuedeExplotar)

	
	#añadirlo a la lista de enemigos al nuevo zombie
	zombies.append(enemigo)	

def zombie_destruido(disparo,enemigo):
	#eliminar el mono alcanzado
	enemigo.eliminar()
	disparo.eliminar()

	#actualizar marcador con un efecto
	puntos.escala=0
	puntos.escala=pilas.interpolar(1,duracion=0.5,tipo="rebote_final")
	puntos.aumentar(1)





#marcador
puntos=pilas.actores.Puntaje(x=230,y=200,color=pilas.colores.blanco)
puntos.magnitud = 40

pilas.mundo.agregar_tarea(1,salezombie())








pilas.fondos.Fondo("fondo_juego.png")





juan=Tirador()
pilas.ejecutar()








