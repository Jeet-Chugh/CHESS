from flask import Flask, render_template, jsonify, request, Response
from chess.game import Game
from chess.pieces import *
from chess.errors import *
import chess.tests as tests
import unittest

# run tests on app startup
testSuite = unittest.TestLoader().loadTestsFromModule(tests)
unittest.TextTestRunner(verbosity=1).run(testSuite)

app = Flask(__name__)
game = None


def get_gameDict(game):
    gameDict = {}
    for location, piece in game.board.items():
        gameDict[Square.tupleToString(location)] = piece.icon
    return gameDict


# default route
@app.route("/")
def index():
    global game
    game = Game(Game.defaultBoard())
    return render_template("index.html")


# on square click
@app.route("/square-clicked", methods=["POST"])
def process_click():
    # get data from POST request
    data = request.get_json()

    returnData = {"circle": [], "highlight": "", "move": False, "check" : ""}
    # return which squares to add a circle to or highlight
    squareLocation = Square.stringtoTuple(data["id"])
    square = game.board.get(squareLocation)

    # if clicked square is highlighted square
    if data["id"] == data["highlightedSquare"]:
        if data["checkHighlightedSquare"] != "":
            returnData["check"] = data["checkHighlightedSquare"]
        return returnData

    if data["highlightedSquare"] != "" or data["checkHighlightedSquare"] != "":
        if data["highlightedSquare"] != "":
            hSquare = data["highlightedSquare"]
        elif data["checkHighlightedSquare"] != "":
            hSquare = data["checkHighlightedSquare"]
        hLocation = Square.stringtoTuple(hSquare)
        # if click is a move
        print(game.board.get(hLocation).availableMoves(
            game.board, hLocation[0], hLocation[1]
        ))
        if squareLocation in game.board.get(hLocation).availableMoves(
            game.board, hLocation[0], hLocation[1]
        ):
            returnData["move"] = True
            game.move(
                Square.stringToDict(hSquare),
                Square.stringToDict(data["id"]),
            )
            if Board.scanForCheck(game.board)[game.turn]:
                for location, piece in game.board.items():
                    if type(piece) == King and piece.color == game.turn:
                        print(Square.tupleToString(location))
                        returnData["check"] = Square.tupleToString(location)
            return returnData

    # if click is on another friendly piece
    if square is not None and square.color == game.turn:
        print("entered")
        circleList = []
        for move in square.availableMoves(
            game.board, squareLocation[0], squareLocation[1]
        ):
            if Board.scanForCheck(
                    Board.executeMove(
                        Square.tupleToDict(squareLocation),
                        Square.tupleToDict(move),
                        game.board.copy(),
                    )
                )[game.turn] == False:
                circleList.append(Square.tupleToString(move))
        returnData["circle"] = circleList
        returnData["highlight"] = Square.tupleToString(squareLocation)
        return returnData

    # if the square is not a move and it is not another friendly piece
    if square is None or square.color != game.turn:
        return returnData

    return returnData


@app.route("/get-board", methods=["GET"])
def get_board():
    return get_gameDict(game)

@app.route("/get-outcome", methods=["GET"])
def get_outcome():
    return jsonify(game.outcome)

@app.route("/new-game", methods=["GET"])
def new_game():
    global game
    game = Game(Game.defaultBoard())
    return get_board()

@app.route("/resign", methods=["POST"])
def resign():
    game.resign()
    return Response(status=204)

@app.route("/offer-draw", methods=["GET"])
def offerDraw():
    game.offerDraw()
    return jsonify({"drawOffered" : game.drawOffered})

@app.route("/reset-draw", methods=["GET"])
def resetDraw():
    game.drawOffered = False
    return ""


@app.route("/flip-board", methods=["GET"])
def flipBoard():
    pass

if __name__ == "__main__":
    app.run(debug=True)
