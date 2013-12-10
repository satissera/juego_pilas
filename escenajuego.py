#-*-coding:utf-8-*-

import pilas
import random
from pistola2 import Tirador
import zombiediana 
class Estado:

	def actualizar(self):
		pass #sobrescribir este metodo

class Juegando(Estado):

	def __init__(self,juego,nivel):
#usamos el contador de puntaje como contador de tiempo
		self.tiempo=pilas.actores.Puntaje(x=-230,y=200,color=pilas.colores.blanco)
#a pesar de que no hay niveles en mi juego, vamos a usarlos para crear los zombies
		self.nivel=nivel
		self.juego=juego
		self.juego.salezombie(cantidad=nivel*3)
		#cuenta los segundos que pasan en la función actualizar
		pilas.mundo.agregar_tarea(1,self.actualizar)

	def actualizar(self):
#aumentamos en uno el contador de tiempo
		self.tiempo.aumentar(1)
#		if self.tiempo==120:
#			self.juego.cambia_estado(SeTermino(juego))
		if self.juego.ha_eliminado_todos_los_zombies():
			self.juego.cambiar_estado(Iniciando(self.juego,self.nivel+1))
			return False

		return True

class Iniciando(Estado):

	def __init__(self,juego,nivel):
		self.texto = pilas.actores.Texto("Empezo %d" %(nivel))
		self.texto.escala = 0.1
		self.texto.escala = [1]
		self.texto.rotacion = [360] 
		self.nivel = nivel
		self.texto.color = pilas.colores.negro
		self.contador_de_segundos = 0
		self.juego = juego
		pilas.mundo.agregar_tarea(1,self.actualizar)

	def actualizar(self):
		self.contador_de_segundos +=1

		if self.contador_de_segundos >2:
			self.juego.cambiar_estado(Juegando(self.juego,self.nivel))
			self.texto.eliminar()
			return False
		return True

class SeTermino(Estado):

	def __init__(self,juego,tiempo):
		self.tiempo=tiempo
	#muestra el mensaje de se acabo el tiempo
		pilas.avisar(u"se acabó el tiempo, Conseguiste % de puntos presiona ESC para volver al menú" %(puntos.obtener()))

	def cuando_pulsa_tecla(self,*k,**kw):
		import escena_menu
		pilas.cambiar_escena(escena_menu.EscenaMenu())

	def actualizar():
		pass

class Juego(pilas.escena.Base):
	def __init__(self):
		pilas.escena.Base.__init__(self)
	
	def iniciar(self):
		pilas.fondos.Fondo("fondo_juego.png")
		self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla_escape)
		self.zombies=[]
		self.crear_tirador()
		self.cambiar_estado(Iniciando(self,1))
		self.puntos=pilas.actores.Puntaje(x=230,y=200,color=pilas.colores.blanco)

	def cambiar_estado(self,estado):
		self.estado=estado

	def crear_tirador(self):
		juan=Tirador()
		juan.definir_enemigos(self.zombies,self.cuando_explota_zombie)

	
	def cuando_explota_zombie(self):
		zombiediana.eliminar(zombie)
		self.puntos.aumentar(1)

	def cuando_pulsa_tecla_escape(self,*k,**kw):
		import escena_menu
		pilas.cambiar_escena(escena_menu.EscenaMenu())
	
	def salezombie(self,cantidad):
		fuera_de_la_pantalla = [-600,-650,-700,-750,-800]
		for x in range(cantidad):
			x= random.choice(fuera_de_la_pantalla)
			y= random.choice(fuera_de_la_pantalla)
			zombie_nuevo=zombiediana.zombie()
			self.zombies.append(zombie_nuevo)
	
	def ha_eliminado_todos_los_zombies(self):
		return len(self.zombies)==0
















		
	

		
	
