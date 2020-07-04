#!/usr/bin/env python3

import arcade
from src import componentes

#region Constantes
SCREEN_TITULO = "Pilla-Pilla"

TCEL = 64	#Tamaño de los cuadros
N_COLS = 18
N_FILS = 12

MARGEN_TOP = 10

SCREEN_ANCHO = TCEL * N_COLS
SCREEN_ALTO = TCEL * N_FILS + MARGEN_TOP

PATH_RES = "res/img/"
PATH_RES_TERRENO = PATH_RES + "terreno/"
PATH_IMG_TERRENO = [
	PATH_RES_TERRENO + "mapTile_022.png",
	PATH_RES_TERRENO + "mapTile_027.png"
]
PATH_IMG_J1 = PATH_RES + "pieceYellow_multi05.png"
PATH_IMG_J2 = PATH_RES + "piecePurple_border01.png"
COLOR_J1 = arcade.csscolor.YELLOW
COLOR_J2 = arcade.csscolor.PURPLE
#endregion

class Pilla(arcade.Window):
	
	def __init__(self):
		super().__init__(SCREEN_ANCHO, SCREEN_ALTO, SCREEN_TITULO)
		arcade.set_background_color(arcade.csscolor.LAVENDER)

		self.sprites_tablero = None
		self.sprites_actores = None
		self.tablero = None
		self.j1 = None
		self.j2 = None
		self.color_perseguidor = None

	def setup(self):
		#region Generar terreno

		# Crear el tablero
		self.tablero = componentes.Tablero(N_COLS, N_FILS)

		# Renderizar el tablero
		self.sprites_tablero = arcade.SpriteList()
		for col in self.tablero.casillas:
			for casilla in col:
				# Crear el sprite con el nivel que le corresponde
				sprite = arcade.Sprite(PATH_IMG_TERRENO[casilla.nivel])
				# Calcular la posición según sus coordenadas
				sprite.center_x = (TCEL / 2) + (TCEL * casilla.x)
				sprite.center_y = (TCEL / 2) + (TCEL * casilla.y)

				# Añardirlo a la lista
				self.sprites_tablero.append(sprite)
		
		#endregion

		#region Colocar jugadores

		# Crear sprites actores
		
		#endregion

		# Establecer el color del perseguidor inicial
		self.color_perseguidor = arcade.csscolor.YELLOW
	
	def on_draw(self):
		arcade.start_render()

		# Indicador de perseguidor
		indicador = arcade.SpriteSolidColor(SCREEN_ANCHO, MARGEN_TOP, self.color_perseguidor)
		indicador.top = SCREEN_ALTO
		indicador.left = 0
		indicador.draw()

		self.sprites_tablero.draw()
		#self.sprites_actores.draw()
	
	def get_coords_from_pos(self, x, y):
		return ((TCEL / 2) + (TCEL * x), (TCEL / 2) + (TCEL * y))
	
	def on_key_press(self, symbol: int, modifiers: int):
		if symbol == arcade.key.C:
			if self.color_perseguidor == COLOR_J1:
				self.color_perseguidor = COLOR_J2
			else:
				self.color_perseguidor = COLOR_J1

#end Pilla

if __name__ == '__main__':
	app = Pilla()
	app.setup()
	arcade.run()
