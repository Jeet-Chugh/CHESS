from pieces import *
from errors import *

WHITE = "white"
BLACK = "black"
class Game():
    # Starting new game sets turn to WHITE and populates board
    def __init__(self) -> None:
        self.turn = WHITE
        self.check = {WHITE : False, BLACK : False}
        self.createBoard()
        self.startGame()

    def switchTurn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE 

    def createBoard(self):
        # First rank piece placement for WHITE and BLACK
        PIECE_ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        ICON_DICT = {
                BLACK : {Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕", Pawn : "♙"}, 
                WHITE : {Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛", Pawn : "♟"}
            }

        board = {}
        for i in range(8):
            # Populate first and second rank (white)
            board[(0, i)] = PIECE_ORDER[i](color=WHITE, icon=ICON_DICT[WHITE][PIECE_ORDER[i]])
            board[(1, i)] = Pawn(color=WHITE, icon=ICON_DICT[WHITE][Pawn], direction=1)

            # Populate eighth and seventh rank (black)
            board[(7, i)] = PIECE_ORDER[i](color=BLACK, icon=ICON_DICT[BLACK][PIECE_ORDER[i]])
            board[(6, i)] = Pawn(color=BLACK, icon=ICON_DICT[BLACK][Pawn], direction=-1)
        self.board = board

    def startGame(self):
        while True:
            # print the board each turn
            print("\n\n" + str(self) + "\n\n")

            # take the users input and store their intended start and end square, a and b
            a, b = self.takeInput()
            if ((a, b) == (None, None)):
                print("Exiting game loop")
                break

            self.move(a, b)

    def move(self, a, b):
        # Check if start and end square are within the board
        if not Square.isOnBoard(a["row"], a["col"]):
            raise SquareNotOnBoardError(a)
        if not Square.isOnBoard(b["row"], b["col"]):
            raise SquareNotOnBoardError(b)

        # Check if start_square is a piece
        aPiece = self.board.get((a["row"], a["col"]))
        if aPiece is None:
            raise PieceNotFoundError(a)

        # Check if piece is correct color
        if aPiece.color != self.turn:
            raise MoveOutOfTurnError(aPiece.color, self.turn)

        # Check if move is legal
        if not aPiece.validateMove(self.board, a, b):
            raise InvalidMoveError(Square.dictToString(a), Square.dictToString(b))
        
        check = Square.scanForCheck(a, b, self.board)
        # If player does not move out of a check
        if self.check[self.turn] and check[self.turn]:
            raise MoveInCheckError()
        
        # If prospective move exposes player to check
        if self.check[self.turn] == False and check[self.turn]:
            raise ExposingCheckError()
        self.check = check

        # Make the move
        # Castling specific logic
        if type(aPiece) == King and (b["row"], b["col"]) not in King.kingList(a["row"], a["col"]):
            # Queenside castling
            if b["col"] == 2:
                self.board[(b["row"], b["col"])] = self.board[(a["row"], a["col"])]
                self.board[(b["row"], 3)] = self.board[(b["row"], 0)]
                del self.board[(a["row"], a["col"])]
                del self.board[(a["row"], 0)]
            # Kingside castling
            elif b["col"] == 6:
                self.board[(b["row"], b["col"])] = self.board[(a["row"], a["col"])]
                self.board[(b["row"], 5)] = self.board[(b["row"], 7)]
                del self.board[(a["row"], a["col"])]
                del self.board[(a["row"], 7)]
        # normal logic 
        else:
            self.board[(b["row"], b["col"])] = self.board[(a["row"], a["col"])]
            del self.board[(a["row"], a["col"])]
        self.switchTurn()

    def takeInput(self):
        originalArgs = input("Enter your move:    ")

        # command to exit the game loop
        QUIT = "quit"
        if (originalArgs.lower() == QUIT):
            return (None, None)
        
        try:
            args = originalArgs.split(" ")
            a = Square.stringToDict(args[0])
            b = Square.stringToDict(args[1])
            return (a, b)
        except:
            raise InputDecodingError(originalArgs)

    # string representation of the game: used for printing
    def __str__(self) -> str:
        row_list = ["-+--------+-"]
        for i in range(8):
            row_string = str(i + 1) + "|"
            for j in range(8):
                piece_at_location = self.board.get((i, j))
                if piece_at_location is not None:
                    row_string += str(piece_at_location)
                else:
                    # prints this character if no piece is found at square
                    EMPTY_SQUARE = "□"
                    row_string += EMPTY_SQUARE
            row_string += "|" + str(i + 1)
            row_list.append(row_string)
        return "\n".join([" |abcdefgh| "] + [row_list[0]] + row_list[::-1] + [" |abcdefgh| "])