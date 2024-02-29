from env import env
from board import board

import random

from pettingzoo.test import api_test


def main():

    ### Testing Board ###
    # board.Board()

    # game = board.Board()

    # game.__init__()

    # print(game.action_to_move_list)

    # game.print_board()

    # game.play_game()

    # done = False
    # team = 0

    # while done is False:

    #     done = game.play_turn(team)

    #     game.total_moves += 1
        
    #     team = not team

    # print("FINAL OBSERVATION:\n", list(game.board_to_obs()))

    # test_action = 3*5*9
    # print("TEST ACTION TO MOVE:", game.action_to_move(test_action))


    ### Testing Env ###
    game = env.env()

    # test = [[[0]*8 for i in range(8)]]

    # print(test[0])

    game.reset()

    # action = game.action_space(game.agent_selection).sample()

    # print("ACTION:", action)
    # print("ACTION:", action % 6)

    # print("ACTION_TO_MOVE_LIST:", game.action_to_move_list)
    # print("LEN:", len(game.action_to_move_list))

    # game.reset()

    # observation_0, *_ = game.last()

    # print("OBS_0:", observation_0)
    # print("OBS_0 Type:", type(observation_0))

    # if isinstance(observation_0, dict) and "observation" in observation_0:
    #     observation_0 = observation_0["observation"]
    #     print("OBS_0:", observation_0)
    #     print("OBS_0 Type:", type(observation_0))


    # while game.game_over is False:

    #     agent = game.agent_selection 
    #     game.observe(agent)
        
    #     done = False

    #     while not done:

    #         action = random.randint(0, 1764)

    #         obs_space = game.observation_space(agent)

    #         if obs_space["action_mask"] == 1:
    #             done = True

    #     game.step(action)
    #     done = True




    agent = game.agent_selection 
    game.observe(agent)
    
    done = False

    while not done:

        action = random.randint(0, 1764)

        obs_space = game.observation_space(agent)

        if obs_space["action_mask"] == 1:
            done = True
        done= True

    game.step(action)




    # api_test(game, num_cycles=10, verbose_progress=True)
    # print(result[0])

    # print("")



if __name__ == "__main__":


    main()

