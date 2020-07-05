import random
import enum

#region Constantes
DENSIDAD_ALTILLOS = 0.3
#endregion

class Direccion(enum.Enum):
	NORTE = 'n'
	SUR = 's'
	ESTE = 'e'
	OESTE = 'o'

class Casilla():
	"""Objeto que representa cada casilla

	Atributos:
		nivel: indica la altura
		transitable: inida si un actor se puede mover a esta casilla
	"""

	def __init__(self, x, y, nivel=0, transitable=True):
		self.nivel = nivel
		self.transitable = transitable
		self.x = x
		self.y = y


class Tablero():
	"""Objeto que representa el tablero
	"""
	def __init__(self, ncols: int, nfils: int, wrap=False):
		"""Constructor
		
		Params:
			ncols: Número de columnas
			nfils: Número de filas
			wrap: Si al salirse de un borde se debe aparecer por el otro
		"""

		self.ncols = ncols
		self.nfils = nfils
		self.wrap = wrap

		# Generar las casillas
		self.casillas = [[Casilla(x, y) for y in range(nfils)] for x in range(ncols)]

		# Elevar algunas casillas
		for x in range(ncols):
			for y in range(nfils):
				if random.random() < DENSIDAD_ALTILLOS:
					self.casillas[x][y].nivel = 1


class Actor():
	"""Objetos que se puede mover e interactuar con el entorno
	"""

	def __init__(self, world, x0, y0):
		self.world = world
		self.x = x0
		self.y = y0
	
	def mover(self, dir: Direccion, n_casillas=1):
		# Paso a paso
		if n_casillas > 1:
			self.mover(dict, n_casillas-1)

		# Guardamos la casilla objetivo
		obj = None
		if dir == Direccion.NORTE:
			try:
				obj = self.world.casillas[self.x][self.y + n_casillas]
			except:
				if self.world.wrap:
					obj = self.world.casillas[self.x][0]
				else:
					return
		if dir == Direccion.SUR:
			if not self.world.wrap and self.y - n_casillas < 0:
				return
			try:
				obj = self.world.casillas[self.x][self.y - n_casillas]
			except:
				if self.world.wrap:
					obj = self.world.casillas[self.x][self.world.nfils]
				else:
					return
		if dir == Direccion.ESTE:
			try:
				obj = self.world.casillas[self.x + n_casillas][self.y]
			except:
				if self.world.wrap:
					obj = self.world.casillas[0][self.y]
				else:
					return
		if dir == Direccion.OESTE:
			if not self.world.wrap and self.x - n_casillas < 0:
				return
			try:
				obj = self.world.casillas[self.x - n_casillas][self.y]
			except:
				if self.world.wrap:
					obj = self.world.casillas[self.world.ncols][self.y]
				else:
					return
		
		# Comprobamos si es transitable
		if not obj.transitable:
			return
		
		# Comprobamos si está por encima
		if self.world.casillas[self.x][self.y].nivel < obj.nivel:
			return
		
		# Movemos
		self.x = obj.x
		self.y = obj.y

	def get_casilla(self):
		return self.world.casillas[self.x][self.y]
