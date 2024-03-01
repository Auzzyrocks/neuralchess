from env import env
from board import board

import random

from pettingzoo.test import api_test


def main():

    ### Testing Board ###
    # board.Board()

    # game = board.Board()

    # game.__init__()


    # done = False
    # team = 0

    # while done is False:

    #     done = game.play_turn(team)

    #     game.total_moves += 1
        
    #     team = not team

    ### DONE TESTING BOARD ###


    ### Testing Env ###
    game = env.env()
    game.reset()



    # while game.game_over is False:

    #     agent = game.agent_selection 
    #     print("Observing from main...")
    #     game.observe(agent)
    #     print("Done observing from main...")
        
    #     done = False

    #     obs_space = game.observation_space(agent)

    #     print("Fetching action space....")

    #     act_space = game.action_space(agent)

    #     print("Fetched ACtion Space:", act_space)

    #     act_mask = obs_space['action_mask']
    #     print(act_mask)

    #     while not done:

    #         action = act_space.sample()
    #         print("ACTION:", action)

    #         if action == 1:
    #             done = True
    #         # done = True

    #     game.step(action)
    
    # # done = True

    # if game.game_over is True:
    #     print("GAME OVER")


    api_test(game, num_cycles=10, verbose_progress=True)
    # print(result[0])

    # print("")



if __name__ == "__main__":


    main()

