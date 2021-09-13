'''Board class'''

import pygame as pg
from src.constants import coin_img

BLACK = (0,0,0)

class Board():
    '''The area all game pieces lie on

    Handles all sprite visualization and movement checking
    '''

    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        # Display
        self._display_surf = None

    def render(self, coins: list, agents: dict) -> None:
        '''Display background, collectables and agents
        
        :param coins: Contains all collectables
        :param agents: Contains all agents
        '''
        # Render background
        self._display_surf.fill(BLACK)

        # Render coins
        for coin in coins:
            coin.draw(self._display_surf)

        # Render agents
        for agent in agents.values():
            agent.draw(self._display_surf, agent._surface)
        
        pg.display.flip()

    def set_window(self) -> None:
        '''Initialize game window'''
        pg.display.set_caption("AI Coliseum")
        self._display_surf = pg.display.set_mode((self.WIDTH, self.HEIGHT), pg.HWSURFACE)

    def set_surfaces(self, agents: dict) -> None:
        '''Initialize all collectables and agents'''
        self._coin_surface = coin_img.convert()
        for _, agent in agents.items():
            agent._surface = agent.r_img.convert_alpha()
