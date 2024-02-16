import Pieces



if __name__ == "__main__":


    board = Pieces.Board()

    board.__init__()

    board.print_board()

    board.play_game()

    board.print_board()