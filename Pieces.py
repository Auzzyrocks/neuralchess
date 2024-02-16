


class Board():

    BOARD_SIZE = 8

    arr = [['--']*8 for i in range(8)]

    def __init__(self):

        self.white = Team(0)
        self.black = Team(1)

        Board.set_board(self)

        
    def set_board(self):

        # Set White 
        for i in range(self.BOARD_SIZE):

            self.arr[6][i] = self.white.pieces[i]
            self.arr[7][i] = self.white.pieces[i + self.BOARD_SIZE]

        # Set Black
        for i in range(self.BOARD_SIZE):
            self.arr[1][i] = self.black.pieces[i]
            self.arr[0][i] = self.black.pieces[i + self.BOARD_SIZE]

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
    


class Team():

    color = 0
    pieces = []
    captured = []

    def __init__(self, color):

        self.color = color

        # Define Pieces
        p0 = Pawn('p0', color)
        p1 = Pawn('p1', color)
        p2 = Pawn('p2', color)
        p3 = Pawn('p3', color)
        p4 = Pawn('p4', color)
        p5 = Pawn('p5', color)
        p6 = Pawn('p6', color)
        p7 = Pawn('p7', color)

        r0 = Rook('r0', color)
        r1 = Rook('r1', color)

        n0 = Knight('n0', color)
        n1 = Knight('n1', color)

        b0 = Bishop('b0', color)
        b1 = Bishop('b1', color)

        q0 = Queen('q0', color)
        k0 = King('k0', color)
    
        # Build Piece List
        self.pieces = [p0, p1, p2, p3, p4, p5, p6, p7]
        self.pieces += [r0]
        self.pieces += [n0]
        self.pieces += [b0]
        self.pieces += [q0]
        self.pieces += [k0]
        self.pieces += [b1]
        self.pieces += [n1]
        self.pieces += [r1]

        # print(self.pieces)
        return




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

        # super().__init__()
        self.name = name
        self.team = team

        for n in range(8):
            i = n + 1
            self.move_set.append((0, i+1)) 
            self.move_set.append((i+1, 0)) 


class Knight(Piece):

    i = 1
    j = 2
    move_set = [(i, j), (j, i), 
                (-i, j), (j, -i),
                (i, -j), (-j, i),
                (-i, -j), (-j, -i)]
    

class Bishop(Piece):

    def __init__(self, name = '', team = ''):

        self.name = name 
        self.team = team

        for i in range(8):
            self.move_set += (i, i)
            self.move_set += (i, -i)
            self.move_set += (-i, i)
            self.move_set += (-i, -i)

class Queen(Piece):

    def __init__(self, name = '', team = ''):

        self.name = name 
        self.team = team

        for n in range(8):

            i = n + 1
            self.move_set += (i, i)
            self.move_set += (i, -i)
            self.move_set += (-i, i)
            self.move_set += (-i, -i)

            self.move_set.append((0, i+1)) 
            self.move_set.append((i+1, 0)) 


class King(Piece):

    move_set = [(0, 1), (1, 0), (0, -1), (-1, 0)]