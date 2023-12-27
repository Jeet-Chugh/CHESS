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
        gameDict[Square.tupleToString(location)] = piece.icon
    jsonBoard = gameDict

    return render_template("index.html", board=jsonBoard)

# on square click
@app.route('/square-clicked', methods=['POST'])
def process_click():
    # get data from POST request
    data = request.get_json()

    returnData = {'circle' : [], 'highlight' : '', 'move' : False}
    # return which squares to add a circle to or highlight
    squareLocation = Square.stringtoTuple(data["id"])
    square = game.board.get(squareLocation)

    # if clicked square is highlighted square
    if data['id'] == data['highlightedSquare']:
        return returnData

    # if click is a move
    if data['highlightedSquare'] != "":
        hLocation = Square.stringtoTuple(data['highlightedSquare'])
        if squareLocation in game.board.get(hLocation).availableMoves(game.board, hLocation[0], hLocation[1]):
            returnData['move'] = True
            game.move()
        return returnData

    # if the square is not a move and it is not another friendly piece
    if square is None or square.color != game.turn:
        return returnData
    
    returnData['circle'] = [Square.tupleToString(x) for x in square.availableMoves(game.board, squareLocation[0], squareLocation[1])]
    returnData['highlight'] = Square.tupleToString(squareLocation)
    return returnData

if __name__ == "__main__":
    app.run(debug=True)