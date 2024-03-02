from env import env
from board import board

import random
import numpy as np

from pettingzoo.test import api_test, seed_test, render_test, performance_benchmark

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
    # render_test(env.env)

    ### Performance Benchmark Test
    performance_benchmark(env.env())

    ### Done Testing Env ###


if __name__ == "__main__":

    main()

