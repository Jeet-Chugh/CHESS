class Piece():
    def __init__(self, color, icon) -> None:
        self.color = color
        self.icon = icon

    def __str__(self) -> str:
        return self.icon
    
    def __repr__(self) -> str:
        return self.icon

class Rook(Piece):
    pass
class Knight(Piece):
    pass
class Bishop(Piece):
    pass
class Queen(Piece):
    pass

class King(Piece):
    pass
class Pawn(Piece):
    pass