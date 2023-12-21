from game import Game
from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from pieces import ICON_DICT, WHITE, BLACK
from errors import *
import unittest

class TestPawn(unittest.TestCase):

    def test_normalMovesWhite(self):
        pass

    def test_normalMovesBlack(self):
        pass

    def test_enPassantRightWhite(self):
        pass

    def test_enPassantRightBlack(self):
        pass

    def test_enPassantLeftWhite(self):
        pass

    def test_enPassantLeftBlack(self):
        pass

    def test_enPassantExpiration(self):
        pass

    def test_promotionWhite(self):
        pass

    def test_promotionBlack(self):
        pass

    def test_doubleMoveWhite(self):
        pass

    def test_doubleMoveBlack(self):
        pass

class TestRook(unittest.TestCase):

    def test_normalMoves(self):
        pass

class TestKnight(unittest.TestCase):

    def test_normalMoves(self):
        pass

class TestBishop(unittest.TestCase):

    def test_normalMoves(self):
        pass

class TestQueen(unittest.TestCase):

    def test_normalMoves(self):
        pass

class TestKing(unittest.TestCase):

    def test_normalMoves(self):
        pass

    def test_castlingQueenWhite(self):
        pass

    def test_castlingQueenBlack(self):
        pass

    def test_castlingKingWhite(self):
        pass

    def test_castlingKingBlack(self):
        pass

class TestCheck(unittest.TestCase):

    def test_movingOutOfCheck(self):
        pass

    def test_movingIntoCheck(self):
        pass

    def test_pawnPromotionCheck(self):
        pass

    def test_enPassantCheck(self):
        pass

    def test_castlingCheck(self):
        pass

class TestWinConditions(unittest.TestCase):

    def test_checkmate(self):
        pass

    def test_stalemate(self):
        pass

    def test_resignation(self):
        pass

    def test_drawOffering(self):
        pass

    def test_drawByRepetition(self):
        pass

    def test_fiftyMoveRule(self):
        pass

    def test_drawByInsufficientMaterial(self):
        pass

class TestGames(unittest.TestCase):
    
    def test_game1(self):
        pass

    def test_game2(self):
        pass

    def test_game3(self):
        pass

if __name__ == "__main__":
    unittest.main()