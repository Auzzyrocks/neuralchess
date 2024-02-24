import functools
from copy import copy

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
from gymnasium.spaces import Dict, Discrete, MultiDiscrete
from gymnasium import logger

import numpy as np

def env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = ChessEnv(render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class ChessEnv(AECEnv):
    metadata = {
        "render_modes": ["human"],
        "name": "neuralchess_v1.0",
    }

    def __init__(self, render_mode=None):

        self.OBS_CHANNELS = 12
        self.ACT_CHANNELS = 64

        self.BOARD_SIZE = 6
        self.possible_agents = ["player_0", "player_1"] # White = 0, Black = 1

        self.turns = None
        self.render_mode = render_mode

        self._observation_space = {agent : MultiDiscrete([6, 6, self.OBS_CHANNELS]) for agent in self.possible_agents}
        self._action_space = {agent : MultiDiscrete([6, 6, self.ACT_CHANNELS]) for agent in self.possible_agents}


    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return self._observation_space[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self._action_space[agent]


    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        if self.render_mode is None:
            logger.warn(
                "You are calling render method without specifying any render mode."
            )
            return

        print("There is no rendering currently available for this enviroment...")


    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])


    def close():
        pass


    def reset(self, seed=None, options=None):

        self.agents = copy(self.possible_agents)
        self.num_moves = 0

        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.states = {agent: None for agent in self.agents}

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

        observation = [[[0]*self.BOARD_SIZE for i in range(self.BOARD_SIZE)] for j in range(100)]

        def set_board(obs):
            """Set observations as a new chess board

            Channel 0/5: Pawn
            Channel 1/6: Rook
            Channel 2/7: Knight
            Channel 3/8: Queen
            Channel 4/9: King
            Channel 10: Current Team (White=0)
            Channel 11: Move Counter 

            """    
            # Channels 0-4: White Pieces 

            # White Pawns
            for i in range(self.BOARD_SIZE):
                obs[5][1][i] = 1

            # White Rooks
            obs[6][0][0] = 1
            obs[6][0][5] = 1
            
            # White Knights
            obs[7][0][1] = 1
            obs[7][0][4] = 1
            
            # White Queen
            obs[8][0][2] = 1


            # White King
            obs[9][0][3] = 1

            # Channels 5-9: Black Pieces
            # Black Pawns
            for i in range(self.BOARD_SIZE):
                obs[0][6][i] = 1

            # Black Rooks
            obs[1][5][0] = 1
            obs[1][5][5] = 1
            
            # Black Knights
            obs[2][5][1] = 1
            obs[2][5][4] = 1
                        
            # Black Queen
            obs[3][5][2] = 1

            # Black King
            obs[4][5][3] = 1

            return obs
        
        observation = set_board(observation)    
        self.observations = {agent: observation for agent in self.agents}
                
        return

    def step(self, action):


        # action = Discrete(3)
        # action = (8, 8, 73)

        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step()
            return


        agent = self.agent_selection

        self._cumulative_rewards[agent] = 0

        self.states[self.agent_selection] = action # [agent]?



        # Update board with move...
        # Pick up a piece...
        for channel in self.observations[self.agent_selection][0:11]:
            print(channel)

            if channel[action[0]][action[1]] == 1:
                channel[action[0]][action[1]]

        # Move a piece
        # Need to decode action_space value into a coordinate set (x, y) to add to the pices current position 
        # Dict? arr[73] = [(x, y), ]
        
        # channel[action[0] + x][action[1] + y]


        # Win Checker - Check if either king was taken
        if sum(self._observation_space[self.agent_selection][5][7][4]) == 0:
            # White Lost...
            self.rewards["player_0"] = -1
            self.rewards["player_1"] = 1
            self.terminations["player_0"] = True
            
        elif sum(self._observation_space[self.agent_selection][11][0][4]) == 0: 
            # Black Lost...
            # Set rewards...
            self.rewards["player_0"] = 1
            self.rewards["player_1"] = -1
            self.terminations["player_1"] = True


            
        self.agent_selection = self._agent_selector.next()
        self._accumulate_rewards()

        return


    def render(self):
        pass

