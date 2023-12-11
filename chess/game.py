from pieces import *
from errors import *

WHITE = "white"
BLACK = "black"
class Game():

    # Starting new game sets turn to WHITE and populates board
    def __init__(self) -> None:
        self.turn = WHITE
        self.create_board()
        self.start_game_loop()

    def create_board(self):

        # First rank piece placement for WHITE and BLACK
        PIECE_ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        ICON_DICT = {
                WHITE : {Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕", Pawn : "♙"}, 
                BLACK : {Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛", Pawn : "♟"}
            }

        board = {}
        for i in range(8):

            # Populate first and second rank (white)
            board[(0, i)] = PIECE_ORDER[i](color=WHITE, icon=ICON_DICT[WHITE][PIECE_ORDER[i]])
            board[(1, i)] = Pawn(color=WHITE, icon=ICON_DICT[WHITE][Pawn])

            # Populate eighth and seventh rank (black)
            board[(7, i)] = PIECE_ORDER[i](color=BLACK, icon=ICON_DICT[BLACK][PIECE_ORDER[i]])
            board[(6, i)] = Pawn(color=BLACK, icon=ICON_DICT[BLACK][Pawn])

        self.board = board

    def start_game_loop(self):
        while True:

            # print the board each turn
            print("\n\n" + str(self) + "\n\n")

            # take the users input and store their intended start and end square
            start_square, end_square = self.take_user_input()
            if ((start_square, end_square) == (None, None)):
                print("Exiting game loop")
                break

            self.make_move(start_square, end_square)

    def make_move(self, start_square, end_square):
        # Check if start and end square are within the board
        if not self.valid_square(start_square):
            raise SquareNotOnBoardError(start_square)
        if not self.valid_square(end_square):
            raise SquareNotOnBoardError(end_square)

        # Check if start_square is a piece
        start_piece = self.board.get((start_square["row"], start_square["col"]))
        if start_piece is None:
            raise PieceNotFoundError(start_square)

        # Check if piece is correct color
        start_piece_color = start_piece.color
        correct_color = self.turn
        if start_piece_color != correct_color:
            raise MoveOutOfTurnError(start_piece_color, correct_color)

    def take_user_input(self):
        original_args = input("Enter your move:    ")

        # command to exit the game loop
        QUIT = "quit"
        if (original_args.lower() == QUIT):
            return (None, None)
        
        try:
            args = original_args.split(" ")
            start_square = self.square_to_dict(args[0])
            end_square = self.square_to_dict(args[1])
            return (start_square, end_square)
        except:
            raise InputDecodingError(original_args)

    
    @staticmethod
    def valid_square(square):
        return 0 <= square["row"] < 8 and 0 <= square["col"] < 8
    
    @staticmethod
    def square_to_dict(square_string):
        VALID_COLS = "abcdefgh"
        col_string, row_string = square_string[0], square_string[1:]

        if col_string in VALID_COLS: 
            col_value = VALID_COLS.index(square_string[0])
        else:  
            col_value = -1

        return {"row" : int(row_string) - 1, "col" : col_value}
    
    @staticmethod
    def dict_to_square(square_tuple):
        col_to_file = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
        return col_to_file[square_tuple[1]]


    # string representation of the game: used for printing
    def __str__(self) -> str:
        row_list = ["-+--------+-"]
        for i in range(8):
            row_string = str(8 - i) + "|"
            for j in range(8):
                piece_at_location = self.board.get((i, j))
                if piece_at_location is not None:
                    row_string += str(piece_at_location)
                else:
                    # prints this character if no piece is found at square
                    EMPTY_SQUARE = "□"
                    row_string += EMPTY_SQUARE
            row_string += "|" + str(8 - i)
            row_list.append(row_string)
        return "\n".join([" |abcdefgh| "] + row_list + [row_list[0]] + [" |abcdefgh| "])