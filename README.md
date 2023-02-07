# Snake Game using Reinforcement Learning
Reinforcement learning is a type of machine learning where an agent learns to make decisions by performing actions in an environment to maximize a reward signal. The agent learns through trial and error, gradually improving its decision-making abilities over time. It's used in problems where the optimal solution is not known beforehand, and the agent must explore its environment to find the best solution. This approach is commonly used in problems such as game playing, robotic control, and recommendation systems.

**The concept of reinforcement learning shares similarities with the traditional education system. However, it has fallen behind in incorporating the recent advancements in technology. I attempted to create a self-learning model and applied it to a snake game to demonstrate the potential improvements that can be achieved. By doing so, I aim to showcase the difference between conventional learning methods and those powered by machine learning.**

# Requirements
- [Anaconda](https://www.anaconda.com/) (Yet Another Configuration System)
- [PyTorch](https://pytorch.org/) (An open source deep learning platform) 

# Table Of Contents
-  [In a Nutshell](#in-a-nutshell)
-  [In Details](#in-details)
-  [Results](#results)

# In a Nutshell   

Reward:
  - eat food +10
  - game over -10
  - else 0
  
Action:
  [1, 0, 0] -> straight
  [0, 1, 0] -> right turn
  [0, 0, 1] -> left turn
  
The game is implemented with the state of the game being represented by the positions of the snake and food on the game board, and the actions being the movements of the snake (up, down, left, right).

The agent uses a reinforcement learning model called Linear_QNet to learn how to play the game. This model is a simple linear regression model that takes the state of the game as input and outputs the Q-values for each possible action. The Q-values represent the expected future rewards for taking a particular action in a given state.

The training process is handled by the QTrainer class, which uses the Q-learning algorithm to update the Q-values based on the observed rewards and the Q-values of the next state. The training process is repeated until the agent is able to play the game optimally.

# Steps to run on your local machine

1. `conda create -n pygame_env`
2. `conda activate pygame_env`
3. `pip install pygame`
4. `pip install torch torchvision`
5. `pip install matplotlib python`
6. `python agent.py`

# In Details
```
├──  model - training model
│    └── Linear_QNet 
│    └── QTrainer
│
├──  agent  
│    └── get_state - initializes the game state
│    └── train - this file contains the train loops
│ 
├──  helper  
│    └── plot - plot the resulting diagram
│
└── game				
     ├── reset - resets the state
     └── is_collision - either hits a boundary or itself
```

# Results

<img width="1288" alt="results" src="https://user-images.githubusercontent.com/85589967/217150521-71113f63-8144-47c6-bb98-f2db8d5fb4a0.png">

The agent is able to learn how to play the game over time, as evidenced by the increasing rewards it receives as it plays more games. After training, the agent is able to play the game optimally, consistently achieving a high score.
