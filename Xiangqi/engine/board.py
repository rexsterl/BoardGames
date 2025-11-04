"""
Xiangqi Board State Management
Handles the game board, move validation, and game rules
"""

from .pieces import Piece


class Board:
    """Represents the Xiangqi game board"""

    def __init__(self):
        """Initialize the board with pieces in starting positions"""
        self.board = [[None for _ in range(9)] for _ in range(10)]
        self.current_player = 'red'
        self.move_history = []
        self.captured_pieces = []
        self._setup_pieces()

    def _setup_pieces(self):
        """Set up pieces in their starting positions"""
        # Black pieces (top of board)
        # Chariots
        self.board[0][0] = Piece('chariot', 'black', (0, 0))
        self.board[0][8] = Piece('chariot', 'black', (0, 8))
        # Horses
        self.board[0][1] = Piece('horse', 'black', (0, 1))
        self.board[0][7] = Piece('horse', 'black', (0, 7))
        # Elephants
        self.board[0][2] = Piece('elephant', 'black', (0, 2))
        self.board[0][6] = Piece('elephant', 'black', (0, 6))
        # Advisors
        self.board[0][3] = Piece('advisor', 'black', (0, 3))
        self.board[0][5] = Piece('advisor', 'black', (0, 5))
        # General
        self.board[0][4] = Piece('general', 'black', (0, 4))
        # Cannons
        self.board[2][1] = Piece('cannon', 'black', (2, 1))
        self.board[2][7] = Piece('cannon', 'black', (2, 7))
        # Soldiers
        for col in range(0, 9, 2):
            self.board[3][col] = Piece('soldier', 'black', (3, col))

        # Red pieces (bottom of board)
        # Soldiers
        for col in range(0, 9, 2):
            self.board[6][col] = Piece('soldier', 'red', (6, col))
        # Cannons
        self.board[7][1] = Piece('cannon', 'red', (7, 1))
        self.board[7][7] = Piece('cannon', 'red', (7, 7))
        # Chariots
        self.board[9][0] = Piece('chariot', 'red', (9, 0))
        self.board[9][8] = Piece('chariot', 'red', (9, 8))
        # Horses
        self.board[9][1] = Piece('horse', 'red', (9, 1))
        self.board[9][7] = Piece('horse', 'red', (9, 7))
        # Elephants
        self.board[9][2] = Piece('elephant', 'red', (9, 2))
        self.board[9][6] = Piece('elephant', 'red', (9, 6))
        # Advisors
        self.board[9][3] = Piece('advisor', 'red', (9, 3))
        self.board[9][5] = Piece('advisor', 'red', (9, 5))
        # General
        self.board[9][4] = Piece('general', 'red', (9, 4))

    def get_piece(self, row, col):
        """Get the piece at the specified position"""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None

    def is_valid_position(self, row, col):
        """Check if a position is within the board boundaries"""
        return 0 <= row < 10 and 0 <= col < 9

    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at the given position"""
        piece = self.get_piece(row, col)
        if not piece:
            return []

        valid_moves = []
        move_generators = {
            'general': self._get_general_moves,
            'advisor': self._get_advisor_moves,
            'elephant': self._get_elephant_moves,
            'horse': self._get_horse_moves,
            'chariot': self._get_chariot_moves,
            'cannon': self._get_cannon_moves,
            'soldier': self._get_soldier_moves,
        }

        if piece.piece_type in move_generators:
            potential_moves = move_generators[piece.piece_type](row, col)
            # Filter moves that would put own general in check
            for move in potential_moves:
                if self._is_legal_move(row, col, move[0], move[1]):
                    valid_moves.append(move)

        return valid_moves

    def _get_general_moves(self, row, col):
        """Get valid moves for the General"""
        moves = []
        piece = self.board[row][col]

        # General moves one step orthogonally within the palace
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Define palace boundaries
        if piece.color == 'red':
            palace_rows = range(7, 10)
            palace_cols = range(3, 6)
        else:
            palace_rows = range(0, 3)
            palace_cols = range(3, 6)

        for dr, dc in deltas:
            new_row, new_col = row + dr, col + dc
            if new_row in palace_rows and new_col in palace_cols:
                target = self.board[new_row][new_col]
                if not target or target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_advisor_moves(self, row, col):
        """Get valid moves for the Advisor"""
        moves = []
        piece = self.board[row][col]

        # Advisor moves one step diagonally within the palace
        deltas = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Define palace boundaries
        if piece.color == 'red':
            palace_rows = range(7, 10)
            palace_cols = range(3, 6)
        else:
            palace_rows = range(0, 3)
            palace_cols = range(3, 6)

        for dr, dc in deltas:
            new_row, new_col = row + dr, col + dc
            if new_row in palace_rows and new_col in palace_cols:
                target = self.board[new_row][new_col]
                if not target or target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_elephant_moves(self, row, col):
        """Get valid moves for the Elephant"""
        moves = []
        piece = self.board[row][col]

        # Elephant moves two steps diagonally, cannot cross the river
        deltas = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

        # Define river boundary
        if piece.color == 'red':
            valid_rows = range(5, 10)
        else:
            valid_rows = range(0, 5)

        for dr, dc in deltas:
            new_row, new_col = row + dr, col + dc
            # Check blocking piece (elephant eye)
            block_row, block_col = row + dr // 2, col + dc // 2

            if (self.is_valid_position(new_row, new_col) and
                    new_row in valid_rows and
                    not self.board[block_row][block_col]):
                target = self.board[new_row][new_col]
                if not target or target.color != piece.color:
                    moves.append((new_row, new_col))

        return moves

    def _get_horse_moves(self, row, col):
        """Get valid moves for the Horse"""
        moves = []
        piece = self.board[row][col]

        # Horse moves in L-shape (one step orthogonal, one step diagonal)
        # Check for blocking piece (horse leg)
        move_patterns = [
            ((0, 1), [(1, 2), (-1, 2)]),   # Right
            ((0, -1), [(1, -2), (-1, -2)]), # Left
            ((1, 0), [(2, 1), (2, -1)]),    # Down
            ((-1, 0), [(-2, 1), (-2, -1)])  # Up
        ]

        for (block_dr, block_dc), destinations in move_patterns:
            block_row, block_col = row + block_dr, col + block_dc
            # Check if blocking position is valid and not blocked
            if self.is_valid_position(block_row, block_col) and not self.board[block_row][block_col]:
                for dest_dr, dest_dc in destinations:
                    new_row, new_col = row + dest_dr, col + dest_dc
                    if self.is_valid_position(new_row, new_col):
                        target = self.board[new_row][new_col]
                        if not target or target.color != piece.color:
                            moves.append((new_row, new_col))

        return moves

    def _get_chariot_moves(self, row, col):
        """Get valid moves for the Chariot"""
        moves = []
        piece = self.board[row][col]

        # Chariot moves any distance orthogonally
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while self.is_valid_position(new_row, new_col):
                target = self.board[new_row][new_col]
                if not target:
                    moves.append((new_row, new_col))
                else:
                    if target.color != piece.color:
                        moves.append((new_row, new_col))
                    break
                new_row += dr
                new_col += dc

        return moves

    def _get_cannon_moves(self, row, col):
        """Get valid moves for the Cannon"""
        moves = []
        piece = self.board[row][col]

        # Cannon moves like chariot but captures by jumping over one piece
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            jumped = False

            while self.is_valid_position(new_row, new_col):
                target = self.board[new_row][new_col]

                if not jumped:
                    if not target:
                        moves.append((new_row, new_col))
                    else:
                        jumped = True
                else:
                    if target:
                        if target.color != piece.color:
                            moves.append((new_row, new_col))
                        break

                new_row += dr
                new_col += dc

        return moves

    def _get_soldier_moves(self, row, col):
        """Get valid moves for the Soldier"""
        moves = []
        piece = self.board[row][col]

        # Soldier moves forward, and sideways after crossing the river
        if piece.color == 'red':
            forward = -1
            has_crossed_river = row < 5
        else:
            forward = 1
            has_crossed_river = row > 4

        # Forward move
        new_row, new_col = row + forward, col
        if self.is_valid_position(new_row, new_col):
            target = self.board[new_row][new_col]
            if not target or target.color != piece.color:
                moves.append((new_row, new_col))

        # Sideways moves (only after crossing river)
        if has_crossed_river:
            for dc in [-1, 1]:
                new_row, new_col = row, col + dc
                if self.is_valid_position(new_row, new_col):
                    target = self.board[new_row][new_col]
                    if not target or target.color != piece.color:
                        moves.append((new_row, new_col))

        return moves

    def _is_legal_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is legal (doesn't leave general in check and doesn't violate flying general rule)"""
        # Make the move temporarily
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]

        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

        # Check if own general is in check
        is_legal = not self._is_in_check(piece.color)

        # Check for flying general rule (generals facing each other)
        if is_legal:
            is_legal = not self._generals_facing()

        # Undo the move
        self.board[from_row][from_col] = piece
        self.board[to_row][to_col] = captured

        return is_legal

    def _generals_facing(self):
        """Check if the two generals are facing each other on the same column with no pieces between"""
        # Find both generals
        red_general_pos = None
        black_general_pos = None

        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.piece_type == 'general':
                    if piece.color == 'red':
                        red_general_pos = (row, col)
                    else:
                        black_general_pos = (row, col)

        if not red_general_pos or not black_general_pos:
            return False

        red_row, red_col = red_general_pos
        black_row, black_col = black_general_pos

        # Check if they're on the same column
        if red_col != black_col:
            return False

        # Check if there are any pieces between them
        min_row = min(red_row, black_row)
        max_row = max(red_row, black_row)

        for row in range(min_row + 1, max_row):
            if self.board[row][red_col] is not None:
                return False  # There's a piece between them, so they're not facing

        return True  # They're on the same column with no pieces between

    def _is_in_check(self, color):
        """Check if the specified color's general is in check"""
        # Find the general
        general_pos = None
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.piece_type == 'general' and piece.color == color:
                    general_pos = (row, col)
                    break
            if general_pos:
                break

        if not general_pos:
            return False

        # Check if any opponent piece can attack the general
        opponent_color = 'black' if color == 'red' else 'red'
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    moves = self._get_piece_attacks(row, col)
                    if general_pos in moves:
                        return True

        return False

    def _get_piece_attacks(self, row, col):
        """Get all squares a piece can attack (without checking if move is legal)"""
        piece = self.get_piece(row, col)
        if not piece:
            return []

        move_generators = {
            'general': self._get_general_moves,
            'advisor': self._get_advisor_moves,
            'elephant': self._get_elephant_moves,
            'horse': self._get_horse_moves,
            'chariot': self._get_chariot_moves,
            'cannon': self._get_cannon_moves,
            'soldier': self._get_soldier_moves,
        }

        if piece.piece_type in move_generators:
            return move_generators[piece.piece_type](row, col)

        return []

    def move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.board[from_row][from_col]
        if not piece:
            return False

        # Capture piece if present
        captured = self.board[to_row][to_col]
        if captured:
            self.captured_pieces.append(captured)

        # Move the piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.position = (to_row, to_col)

        # Record move
        self.move_history.append((from_pos, to_pos, captured))

        # Switch player
        self.current_player = 'black' if self.current_player == 'red' else 'red'

        return True

    def make_move(self, move):
        """Make a move (from AI)"""
        from_pos, to_pos = move
        return self.move_piece(from_pos, to_pos)

    def is_game_over(self):
        """Check if the game is over"""
        # Check for checkmate or stalemate
        return self.is_checkmate() or self.is_stalemate()

    def is_checkmate(self):
        """Check if current player is in checkmate"""
        if not self._is_in_check(self.current_player):
            return False

        # Check if any move can get out of check
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    moves = self.get_valid_moves(row, col)
                    if moves:
                        return False

        return True

    def is_stalemate(self):
        """Check if current player has no valid moves (stalemate)"""
        if self._is_in_check(self.current_player):
            return False

        # Check if any move is available
        for row in range(10):
            for col in range(9):
                piece = self.board[row][col]
                if piece and piece.color == self.current_player:
                    moves = self.get_valid_moves(row, col)
                    if moves:
                        return False

        return True

    def get_game_status(self):
        """Get the current game status as a string"""
        if self.is_checkmate():
            winner = 'Black' if self.current_player == 'red' else 'Red'
            return f"Checkmate! {winner} wins!"
        elif self.is_stalemate():
            return "Stalemate! Game is a draw."
        elif self._is_in_check(self.current_player):
            return f"{self.current_player.capitalize()} is in check!"
        else:
            return f"{self.current_player.capitalize()}'s turn"

    def to_dict(self):
        """Convert board state to dictionary for serialization"""
        board_data = []
        for row in range(10):
            row_data = []
            for col in range(9):
                piece = self.board[row][col]
                row_data.append(piece.to_dict() if piece else None)
            board_data.append(row_data)

        return {
            'board': board_data,
            'current_player': self.current_player,
            'move_history': self.move_history,
            'captured_pieces': [p.to_dict() for p in self.captured_pieces],
            'is_game_over': self.is_game_over(),
            'is_checkmate': self.is_checkmate(),
            'is_stalemate': self.is_stalemate(),
            'status': self.get_game_status()
        }

    def copy(self):
        """Create a deep copy of the board"""
        import copy
        return copy.deepcopy(self)
