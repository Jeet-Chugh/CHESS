from chess.pieces import Square, Board, Pawn, Rook, Knight, Bishop, Queen, King
from chess.pieces import WHITE, BLACK, ICON_DICT
from chess.errors import *

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
        self.outcome = None

        if self.testMoves:
            self.runTestMoves()

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
            board[(0, i)] = PIECE_ORDER[i](WHITE)
            board[(1, i)] = Pawn(WHITE)

            # Populate eighth and seventh rank (black)
            board[(7, i)] = PIECE_ORDER[i](BLACK)
            board[(6, i)] = Pawn(BLACK)
        return board

    def runTestMoves(self):
        doneTesting = False
        testMovesIndex = 0
        while True:
            # if self.testMoves, pull from that list, otherwise take string input
            if testMovesIndex == len(self.testMoves) - 1:
                doneTesting = True
            i = self.takeInput(self.testMoves[testMovesIndex])
            testMovesIndex += 1

            if i == QUIT:
                return None
            if i == RESIGN:
                self.outcome = self.opposingSide(self.turn)
                break

            if i == DRAW:
                self.outcome = "draw"
                break

            if i.get("drawOffered"):
                if self.offerDraw() == "draw":
                    self.outcome = "draw"
                    break

            self.move(i["a"], i["b"], i.get("promotionPiece"))

            if not i.get("drawOffered") and self.drawOffered:
                self.drawOffered = False

            if self.outcome is not None or doneTesting:
                break

    def move(self, a=None, b=None, promotionPiece=None, input=""):
        if self.outcome is not None:
            raise RuntimeError()

        if not self.testMoves:
            if a is None and b is None:
                i = self.takeInput(input)
                a, b, promotionPiece = i.get("a"), i.get("b"), i.get("promotionPiece")

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
                self.outcome = "draw"
                return

        # check for insufficient material
        if Board.insufficientMaterial(self.board):
            self.outcome = "draw"
            return

        # check for repetition
        if str(self) not in self.positionHistory.keys():
            self.positionHistory[str(self)] = 1
        else:
            self.positionHistory[str(self)] += 1
            if self.positionHistory[str(self)] == 3:
                self.outcome = "draw"
                return

        # scan for checkmate or stalemate
        if self.noLegalMoves():
            if self.check[self.opposingSide(self.turn)]:
                # checkmate
                self.outcome = self.turn
                return
            # stalemate
            self.outcome = "draw"
            return

        self.turn = self.opposingSide(self.turn)

    def offerDraw(self):
        if self.drawOffered:
            return "draw"
        else:
            self.drawOffered = True

    def resign(self):
        self.outcome = self.opposingSide(self.turn)

    def noLegalMoves(self):
        for location, piece in self.board.items():
            if piece.color != self.turn:
                for move in piece.availableMoves(self.board, location[0], location[1]):
                    if not (
                        Board.scanForCheck(
                            Board.executeMove(
                                Square.tupleToDict(location),
                                Square.tupleToDict(move),
                                self.board.copy(),
                            )
                        )[self.opposingSide(self.turn)]
                    ):
                        return False
        return True

    # TAKE INPUT IN THE FOLLOWING FORMAT: a (e2), b (e4), promotionPiece (q), drawOffered (True)
    def takeInput(self, input):
        # Game loop break condition
        if input.lower() == QUIT:
            return QUIT

        if input.lower() == RESIGN:
            return RESIGN

        if input.lower() == DRAW and self.drawOffered:
            return DRAW

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
