import torch
import random
import numpy as np

from collections import deque
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:

    def __init__(self):
        self.number_games = 0

        self.epsilon = 0 # Parameter to control randomness
        self.gamma = 0 # Discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # Call popleft()

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

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