#!/usr/bin/env python3

import arcade
from src import componentes

#region Constantes
SCREEN_TITULO = "Pilla-Pilla"

#Tamaño de los cuadros
TCEL = 60
N_COLS = 17
N_FILS = 12

SCREEN_ANCHO = TCEL * N_COLS
SCREEN_ALTO = TCEL * N_FILS
#endregion

class Pilla(arcade.Window):
	
	def __init__(self):
		super().__init__(SCREEN_ANCHO, SCREEN_ALTO, SCREEN_TITULO)
		arcade.set_background_color(arcade.csscolor.LAWNGREEN)

		self.sprites_tablero = None
		self.tablero = None
	
	def on_draw(self):
		arcade.start_render()



	def setup(self):
		#region Generar terreno

		# Crear el tablero
		self.tablero = componentes.Tablero(N_COLS, N_FILS)

		# Renderizar el tablero
		self.sprites_tablero = arcade.SpriteList()

		#endregion

		#region Colocar jugadores
		#endregion
#end Pilla

if __name__ == '__main__':
	app = Pilla()
	app.setup()
	arcade.run()