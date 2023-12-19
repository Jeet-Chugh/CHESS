from pieces import Square, Board, Pawn, Rook, Knight, Bishop, Queen, King
from pieces import WHITE, BLACK, ICON_DICT
from errors import *

class Game():
    def __init__(self) -> None:
        self.turn = WHITE
        self.check = {WHITE : False, BLACK : False}
        self.createBoard()
        self.startGame()

    def switchTurn(self):
        switch = {WHITE : BLACK, BLACK : WHITE}
        self.turn = switch[self.turn]

    def createBoard(self):
        PIECE_ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
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
        gameFinished = False
        while not gameFinished:
            # print the board each turn
            print("\n\n" + str(self) + "\n\n")

            # map user inputted moves to a,b in dict form {"row" : r, "col" : c}
            a, b = self.takeInput()
            if ((a, b) == (None, None)):  break
            
            gameFinished = self.move(a, b)

    def move(self, a, b):

        # Check both squares exist on a board
        if not Square.isOnBoard(a["row"], a["col"]):
            raise SquareNotOnBoardError(a)
        if not Square.isOnBoard(b["row"], b["col"]):
            raise SquareNotOnBoardError(b)

        # Check starting square is a piece
        aPiece = self.board.get((a["row"], a["col"]))
        if aPiece is None:
            raise PieceNotFoundError(a)

        # Check if piece is correct color
        if aPiece.color != self.turn:
            raise MoveOutOfTurnError(aPiece.color, self.turn)

        # Check if move is legal
        if not aPiece.validateMove(self.board, a, b, test=True):
            raise InvalidMoveError(Square.dictToString(a), Square.dictToString(b))
        
        scan = Board.scanForCheck(a, b, self.board)
        Board.updateEnPassant(self.board)

        # If player does not move out of a check
        if self.check[self.turn] and scan["status"][self.turn]:
            raise MoveInCheckError()
        
        # If prospective move exposes player to check
        if self.check[self.turn] == False and scan["status"][self.turn]:
            raise ExposingCheckError()
        self.check = scan["status"]
        print(self.check)

        # If tests have passed, assign updated board
        self.board = scan["board"]

        # If pawn promotion, refresh check conditions
        if type(self.board.get((a["row"], a["col"]))) == Pawn and b["row"] in [0, 7]:
            self.check = Board.scanForCheck(None, None, self.board)

        self.switchTurn()

        # Check for any win conditions
        if self.noLegalMoves():
            if self.check[self.turn]:
                # CHECKMATE
                print(("checkmate, " + self.turn + " wins!").upper())
                return True
            # STALEMATE
            print("STALEMATE!")
            return True

    def noLegalMoves(self):
        for location, piece in self.board.items():
            if piece.color == self.turn:
                for move in piece.availableMoves(self.board, location[0], location[1]):
                    if Board.scanForCheck(Square.tupleToDict(location), Square.tupleToDict(move), self.board)["status"][self.turn] == False:
                        return False
        return True

    def takeInput(self):
        originalArgs = input("Enter your move:    ")

        # Game loop break condition
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

    # string representation of the game used for printing
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