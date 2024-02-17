
import random

class Board():

    BOARD_SIZE = 8

    arr = [['--']*8 for i in range(8)]

    def __init__(self):

        self.white = Team(0)
        self.black = Team(1)

        Board.set_board(self)

        
    def set_board(self):

        # Set White
        for piece in self.white.pieces:
            self.arr[piece.pos[0]][piece.pos[1]] = piece

        # Set Black
        for piece in self.black.pieces:
            self.arr[piece.pos[0]][piece.pos[1]] = piece

        return
    
    
    def print_board(self):

        c = 65

        print(f"   ", end='')
        for j in range(self.BOARD_SIZE):
            print(f"  {j}  ", end='')
        print("")
        print("  ", (self.BOARD_SIZE*5)*"-")


        for i in range(self.BOARD_SIZE):
            print(f" {i} ", end='')

            for j in range(self.BOARD_SIZE):
                print(f"| {self.arr[i][j]} ", end='')
            print("|", end='')
            print(f" {self.BOARD_SIZE-i} ")
            print("  ", (self.BOARD_SIZE*5)*"-")
            
        print(f"   ", end='')
        for j in range(self.BOARD_SIZE):
            print(f"  {chr(c+j)}  ", end='')
        print("")

    

    def play_game(self):
            
        checkmate = False
        stalemate = False
        done = False

        team = 0

        while not done:

            valid = False

            if team == 0:

                while not valid:

                    move = self.white.turn()
                    print(" ")
                    # print('White is trying to move...', move)

                    # print(self.white.p0)
                    # print(type(move[0]))
                    # print('Move:', move)


                    ### TEST CASES ###

                    # Rook captures pawn
                    # move = [self.arr[7][7], (-6, 0)]
                    # self.arr[6][7] = '--'

                    # Pawn moving diagonally
                    # move = [self.arr[6][5], (-1, -1)]

                    # Pawn first move, two spaces
                    move = [self.arr[6][5], (-2, 0)]


                    ### END TEST CASES ###

                    cur_pos = move[0].pos
                    new_pos = [cur_pos[0] + move[1][0], cur_pos[1] + move[1][1]]
                    # print("Move from:", cur_pos, "to:", new_pos)


                    valid = self.validate_move(move[0], move[1], cur_pos, new_pos) 
                    
                    if not valid:
                        print("The move was not valid. Try again...")
                        
                    
                    # valid = True

                self.arr[new_pos[0]][new_pos[1]] = move[0]
                move[0].pos = new_pos
                print(move[0], move[0].pos)
                self.arr[cur_pos[0]][cur_pos[1]] = "--"


            elif team == 1:
                #Black Moves
                print('Black is tying to move...')
                pass

            if checkmate or stalemate: 
                done = True

                pass
            
            team = not team # Change Team
            done = True

        return
    

    def validate_move(self, piece, move, cur_pos, new_pos):


        def take_step(move, step):

            # Set first step
            if move[0] < 0:
                step[0] -= 1

            if move[0] > 0:
                step[0] += 1

            if move[1] < 0:
                step[1] -= 1

            if move[1] > 0:
                step[1] += 1

            return step

            
        # Check if move is onto board
        if new_pos[0] < 0 or new_pos [0] >= self.BOARD_SIZE:
            return False
        
        if new_pos[1] < 0 or new_pos [1] >= self.BOARD_SIZE:
            return False
        
        print(type(piece))
        
        # Nothing gets in the way of a knight...
        if type(piece) == "<class 'Pieces.Knight'>":
            print("Nothing gets in the way of a Knight...")
            # print("NOW AT:", pos)

            if self.arr[pos[0]][pos[1]] == '--':
                print("Space is available. Move is Valid.")
                return True

            elif self.arr[pos[0]][pos[1]].team == piece.team:
                print("The space occupied by your own piece...")
                return False
            
            else:
                self.capture()
                # Need to write capture code...
                return True
        

        # Take ya to the pawn shop...
        elif type(piece) is Pawn:

            print("Piece Type: Pawn")

            step = [0, 0]
            pos = list(piece.pos)
            step = take_step(move, step)

            pos[0] += step[0]
            pos[1] += step[1]

            # If trying to make it's first move...
            if piece.num_moves == 0:
                
                if move[0] or move[1] == 2 or -2:

                     # Step to the target position 
                    while pos != new_pos:
                
                        pos[0] += step[0]
                        pos[1] += step[1]

                        if pos != new_pos:
                        
                            # Check a piece is in the way
                            if self.arr[pos[0]][pos[1]] != '--':
                                print("space not empty...")
                                return False
                        
                        # Have reached the target spot..
                        else:  

                            if self.arr[pos[0]][pos[1]] == '--':
                                print("Space is available. Move is Valid.")
                                return True

                            elif self.arr[pos[0]][pos[1]].team == piece.team:
                                print("The space occupied by your own piece...")
                                return False
                            

                pass
            
            #Trying to capture diagonally...
            print(move)
            if (abs(move[0]) + abs(move[1]) ) > 1:

                if self.arr[pos[0]][pos[1]] == '--':
                    print("Pawn cannot move diagonally without capturing... Move invalid")
                    return False
                
                if self.arr[pos[0]][pos[1]].team == piece.team:
                    print("The space occupied by your own piece...")
                    return False
                
                self.capture()
                return True
                
            # Trying to move forward
            else:

                if self.arr[pos[0]][pos[1]] != '--':
                    print("The space is infront of the pawn is occupied...")
                    return False

                print("Pawn is moving forward one space!")
                return True
                pass


        # Piece is not a kinght or Pawn
        else:

            step = [0, 0]
            pos = list(piece.pos)

            step = take_step(move, step)

            # Step to the target position 
            while pos != new_pos:
                
                    pos[0] += step[0]
                    pos[1] += step[1]

                    # print("stepping to:", pos)
                    
                    if pos != new_pos:
                    
                        # Check a piece is in the way
                        if self.arr[pos[0]][pos[1]] != '--':
                            print("space not empty...")
                            return False
                    
                    # Have reached the target spot..
                    else:  

                        # print("NOW AT:", pos)

                        if self.arr[pos[0]][pos[1]] == '--':
                            print("Space is available. Move is Valid.")
                            return True

                        elif self.arr[pos[0]][pos[1]].team == piece.team:
                            print("The space occupied by your own piece...")
                            return False
                        
                        else:
                            self.capture()
                            # Capture!

                            # Need to write capture code...
                            return True


    def capture():
        print("Capturing..!")
        pass


class Team():

    color = 0
    pieces = []
    captured = []

    def __init__(self, color):

        self.color = color

        if self.color == 0:
            # Define White Pieces
            self.p0 = Pawn('p0', color, (6, 0))
            self.p1 = Pawn('p1', color, (6, 1))
            self.p2 = Pawn('p2', color, (6, 2))
            self.p3 = Pawn('p3', color, (6, 3))
            self.p4 = Pawn('p4', color, (6, 4))
            self.p5 = Pawn('p5', color, (6, 5))
            self.p6 = Pawn('p6', color, (6, 6))
            self.p7 = Pawn('p7', color, (6, 7))

            self.r0 = Rook('r0', color, (7, 0))
            self.r1 = Rook('r1', color, (7, 7))

            self.n0 = Knight('n0', color, (7, 1))
            self.n1 = Knight('n1', color, (7, 6))

            self.b0 = Bishop('b0', color, (7, 2))
            self.b1 = Bishop('b1', color, (7, 5))

            self.q0 = Queen('q0', color, (7, 3))
            self.k0 = King('k0', color, (7, 4))
        
        else: 
            # Define Black Pieces
            self.p0 = Pawn('p0', color, (1, 7))
            self.p1 = Pawn('p1', color, (1, 6))
            self.p2 = Pawn('p2', color, (1, 5))
            self.p3 = Pawn('p3', color, (1, 4))
            self.p4 = Pawn('p4', color, (1, 3))
            self.p5 = Pawn('p5', color, (1, 2))
            self.p6 = Pawn('p6', color, (1, 1))
            self.p7 = Pawn('p7', color, (1, 0))

            self.r0 = Rook('r0', color, (0, 7))
            self.r1 = Rook('r1', color, (0, 0))

            self.n0 = Knight('n0', color, (0, 6))
            self.n1 = Knight('n1', color, (0, 1))

            self.b0 = Bishop('b0', color, (0, 5))
            self.b1 = Bishop('b1', color, (0, 2))

            self.q0 = Queen('q0', color, (0, 4))
            self.k0 = King('k0', color, (0, 3))
    
        # Build Piece List
        self.pieces = [self.p0, self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7]
        self.pieces += [self.r0]
        self.pieces += [self.n0]
        self.pieces += [self.b0]
        self.pieces += [self.q0]
        self.pieces += [self.k0]
        self.pieces += [self.b1]
        self.pieces += [self.n1]
        self.pieces += [self.r1]

        # print(self.pieces)
        return


    def turn(self):

        piece = random.choice(self.pieces)
        print('Piece:', piece)

        move = random.choice(piece.move_set)
        print('Move', move)


        return [piece, move]


class Piece():

    name = ''
    team = 0 # 0 = white, 1 = black 
    num_moves = 0
    move_set = []

    pos = (-1, -1)
    
    def __init__(self, name = '', team = '', pos = (-1, 1)):

        self.name = name 
        self.team = team
        self.pos = pos

    def __repr__(self):

        if self.team == 0:
            return 'w' + self.name[0]
            # return 'w' + self.name
        elif self.team == 1:
            return 'b' + self.name[0]
            # return 'b' + self.name


class Pawn(Piece):

    move_set = [(0, 1), (0, 2), (-1, 1), (1, 1)]


class Rook(Piece):

    def __init__(self, name = '', team = '', pos = (-1, 1)):

        # super().__init__()
        self.name = name
        self.team = team
        self.pos = pos
        self.move_set = []

        for n in range(8):
            i = n + 1
            self.move_set.append((i, 0))
            self.move_set.append((0, i)) 
            self.move_set.append((-i, 0)) 
            self.move_set.append((0, -i)) 


class Knight(Piece):

    i = 1
    j = 2
    move_set = [(i, j), (j, i), 
                (-i, j), (j, -i),
                (i, -j), (-j, i),
                (-i, -j), (-j, -i)]
    

class Bishop(Piece):

    def __init__(self, name = '', team = '', pos = (-1, 1)):

        self.name = name 
        self.team = team
        self.pos = pos
        self.move_set = []

        for n in range(8):
            i = n + 1
            self.move_set.append((i, i))
            self.move_set.append((i, -i))
            self.move_set.append((-i, i))
            self.move_set.append((-i, -i))


class Queen(Piece):

    def __init__(self, name = '', team = '', pos = (-1, 1)):

        self.name = name 
        self.team = team
        self.pos = pos
        self.move_set = []

        for n in range(8):
            i = n + 1
            self.move_set.append((i, i))
            self.move_set.append((i, -i))
            self.move_set.append((-i, i))
            self.move_set.append((-i, -i))

            self.move_set.append((i, 0))
            self.move_set.append((0, i)) 
            self.move_set.append((-i, 0)) 
            self.move_set.append((0, -i)) 


class King(Piece):

    move_set = [(0, 1), (1, 0), (0, -1), (-1, 0)]