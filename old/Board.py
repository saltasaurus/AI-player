'''Board class'''

import pygame as pg
from src.constants import coin_img

BLACK = (0,0,0)
LIGHT_BLUE = (185,232,234)

class Board():
    '''The area all game pieces lie on

    Handles all sprite visualization and movement checking
    '''

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        # Display
        self._display_surf = None
        self.font = pg.font.SysFont('consalas', 20)

    def render(self, coins, agents) -> None:
        '''Display background, collectables and agents
        
        :param coins: Contains all collectables
        :param agents: Contains all agents
        '''
        # Render background
        self._display_surf.fill(LIGHT_BLUE)

        # Render coins
        for coin in coins:
            coin.draw(self._display_surf)

        # Render agents
        for i, agent in enumerate(agents):
            agent.draw(self._display_surf, agent._surface)
            agent.show_score(self._display_surf, i, self.WIDTH, (0,0,0), self.font)
        
        
        pg.display.flip()

    def set_window(self) -> None:
        '''Initialize game window'''
        pg.display.set_caption("AI Coliseum")
        self._display_surf = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.HWSURFACE)

    def set_surfaces(self, agents: list) -> None:
        '''Initialize all collectables and agents'''
        self._coin_surface = coin_img.convert()
        for agent in agents:
            agent._surface = agent.r_img.convert_alpha()
