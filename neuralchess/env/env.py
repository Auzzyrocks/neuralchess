import functools
from copy import copy

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
from gymnasium.spaces import Box, Dict, Discrete, MultiDiscrete
from gymnasium import logger

import numpy as np

from board import board

""" Observation Channel Info

    Game Info:
        Channel 0: Current Team (White=0)
        Channel 1: Move Counter 
        Channel 2: Board Edges (All ones) 

    Piecs:      W/B
        Channel 3/8: Pawn
        Channel 4/9: Rook
        Channel 5/10: Knight
        Channel 6/11: Queen
        Channel 7/12: King
    
    Previous Boards:
        Channel 13-22: Board - 1
        Channel 23-32: Board - 2
        Channel 33-42: Board - 3
        Channel 43-52: Board - 4
        Channel 53-62: Board - 5
        Channel 63-72: Board - 6
        Channel 73-82: Board - 7
"""    


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

        self.OBS_CHANNELS = 83
        self.ACT_CHANNELS = 49

        self.BOARD_SIZE = 6
        self.possible_agents = ["player_0", "player_1"] # White = 0, Black = 1

        self.board = board.Board()
        self.game_over = False

        self.turns = 0
        self.render_mode = render_mode

        self.observation_spaces = {
            agent : Dict(
                {
                    "observation" : Box(low=0, high=1, shape=(6, 6, self.OBS_CHANNELS), dtype=bool),
                    "action_mask" : Box(low=0, high=1, shape=(1764, ), dtype=np.int8)
                }
            ) for agent in self.possible_agents}


        self.action_spaces = {agent : Discrete(6 * 6 * self.ACT_CHANNELS) for agent in self.possible_agents}

        self.board_history = np.zeros((6, 6, 80), dtype=bool)


    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return self.observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self.action_spaces[agent]


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
        observation = self.board.board_to_obs(agent)
        observation = np.dstack((observation[:, :, :3], self.board_history))
        
        action_mask = self.board.get_action_mask()

        return {"observation" : observation, "action_mask" : action_mask}


    def close():
        return


    def reset(self, seed=None, options=None):

        self.__init__()

        self.board.reset()

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

        # observation = [[[0]*self.BOARD_SIZE for i in range(self.BOARD_SIZE)] for j in range(100)]
        observation = Box(low=0, high=1, shape=(6, 6, self.OBS_CHANNELS), dtype=bool)

        # observation = set_board(observation)    
        self.observations = {agent: observation for agent in self.agents}
        return


    def step(self, action):

        print("Starting Step #", self.turns)
        # action = Discrete(3)
        # action = (8, 8, 73)

        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            self._was_dead_step(action)
            return


        agent = self.agent_selection

        team = -1

        if agent == 'player_0':
            team == 0
        else:
            team == 1

        self._cumulative_rewards[agent] = 0

        # self.states[self.agent_selection] = action 

        action = int(action)

        move = self.board.action_to_move(action)

        # print("PRINTING MY ACTION:", action)
        # print("PRINTING MY MOVE:", move)

        legal_moves = self.board.get_legal_moves()

        # print("PRINTING MY ACTION:", action)
        # print("PRINTING MY MOVE:", move)
        # print("LEGAL MOVES:", legal_moves)

        # assert move in legal_moves
        if move not in legal_moves:
            print("Illegal Move:", move)

            for player in self.possible_agents:
                self.terminations[player] = True

                if player is agent:
                    self.rewards[player] = -1
                else:
                    self.rewards[player] = 0

                self.infos[player] = {"legal_moves": []}
                print(player, "tried to play illegal move. Game over...")
                self.game_over = True


        print("** Playing Turn Number:", self.turns)

        done = self.board.play_turn(team, move)

        if done:
            for player in self.agents:
                self.terminations[player] = True

                if player is agent:
                    self.rewards[player] = 1
                else:
                    self.rewards[player] = -1

                self.infos[player] = {"legal_moves": []}
                self.game_over = True


        self.turns += 1
        self._accumulate_rewards()
        self.agent_selection = self._agent_selector.next()

        ### Need to update observation space with previous observations...
        next_board = self.observe(agent)
        # print("NEXT BOARD:", next_board)

        # print(np.shape(self.board_history))
        # print(np.shape(next_board['observation']))

        # self.observation_space[agent]['observation'] = np.dstack((next_board['observation'][:, :, 3:], self.board_history[:, :, :-10]))
        self.observation_spaces[agent] = self.observe(agent)
        # self.observation_space[agent]['action_mask'] = next_board['action_mask']
        
        if self.game_over is False:
            self.render()

        print("Done step #", self.turns)
        return


    def render(self):

        self.board.print_board()
        print("moves:", self.turns)
        pass


    