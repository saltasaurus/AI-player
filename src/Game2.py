from src.Board2 import Board
from src.Agents2 import ClosestCoinAgent, Djikstra, Greedy, GreedyClose
from src.Items import Coin
import pygame as pg
from pygame.locals import *
import random
import time
  
# Colors
# TODO Add to file for other color manage (i.e. colorblind mode)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

STATUS = None



class Game:
    def __init__(self, width, height, names, rounds = 1):
        self.WIDTH = width
        self.HEIGHT = height
        self.names = names
        self.TOTAL_ROUNDS = rounds
        self.start_point = (10, 300)
        self.end_point = (750, 300)

    def on_init(self):
        '''Reset game'''
        # Initialize pygame
        pg.init()
        # self.font = pg.font.SysFont('consalas', 20)

        self._running = True

        self.create_board()
        self.get_coin_pos(10)
        self.create_coins()
        self.create_agent(0)        

    def on_new_round(self, n):
        self.get_coin_pos(n)
        self.create_coins()
        for agent in self.agents:
            agent.score = 0
            agent.x = 10
            agent.y = 300
            agent.create_path(self.coins)

    def on_next_agent(self, round):
        self.create_coins()
        agent = self.create_agent(round)
        return agent


    # Functions that initialize the board, coins and agents
    def create_board(self):
        self.board = Board(self.WIDTH, self.HEIGHT)

    def get_coin_pos(self, n):
        self.coin_positions = []
        self.values = []
        
        # Create n coins with random values and positions
        for _ in range(n):
            x = random.randrange(0, self.WIDTH-20, 2)
            y = random.randrange(0, self.HEIGHT-20, 2)

            value = random.randint(1, 7)

            pos = (x, y)
            self.coin_positions.append(pos)
            self.values.append(value)

        # Add end "coin" 
        self.coin_positions.append(self.end_point)
        self.values.append(0)
        

    def create_coins(self):
        self.coins = []
        
        for i, ((x,y), v) in enumerate(zip(self.coin_positions, self.values)):
            if v == 0:
                i = -1
            coin = Coin(x, y, v, i)
            self.coins.append(coin)
        print("Num coins created:", len(self.coins))
        
                
    def create_agent(self, turn):
        self.agents = []

        # self.agentTypes = ["Closest", "Djikstra", "GreedyClose"]
        self.agentTypes = ["Closest", "Closest", "Closest"]

        if len(self.agentTypes) != len(self.names):
            raise ValueError
        agent_type = self.agentTypes[turn]
        name = self.names[turn]

        new_agent = None

        x = self.start_point[0]
        y = self.start_point[1]

        if agent_type == 'Closest':
            new_agent = ClosestCoinAgent(x=x, y=y, initial_coins=self.coins)
        elif agent_type == 'Djikstra':
            new_agent = Djikstra(x=x, y=y, initial_coins=self.coins)
        elif agent_type == 'Greedy':
            new_agent = Greedy(x=x, y=y, initial_coins=self.coins)
        elif agent_type == 'GreedyClose':
            new_agent = GreedyClose(x, y, self.coins)

        if new_agent is not None:
            new_agent.name = name

            return new_agent
        else:
            raise ValueError

    def on_play(self):
        global STATUS

        if self.on_init() == False:
            return 

        winner = None
        win_agent = None
        win_score = None

        for current_round in range(1, self.TOTAL_ROUNDS+1):
            
            self.on_new_round(10)
            win_score = 0

            for turn,_ in enumerate(self.names):
                agent = self.on_next_agent(turn)
                r = Round(agent, self.board, self.coins, current_round)
                score = r.on_play()
        
                if STATUS == 'EXIT':
                    break
        
                print(f'{agent.name} scored {score} points')
                if score > win_score:
                    win_agent = agent.name
                    win_score = score
            
            if STATUS == 'EXIT':
                break

            print(f'{win_agent} won round {current_round} with a score of {win_score}')

        self.on_cleanup()

    def on_cleanup(self):
        '''Close PyGame window'''
        pg.quit()

class Round:
    '''Defines the rules for the Agents
    and handles all interactions'''

    def __init__(self, agent, board, coins, round):
        '''
        :param width: (int) Width of Game window
        :param height: (int) Height of Game window
        :param agents: ([string]) List of agent types
        '''
        self.agent = agent
        self.board = board
        self.coins = coins
        self.current_round = round
        self._FPS = 60

        self._running = None


    def on_init(self):

        self._running = True

        # Initialize window
        self.board.set_window()
        
        # initialize surfaces
        self.board.set_surfaces(self.agent)

        self.clock = pg.time.Clock()
        self.clock_tick = self.clock.tick(self._FPS)


    # Functions that handle events
    def on_play(self):
        '''Begins game!'''
        start_time = time.time()
        self._run()
        end_time = time.time()
        score = self.calc_score(self.agent.score, end_time - start_time)
        return score

    def _run(self):
        global STATUS

        # Check for init failure
        if self.on_init() == False:
            self._running = False
        
        # Main game loop
        while self._running:
            self.clock.tick(self._FPS)
            # Check if user quits
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._running = False
                    STATUS = 'EXIT'
            pg.event.pump()
            self.on_loop()
            self.on_render()
        
    def calc_score(self, points, time_taken):
        return round(points / time_taken, 3)

    def on_event(self, event):
        '''Quit game if X (exit) is pressed'''
        if event.type == QUIT:
            self._running = False

    # Functions that handle gameplay
    def on_loop(self):
        # if self.agent.AT_END:
        #     self._running = False
        #     return
        stop = False

        self.agent.target()
        self.agent.update()

        for coin in self.coins:
            if self.agent.collect_coin(coin):
                id = coin.id
                self.agent.score += coin.value
                self.coins.remove(coin)
                if id == -1:
                    print("End point reached")
                    stop = True
                if len(self.coins) == 0:
                    print("All coins collected")
                    stop = True
            if stop:
                self._running = False
                return

    def on_render(self):
        '''Calls board object to render game'''
        self.board.render(self.coins, self.agent)

    def get_winner(self):
        print("Finished: ")
    
    def __str__(self) -> str:
        # return f'Game dimensions: {self.WIDTH} x {self.HEIGHT}'
        return f'{self.agent.name}'



    

