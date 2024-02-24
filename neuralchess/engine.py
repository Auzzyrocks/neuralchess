from env import env

from pettingzoo.test import api_test


def main():

    # board.Board()

    # game = board.Board()

    # game.__init__()

    # game.print_board()

    # game.play_game()

    game = env.env()


    # test = [[[0]*8 for i in range(8)]]

    # print(test[0])

    game.reset()

    # api_test(game, num_cycles=10, verbose_progress=True)
    # print(result[0])


    print("")

if __name__ == "__main__":


    main()

