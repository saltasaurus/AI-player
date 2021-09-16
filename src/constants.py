'''Define all global constants used within game

coin_img
red_img
blue_img
green_img
'''

import pygame as pg

path = "src/sprites/"

coin_img = pg.image.load("src/sprites/default/coin.png")
red_agent = pg.image.load("src/sprites/default/red_player.png")
penguin_agent = pg.image.load("src/sprites/penguins/penguin_left.png")
penguin_left = pg.image.load(path+"penguins/penguin_left.png")
penguin_right = pg.image.load(path+"penguins/penguin_right.png")
penguin_up = pg.image.load(path+"penguins/penguin_up.png")
penguin_down = pg.image.load(path+"penguins/penguin_down.png")
fish_img = pg.image.load(path+"penguins/fish.png")