from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

game_state = {
    "board": [None] * 9,
    "turn": "X"
}

def check_winner(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('player_move')
def handle_move(data):
    index = data['index']
    if game_state["board"][index] is None:
        symbol = game_state["turn"]
        game_state["board"][index] = symbol
        winner = check_winner(game_state["board"])
        emit('update_board', {'index': index, 'symbol': symbol, 'winner': winner}, broadcast=True)
        game_state["turn"] = "O" if symbol == "X" else "X"

@socketio.on('reset_game')
def handle_reset():
    game_state["board"] = [None] * 9
    game_state["turn"] = "X"
    emit('reset_board', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, debug=True)