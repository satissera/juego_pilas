#-*-coding:utf-8-*-
import pilas
import random
#creo un actor que es un zombie (diana para disparar)


class zombie(pilas.actores.Actor):

	def __init__(self):
		pilas.actores.Actor.__init__(self,x=0,y=0)
		self.imagen = pilas.imagenes.cargar('zombie2.png')
		self.radio_de_colision=200
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
		pilas.actores.Explosion(self.x,self.y)

#----------------------------------------------------------------------

