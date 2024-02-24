from env import env
from board import board

from pettingzoo.test import api_test


def main():

    ### Testing Board ###
    board.Board()

    game = board.Board()

    game.__init__()

    print(game.action_to_move_list)

    # game.print_board()

    # game.play_game()
    done = False
    team = 0

    while done is False:

        done = game.play_turn(team)

        game.total_moves += 1
        
        team = not team

    # print("FINAL OBSERVATION:\n", list(game.board_to_obs()))

    test_action = 3*5*9

    print("TEST ACTION TO MOVE:", game.action_to_move(test_action))


    ### Testing Env ###
    game = env.env()

    # test = [[[0]*8 for i in range(8)]]

    # print(test[0])

    game.reset()

    # action = game.action_space(game.agent_selection).sample()

    # print("ACTION:", action)
    # print("ACTION:", action % 6)

    # api_test(game, num_cycles=10, verbose_progress=True)
    # print(result[0])

    # print("")



if __name__ == "__main__":


    main()

