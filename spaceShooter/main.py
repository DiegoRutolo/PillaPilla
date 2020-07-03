#!/usr/bin/env python3

import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade space shooter"
SCALING = 1.5
IMG_PATH = "spaceShooter/res/img/"

SPEED_PLAYER = 5
SPEED_CLOUD_MAX = 3
SPEED_CLOUD_MIN = 1
SPEED_ENEMY_MAX = 15
SPEED_ENEMY_MIN = 5

INTERVAL_ENEMIES = 0.5
DENSITY_ENEMIES = 0.8
INTERVAL_CLOUDS = 1.0
DENSITY_CLOUDS = 0.35


class FlyingSprite(arcade.Sprite):
	def update(self):
		super().update()

		if self.right < 0:
			self.remove_from_sprite_lists()
#end FlyingSprite

class SpaceShooter(arcade.Window):

	def __init__(self, width, height, title):
		super().__init__(width, height, title)

		self.paused = False

		self.enemies_list = arcade.SpriteList()
		self.clouds_list = arcade.SpriteList()
		self.all_sprites = arcade.SpriteList()
	
	def setup(self):
		arcade.set_background_color(arcade.color.SKY_BLUE)

		self.player = arcade.Sprite(IMG_PATH + "jet.png", SCALING)
		self.player.center_y = self.height / 2
		self.player.left = 10
		self.all_sprites.append(self.player)

		arcade.schedule(self.add_enemy, INTERVAL_ENEMIES)
		arcade.schedule(self.add_cloud, INTERVAL_CLOUDS)


	def add_enemy(self, delta_time: float):
		if random.random() > DENSITY_ENEMIES:
			return

		enemy = FlyingSprite(IMG_PATH + "missile.png")

		#enemy.left = random.randint(0, self.width)
		enemy.left = random.randint(self.width, self.width + 80)
		enemy.top = random.randint(10, self.height - 10)

		enemy.velocity = (random.randint(SPEED_ENEMY_MAX * -1, SPEED_ENEMY_MIN * -1), 0)

		self.enemies_list.append(enemy)
		self.all_sprites.append(enemy)


	def add_cloud(self, delta_time: float):
		if random.random() > DENSITY_CLOUDS:
			return
		
		cloud = FlyingSprite(IMG_PATH + "cloud.png")

		cloud.left = random.randint(self.width, self.width + 80)
		cloud.top = random.randint(10, self.height - 10)

		cloud.velocity = (random.randint(SPEED_CLOUD_MAX * -1, SPEED_CLOUD_MIN * -1), 0)

		self.clouds_list.append(cloud)
		self.all_sprites.append(cloud)
	
	def on_update(self, delta_time: float):
		if self.paused:
			return
		
		self.all_sprites.update()

		if self.player.top > self.height:
			self.player.top = self.height
		if self.player.right > self.width:
			self.player.right = self.width
		if self.player.bottom < 0:
			self.player.bottom = 0
		if self.player.left < 0:
			self.player.left = 0
	
	def on_draw(self):
		arcade.start_render()
		self.all_sprites.draw()
	
	def on_key_press(self, symbol, modifiers):
		if symbol == arcade.key.Q:
			arcade.close_window()

		if symbol == arcade.key.P:
			self.paused = not self.paused
		
		if symbol == arcade.key.W or symbol == arcade.key.I or symbol == arcade.key.UP:
			self.player.change_y = SPEED_PLAYER
		if symbol == arcade.key.S or symbol == arcade.key.K or symbol == arcade.key.DOWN:
			self.player.change_y = SPEED_PLAYER * -1
		if symbol == arcade.key.A or symbol == arcade.key.J or symbol == arcade.key.LEFT:
			self.player.change_x = SPEED_PLAYER * -1
		if symbol == arcade.key.D or symbol == arcade.key.L or symbol == arcade.key.RIGHT:
			self.player.change_x = SPEED_PLAYER
	
	def on_key_release(self, symbol, modifiers):
		if (
			symbol == arcade.key.W or
			symbol == arcade.key.I or
			symbol == arcade.key.UP or 
			symbol == arcade.key.S or
			symbol == arcade.key.K or
			symbol == arcade.key.DOWN
		):
			self.player.change_y = 0
		
		if (
			symbol == arcade.key.A or
			symbol == arcade.key.J or
			symbol == arcade.key.LEFT or 
			symbol == arcade.key.D or
			symbol == arcade.key.L or
			symbol == arcade.key.RIGHT
		):
			self.player.change_x = 0

#end SpaceShooter


if __name__ == '__main__':
	app = SpaceShooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	app.setup()
	arcade.run()