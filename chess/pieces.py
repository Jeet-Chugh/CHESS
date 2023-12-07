class Piece():
    def __init__(self, color) -> None:
        self.color = color

class Rook(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def __str__(self) -> str:
        return "Rook  "

class Knight(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def __str__(self) -> str:
        return "Knight"

class Bishop(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)
    
    def __str__(self) -> str:
        return "Bishop"

class Queen(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def __str__(self) -> str:
        return "Queen "

class King(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def __str__(self) -> str:
        return "King  "

class Pawn(Piece):
    def __init__(self, color) -> None:
        super().__init__(color)

    def __str__(self) -> str:
        return "Pawn  "