#!/usr/bin/env python3

import arcade
from src import componentes

#region Constantes
SCREEN_TITULO = "Pilla-Pilla"

#Tamaño de los cuadros
TCEL = 64
N_COLS = 12
N_FILS = 10

SCREEN_ANCHO = TCEL * N_COLS
SCREEN_ALTO = TCEL * N_FILS

RES_PATH = "res/img/terreno/"
IMG_PATH_TERRENO = [
	RES_PATH + "mapTile_022.png",
	RES_PATH + "mapTile_027.png"
]
#endregion

class Pilla(arcade.Window):
	
	def __init__(self):
		super().__init__(SCREEN_ANCHO, SCREEN_ALTO, SCREEN_TITULO)
		arcade.set_background_color(arcade.csscolor.LAVENDER)

		self.sprites_tablero = None
		self.tablero = None

	def setup(self):
		#region Generar terreno

		# Crear el tablero
		self.tablero = componentes.Tablero(N_COLS, N_FILS)

		# Renderizar el tablero
		self.sprites_tablero = arcade.SpriteList()
		for col in self.tablero.world:
			for casilla in col:
				# Crear el sprite con el nivel que le corresponde
				sprite = arcade.Sprite(IMG_PATH_TERRENO[casilla.nivel])
				# Calcular la posición según sus coordenadas
				sprite.center_x = (TCEL / 2) + (TCEL * casilla.x)
				sprite.center_y = (TCEL / 2) + (TCEL * casilla.y)

				# Añardirlo a la lista
				self.sprites_tablero.append(sprite)
		
		#endregion

		#region Colocar jugadores
		#endregion
	
	def on_draw(self):
		arcade.start_render()
		self.sprites_tablero.draw()

#end Pilla

if __name__ == '__main__':
	app = Pilla()
	app.setup()
	arcade.run()