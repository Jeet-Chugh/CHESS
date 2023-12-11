class SquareNotOnBoardError(Exception):
    def __init__(self, square) -> None:
        self.message = f"Unable to find square at location ({str(square['row'])}, {str(square['col'])})"
        super().__init__(self.message)

class InputDecodingError(Exception):
    def __init__(self, input) -> None:
        self.message = f"Unable to decode move with input: \"{input}\""
        super().__init__(self.message)
    
class PieceNotFoundError(Exception):
    def __init__(self, square) -> None:
        self.message = f"Unable to find piece at location ({str(square['row'])}, {str(square['col'])})"
        super().__init__(self.message)

class MoveOutOfTurnError(Exception):
    def __init__(self, given_color, correct_color) -> None:
        self.message = f"Unable to move {given_color} piece during {correct_color}'s turn"
        super().__init__(self.message)