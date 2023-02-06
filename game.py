import pygame
import random

from enum import Enum

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # Initialize the display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # Initialize the game state (direction, food placement)
        self.direction = Direction.RIGHT

    def play_step(self):
        pass


if __name__ == '__main__':
    game = SnakeGame()

    # Game loop
    while True:
        game.play_step()

        # Break the loop if game is over


    pygame.quit()