from pieces import Square, Board, Pawn, Rook, Knight, Bishop, Queen, King
from pieces import WHITE, BLACK, ICON_DICT
from errors import *


class Game:
    def __init__(self) -> None:
        self.turn = WHITE
        self.check = {WHITE: False, BLACK: False}
        self.drawOffered = False
        self.fiftyMoveRule = 0
        self.positionHistory = {}
        self.boardHistory = []
        self.board = self.defaultBoard()
        self.startGame()

    @staticmethod
    def opposingSide(turn):
        switch = {WHITE: BLACK, BLACK: WHITE}
        return switch[turn]

    @staticmethod
    def defaultBoard():
        PIECE_ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        board = {}
        for i in range(8):
            # Populate first and second rank (white)
            board[(0, i)] = PIECE_ORDER[i](
                color=WHITE, icon=ICON_DICT[WHITE][PIECE_ORDER[i]]
            )
            board[(1, i)] = Pawn(color=WHITE, icon=ICON_DICT[WHITE][Pawn], direction=1)

            # Populate eighth and seventh rank (black)
            board[(7, i)] = PIECE_ORDER[i](
                color=BLACK, icon=ICON_DICT[BLACK][PIECE_ORDER[i]]
            )
            board[(6, i)] = Pawn(color=BLACK, icon=ICON_DICT[BLACK][Pawn], direction=-1)
        return board

    def startGame(self):
        gameFinished = False
        while not gameFinished:
            # print the board each turn
            print("\n\n" + str(self) + "\n\n")

            # map user inputted moves to a,b in dict form {"row" : r, "col" : c}
            a, b, arg = self.takeInput()
            if (a, b) == (None, None):
                break

            # resignation
            if (a, b) == ("resign", None):
                return self.opposingSide(self.turn)

            # draw
            if self.drawOffered:
                if arg is not None and arg == "draw":
                    return "draw"
                else:
                    self.drawOffered = False
            else:
                if arg is not None and arg == "draw":
                    self.drawOffered = True

            gameFinished = self.move(a, b)
        print(gameFinished)

    def move(self, a, b, c=None):
        self.boardHistory.append(self.board.copy())
        Board.updateEnPassant(self.board)

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
        if not aPiece.validateMove(self.board, a, b):
            raise InvalidMoveError(Square.dictToString(a), Square.dictToString(b))

        # Make the move
        self.board = Board.executeMove(a, b, self.board)
        checkStatus = Board.scanForCheck(self.board)

        # If player does not move out of a check
        if checkStatus[self.turn] and self.check[self.turn]:
            self.board = self.boardHistory[-1]
            raise MoveInCheckError()

        # If prospective move exposes player to check
        if not self.check[self.turn] and checkStatus[self.turn]:
            self.board = self.boardHistory[-1]
            raise ExposingCheckError()

        self.check = checkStatus

        # DONE VALIDATING MOVE

        # 50 move rule
        if (
            type(aPiece) == Pawn
            or self.boardHistory[-1].get((b["row"], b["col"])) is not None
        ):
            self.fiftyMoveRule = 0
        else:
            self.fiftyMoveRule += 1
            if self.fiftyMoveRule == 50:
                return "draw"

        # check for insufficient material
        if Board.insufficientMaterial(self.board):
            return "draw"

        # check for repetition
        if str(self) not in self.positionHistory.keys():
            self.positionHistory[str(self)] = 1
        else:
            self.positionHistory[str(self)] += 1
            for count in self.positionHistory.values():
                if count == 3:
                    return "draw"

        # if pawn promotion, refresh check conditions
        if type(aPiece) == Pawn and b["row"] in [0, 7]:
            self.check = Board.scanForCheck(self.board)

        # scan for checkmate or stalemate
        if self.noLegalMoves():
            if self.check[self.turn]:
                # checkmate
                return self.opposingSide(self.turn)
            # stalemate
            return "draw"

        self.turn = self.opposingSide(self.turn)

    def noLegalMoves(self):
        for location, piece in self.board.items():
            if piece.color == self.turn:
                for move in piece.availableMoves(self.board, location[0], location[1]):
                    if not (
                        Board.scanForCheck(
                            Board.executeMove(
                                Square.tupleToDict(location),
                                Square.tupleToDict(move),
                                self.board.copy(),
                            )
                        )[self.turn]
                    ):
                        return False
        return True

    def takeInput(self):
        originalArgs = input("Enter your move:    ")

        # Game loop break condition
        QUIT = "quit"
        if originalArgs.lower() == QUIT:
            return (None, None)

        RESIGN = "resign"
        if originalArgs.lower() == RESIGN:
            return ("resign", None)

        try:
            args = originalArgs.split(" ")
            a = Square.stringToDict(args[0])
            b = Square.stringToDict(args[1])
            if len(args) > 2:
                return (a, b, args[2])
            return (a, b, None)
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
        return "\n".join(
            [" |abcdefgh| "] + [row_list[0]] + row_list[::-1] + [" |abcdefgh| "]
        )
