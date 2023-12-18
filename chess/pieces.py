WHITE = "white"
BLACK = "black"

class Square():
    # Checks if square in form row,col is on the board
    @staticmethod
    def isOnBoard(r, c):
        return 0 <= r < 8 and 0 <= c < 8
    
    @staticmethod
    def scanForCheck(a, b, board):

        def canSeeKing(kingLocation, pieceList, board):
            for piece,position in pieceList:
                if piece.validateMove(board, Square.tupleToDict(position), Square.tupleToDict(kingLocation)):
                    return True
            return False
    
        # create shallow copy of board to see if prospective move causes check
        prospectiveBoard = board.copy()

        # make the move on the copied board
        if a != b:
            prospectiveBoard[(b["row"], b["col"])] = prospectiveBoard[(a["row"], a["col"])]
            del prospectiveBoard[(a["row"], a["col"])]

        # find locations for both kings on the board
        kingLocations = {}
        pieceDict = {BLACK : [], WHITE : []}
        for location,piece in prospectiveBoard.items():
            if type(piece) == King:
                kingLocations[piece.color] = location
                continue
            if type(piece) == Pawn:
                piece.enPassant["age"] += 1
                if piece.enPassant["age"] > 1:
                    piece.enPassant["age"] = 0
                    piece.enPassant["col"] = -1
            pieceDict[piece.color].append((piece, location))

        # Returns a dictionary that determines each colors check status
        checkDict = {}
        checkDict[WHITE] = canSeeKing(kingLocations[WHITE], pieceDict[BLACK], prospectiveBoard)
        checkDict[BLACK] = canSeeKing(kingLocations[BLACK], pieceDict[WHITE], prospectiveBoard)
        return checkDict
    
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

    # Turns tuple in format (r, c) into dict with format {"row" : row, "col" : col}
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
    def validateMove(self, board, a, b, test=False):
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

# Class for pieces that need to be tracked for their first move (king, rook)
class TrackedPiece(Piece):
    def __init__(self, color, icon) -> None:
        super().__init__(color, icon)
        self.moved = False

    # Overrides validateMove to reset moved to False if the attempted move is illegal
    def validateMove(self, board, a, b, test=False):
        validity = (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"])
        if not self.moved:
            self.moved = validity
        return validity

class Rook(TrackedPiece):
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

class King(TrackedPiece):
    # Set of all legal king moves given a base square
    @staticmethod
    def kingList(r, c):
        return [(r + 1, c), (r + 1, c + 1), (r + 1, c - 1), (r, c + 1), 
                (r, c - 1), (r - 1, c), (r - 1, c + 1), (r - 1, c - 1)]

    def availableMoves(self, board, r, c):
        castlingMoves = self.castlingMoves(board, r, c)
        return [(row, col) for row, col in self.kingList(r, c) if self.noConflict(board, row, col)] + castlingMoves
    
    # Overrides validateMove to reset moved to False if the attempted move is illegal
    def validateMove(self, board, a, b, test=False):
        if test:
            print(self.availableMoves(board, a["row"], a["col"]))
        validity = (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"])
        if not self.moved:
            self.moved = validity
        return validity

    def castlingMoves(self, board, r, c):
        if self.color == WHITE:  col = 0
        elif self.color == BLACK:  col = 7
        castlingMoves = []

        # If we are WHITE and the king hasnt moved
        if self.moved:
            return castlingMoves
        
        # queenside castle, rook present, rook hasnt moved, no pieces in between 
        if type(board.get((col, 0))) == Rook and board.get((col, 0)).moved == False \
            and [board.get((col, 1)), board.get((col, 2)), board.get((col, 3))] == [None, None, None]:
            # if we arent currently in check
            if self.scanForCheck(self.tupleToDict((col, 4)), self.tupleToDict((col, 4)), board)[self.color] == False:
                # if moving one to the left doesnt result in check
                if self.scanForCheck(self.tupleToDict((0, 4)), self.tupleToDict((col, 3)), board)[self.color] == False:
                    prospectiveBoard = board.copy()
                    prospectiveBoard[(col, 3)] = prospectiveBoard[(col, 4)]
                    del prospectiveBoard[(col, 4)]
                    # if moving two to the left doesnt result in check
                    if self.scanForCheck(self.tupleToDict((col, 3)), self.tupleToDict((col, 2)), prospectiveBoard)[self.color] == False:
                        castlingMoves.append((col, 2))

        # kingside castle, rook present, rook hasnt moved, no pieces in between 
        if type(board.get((col, 7))) == Rook and board.get((col, 7)).moved == False \
        and [board.get((col, 5)), board.get((col, 6))] == [None, None]:
            # if we arent currently in check
            if self.scanForCheck(self.tupleToDict((col, 4)), self.tupleToDict((col, 4)), board)[self.color] == False:
                # if moving one to the right doesnt result in check
                if self.scanForCheck(self.tupleToDict((col, 4)), self.tupleToDict((col, 5)), board)[self.color] == False:
                    prospectiveBoard = board.copy()
                    prospectiveBoard[(col, 5)] = prospectiveBoard[(col, 4)]
                    del prospectiveBoard[(col, 4)]
                    # if moving two to the right doesnt result in check
                    if self.scanForCheck(self.tupleToDict((col, 5)), self.tupleToDict((col, 6)), prospectiveBoard)[self.color] == False:
                        castlingMoves.append((col, 6))
        return castlingMoves

class Pawn(Piece):
    # Accepts a direction, which is 1 for white and -1 for black
    def __init__(self, color, icon, direction):
        self.color = color
        self.icon = icon
        self.direction = direction
        # En passant validity status for each individual piece
        self.enPassant = {"col" : -1, "age" : 0}

    def availableMoves(self, board, r, c):
        moves = []
        # En passant
        if self.enPassant["col"] != -1 and self.color == WHITE and r == 4:
            moves.append((5, self.enPassant["col"]))
        elif self.enPassant["col"] != -1 and self.color == BLACK and r == 3:
            moves.append((2, self.enPassant["col"]))
        # capturing to the left
        if (r + self.direction, c - 1) in board and self.noConflict(board, r + self.direction, c - 1): 
            moves.append((r + self.direction, c - 1))
        # capturing to the right
        if (r + self.direction, c + 1) in board and self.noConflict(board, r + self.direction, c + 1):
            moves.append((r + self.direction, c + 1))
        # moving forward by one
        if (r + self.direction, c) not in board: 
            moves.append((r + self.direction, c))
        # moving forward by two on first move
        if self.color == WHITE and r == 1 and ((r + self.direction, c) in moves):
            moves.append((r + 2, c))
        elif self.color == BLACK and r == 6 and ((r + self.direction, c) in moves):
            moves.append((r - 2, c))
        return moves
    
    # Returns a boolean that dictates whether the move is legal
    def validateMove(self, board, a, b, test=False):
        if not (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"]):
            return False
        
        # If double pawn move, update en passants for horizontally adjacent opposing pawns
        magnitude = b["row"] - a["row"]
        if magnitude in [-2, 2]:
            left = board.get((b["row"], b["col"] - 1))
            right = board.get((b["row"], b["col"] + 1))
            if left is not None and type(left) == Pawn and left.color != self.color:
                left.enPassant["col"] = b["col"]
                left.enPassant["age"] = 0
            if right is not None and type(right) == Pawn and right.color != self.color:
                right.enPassant["col"] = b["col"]
                right.enPassant["age"] = 0
        self.enPassant = {"col" : -1, "age" : 0}
        return True