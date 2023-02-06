import torch
import random
import numpy as np

from model import Linear_QNet, QTrainer
from collections import deque
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:

    def __init__(self):
        self.number_games = 0

        self.epsilon = 0  # Parameter to control randomness
        self.gamma = 0.9  # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # Call popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.snake[0]

        point_left = Point(head.x - 20, head.y)
        point_right = Point(head.x + 20, head.y)
        point_up = Point(head.x, head.y - 20)
        point_down = Point(head.x, head.y + 20)

        dir_left = game.direction == Direction.LEFT
        dir_right = game.direction == Direction.RIGHT
        dir_up = game.direction == Direction.UP
        dir_down = game.direction == Direction.DOWN

        state = [
            # Danger is right in front of us
            (dir_right and game.is_collision(point_right)) or
            (dir_left and game.is_collision(point_left)) or
            (dir_up and game.is_collision(point_up)) or
            (dir_down and game.is_collision(point_down)),

            # Danger on the right
            (dir_up and game.is_collision(point_right)) or
            (dir_down and game.is_collision(point_left)) or
            (dir_left and game.is_collision(point_up)) or
            (dir_right and game.is_collision(point_down)),

            # Danger on the left
            (dir_down and game.is_collision(point_right)) or
            (dir_up and game.is_collision(point_left)) or
            (dir_right and game.is_collision(point_up)) or
            (dir_left and game.is_collision(point_down)),

            # Move direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        # If this exceeds maximum memory, pop left
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.number_games
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state_zero = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_zero)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_score = []
    total_score = 1
    best_score = 0
    agent = Agent()
    game = SnakeGameAI

    while True:
        # Get the current state
        state_old = agent.get_state(game)

        # Get the move
        final_move = agent.get_action(state_old)

        # Perform the move
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # Train short memory of the Agent
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Remember the steps and store in memory
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train the long memory and plot the results
            game.reset()
            agent.number_games += 1
            agent.train_long_memory()

            if score > best_score:
                best_score = score

            print('Game: ', agent.number_games, 'Score: ', score, 'Best Score: ', best_score)

if __name__ == 'main':
    train()