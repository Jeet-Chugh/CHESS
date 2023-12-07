from pieces import Rook, Knight, Bishop, Queen, King, Pawn
from board import Board

class Game():

    # When starting a new game, create a new board and set it to be whites turn
    def __init__(self) -> None:
        self.board = Board()
        self.turn = "white"

    # printing a game just prints the board
    def __str__(self) -> str:
        return str(self.board)
    
    # alternates turns between black and white, calls move function depending on whos turn it is
    def move(self, from_num, to_num):
        if (self.turn == "white"):
            self.turn = "black"
        elif (self.turn == "black"):
            self.turn = "white"
        else:
            raise ValueError("Illegal turn: " + self.turn)
        
        from_row, from_col = self.board.get_location(from_num)
        found_piece = self.board.grid[from_row][from_col].piece
        if (found_piece is not None):
            pass
        else:
            raise ValueError("No piece found at square number " + from_num)

