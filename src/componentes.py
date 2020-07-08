import random
import enum

#region Constantes
DENSIDAD_ALTILLOS = 0.4
SEED = random.randint(0, 2**32 - 1)
#endregion

#region Funciones

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

		generador = Generador(self.ncols, self.nfils, seed=SEED)
		generador.bloques(n_bloques=5)
		for x in range(ncols):
			for y in range(nfils):
				self.casillas[x][y].nivel = generador.get(x, y)


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

class Generador():

	def __init__(self, ncols, nfils, alturas=1, ancho_muros=1, area_habitacion=9, margen_area_habitacion=0.1, seed=0):
		self.ncols = ncols
		self.nfils = nfils
		self.alturas = alturas
		self.ancho_muros = ancho_muros
		self.area_habitacion = area_habitacion
		self.margen_area_habitacion = margen_area_habitacion

		self.id = 0

		self.area_min = int(area_habitacion - area_habitacion * margen_area_habitacion)
		self.area_max = int(area_habitacion + area_habitacion * margen_area_habitacion)

		self.lista_habitaciones = []
		random.seed(seed)

		# Inicializa el mapa de alturas a 0
		self.mapa = self.casillas = [[0 for y in range(nfils)] for x in range(ncols)]
	
	def get(self, x, y):
		""" Devuelve la altura (int) en las coordenadas especificadas
		"""
		return self.mapa[x][y]
	
	def bloques(self, n_bloques = 3, tamanho_min=3, tamanho_max=8):
		for j in range(n_bloques):
			# Punto aleatorio
			x0 = random.randint(0, self.ncols-1)
			y0 = random.randint(0, self.nfils-1)
			
			# Primer bloque
			self.mapa[x0][y0] = 1
			# Siguientes bloques
			tamanho = random.randint(tamanho_min, tamanho_max)
			bloques_colocados = 0
			while bloques_colocados < tamanho:
				# Dirección
				dx = random.randint(-1, 1)
				dy = random.randint(-1, 1)
				try:
					# Reposicionar el origen
					if self.mapa[x0+dx][y0+dy] == 1:
						x0, y0 = x0+dx, y0+dy
						continue

					self.mapa[x0+dx][y0+dy] = 1
					bloques_colocados += 1
				except:
					continue
	
	def bsp(self):
		""" Divide el mapa en habitaciones usando un árbol BSP
		"""
		self._partir_area((0, 0, self.ncols-1, self.nfils-1))
		for h in self.lista_habitaciones:
			self._crear_pasillo(h)
	
	def _partir_area(self, coords):
		print("Generando " + str(coords))
		x0 = coords[0]
		y0 = coords[1]
		x1 = coords[2]
		y1 = coords[3]

		# Salir si el cuadrado se cruza
		if x0 >= x1 or y0 >= y1:
			return
		
		# Comprobamos el tamaño de la habitación antes de seguir
		base = int(x1 - x0)
		altura = int(y1-y0)
		area = int(base * altura)
		if area <= self.area_max:
			return

		# Eliminar la división actual de la lista
		for i in range(len(self.lista_habitaciones)-1):
			if self.lista_habitaciones[i] == coords:
				del self.lista_habitaciones[i]

		# Decidir dirección del muro
		vertical = bool(random.getrandbits(1))

		# Decidir punto
		if vertical:
			punto = random.randint(x0, x1)
			for y in range(y0, self.nfils):
				self.mapa[punto][y] = 1
			self.lista_habitaciones.append((x0, y0, punto-1, y1))
			self.lista_habitaciones.append((punto+1, y0, x1, y1))

		else:
			punto = random.randint(y0, y1)
			for x in range(x0, self.ncols):
				self.mapa[x][punto] = 1
			
			self.lista_habitaciones.append((x0, y0, x1, punto-1))
			self.lista_habitaciones.append((x0, punto+1, x1, y1))
		
		self._partir_area(self.lista_habitaciones[-1])
		self._partir_area(self.lista_habitaciones[-2])

	def _rnd_point_in_habitacion(self, habitacion):
		return (random.randint(habitacion[0], habitacion[2]), random.randint(habitacion[1], habitacion[3]))

	def _crear_pasillo(self, habitacion, n_pasillos=2):
		n_pasillos_creados = 0
		while n_pasillos_creados >= n_pasillos:
			pass
			# Elegir dirección y origren
			#dir = random.choice(list(Direccion))
			dir = Direccion.NORTE
			x0, y0 = self._rnd_point_in_habitacion(habitacion)
			
			# Comprobar si hay otra habitación en esa dirección
			flag_luz_al_final_del_tunel = False
			if dir == Direccion.NORTE:
				for y in range(habitacion[3], self.nfils):
					if self.mapa[x0][y] == 0:
						flag_luz_al_final_del_tunel = True
						print(habitacion)
			
			# Hacer el pasillo