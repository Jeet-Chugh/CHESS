WHITE = "white"
BLACK = "black"

class Square():
    # Checks if square in form row,col is on the board
    @staticmethod
    def isOnBoard(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    # Turns tuple in format (r, c) into dict with format {"row" : row, "col" : col}
    @staticmethod
    def tupleToDict(squareString):
        return {"row" : squareString[0], "col" : squareString[1]}

    # Turns dict in format "{"row" : 3, "col" : 4}" into string in format "e4"
    @staticmethod
    def dictToString(squareDict):
        COL_DICT = {0 : "a", 1 : "b", 2 : "c", 3 : "d", 4 : "e", 5 : "f", 6 : "g", 7 : "h"}
        return COL_DICT[squareDict["col"]] + str(squareDict["row"] + 1)
    
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

class Board():
    @staticmethod
    def executeMove(a, b, board):
        piece = board.get((a["row"], a["col"]))
        # Pawn promotion
        if type(piece) == Pawn and b["row"] in [0, 7]:
            promotionDict = {"r" : Rook, "n" : Knight, "b" : Bishop, "q" : Queen}
            newPiece = promotionDict[input("Promote to: ").lower()]
            board[(b["row"], b["col"])] = newPiece(piece.color, ICON_DICT[piece.color][newPiece])

        # En Passant 
        elif type(piece) == Pawn and b["col"] != a["col"] and board.get((b["row"], b["col"])) is None:
            board[(b["row"], b["col"])] = board[(a["row"], a["col"])]
            del board[(a["row"], b["col"])]

        # Castling
        elif type(piece) == King and (b["row"], b["col"]) not in King.kingList(a["row"], a["col"]):
            if b["col"] == 2:
                board[(b["row"], b["col"])] = board[(a["row"], a["col"])]
                board[(b["row"], 3)] = board[(b["row"], 0)]
                del board[(a["row"], 0)]
            elif b["col"] == 6:
                board[(b["row"], b["col"])] = board[(a["row"], a["col"])]
                board[(b["row"], 5)] = board[(b["row"], 7)]
                del board[(a["row"], 7)]

        # Normal move 
        else:
            board[(b["row"], b["col"])] = board[(a["row"], a["col"])]

        del board[(a["row"], a["col"])]
        return board
    
    @staticmethod
    def updateEnPassant(board):
        for location, piece in board.items():
            if type(piece) == Pawn:
                piece.enPassant["age"] += 1
                if piece.enPassant["age"] > 1:
                    piece.enPassant["age"] = 0
                    piece.enPassant["col"] = -1

    @staticmethod
    def scanForCheck(a, b, board):

        def canSeeKing(kingLocation, pieceList, board):
            for piece,position in pieceList:
                if piece.validateMove(board, Square.tupleToDict(position), Square.tupleToDict(kingLocation)):
                    return True
            return False
        
        # make the move on a copy of the board
        if a != b:
            board = Board.executeMove(a, b, board.copy())

        # find locations for both kings on the board
        kingLocations = {}
        pieceDict = {BLACK : [], WHITE : []}
        for location,piece in board.items():
            if type(piece) == King:
                kingLocations[piece.color] = location
                continue
            pieceDict[piece.color].append((piece, location))

        # Returns a dictionary that determines each colors check status
        return {
            "status" : {WHITE : canSeeKing(kingLocations[WHITE], pieceDict[BLACK], board),
                        BLACK : canSeeKing(kingLocations[BLACK], pieceDict[WHITE], board)},
            "board"  : board
        }

class Piece():
    def __init__(self, color, icon) -> None:
        self.color = color
        self.icon = icon
        self.CARDINALS = [(1,0), (0,1), (-1,0), (0,-1)]
        self.DIAGONALS = [(1,1), (-1,1), (1,-1), (-1,-1)]

    # Returns a boolean that dictates whether the move is legal
    def validateMove(self, board, a, b, test=False):
        if test:
            print(self.availableMoves(board, a["row"], a["col"]))
        return (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"])
    
    def availableMoves(self, board, r, c):
        raise RuntimeError()
    
    # Checks if the prospective move is on the board and either empty or an opposing piece
    def noConflict(self, board, r, c):
        return Square.isOnBoard(r, c) and (((r, c) not in board) or board[(r, c)].color != self.color)
    
    # Returns list of potential moves using iterative approach on either CARDINALS or DIAGONALS
    def findAvailableMoves(self, board, r, c, intervals):
        moves = []
        for row,col in intervals:
            tempRow, tempCol = r + row, c + col
            while Square.isOnBoard(tempRow, tempCol):                
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
        if test:
            print(self.availableMoves(board, a["row"], a["col"]))
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
        castlingMoves = self.castlingMoves(board)
        return [(row, col) for row, col in self.kingList(r, c) if self.noConflict(board, row, col)] + castlingMoves
    
    # Overrides validateMove to reset moved to False if the attempted move is illegal
    def validateMove(self, board, a, b, test=False):
        if test:
            print(self.availableMoves(board, a["row"], a["col"]))
        validity = (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"])
        if not self.moved:
            self.moved = validity
        return validity

    def castlingMoves(self, board):
        if self.moved:
            return []
        
        col = {WHITE : 0, BLACK : 7}[self.color]
        castlingMoves = []
        # queenside castle, rook present, rook hasnt moved, no pieces in between, not in check 
        if type(board.get((col, 0))) == Rook and \
           not board.get((col, 0)).moved and \
           [board.get((col, 1)), board.get((col, 2)), board.get((col, 3))] == [None, None, None] and \
           Board.scanForCheck(None, None, board)["status"][self.color] == False:
            # if moving one to the left doesnt result in check
            if not Board.scanForCheck(Square.tupleToDict((col, 4)), Square.tupleToDict((col, 3)), board)["status"][self.color]:
                prospectiveBoard = Board.executeMove(Square.tupleToDict((col, 4)), Square.tupleToDict((col, 3)), board.copy())
                # if moving two to the left doesnt result in check
                if not Board.scanForCheck(Square.tupleToDict((col, 3)), Square.tupleToDict((col, 2)), prospectiveBoard)["status"][self.color]:
                    castlingMoves.append((col, 2))
        # kingside castle, rook present, rook hasnt moved, no pieces in between and not in check
        if type(board.get((col, 7))) == Rook and \
           not board.get((col, 7)).moved and \
           [board.get((col, 5)), board.get((col, 6))] == [None, None] and \
           Board.scanForCheck(None, None, board)["status"][self.color] == False:
            # if moving one to the right doesnt result in check
            if not Board.scanForCheck(Square.tupleToDict((col, 4)), Square.tupleToDict((col, 5)), board)["status"][self.color]:
                prospectiveBoard = Board.executeMove(Square.tupleToDict((col, 4)), Square.tupleToDict((col, 5)), board.copy())
                # if moving two to the right doesnt result in check
                if not Board.scanForCheck(Square.tupleToDict((col, 5)), Square.tupleToDict((col, 6)), prospectiveBoard)["status"][self.color]:
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
        enPassantRow = {WHITE : 4, BLACK : 3}[self.color]
        startingRow = {WHITE : 1, BLACK : 6}[self.color]
        # En passant
        if self.enPassant["col"] != -1 and r == enPassantRow:
            moves.append((enPassantRow + self.direction, self.enPassant["col"]))
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
        if r == startingRow and ((r + self.direction, c) in moves):
            moves.append((r + (2 * self.direction), c))
        return moves
    
    # Returns a boolean that dictates whether the move is legal
    def validateMove(self, board, a, b, test=False):
        if test:
            print(self.availableMoves(board, a["row"], a["col"]))
        if not (b["row"], b["col"]) in self.availableMoves(board, a["row"], a["col"]):
            return False
        
        # If double pawn move, update en passants for horizontally adjacent opposing pawns
        if b["row"] - a["row"] in [-2, 2]:
            sides = [board.get((b["row"], b["col"] - 1)), board.get((b["row"], b["col"] + 1))]
            for side in sides:
                if side is not None and type(side) == Pawn and side.color != self.color:
                    side.enPassant["col"] = b["col"]
                    side.enPassant["age"] = 0
        return True
    
ICON_DICT = {
                BLACK : {Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕", Pawn : "♙"}, 
                WHITE : {Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛", Pawn : "♟"}
            }