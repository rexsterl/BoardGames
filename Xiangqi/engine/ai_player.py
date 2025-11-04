"""
Xiangqi AI Engine
Implements minimax algorithm with alpha-beta pruning for computer opponent
"""


class AIPlayer:
    """AI opponent using minimax with alpha-beta pruning"""

    def __init__(self, depth=3, color='black'):
        """
        Initialize the AI

        Args:
            depth: Search depth for minimax algorithm
            color: Color AI plays as ('red' or 'black')
        """
        self.depth = depth
        self.color = color

        # Piece values for evaluation
        self.piece_values = {
            'general': 10000,
            'advisor': 20,
            'elephant': 20,
            'horse': 40,
            'chariot': 90,
            'cannon': 45,
            'soldier': 10
        }

    def get_best_move(self, board):
        """
        Get the best move for the AI using minimax with alpha-beta pruning

        Args:
            board: Current board state

        Returns:
            Tuple of (from_pos, to_pos) or None if no moves available
        """
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Get all possible moves
        moves = self._get_all_moves(board, self.color)

        if not moves:
            return None

        # Evaluate each move
        for move in moves:
            from_pos, to_pos = move

            # Make the move
            board_copy = board.copy()
            board_copy.move_piece(from_pos, to_pos)

            # Evaluate the position
            value = self._minimax(board_copy, self.depth - 1, alpha, beta, False)

            # Update best move
            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, value)

        return best_move

    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        """
        Minimax algorithm with alpha-beta pruning

        Args:
            board: Current board state
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: True if maximizing player, False if minimizing

        Returns:
            Evaluation score
        """
        # Base case: depth is 0 or game is over
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board)

        if is_maximizing:
            max_eval = float('-inf')
            moves = self._get_all_moves(board, self.color)

            # If no legal moves, evaluate the position (checkmate or stalemate)
            if not moves:
                return self._evaluate_board(board)

            for move in moves:
                from_pos, to_pos = move
                board_copy = board.copy()
                board_copy.move_piece(from_pos, to_pos)

                eval_score = self._minimax(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                if beta <= alpha:
                    break  # Beta cutoff

            return max_eval
        else:
            min_eval = float('inf')
            opponent_color = 'red' if self.color == 'black' else 'black'
            moves = self._get_all_moves(board, opponent_color)

            # If no legal moves, evaluate the position (checkmate or stalemate)
            if not moves:
                return self._evaluate_board(board)

            for move in moves:
                from_pos, to_pos = move
                board_copy = board.copy()
                board_copy.move_piece(from_pos, to_pos)

                eval_score = self._minimax(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                if beta <= alpha:
                    break  # Alpha cutoff

            return min_eval

    def _get_all_moves(self, board, color):
        """
        Get all possible moves for a given color

        Args:
            board: Current board state
            color: Color of pieces to get moves for

        Returns:
            List of tuples (from_pos, to_pos)
        """
        moves = []
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    valid_moves = board.get_valid_moves(row, col)
                    for to_pos in valid_moves:
                        moves.append(((row, col), to_pos))

        return moves

    def _evaluate_board(self, board):
        """
        Evaluate the board state

        Args:
            board: Current board state

        Returns:
            Evaluation score (positive is good for AI, negative is good for opponent)
        """
        score = 0

        # Material evaluation
        for row in range(10):
            for col in range(9):
                piece = board.get_piece(row, col)
                if piece:
                    piece_value = self.piece_values.get(piece.piece_type, 0)

                    # Add positional bonus
                    position_bonus = self._get_position_value(piece, row, col)

                    if piece.color == self.color:
                        score += piece_value + position_bonus
                    else:
                        score -= piece_value + position_bonus

        # Check/checkmate/stalemate bonus
        if board.is_checkmate():
            if board.current_player != self.color:
                score += 100000  # AI wins
            else:
                score -= 100000  # AI loses
        elif board.is_stalemate():
            # Stalemate is a draw - return neutral score
            score = 0
        elif board._is_in_check(board.current_player):
            if board.current_player != self.color:
                score += 50  # Opponent in check
            else:
                score -= 50  # AI in check

        return score

    def _get_position_value(self, piece, row, col):
        """
        Get positional value for a piece

        Args:
            piece: The piece
            row: Row position
            col: Column position

        Returns:
            Positional bonus value
        """
        # Simple positional bonuses
        bonus = 0

        if piece.piece_type == 'soldier':
            # Encourage soldiers to advance
            if piece.color == 'black':
                bonus = row * 2  # More bonus for advanced soldiers
            else:
                bonus = (9 - row) * 2

        elif piece.piece_type == 'chariot' or piece.piece_type == 'cannon':
            # Encourage mobility (central positions)
            center_distance = abs(col - 4)
            bonus = (4 - center_distance)

        elif piece.piece_type == 'horse':
            # Horses are better in the center
            center_distance_row = abs(row - 4.5)
            center_distance_col = abs(col - 4)
            bonus = 5 - (center_distance_row + center_distance_col) / 2

        return bonus
