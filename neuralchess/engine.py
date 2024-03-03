from env import env
from board import board

import random
import numpy as np

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

    # runEnvTests()


    # Usage framework from https://pettingzoo.farama.org/environments/classic/chess/#usage
    game = env.env()
    game.reset(seed=42)

    for agent in game.agent_iter():
        observation, reward, termination, truncation, info = game.last()

        if termination or truncation:
            action = None
        else:
            mask = observation["action_mask"]
            # this is where you would insert your policy


            action = game.action_space(agent).sample(mask)

        game.step(action)
    game.close()



if __name__ == "__main__":

    main()

