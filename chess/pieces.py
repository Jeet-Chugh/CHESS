class Square():
    # Checks if square in either form r,c or (r,c) is a valid square on the board
    @staticmethod
    def isOnBoard(r=None, c=None, square=None):
        if square is not None:
            return 0 <= square["row"] < 8 and 0 <= square["col"] < 8
        return 0 <= r < 8 and 0 <= c < 8
    
    # Turns string in format "e4" into dict "{"row" : 3, "col" : 4}"
    @staticmethod
    def stringToDict(squareString):
        VALID_COLS = "abcdefgh"
        colString, rowString = squareString[0], squareString[1:]
        if colString in VALID_COLS: 
            colVal = VALID_COLS.index(squareString[0])
        else:
            colVal = -1
        return {"row" : int(rowString) - 1, "col" : colVal}

    @staticmethod
    def tupleToDict(squareString):
        return {"row" : squareString[0], "col" : squareString[1]}

    # Turns dict in format "{"row" : 3, "col" : 4}" into string in format "e4"
    @staticmethod
    def dictToString(squareDict):
        COL_DICT = {0 : "a", 1 : "b", 2 : "c", 3 : "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}
        return COL_DICT[squareDict["col"]] + str(squareDict["row"] + 1)

class Piece(Square):
    def __init__(self, color, icon) -> None:
        self.color = color
        self.icon = icon
        self.CARDINALS = [(1,0), (0,1), (-1,0), (0,-1)]
        self.DIAGONALS = [(1,1), (-1,1), (1,-1), (-1,-1)]

    # Returns a boolean that dictates whether the move is legal
    def validateMove(self, board, a, b):
        print(a, b)
        return (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"])
    
    def availableMoves(self, board, r, c):
        print("Error: running availableMoves() from Piece parent class")
    
    # Checks if the prospective move is on the board and either empty or an opposing piece
    def noConflict(self, board, r, c):
        return self.isOnBoard(r, c) and (((r, c) not in board) or board[(r, c)].color != self.color)
    
    # Returns list of potential moves using iterative approach on either CARDINALS or DIAGONALS
    def findAvailableMoves(self, board, r, c, intervals):
        moves = []
        for row,col in intervals:
            tempRow, tempCol = r + row, c + col
            while self.isOnBoard(tempRow, tempCol):                
                target = board.get((tempRow, tempCol))
                if target is None: 
                    moves.append((tempRow, tempCol))
                elif target.color != self.color: 
                    moves.append((tempRow, tempCol))
                    break
                else:
                    break
                tempRow, tempCol = tempRow + row, tempCol + col
        return moves

    def __str__(self) -> str:
        return self.icon
    
    def __repr__(self) -> str:
        return self.icon

class Rook(Piece):
    def availableMoves(self, board, r, c):
        return self.findAvailableMoves(board, r, c, self.CARDINALS)
class Knight(Piece):
    # Set of all legal knight moves given a base square
    @staticmethod
    def knightList(r, c, a, b):
        return [(r + a, c + b), (r - a, c + b), (r + a, c - b), (r - a, c - b),
                (r + b, c + a), (r - b, c + a), (r + b, c - a), (r - b, c - a)]

    def availableMoves(self, board, r, c):
        return [(row, col) for row, col in self.knightList(r, c, 2, 1) if self.noConflict(board, row, col)]
class Bishop(Piece):
    def availableMoves(self, board, r, c):
        return self.findAvailableMoves(board, r, c, self.DIAGONALS)
    
class Queen(Piece):
    def availableMoves(self, board, r, c):
        return self.findAvailableMoves(board, r, c, self.CARDINALS + self.DIAGONALS)

class King(Piece):
    # Set of all legal king moves given a base square
    @staticmethod
    def kingList(r, c):
        return [(r + 1, c), (r + 1, c + 1), (r + 1, c - 1), (r, c + 1), 
                (r, c - 1), (r - 1, c), (r - 1, c + 1), (r - 1, c - 1)]

    def availableMoves(self, board, r, c):
        return [(row, col) for row, col in self.kingList(r, c) if self.noConflict(board, row, col)]
    
class Pawn(Piece):
    # Accepts a direction, which is 1 for white and -1 for black
    def __init__(self, color, icon, direction):
        self.color = color
        self.icon = icon
        self.direction = direction
        self.moved = False

    # Overrides validateMove to reset moved to False if the attempted move is illegal
    def validateMove(self, board, a, b):
        if not (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"]):
            self.moved = False
            return False
        return True

    def availableMoves(self, board, r, c):
        moves = []
        forward = False
        # capturing to the left
        if (r + self.direction, c - 1) in board and self.noConflict(board, r + self.direction, c - 1): 
            moves.append((r + self.direction, c - 1))
        # capturing to the right
        if (r + self.direction, c + 1) in board and self.noConflict(board, r + self.direction, c + 1):
            moves.append((r + self.direction, c + 1))
        # moving forward by one
        if (r + self.direction, c) not in board: 
            moves.append((r + self.direction, c))
            forward = True
        # moving forward by two on first move
        if (not self.moved) and forward and (r + (self.direction * 2), c) not in board:
            moves.append((r + (self.direction * 2), c))
            self.moved = True
        return moves