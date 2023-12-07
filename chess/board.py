from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self) -> None:
        self.grid = self.create_board()

    # CREATES BOARD AND ASSIGNS PIECES TO STARTING POSITION
    def create_board(self):

        # HELPER FUNCTION TO ASSIGN PIECES TO SQUARES UPON BOARD CREATION
        def assign_piece(num):

            # no pieces assigned to squares 17 - 48
            if (num >= 17 and num <= 48):
                return None
            # white pawns from squares 9 - 16
            if (num >= 9 and num <= 16):
                return Pawn("white")
            # black pawns from squares 49 - 56
            if (num >= 49 and num <= 56):
                return Pawn("black")

            color = "white"
            # switch assignment color to black after 1st rank is filled
            if (num > 8):
                color = "black"

            # ensures the piece_dict works for black and white piecess using our numbering system
            num = num % 56

            piece_dict = {
                1 : Rook(color),
                2 : Knight(color),
                3 : Bishop(color),
                4 : Queen(color),
                5 : King(color),
                6 : Bishop(color),
                7 : Knight(color),
                8 : Rook(color),
            }
            return piece_dict[num]

        # Create empty grid
        grid = [[0 for y in range(8)] for x in range(8)]
        num = 1
        for i in range(0, 8):
            for j in range(0, 8):   
                # Assign each square to a Square Object with its piece defined from assign_piece method
                grid[i][j] = Square(num, assign_piece(num))
                num += 1
        # returns grid in the POV of whites move
        return grid[::-1]
    
    # turns board instance into a print-friendly string
    def __str__(self) -> str:
        printable_string = ""
        for row in self.grid:
            printable_string += "  ".join([str(square.get_piece_name()) for square in row])
            printable_string += "\n"
        return printable_string
    
class Square:
    def __init__(self, number, piece=None) -> None:
        self.number = number
        self.piece = piece

    def get_piece_name(self):
        if (self.piece is None):
            # placeholder for "empty" squares ("empty" = squares without pieces)
            return "0" * 11
        # returns in format "whiteRook"
        return self.piece.color + str(self.piece)
    
    # Returns position of square as a grid location (examples: "h1, b5")
    def get_position(self):
        col_dict = {1 : "a", 2 : "b", 3 : "c", 4 : "d", 5 : "e", 6 : "f", 7 : "g", 0 : "h"}
        return col_dict[self.number % 8] + str(int((self.number - 1) / 8) + 1)