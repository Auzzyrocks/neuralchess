from env import env as ChessEnv
from board import board

import tensordict

import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from collections import namedtuple, deque
from torchrl import PettingZooWrapper


from pettingzoo.test import api_test, seed_test, render_test, performance_benchmark, test_save_obs

def myEnvTest(game):

    while game.game_over is False:

        agent = game.agent_selection 
        game.observe(agent)
        
        act_space = game.action_space(agent)

        action = act_space.sample(game.board.get_action_mask())

        game.step(action)

    if game.game_over is True:
        print("GAME OVER")
    return
    
def runEnvTests():
    game = env.env()
    game.reset()

    ### My Test - Working
    # myEnvTest(game)
    # game.reset()
    
    ### Petting Zoo API Test - Working 
    api_test(game, num_cycles=10, verbose_progress=True)


    ### Seed Test - Working 
        # Although, not applying action mask to action.samples..
        # If this is how the model chooses a move, action_mask won't work
    seed_test(env.env, num_cycles=10)

    ### Render Test - Working
    render_test(env.env)

    ### Performance Benchmark Test - Working
    performance_benchmark(env.env())
    
def testBoard():
    board.Board()

    game = board.Board()

    game.__init__()


    done = False
    team = 0

    while done is False:

        done = game.play_turn_backup(team)

        game.total_moves += 1
        
        team = not team
    return


def main():

    # https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

    env = PettingZooWrapper(
        env = ChessEnv.env(),
        use_mask = True,
        group_map = None
    )


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    ### Replay Memory
    Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


    class ReplayMemory(object):

        def __init__(self, capacity):
            self.memory = deque([], maxlen=capacity)

        def push(self, *args):
            """Save a transition"""
            self.memory.append(Transition(*args))

        def sample(self, batch_size):
            return random.sample(self.memory, batch_size)

        def __len__(self):
            return len(self.memory)

    class DQN(nn.Module):

        def __init__(self, n_observations, n_actions, n_internal=1764):
            super(DQN, self).__init__()
            self.layer1 = nn.Linear(n_observations, n_internal)
            self.layer2 = nn.Linear(n_internal, n_internal)
            self.layer3 = nn.Linear(n_internal, n_actions)

        # Called with either one element to determine next action, or a batch
        # during optimization. Returns tensor([[left0exp,right0exp]...]).
        def forward(self, x):
            x = F.relu(self.layer1(x))
            x = F.relu(self.layer2(x))
            return self.layer3(x)

    ### Hyperparameters
        
    # BATCH_SIZE is the number of transitions sampled from the replay buffer
    # GAMMA is the discount factor as mentioned in the previous section
    # EPS_START is the starting value of epsilon
    # EPS_END is the final value of epsilon
    # EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
    # TAU is the update rate of the target network
    # LR is the learning rate of the ``AdamW`` optimizer
    BATCH_SIZE = 128
    GAMMA = 0.99
    EPS_START = 0.9
    EPS_END = 0.05
    EPS_DECAY = 1000
    TAU = 0.005
    LR = 1e-4

    # Get number of actions from gym action space
    n_actions = 1764

    # Get the number of state observations
    state, info = env.reset()
    n_observations = len(state)

    # Usage framework from https://pettingzoo.farama.org/environments/classic/chess/#usage
    # game = env.env()
    # game.reset(seed=42)

    # for agent in game.agent_iter():
    #     observation, reward, termination, truncation, info = game.last()

    #     if termination or truncation:
    #         action = None
    #     else:
    #         mask = observation["action_mask"]
    #         # this is where you would insert your policy


    #         action = game.action_space(agent).sample(mask)

    #     game.step(action)
    # game.close()



if __name__ == "__main__":

    main()

