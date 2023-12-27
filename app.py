from flask import Flask, render_template, jsonify, request
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

# default route
@app.route("/")
def index():

    global game 
    game = Game(Game.defaultBoard())
    gameDict = {}
    for location, piece in game.board.items():
        gameDict[Square.dictToString(Square.tupleToDict(location))] = piece.icon
    jsonBoard = gameDict

    return render_template("index.html", board=jsonBoard)

# on square click
@app.route('/square-clicked', methods=['POST'])
def process_click():
    data = request.get_json()
    squareLocation = Square.stringtoTuple(data["id"])
    square = game.board.get(squareLocation)
    if square is None:
        return []
    else:
        return [Square.dictToString(Square.tupleToDict(x)) for x in square.availableMoves(game.board, squareLocation[0], squareLocation[1])]

if __name__ == "__main__":
    app.run(debug=True)