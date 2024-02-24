
import random
import numpy as np


class Board():

    BOARD_SIZE = 6
    game_print_board_file = "data/game.txt"

    arr = [['--']*6 for i in range(BOARD_SIZE)]

    def __init__(self):

        self.white = Team(0)
        self.black = Team(1)
        self.total_moves = 0
        self.invalid_move_set = []

        self.action_to_move_list = self.generate_action_to_move_list()

        Board.set_board(self)

        
    def set_board(self):

        # Set White
        for piece in self.white.pieces:
            self.arr[piece.pos[0]][piece.pos[1]] = piece

        # Set Black
        for piece in self.black.pieces:
            self.arr[piece.pos[0]][piece.pos[1]] = piece

        return
    

    def print_board(self, f = None):

        if f != None:
            f = open(self.game_print_board_file, "a")

        c = 65
        print(f"   ", end='', file=f)
        for j in range(self.BOARD_SIZE):
            print(f"  {j}  ", end='', file=f)
        print("", file=f)
        print("   ", (self.BOARD_SIZE*5)*"-", file=f)

        for i in range(self.BOARD_SIZE):
            print(f" {i} ", end='', file=f)

            for j in range(self.BOARD_SIZE):
                print(f"| {self.arr[i][j]} ", end='', file=f)
            print("|", end='', file=f)
            print(f" {self.BOARD_SIZE-i} ", file=f)
            print("   ", (self.BOARD_SIZE*5)*"-", file=f)
            
        print(f"   ", end='', file=f)
        for j in range(self.BOARD_SIZE):
            print(f"  {chr(c+j)}  ", end='', file=f)
        print("", file=f)

        print("")
        print("*" * 47, "\n", file=f)

        if f != None:
            f.close()
        return
    

    def print_stats(self, f = None):

        if f != None:
            f = open(self.game_print_board_file, 'a')

        print("Total Moves:", self.total_moves, file=f)
        print("\nTotal Invalid moves:", sum(self.invalid_move_set), file=f)
        if self.total_moves != 0:
            print("\nAverage Invalid moves / Turn:", sum(self.invalid_move_set) / self.total_moves, file=f)
        print("\nInvalid Moves / Turn:", self.invalid_move_set, file=f)
    
        if f != None:
            f.close()


    def play_game(self, move=None):

        f = open(self.game_print_board_file, "w")
        print("New Game:\n", file=f)
        f.close()

        self.print_board()
        self.print_board(self.game_print_board_file)
            
        done = False
        team = 0 # White moves first

        while not done:

            valid = False

            invalid_moves = 0

            while not valid:

                print("Moves attempted:", invalid_moves)
                print("Valid Moves:", self.total_moves)

                if team == 0:
                    print("White's Turn...")
                    move = self.white.turn()
                else:
                    print("Black's Turn...")
                    move = self.black.turn()

                print(" ")
                # print('White is trying to move...', move)


                ### TEST CASES ###
                TESTING_LIMIT = 1000

                # Rook captures pawn
                # move = [self.arr[7][7], (-6, 0)]
                # self.arr[6][7] = '--'

                # Pawn moving diagonally
                # move = [self.arr[6][5], (-1, -1)]

                # Pawn first move, two spaces
                # move = [self.arr[6][5], (-2, 0)]

                # Pawn moving off the board
                # move = [self.arr[1][5], (0, 2)]

                # Knight first move
                # move = [self.arr[7][1], (-2, 1)]


                ### END TEST CASES ###

                cur_pos = move[0].pos
                new_pos = [cur_pos[0] + move[1][0], cur_pos[1] + move[1][1]]

                valid = self.validate_move(move[0], move[1], new_pos) 
                
                if not valid:
                    print("The move was not valid. Try again...")
                    invalid_moves += 1
    
                    # Debugging
                    if invalid_moves == TESTING_LIMIT:

                        print("Invalid Moves is", TESTING_LIMIT, "... Total moves is:", self.total_moves)

                        self.print_board()
                        self.print_board(self.game_print_board_file)
                        valid = True
                        done = True
                        return True
                
                elif valid: 

                    print("Move is Valid!\n")

                    # Move piece on board

                    # Basic win checker 
                        # Is King on the square we're taking...?
                    winner = -1
                    captured = self.arr[new_pos[0]][new_pos[1]]
                    if type(captured) == King: 

                        if captured.team == 1:
                            winner = 0
                            done = True

                        if captured.team == 0:
                            winner = 1 
                            done = True

                    # End Basic win checker   
                    
                    self.arr[new_pos[0]][new_pos[1]] = move[0] 

                    # update piece object's position
                    move[0].pos = new_pos

                    # Set old space to '--'
                    self.arr[cur_pos[0]][cur_pos[1]] = "--" 

                    # Update total moves and print
                    self.total_moves += 1   

                    print("")

                    # Winner output for Basic win checker
                    if winner != -1:

                        f = open(self.game_print_board_file, 'a')

                        if winner == 0:

                            print("*" * 15)                
                            print("* White Wins! *") 
                            print("*" * 15)  
                        
                            print("*" * 15, file=f)  
                            print("* White Wins! *", file=f)
                            print("*" * 15, file=f)  

                        elif winner == 1:

                            print("*" * 15)  
                            print("* Black Wins! *")
                            print("*" * 15) 
                        
                            print("*" * 15, file=f)  
                            print("* Black Wins! *", file=f)
                            print("*" * 15, file=f)  

                        f.close()

                        self.print_board(self.game_print_board_file)
                        self.print_stats(self.game_print_board_file)

                        self.print_board()
                        self.print_stats()


                    # End Winner output for Basic win checker


            # TURN IS DONE
            team = not team # Change Team
            self.invalid_move_set += [invalid_moves] # Track list of invald_moves / turn
            
        # GAME IS DONE
        return
    

    def play_turn(self, team, input = None):

        state = [self.arr.copy(), None, None, None]
        reward = 0

        f = open(self.game_print_board_file, "w")
        print("New Game:\n", file=f)
        f.close()

        self.print_board()
        self.print_board(self.game_print_board_file)
            
        done = False
        valid = False

        invalid_moves = 0

        while not valid:

            if input is None:
                print("Moves attempted:", invalid_moves)
                print("Valid Moves:", self.total_moves)

                if team == 0:
                    print("White's Turn...")
                    move = self.white.turn()
                else:
                    print("Black's Turn...")
                    move = self.black.turn()
            
            else:
                move = input

            ### TEST CASES ###
            TESTING_LIMIT = 1000

            # Rook captures pawn
            # move = [self.arr[7][7], (-6, 0)]
            # self.arr[6][7] = '--'

            # Pawn moving diagonally
            # move = [self.arr[6][5], (-1, -1)]

            # Pawn first move, two spaces
            # move = [self.arr[6][5], (-2, 0)]

            # Pawn moving off the board
            # move = [self.arr[1][5], (0, 2)]

            # Knight first move
            # move = [self.arr[7][1], (-2, 1)]


            ### END TEST CASES ###

            cur_pos = move[0].pos
            new_pos = [cur_pos[0] + move[1][0], cur_pos[1] + move[1][1]]

            valid = self.validate_move(move[0], move[1], new_pos) 
            
            if not valid:
                print("The move was not valid. Try again...")
                invalid_moves += 1

                # Debugging
                if invalid_moves == TESTING_LIMIT:

                    print("Invalid Moves is", TESTING_LIMIT, "... Total moves is:", self.total_moves)

                    self.print_board()
                    self.print_board(self.game_print_board_file)
                    valid = True
                    done = True
                    return True
            
            elif valid: 

                print("Move is Valid!\n")

                # Move piece on board

                # Basic win checker 
                    # Is King on the square we're taking...?
                winner = -1
                captured = self.arr[new_pos[0]][new_pos[1]]
                if type(captured) == King: 

                    reward = 1

                    if captured.team == 1:
                        winner = 0
                        done = True

                    if captured.team == 0:
                        winner = 1 
                        done = True

                # End Basic win checker   
                
                self.arr[new_pos[0]][new_pos[1]] = move[0] 

                # update piece object's position
                move[0].pos = new_pos

                # Set old space to '--'
                self.arr[cur_pos[0]][cur_pos[1]] = "--" 

                # Update total moves and print
                self.total_moves += 1   

                print("")

                # Winner output for Basic win checker
                if winner != -1:

                    f = open(self.game_print_board_file, 'a')

                    if winner == 0:

                        print("*" * 15)                
                        print("* White Wins! *") 
                        print("*" * 15)  
                    
                        print("*" * 15, file=f)  
                        print("* White Wins! *", file=f)
                        print("*" * 15, file=f)  

                    elif winner == 1:

                        print("*" * 15)  
                        print("* Black Wins! *")
                        print("*" * 15) 
                    
                        print("*" * 15, file=f)  
                        print("* Black Wins! *", file=f)
                        print("*" * 15, file=f)  

                    f.close()

                    self.print_board(self.game_print_board_file)
                    self.print_stats(self.game_print_board_file)

                    self.print_board()
                    self.print_stats()


                    # End Winner output for Basic win checker


        self.invalid_move_set += [invalid_moves] # Track list of invald_moves / turn
        # state[1] = move
        # state[2] = self.arr.copy()
        # state[3] = reward

        # Turn is done
        if done:
            return True #, team, state
        else:
            return False #, team, state


    def take_step(self, move, step):

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
    

    def validate_move(self, piece, move, new_pos):

        # Check if move is onto board
        if new_pos[0] < 0 or new_pos [0] >= self.BOARD_SIZE:
            return False
        
        if new_pos[1] < 0 or new_pos [1] >= self.BOARD_SIZE:
            return False
        
        print(type(piece))
        print("Move:", move)
        print("New Position:", new_pos)

        # KNIGHT: Nothing gets in the way of a knight...
        if type(piece) is Knight:

            if self.validate_knight(piece, new_pos):
                return True
            return False
    
        # PAWN: Take ya to the pawn shop...
        elif type(piece) is Pawn:
            
            if self.validate_pawn(piece, move, new_pos):
                return True
            return False
        
        elif type(piece) is King:

            # Add King move Checking (for castling and ..?)
            # temp solution, treat as type other piece
            if self.validate_other(piece, move, new_pos):
                return True
            return False

        # OTHER: Piece is not a Kinght or Pawn or King
        else:
     
            if self.validate_other(piece, move, new_pos):
                return True
            return False


    def validate_knight(self, piece, new_pos):

        print("Nothing gets in the way of a Knight...")

        if self.arr[new_pos[0]][new_pos[1]] == '--':
            print("Space is available. Move is Valid.")
            return True

        if self.arr[new_pos[0]][new_pos[1]].team == piece.team:
            print("The space occupied by your own piece...")
            return False
        
        else:
            self.capture()
            # Need to write capture code...
            return True
        

    def validate_pawn(self, piece, move, new_pos):

        step = [0, 0]
        pos = list(piece.pos)
        step = self.take_step(move, step)

        print('Move:', move)

        # If trying to move 2 spaces...
        if (move[0] == 2 or move[0] == -2) or (move[1] == 2 or move[1] == -2):

            if piece.num_moves != 0:
                print("Pawn can only move 2 spaces on its first turn...")
                return False
            
            else:
                # Step to the target position 
                while pos != new_pos:

                    pos[0] += step[0]
                    pos[1] += step[1]
            
                    if pos != new_pos:

                        # Check if step is off the board
                        if pos[0] < 0 or pos[1] >= self.BOARD_SIZE:
                            print("Piece is stepping off the board")
                            return False
                        
                        if pos[0] < 0 or pos[1] >= self.BOARD_SIZE:
                            print("Piece is stepping off the board")
                            return False
                        
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

        #Trying to capture diagonally...
        if ( abs(move[0]) + abs(move[1]) ) > 1:

            pos[0] += step[0]
            pos[1] += step[1]

            # Check if step is off the board
            if pos[0] < 0 or pos[1] >= self.BOARD_SIZE:
                print("Piece is stepping off the board")
                return False

            if self.arr[pos[0]][pos[1]] == '--':
                print("Pawn cannot move diagonally without capturing... Move invalid")
                return False
            
            elif self.arr[pos[0]][pos[1]].team == piece.team:
                print("The space occupied by your own piece...")
                return False
            
            else:
                self.capture()
                return True
            
        # Trying to move forward
        else:

            pos[0] += step[0]
            pos[1] += step[1]

            # Need to add pawn upgrading
                # pawns currently will get stuck at the end of the board

            # Check if step is off the board
            if pos[0] < 0 or pos[1] >= self.BOARD_SIZE:
                print("Piece is stepping off the board")
                return False

            if self.arr[pos[0]][pos[1]] != '--':
                print("The space is infront of the pawn is occupied...")
                return False

            else:
                print("Pawn is moving forward one space!")
                return True


    def validate_king(self, piece, move, new_pos):
        pass


    def validate_other(self, piece, move, new_pos):

        step = [0, 0]
        pos = list(piece.pos)
        step = self.take_step(move, step)

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
                    
                    else:
                        self.capture()
                        # Capture!
                        # Need to write capture code...
                        return True
        

    def capture(self):
        print("Capturing..!")
        # Capturing already works by default, because the piece captured is replaced on the board by the capturing piece
        # Not sure what happens when the engine tries to move a piece that has been captured.... should add checking if the piece is still active.. or only choose a move from active pieces
        self.print_board()
        self.print_board(self.game_print_board_file)
        pass


    def action_to_move(self, a: int):
        """Takes an integer representing an action 
            and returns a move to be input to the game"""

        x = a // (6*49)
        y = (a // 49) % 6
        mv = a % (6*49) % 49

        piece = self.arr[x][y]
        move = self.action_to_move_list[mv]

        return [piece, move]


    def generate_action_to_move_list(self):

        actions = []

        # Generate Queen moves
        for x in range(-5, 6):
            for y in range(-5, 6):

                if x==0 or y==0 or abs(x)==abs(y):
                    actions += [[x, y]]
                    # pass

        # Generate Knight Moves
        for x in range(-2, 3):
            for y in range(-2, 3):

                if (abs(x)==2 and abs(y)==1) or (abs(x)==1 and abs(y)==2):
                    actions += [[x, y]]

        print(actions)
        print(len(actions))
        return actions


    CHANNEL_DICT = {

        "wp" : 0, # 3
        "wr" : 1, # 4 ..
        "wn" : 2, 
        "wq" : 3,
        "wk" : 4,

        "bp" : 5,
        "br" : 6, 
        "bn" : 7,
        "bq" : 8,
        "bk" : 9 # .. 12
    }


    def board_to_obs(self):
        """Takes the current board state, converts it to a 3d array 
            represnting an observation and returns"""

        observation = np.zeros((6, 6, 10), dtype=bool)

        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):

                square = self.arr[i][j]

                if square != "--":

                    print("Square not empty.. Updating Obs at:", i, j, self.CHANNEL_DICT[square.__repr__()])
                    observation[i][j][self.CHANNEL_DICT[square.__repr__()]] =True

        return observation


class Team():

    color = 0
    pieces = []
    captured = []

    def __init__(self, color):

        self.color = color

        if self.color == 0:
            # Define White Pieces
            self.p0 = Pawn('p0', color, (4, 0))
            self.p1 = Pawn('p1', color, (4, 1))
            self.p2 = Pawn('p2', color, (4, 2))
            self.p3 = Pawn('p3', color, (4, 3))
            self.p4 = Pawn('p4', color, (4, 4))
            self.p5 = Pawn('p5', color, (4, 5))

            self.r0 = Rook('r0', color, (5, 0))
            self.r1 = Rook('r1', color, (5, 5))

            self.n0 = Knight('n0', color, (5, 1))
            self.n1 = Knight('n1', color, (5, 4))

            self.q0 = Queen('q0', color, (5, 2))
            self.k0 = King('k0', color, (5, 3))
        
        else: 
            # Define Black Pieces
            self.p0 = Pawn('p0', color, (1, 5))
            self.p1 = Pawn('p1', color, (1, 4))
            self.p2 = Pawn('p2', color, (1, 3))
            self.p3 = Pawn('p3', color, (1, 2))
            self.p4 = Pawn('p4', color, (1, 1))
            self.p5 = Pawn('p5', color, (1, 0))

            self.r0 = Rook('r0', color, (0, 5))
            self.r1 = Rook('r1', color, (0, 0))

            self.n0 = Knight('n0', color, (0, 4))
            self.n1 = Knight('n1', color, (0, 1))

            self.q0 = Queen('q0', color, (0, 3))
            self.k0 = King('k0', color, (0, 2))
    
        # Build Piece List
        self.pieces = [self.p0, self.p1, self.p2, self.p3, self.p4, self.p5]
        self.pieces += [self.r0]
        self.pieces += [self.n0]
        self.pieces += [self.q0]
        self.pieces += [self.k0]
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
    
    def __init__(self, name = '', team = '', pos = None):

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

    move_set = [(0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


class Rook(Piece):

    def __init__(self, name = '', team = '', pos = None):

        # super().__init__()
        self.name = name
        self.team = team
        self.pos = pos
        self.move_set = []

        for n in range(Board.BOARD_SIZE):
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
    

# class Bishop(Piece):

#     def __init__(self, name = '', team = '', pos = None):

#         self.name = name 
#         self.team = team
#         self.pos = pos
#         self.move_set = []

#         for n in range(8):
#             i = n + 1
#             self.move_set.append((i, i))
#             self.move_set.append((i, -i))
#             self.move_set.append((-i, i))
#             self.move_set.append((-i, -i))


class Queen(Piece):

    def __init__(self, name = '', team = '', pos = None):

        self.name = name 
        self.team = team
        self.pos = pos
        self.move_set = []

        for n in range(Board.BOARD_SIZE):
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

