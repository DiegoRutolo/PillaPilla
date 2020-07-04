import arcade
import random

#region Constantes
#endregion

class Casilla():
	"""Objeto que representa cada casilla

	Atributos:
		nivel: indica la altura
		abierta: inida si un actor se puede mover
	"""

	def __init__(self, x, y, nivel=0, abierta=True):
		self.nivel = nivel
		self.abierta = abierta
		self.x = x
		self.y = y


class Actor():
	"""Objetos que se puede mover e interactuar con el entorno
	"""

	def __init__(self, world, casilla_inicial: Casilla):
		self.world = world
		

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
		self.world = [[Casilla(x, y) for y in range(nfils)] for x in range(ncols)]

		# Hacer una fila de casillas de nivel 1
		for x in range(ncols):
			self.world[x][3].nivel = 1
