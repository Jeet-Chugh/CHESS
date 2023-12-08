from pieces import Rook, Knight, Bishop, Queen, King, Pawn

WHITE = "white"
BLACK = "black"
class Game():

    # Starting new game sets turn to WHITE and populates board
    def __init__(self) -> None:
        self.turn = WHITE
        self.create_board()

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

    def take_user_input(self):
        args = input("Enter your move:    ").split(" ")
        assert len(args) == 2
        start_square = self.square_to_tuple(args[0])
        end_square = self.square_to_tuple(args[1])
        return (start_square, end_square)

    
    @staticmethod
    def square_to_tuple(square_string):
        return (int(square_string[1]) - 1, "abcdefgh".index(square_string[0]))

    # print the chessboard by printing the desired game instance
    def __str__(self) -> str:
        row_list = ["-+--------+-"]
        for i in range(8):
            row_string = str(8 - i) + "|"
            for j in range(8):
                piece_at_location = self.board.get((i, j))
                if piece_at_location is not None:
                    row_string += str(piece_at_location)
                # prints this character if no piece is found at square
                else:
                    row_string += "□"
            row_string += "|" + str(8 - i)
            row_list.append(row_string)
        return "\n".join([" |abcdefgh| "] + row_list + [row_list[0]] + [" |abcdefgh| "])

