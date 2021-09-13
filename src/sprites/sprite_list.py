'''Defines sprite list that will be used in game based on mode

Default:

    Collectable: coin
    Agent: Pacman
    '''

import os

class Sprite_list():
    ''' Create and hold all sprites'''
    def __init__(self, theme='default'):
        self.theme = theme
        self.collectable_sprite = None
        self.player_sprite = None
        self.AI_sprite = []

        # TODO
        # Create JSON or YAML file in each theme folder that maps to each default sprite

    def set_sprites(self):
        '''Set game sprites based on theme'''
        # if os.path.exists()
        pass

    def read_file(self, path):
        '''Read JSON file to get sprite mappings'''
        pass
