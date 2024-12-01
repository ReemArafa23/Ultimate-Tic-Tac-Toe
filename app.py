from flask import Flask, render_template, jsonify, request # type: ignore
from game_logic import Game # type: ignore

app = Flask(__name__)
game = Game()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the current game state (board, current turn, winner)
@app.route('/game_state')
def get_game_state():
    return jsonify(game.get_game_state())

# Route to make a move
@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    x, y, cell = data['x'], data['y'], data['cell']
    game.make_move(x, y, cell)
    return jsonify(game.get_game_state())

# Route to reset the game
@app.route('/reset_game', methods=['POST'])
def reset_game():
    game.reset()
    return jsonify(game.get_game_state())

if __name__ == '__main__':
    app.run(debug=True)
