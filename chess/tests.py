from game import Game, QUIT, DRAW, RESIGN
from pieces import Pawn, Rook, Knight, Bishop, Queen, King, Square
from pieces import ICON_DICT, WHITE, BLACK
from errors import *
import unittest

TESTING_BOARD = {
    Square.stringtoTuple("e1"): King(WHITE),
    Square.stringtoTuple("d1"): Queen(WHITE),
    Square.stringtoTuple("e8"): King(BLACK),
    Square.stringtoTuple("d8"): Queen(BLACK),
}


def testNormalMove(piece, a, b, board):
    return piece.validateMove(
        board=board,
        a=Square.stringToDict(a),
        b=Square.stringToDict(b),
    )


class TestPawn(unittest.TestCase):
    def test_normalMovesWhite(self):
        piece = Pawn(WHITE)
        a = "d4"
        board = {Square.stringtoTuple(a): piece}
        valid = "d5"
        invalid = "c4,e4,c5,e5,d6".split(",")

        self.assertTrue(testNormalMove(piece, a, valid, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))

    def test_normalMovesBlack(self):
        piece = Pawn(BLACK)
        a = "e5"
        board = {Square.stringtoTuple(a): piece}
        valid = "e4"
        invalid = "d5,f5,d4,f4,e3".split(",")

        self.assertTrue(testNormalMove(piece, a, valid, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))

    def test_enPassantRightWhite(self):
        piece1 = Pawn(WHITE)
        piece2 = Pawn(BLACK)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("d4"): piece1,
            Square.stringtoTuple("e7"): piece2,
        }
        try:
            game = Game(board=board, testMoves=["d4 d5", "e7 e5", "d5 e6"])
            self.assertIsNone(game.outcome)
        except:
            self.fail()

    def test_enPassantRightBlack(self):
        piece1 = Pawn(WHITE)
        piece2 = Pawn(BLACK)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("f2"): piece1,
            Square.stringtoTuple("e4"): piece2,
        }
        try:
            game = Game(board=board, testMoves=["f2 f4", "e4 f3"])
            self.assertIsNone(game.outcome)
        except:
            self.fail()

    def test_enPassantLeftWhite(self):
        piece1 = Pawn(WHITE)
        piece2 = Pawn(BLACK)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("d4"): piece1,
            Square.stringtoTuple("c7"): piece2,
        }
        try:
            game = Game(board=board, testMoves=["d4 d5", "c7 c5", "d5 c6"])
            self.assertIsNone(game.outcome)
        except:
            self.fail()

    def test_enPassantLeftBlack(self):
        piece1 = Pawn(WHITE)
        piece2 = Pawn(BLACK)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("d2"): piece1,
            Square.stringtoTuple("e4"): piece2,
        }
        try:
            game = Game(board=board, testMoves=["d2 d4", "e4 d3"])
            self.assertIsNone(game.outcome)
        except:
            self.fail()

    def test_enPassantExpiration(self):
        piece1 = Pawn(WHITE)
        piece2 = Pawn(BLACK)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("d4"): piece1,
            Square.stringtoTuple("e7"): piece2,
        }
        self.assertRaises(
            InvalidMoveError,
            Game,
            board=board,
            testMoves=["d4 d5", "e7 e5", "e1 d1", "e8 d8", "d5 e6"],
        )

    def test_promotionWhite(self):
        piece = Pawn(WHITE)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("a7"): piece,
        }
        for letter, pieceType in {
            "q": Queen,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
        }.items():
            game = Game(board.copy(), testMoves=["a7 a8 " + letter])
            self.assertTrue(
                type(game.board.get(Square.stringtoTuple("a8"))) == pieceType
            )

    def test_promotionBlack(self):
        piece = Pawn(BLACK)
        board = {
            Square.stringtoTuple("e1"): Queen(WHITE),
            Square.stringtoTuple("e8"): Queen(BLACK),
            Square.stringtoTuple("h2"): piece,
        }
        for letter, pieceType in {
            "q": Queen,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
        }.items():
            game = Game(board.copy(), testMoves=["e1 d1", "h2 h1 " + letter])
            self.assertTrue(
                type(game.board.get(Square.stringtoTuple("h1"))) == pieceType
            )

    def test_doubleMoveWhite(self):
        piece = Pawn(WHITE)
        a = "b2"
        board = {Square.stringtoTuple(a): piece}
        valid = "b3,b4".split(",")
        invalid = "a3,a4,c3,c4,b5".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))

    def test_doubleMoveBlack(self):
        piece = Pawn(BLACK)
        a = "g7"
        board = {Square.stringtoTuple(a): piece}
        valid = "g6,g5".split(",")
        invalid = "f6,h6,f5,h5,g4".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))


class TestRook(unittest.TestCase):
    def test_normalMoves(self):
        piece = Rook(WHITE)
        a = "c2"
        board = {Square.stringtoTuple(a): piece}
        valid = "c1,a2,b2,d2,e2,f2,g2,h2,c3,c4,c5,c6,c7,c8".split(",")
        invalid = "b1,d1,b3,d3".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))


class TestKnight(unittest.TestCase):
    def test_normalMoves(self):
        piece = Knight(WHITE)
        a = "d4"
        board = {Square.stringtoTuple(a): piece}
        valid = "c2,b3,b5,c6,e6,f5,f3,e2".split(",")
        invalid = "c3,d3,e3,c4,e4,c5,d5,e5,d2,b4,d6,f4".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))


class TestBishop(unittest.TestCase):
    def test_normalMoves(self):
        piece = Bishop(WHITE)
        a = "d4"
        board = {Square.stringtoTuple(a): piece}
        valid = "a1,g1,b2,f2,c3,e3,c5,e5,b6,f6,a7,g7,h8".split(",")
        invalid = "d3,c4,e4,d5".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))


class TestQueen(unittest.TestCase):
    def test_normalMoves(self):
        piece = Queen(WHITE)
        a = "d4"
        board = {Square.stringtoTuple(a): piece}
        valid = "a1,d1,g1,b2,d2,f2,c3,d3,e3,a4,b4,c4,e4,f4,g4,h4,c5,d5,e5,b6,d6,f6,a7,d7,g7,d8,h8".split(
            ","
        )
        invalid = "c2,e2,b3,f3,b5,f5,c6,e6".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))


class TestKing(unittest.TestCase):
    def test_normalMoves(self):
        piece = King(WHITE)
        a = "d4"
        board = {Square.stringtoTuple(a): piece}
        valid = "c3,d3,e3,c4,e4,c5,d5,e5".split(",")
        invalid = "b2,c2,d2,e2,f2,b3,f3,b4,f4,b5,f5,b6,c6,d6,e6,f6".split(",")

        for b in valid:
            self.assertTrue(testNormalMove(piece, a, b, board))
        for b in invalid:
            self.assertFalse(testNormalMove(piece, a, b, board))

    def test_castlingQueenWhite(self):
        king = King(WHITE)
        rook = Rook(WHITE)
        board = {
            Square.stringtoTuple("e1"): king,
            Square.stringtoTuple("a1"): rook,
            Square.stringtoTuple("h8"): King(BLACK),
        }

        for square in ["c8", "d8", "e8"]:
            testBoard = board.copy()
            testBoard[Square.stringtoTuple(square)] = Rook(BLACK)
            self.assertRaises(
                InvalidMoveError, Game, board=testBoard, testMoves=["e1 c1"]
            )

        legal = Game(board=board, testMoves=["e1 c1"])
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("c1")), King)
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("d1")), Rook)

    def test_castlingQueenBlack(self):
        king = King(BLACK)
        rook = Rook(BLACK)
        board = {
            Square.stringtoTuple("e8"): king,
            Square.stringtoTuple("a8"): rook,
            Square.stringtoTuple("h1"): King(WHITE),
        }

        for square in ["c1", "d1", "e1"]:
            testBoard = board.copy()
            testBoard[Square.stringtoTuple(square)] = Rook(WHITE)
            self.assertRaises(
                InvalidMoveError, Game, board=testBoard, testMoves=["h1 g1", "e8 c8"]
            )

        legal = Game(board=board, testMoves=["h1 g1", "e8 c8"])
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("c8")), King)
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("d8")), Rook)

    def test_castlingKingWhite(self):
        king = King(WHITE)
        rook = Rook(WHITE)
        board = {
            Square.stringtoTuple("e1"): king,
            Square.stringtoTuple("h1"): rook,
            Square.stringtoTuple("a8"): King(BLACK),
        }

        for square in ["g8", "f8", "e8"]:
            testBoard = board.copy()
            testBoard[Square.stringtoTuple(square)] = Rook(BLACK)
            self.assertRaises(
                InvalidMoveError, Game, board=testBoard, testMoves=["e1 g1"]
            )

        legal = Game(board=board, testMoves=["e1 g1"])
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("g1")), King)
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("f1")), Rook)

    def test_castlingKingBlack(self):
        king = King(BLACK)
        rook = Rook(BLACK)
        board = {
            Square.stringtoTuple("e8"): king,
            Square.stringtoTuple("h8"): rook,
            Square.stringtoTuple("a1"): King(WHITE),
        }

        for square in ["g1", "f1", "e1"]:
            testBoard = board.copy()
            testBoard[Square.stringtoTuple(square)] = Rook(WHITE)
            self.assertRaises(
                InvalidMoveError, Game, board=testBoard, testMoves=["a1 b1", "e8 g8"]
            )

        legal = Game(board=board, testMoves=["a1 b1", "e8 g8"])
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("g8")), King)
        self.assertIsInstance(legal.board.get(Square.stringtoTuple("f8")), Rook)


class TestCheck(unittest.TestCase):
    def test_movingInAndOutOfCheck(self):
        check = Game(board=Game.defaultBoard(), testMoves=["e2 e3", "f7 f6", "d1 h5"])
        self.assertTrue(check.check[BLACK])

        legal = Game(
            board=Game.defaultBoard(), testMoves=["e2 e3", "f7 f6", "d1 h5", "g7 g6"]
        )
        self.assertFalse(legal.check[BLACK])

        self.assertRaises(
            MoveInCheckError,
            Game,
            board=Game.defaultBoard(),
            testMoves=["e2 e3", "f7 f6", "d1 h5", "e8 f7"],
        )
        self.assertRaises(
            ExposingCheckError,
            Game,
            board=Game.defaultBoard(),
            testMoves=["e2 e3", "e7 e6", "d1 h5", "f7 f6"],
        )

    def test_pawnPromotionCheck(self):
        board = TESTING_BOARD.copy()
        board[Square.stringtoTuple("h7")] = Pawn(WHITE)
        game = Game(board=board, testMoves=["h7 h8 r"])
        self.assertTrue(game.check[BLACK])

    def test_enPassantCheck(self):
        board = {
            Square.stringtoTuple("f7"): King(BLACK),
            Square.stringtoTuple("d8"): Queen(BLACK),
            Square.stringtoTuple("e1"): King(WHITE),
            Square.stringtoTuple("d1"): Queen(WHITE),
            Square.stringtoTuple("e7"): Pawn(BLACK),
            Square.stringtoTuple("d4"): Pawn(WHITE),
        }
        game = Game(board=board, testMoves=["d4 d5", "e7 e5", "d5 e6"])
        self.assertTrue(game.check[BLACK])

    def test_castlingCheck(self):
        board = {
            Square.stringtoTuple("e1"): King(WHITE),
            Square.stringtoTuple("h1"): Rook(WHITE),
            Square.stringtoTuple("f8"): King(BLACK),
            Square.stringtoTuple("d8"): Queen(BLACK),
        }
        game = Game(board=board, testMoves=["e1 g1"])
        self.assertTrue(game.check[BLACK])


class TestWinConditions(unittest.TestCase):
    def test_checkmate(self):
        board = {
            Square.stringtoTuple("h8"): King(WHITE),
            Square.stringtoTuple("a6"): King(BLACK),
            Square.stringtoTuple("g2"): Queen(BLACK),
            Square.stringtoTuple("b2"): Rook(WHITE),
            Square.stringtoTuple("b1"): Rook(WHITE),
        }
        game = Game(board=board, testMoves=["b1 a1"])
        self.assertTrue(game.outcome == WHITE)

    def test_stalemate(self):
        board = {
            Square.stringtoTuple("e2"): Queen(WHITE),
            Square.stringtoTuple("a1"): King(WHITE),
            Square.stringtoTuple("h1"): King(BLACK),
        }
        game = Game(board=board, testMoves=["e2 f2"])
        self.assertTrue(game.outcome == DRAW)

    def test_resignation(self):
        board = TESTING_BOARD.copy()
        game = Game(board, testMoves=["d1 c1", RESIGN])
        self.assertTrue(game.outcome == WHITE)

    def test_drawOffering(self):
        board1 = TESTING_BOARD.copy()
        game1 = Game(board=board1, testMoves=["d1 c1 none draw", "d8 c8 none draw"])
        self.assertTrue(game1.outcome == "draw")

        board2 = TESTING_BOARD.copy()
        game2 = Game(board=board2, testMoves=["d1 c1 none draw", "draw"])
        self.assertTrue(game2.outcome == "draw")

        board3 = TESTING_BOARD.copy()
        game3 = Game(board=board3, testMoves=["d1 c1 none draw", "d8 c8"])
        self.assertTrue(game3.outcome == None)

        board4 = TESTING_BOARD.copy()
        game3 = Game(
            board=board4, testMoves=["d1 c1 none draw", "d8 c8", "c1 b1 none draw"]
        )
        self.assertTrue(game3.outcome == None)

    def test_drawByRepetition(self):
        board = TESTING_BOARD.copy()
        game = Game(
            board=board, testMoves=["e1 f1", "e8 f8", "f1 e1", "f8 e8"] * 2 + ["e1 f1"]
        )
        self.assertTrue(game.outcome == "draw")

    def test_drawByInsufficientMaterial(self):
        kings = TESTING_BOARD.copy()
        game = Game(board=kings, testMoves=["d1 d8", "e8 d8"])
        self.assertTrue(game.outcome == "draw")

        knightsDict = {
            Square.stringtoTuple("a1"): Knight(WHITE),
            Square.stringtoTuple("a2"): Knight(WHITE),
            Square.stringtoTuple("a8"): Knight(BLACK),
            Square.stringtoTuple("a7"): Knight(BLACK),
        }
        knights = TESTING_BOARD.copy() | knightsDict.copy()
        game2 = Game(board=knights, testMoves=["d1 d8", "e8 d8"])
        self.assertTrue(game2.outcome == "draw")

        knightAndBishop = TESTING_BOARD.copy() | knightsDict.copy()
        knightAndBishop[Square.stringtoTuple("a1")] = Bishop(WHITE)
        game3 = Game(board=knightAndBishop, testMoves=["d1 d8", "e8 d8"])
        self.assertTrue(game3.outcome == "draw")

        bishops = TESTING_BOARD.copy() | knightsDict.copy()
        bishops[Square.stringtoTuple("a1")] = Bishop(WHITE)
        bishops[Square.stringtoTuple("a2")] = Bishop(WHITE)
        game4 = Game(board=bishops, testMoves=["d1 d8", "e8 d8"])
        self.assertFalse(game4.outcome == "draw")

if __name__ == "__main__":
    unittest.main()
