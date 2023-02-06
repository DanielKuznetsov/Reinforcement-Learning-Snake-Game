import pygame
import random
import numpy as np

from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# reset
# reward
# play (action) -> direction
# game_iteration
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 15

class SnakeGameAI:

    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # Initialize the display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # Reset the game
        self.reset()


    def reset(self):
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
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        # 1. Collect the user's input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move the snake

        # Update the head
        self._move(action)
        self.snake.insert(0, self.head)

        # 3. Check if the game is over
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward -= 10
            return reward, game_over, self.score

        # 4. Place food in a new place or move the snake
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Return if game is over and the score afterwards
        game_over = False
        return reward, game_over, self.score

    def _is_collision(self, point=None):
        if point is None:
            point = self.head

        # Boundary is hit
        if point.x > self.width - BLOCK_SIZE or point.x < 0 or point.y > self.height - BLOCK_SIZE or point.y < 0:
            return True

        # Or hits itself
        if point in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x + 4, point.y + 4, 12, 12))

        # Food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        # Updating the full surface of the screen
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[index]  # No changes
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (index + 1) % 4
            new_direction = clock_wise[next_idx]  # Right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (index - 1) % 4
            new_direction = clock_wise[next_idx]  # Left turn r -> u -> l ->

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)