from pieces import Square, Board, Pawn, Rook, Knight, Bishop, Queen, King
from pieces import WHITE, BLACK, ICON_DICT
from errors import *

QUIT = "quit"
RESIGN = "resign"
DRAW = "draw"


class Game:
    def __init__(self, board, testMoves=False) -> None:
        self.turn = WHITE
        self.check = {WHITE: False, BLACK: False}
        self.drawOffered = False
        self.fiftyMoveRule = 0
        self.positionHistory = {}
        self.boardHistory = []
        self.testMoves = testMoves
        self.board = board
        self.outcome = self.startGame()

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
        if self.testMoves:
            testMovesIndex = 0
        while True:
            # print the board each turn
            print("\n\n" + str(self) + "\n\n")

            # if self.testMoves, pull from that list, otherwise take string input
            if not self.testMoves:
                i = self.takeInput(input("Enter your move:    "))
            else:
                i = self.takeInput(self.testMoves[testMovesIndex])
                testMovesIndex += 1
                if len(self.testMoves) == testMovesIndex:
                    return None

            if i == QUIT:
                return None
            if i == RESIGN:
                return self.opposingSide(self.turn)

            if self.drawOffered:
                if i.get("drawOffered"):
                    return "draw"
                else:
                    self.drawOffered = False
            else:
                if i.get("drawOffered"):
                    self.drawOffered = True

            outcome = self.move(i["a"], i["b"], i.get("promotionPiece"))
            if outcome is not None:
                return outcome

    def move(self, a, b, promotionPiece):
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
        self.board = Board.executeMove(a, b, self.board, promotionPiece)
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

    # TAKE INPUT IN THE FOLLOWING FORMAT: a (e2), b (e4), promotionPiece (q), drawOffered (True)
    @staticmethod
    def takeInput(input):

        # Game loop break condition
        if input.lower() == QUIT:
            return QUIT

        if input.lower() == RESIGN:
            return RESIGN

        try:
            resultDict = {}
            args = input.split(" ")
            if len(args) >= 2:
                resultDict = {
                    "a": Square.stringToDict(args[0]),
                    "b": Square.stringToDict(args[1]),
                }

            if len(args) >= 3:
                promotionDict = {"r": Rook, "n": Knight, "b": Bishop, "q": Queen}
                resultDict["promotionPiece"] = promotionDict.get(args[2])
            
            if len(args) == 4:
                if args[3] == DRAW:
                    resultDict["drawOffered"] = True

            return resultDict
        except:
            raise InputDecodingError(input)

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
