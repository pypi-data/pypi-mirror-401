"""Flask application for LEX game."""

import os
import random
import logging
import uuid
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from lexcel.lex import Board, CYAN, VIOLET, other
from lexcel.game import get_move, learn

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

# In-memory storage for game states
# In production, use Redis or a database
games = {}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_game_state():
    """Get current game state from server-side storage."""
    game_id = session.get('game_id')
    if game_id and game_id in games:
        return games[game_id]
    return None


def save_game_state(state: dict):
    """Save game state to server-side storage."""
    if 'game_id' not in session:
        session['game_id'] = str(uuid.uuid4())
    games[session['game_id']] = state


def get_player_type(state: dict, player: int) -> str:
    """Get player type (human or computer)."""
    if player == CYAN:
        return state.get('player1_type', 'human')
    return state.get('player2_type', 'human')


def get_player_exp(state: dict, player: int) -> str | None:
    """Get player experience file path."""
    if player == CYAN:
        return state.get('player1_exp')
    return state.get('player2_exp')


def apply_learning(state: dict, winner: int):
    """Apply learning to computer players."""
    # Learn for player 1 (CYAN)
    if state.get('player1_type') == 'computer':
        exp_start = state.get('player1_exp')
        exp_save = state.get('player1_exp')  # Save to same file
        if exp_start and exp_save:
            learn(CYAN, winner,
                  state['memory'][CYAN],
                  exp_start, exp_save)

    # Learn for player 2 (VIOLET)
    if state.get('player2_type') == 'computer':
        exp_start = state.get('player2_exp')
        exp_save = state.get('player2_exp')  # Save to same file
        if exp_start and exp_save:
            learn(VIOLET, winner,
                  state['memory'][VIOLET],
                  exp_start, exp_save)


def board_to_dict(board: Board) -> dict:
    """Convert Board to dictionary for JSON serialization."""
    return {
        'code': board.get_code(),
        'cols': board.COLS,
        'nrows': board.NROWS,
        'pawns': {col: board[col] for col in board.COLS},
        'is_symmetrical': board.is_symmetrical()
    }


def initialize_board(board_code: str | None) -> Board:
    """Initialize a board from code or create a new 3x3 board."""
    if board_code:
        return Board(board_code)
    return Board(ncols=3)


def create_initial_state(board: Board,
                        player1_type: str, player2_type: str,
                        player1_exp: str | None, player2_exp: str | None) -> dict:
    """Create the initial game state dictionary.

    First player is always CYAN.
    """
    return {
        'board_code': board.get_code(),
        'current_player': CYAN,
        'turn': 1,
        'winner': None,
        'memory': {CYAN: [], VIOLET: []},
        'player1_type': player1_type,
        'player2_type': player2_type,
        'player1_exp': player1_exp,
        'player2_exp': player2_exp,
        'random_state': random.Random().getstate()
    }


def handle_computer_move(state: dict, board: Board, current_player: int,
                        turn: int, rand: random.Random, exp_file: str) -> tuple[Board, int | None]:
    """Handle a computer player's move."""
    move_memory = state['memory'][current_player]
    new_board, new_winner = get_move(
        board, current_player, turn, rand,
        exp_file, move_memory
    )
    state['memory'][current_player] = move_memory
    return new_board, new_winner


def handle_human_move(board: Board, current_player: int, move: str) -> tuple[Board, int | None]:
    """Handle a human player's move."""
    move = move.upper()
    if move not in board.WELL_FORMED_MOVES:
        raise ValueError('Invalid move format')

    new_board = board.move(current_player, move[0], move[1])
    new_winner = current_player if new_board.is_winner(current_player) else None
    return new_board, new_winner


def update_game_state_after_move(state: dict, new_board: Board,
                                 new_winner: int | None, turn: int,
                                 rand: random.Random) -> list[str]:
    """Update game state after a move and return next legal moves."""
    state['random_state'] = rand.getstate()
    state['board_code'] = new_board.get_code()
    state['turn'] = turn + 1
    state['winner'] = new_winner

    if not new_winner:
        state['current_player'] = other(state['current_player'])
        return new_board.get_legal_moves(other(state['current_player']))

    apply_learning(state, new_winner)
    return []


def save_uploaded_file(file, player: str, state: dict | None) -> tuple[str, str]:
    """Save uploaded experience file and update game state."""
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    if state:
        if player == 'player1':
            state['player1_exp'] = filepath
        else:
            state['player2_exp'] = filepath
        save_game_state(state)

    return filename, filepath


def get_available_experience_files() -> list[str]:
    """Get list of available experience files in upload folder."""
    if not os.path.exists(UPLOAD_FOLDER):
        return []

    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            files.append(filename)

    return sorted(files)


def create_app(test_config=None) -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    if test_config is not None:
        app.config.update(test_config)

    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @app.route('/')
    def index():
        """Render the main game page."""
        return render_template('index.html')

    @app.route('/api/new_game', methods=['POST'])
    def new_game():
        """Start a new game."""
        data = request.get_json()

        board_code = data.get('board_code', None)
        player1_type = data.get('player1_type', 'human')
        player2_type = data.get('player2_type', 'human')
        player1_exp = data.get('player1_exp', None)
        player2_exp = data.get('player2_exp', None)

        board = initialize_board(board_code)
        state = create_initial_state(board, player1_type, player2_type,
                                    player1_exp, player2_exp)
        save_game_state(state)

        return jsonify({
            'success': True,
            'board': board_to_dict(board),
            'current_player': CYAN,
            'turn': 1,
            'legal_moves': board.get_legal_moves(CYAN)
        })

    @app.route('/api/move', methods=['POST'])
    def make_move():
        """Make a move (human or computer)."""
        state = get_game_state()
        if not state:
            return jsonify({'error': 'No game in progress'}), 400

        data = request.get_json()
        move = data.get('move', None)

        board = Board(state['board_code'])
        current_player = state['current_player']
        turn = state['turn']
        winner = state.get('winner')

        if winner:
            return jsonify({'error': 'Game is already finished'}), 400

        player_type = get_player_type(state, current_player)
        rand = random.Random()
        if 'random_state' in state:
            rand.setstate(state['random_state'])

        exp_file = get_player_exp(state, current_player)

        try:
            if player_type == 'computer' and exp_file and move is None:
                new_board, new_winner = handle_computer_move(
                    state, board, current_player, turn, rand, exp_file
                )
            elif move:
                new_board, new_winner = handle_human_move(
                    board, current_player, move
                )
            else:
                return jsonify({'error': 'Move required for human player'}), 400

            next_legal_moves = update_game_state_after_move(
                state, new_board, new_winner, turn, rand
            )
            save_game_state(state)

            return jsonify({
                'success': True,
                'board': board_to_dict(new_board),
                'current_player': state['current_player'],
                'turn': state['turn'],
                'winner': new_winner,
                'legal_moves': next_legal_moves
            })

        except Board.IllegalMoveError as e:
            return jsonify({'error': str(e)}), 400
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error("Error making move: %s", e)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/upload_experience', methods=['POST'])
    def upload_experience():
        """Upload an experience Excel file."""
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        player = request.form.get('player', 'player1')

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            state = get_game_state()
            filename, filepath = save_uploaded_file(file, player, state)

            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })

        return jsonify({'error': 'Invalid file type'}), 400

    @app.route('/api/experience_files', methods=['GET'])
    def list_experience_files():
        """Get list of available experience files."""
        files = get_available_experience_files()
        return jsonify({
            'success': True,
            'files': files
        })

    return app


def main():
    """Run the Flask development server."""
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
