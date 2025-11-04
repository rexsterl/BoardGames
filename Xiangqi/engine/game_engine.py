"""
Xiangqi Game Engine
Provides a clean API for game management and interaction
"""

import uuid
from .board import Board
from .ai_player import AIPlayer


class GameEngine:
    """Main game engine managing game sessions"""

    def __init__(self):
        """Initialize the game engine"""
        self.games = {}  # Map game_id -> game_state

    def new_game(self, ai_enabled=True, ai_color='black', ai_depth=3):
        """
        Create a new game session

        Args:
            ai_enabled: Whether to enable AI opponent
            ai_color: Color for AI player ('red' or 'black')
            ai_depth: Search depth for AI

        Returns:
            Game ID (string)
        """
        game_id = str(uuid.uuid4())

        game_state = {
            'id': game_id,
            'board': Board(),
            'ai_enabled': ai_enabled,
            'ai': AIPlayer(depth=ai_depth, color=ai_color) if ai_enabled else None,
            'ai_color': ai_color if ai_enabled else None
        }

        self.games[game_id] = game_state
        return game_id

    def get_game(self, game_id):
        """Get game state by ID"""
        return self.games.get(game_id)

    def get_board(self, game_id):
        """Get the board for a game"""
        game = self.get_game(game_id)
        return game['board'] if game else None

    def get_game_state(self, game_id):
        """
        Get the complete game state as a dictionary

        Args:
            game_id: Game ID

        Returns:
            Dictionary with game state information
        """
        game = self.get_game(game_id)
        if not game:
            return None

        board = game['board']
        return {
            'game_id': game_id,
            'board_state': board.to_dict(),
            'ai_enabled': game['ai_enabled'],
            'ai_color': game['ai_color']
        }

    def make_move(self, game_id, from_pos, to_pos):
        """
        Make a move in the game

        Args:
            game_id: Game ID
            from_pos: Tuple (row, col) of piece to move
            to_pos: Tuple (row, col) of destination

        Returns:
            Dictionary with move result and updated state
        """
        game = self.get_game(game_id)
        if not game:
            return {'success': False, 'error': 'Game not found'}

        board = game['board']

        # Validate move
        piece = board.get_piece(from_pos[0], from_pos[1])
        if not piece:
            return {'success': False, 'error': 'No piece at source position'}

        if piece.color != board.current_player:
            return {'success': False, 'error': 'Not your turn'}

        valid_moves = board.get_valid_moves(from_pos[0], from_pos[1])
        if to_pos not in valid_moves:
            return {'success': False, 'error': 'Invalid move'}

        # Make the move
        board.move_piece(from_pos, to_pos)

        return {
            'success': True,
            'state': self.get_game_state(game_id)
        }

    def get_valid_moves(self, game_id, row, col):
        """
        Get valid moves for a piece

        Args:
            game_id: Game ID
            row: Row of piece
            col: Column of piece

        Returns:
            List of valid move positions
        """
        game = self.get_game(game_id)
        if not game:
            return []

        board = game['board']
        return board.get_valid_moves(row, col)

    def get_ai_move(self, game_id):
        """
        Get the AI's move for the current position

        Args:
            game_id: Game ID

        Returns:
            Tuple (from_pos, to_pos) or None if no move available
        """
        game = self.get_game(game_id)
        if not game or not game['ai_enabled']:
            return None

        board = game['board']
        ai = game['ai']

        # Only get AI move if it's AI's turn
        if board.current_player != game['ai_color']:
            return None

        return ai.get_best_move(board)

    def make_ai_move(self, game_id):
        """
        Make the AI's move

        Args:
            game_id: Game ID

        Returns:
            Dictionary with move result and updated state
        """
        game = self.get_game(game_id)
        if not game or not game['ai_enabled']:
            return {'success': False, 'error': 'AI not enabled'}

        board = game['board']

        # Check if it's AI's turn
        if board.current_player != game['ai_color']:
            return {'success': False, 'error': 'Not AI turn'}

        # Get AI move
        ai_move = self.get_ai_move(game_id)
        if not ai_move:
            return {'success': False, 'error': 'No valid AI move available'}

        # Make the move
        from_pos, to_pos = ai_move
        board.move_piece(from_pos, to_pos)

        return {
            'success': True,
            'move': {'from': from_pos, 'to': to_pos},
            'state': self.get_game_state(game_id)
        }

    def is_game_over(self, game_id):
        """Check if game is over"""
        game = self.get_game(game_id)
        if not game:
            return True

        return game['board'].is_game_over()

    def get_game_status(self, game_id):
        """Get game status message"""
        game = self.get_game(game_id)
        if not game:
            return "Game not found"

        return game['board'].get_game_status()

    def delete_game(self, game_id):
        """Delete a game session"""
        if game_id in self.games:
            del self.games[game_id]
            return True
        return False
