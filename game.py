import pygame
import random

from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20

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

        # Initialize snake
        self.head = Point(self.width / 2, self.height / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. Collect the user's input

        # 2. Move the snake

        # 3. Check if the game is over

        # 4. Place food in a new place or move the snake

        # 5. Update UI and clock

        # 6. Return if game is over and the score afterwards
        game_over = False
        return game_over, self.score


if __name__ == '__main__':
    game = SnakeGame()

    # Game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score: ', score)


    pygame.quit()