'''Initial game call and cleanup'''

from src.Game import Game

# from argparse import ArgumentParser


if __name__ == "__main__":

    # Command Line Argument Parser
    # parser = ArgumentParser.add_argument(description="Artificial Intelligence Game")

    width = 800
    height = 600
    agents = ["Agent Varnson", "BriMachine", "Dinoboy", "Rico", "Agentlement"]

    print("Creating game")
    game = Game(width, height, agents)
    print("Beginning game")
    game.on_play()

    print("Ending game")


