from board import board


def main():

    board.Board()

    game = board.Board()

    game.__init__()

    game.print_board()

    game.play_game()

    game.print_board()



if __name__ == "__main__":


    main()

