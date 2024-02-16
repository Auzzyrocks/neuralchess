


class Board():

    BOARD_SIZE = 8

    arr = [['--']*8 for i in range(8)]

    def __init__(self):

        # print(self.arr)
        def set_white_pawns():

            t = 0
            p0w = Pawn('p0', t)
            p1w = Pawn('p1', t)
            p2w = Pawn('p2', t)
            p3w = Pawn('p3', t)
            p4w = Pawn('p4', t)
            p5w = Pawn('p5', t)
            p6w = Pawn('p6', t)
            p7w = Pawn('p7', t)

            w_pawns = [p0w, p1w, p2w, p3w, p4w, p5w, p6w, p7w]

            for i in range(8):

                self.arr[6][i] = w_pawns[i]
            return
        
        def set_black_pawns():

            t = 1
            p0b = Pawn('p0', t)
            p1b = Pawn('p1', t)
            p2b = Pawn('p2', t)
            p3b = Pawn('p3', t)
            p4b = Pawn('p4', t)
            p5b = Pawn('p5', t)
            p6b = Pawn('p6', t)
            p7b = Pawn('p7', t)

            b_pawns = [p0b, p1b, p2b, p3b, p4b, p5b, p6b, p7b]

            for i in range(8):

                self.arr[1][i] = b_pawns[i]
            return
        
        def set_white_rooks():

            t = 0
            r0w = Rook('r0', t)
            r1w = Rook('r1', t)
            self.arr[self.BOARD_SIZE-1][0] = r0w
            self.arr[self.BOARD_SIZE-1][self.BOARD_SIZE-1] = r1w
            return
        
        def set_black_rooks():

            t = 1
            r0b = Rook('r0', t)
            r1b = Rook('r1', t)
            self.arr[0][0] = r0b
            self.arr[0][self.BOARD_SIZE-1] = r1b
            return
        
        def set_white_knights():

            t = 0
            n0w = Knight('n0', t)
            n1w = Knight('n1', t)
            self.arr[self.BOARD_SIZE-1][1] = n0w
            self.arr[self.BOARD_SIZE-1][self.BOARD_SIZE-2] = n1w
            return

        def set_black_knights():

            t = 1
            n0b = Knight('n0', t)
            n1b = Knight('n1', t)
            self.arr[0][1] = n0b
            self.arr[0][self.BOARD_SIZE-2] = n1b
            return


        def set_board():
            set_white_pawns()
            set_black_pawns()

            set_white_rooks()
            set_black_rooks()

            set_white_knights()
            set_black_knights()
            return
        
        set_board()
        return

    def print_board(self):

        c = 65

        for i in range(self.BOARD_SIZE):
            print(f"{self.BOARD_SIZE-i} ", end='')
            for j in range(self.BOARD_SIZE):
                print(f"| {self.arr[i][j]} ", end='')
            print("| ")
            print((self.BOARD_SIZE*5+2)*"-")
            
        print(f"  ", end='')
        for j in range(self.BOARD_SIZE):
            print(f"| {chr(c+j)}  ", end='')
        print("| ")
        print((self.BOARD_SIZE*5+2)*"-")


class Piece():

    name = ''
    team = 0 # 0 = white, 1 = black 
    num_moves = 0
    move_set = []
    
    def __init__(self, name = '', team = ''):

        self.name = name 
        self.team = team

    def __repr__(self):

        if self.team == 0:
            return 'w' + self.name[0]
        elif self.team == 1:
            return 'b' + self.name[0]

 

class Pawn(Piece):

    move_set = [(0, 1), (0, 2), (-1, 1), (1, 1)]


class Rook(Piece):

    def __init__(self, name = '', team = ''):

        self.name = name
        self.team = team

        for i in range(8):
            self.move_set.append((0, i+1)) 
            self.move_set.append((i+1, 0)) 


class Knight(Piece):

    i = 1
    j = 2
    move_set = [(i, j), (j, i), 
                (-i, j), (j, -i),
                (i, -j), (-j, i),
                (-i, -j), (-j, -i)]