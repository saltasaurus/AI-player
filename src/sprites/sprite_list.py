'''Defines sprite list that will be used in game based on mode

Default:

    Collectable: coin
    Agent: Pacman
    '''

import json
import os

from pygame.constants import SRCALPHA

class Item_Sprites():

    def __init__(self):
        self.items = []

    def add_sprite(self, x: str):
        self.items.append(x)

class Agent_Sprites():

    def __init__(self):
        self.l_img = None
        self.r_img = None
        self.up_img = None
        self.down_img = None

    def add_agent_sprites(self, sprite_list: dict):
        if 'left' in sprite_list.keys():
            self.l_img = sprite_list['left']
        if 'right' in sprite_list.keys():
            self.r_img = sprite_list['right']
        if 'up' in sprite_list.keys():
            self.up_img = sprite_list['up']
        if 'down' in sprite_list.keys():
            self.down_img = sprite_list['down']

    def get_agent_sprites(self):
        '''Return an agents sprite list
        
        :return: left, right, up, down '''
        return self.l_img, self.r_img, self.up_img, self.down_img


class SpriteLoader():
    ''' Create and hold all sprites'''
    def __init__(self, theme='default'):
        self.theme = theme
        self.collectables = None
        self.agents = None
        self.items = []

    def set_sprites(self):
        '''Set game sprites based on theme'''
        # if os.path.exists()
        pass

    def read_json(self, path):
        '''Read JSON file to get sprite mappings'''

        path = os.path.join(self.theme + "/mappings.json")
        with open(path) as f:
            sprite_list = json.load(f)
        
        sprite_package = sprite_list[self.theme]

        self.agents = sprite_package["agents"]
        self.collectables = sprite_package["collectables"]

    def __str__(self) -> str:
        return f'Game is using the {self.theme} theme'
