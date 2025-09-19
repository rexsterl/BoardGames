import random
import time

class Checkers:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'human'  # human or ai
        self.human_pieces = 12
        self.ai_pieces = 12
        self.game_count = 0
        self.human_wins = 0
        self.ai_wins = 0
        
    def initialize_board(self):
        """Initialize the checkers board with pieces in starting positions"""
        board = [[' ' for _ in range(8)] for _ in range(8)]
        
        # Place human pieces (X) at the top
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'X'
        
        # Place AI pieces (O) at the bottom
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'O'
        
        return board
    
    def display_board(self):
        """Display the current game board with coordinates"""
        print("\n" + "="*50)
        print("    A   B   C   D   E   F   G   H")
        print("  +---+---+---+---+---+---+---+---+")
        
        for row in range(8):
            print(f"{8-row} |", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece == ' ':
                    print("   |", end="")
                else:
                    print(f" {piece} |", end="")
            print(f" {8-row}")
            print("  +---+---+---+---+---+---+---+---+")
        
        print("    A   B   C   D   E   F   G   H")
        print("="*50)
        print(f"Human pieces (X): {self.human_pieces}")
        print(f"AI pieces (O): {self.ai_pieces}")
        print("="*50)
    
    def get_coordinates(self, position):
        """Convert position like 'A1' to board coordinates (row, col)"""
        if len(position) != 2:
            return None, None
        
        col_char = position[0].upper()
        row_char = position[1]
        
        if col_char not in 'ABCDEFGH' or row_char not in '12345678':
            return None, None
        
        col = ord(col_char) - ord('A')
        row = 8 - int(row_char)
        
        return row, col
    
    def get_position_string(self, row, col):
        """Convert board coordinates to position string like 'A1'"""
        col_char = chr(ord('A') + col)
        row_char = str(8 - row)
        return col_char + row_char
    
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece(self, row, col):
        """Get piece at position, return ' ' if out of bounds"""
        if not self.is_valid_position(row, col):
            return ' '
        return self.board[row][col]
    
    def is_human_piece(self, piece):
        """Check if piece belongs to human player"""
        return piece in ['X', 'K']  # X = regular, K = king
    
    def is_ai_piece(self, piece):
        """Check if piece belongs to AI player"""
        return piece in ['O', 'Q']  # O = regular, Q = king
    
    def is_king(self, piece):
        """Check if piece is a king"""
        return piece in ['K', 'Q']
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at given position"""
        piece = self.get_piece(row, col)
        if piece == ' ':
            return []
        
        moves = []
        is_human = self.is_human_piece(piece)
        is_king_piece = self.is_king(piece)
        
        # Define movement directions
        if is_human and not is_king_piece:
            # Human regular pieces move down
            directions = [(1, 1), (1, -1)]
        elif not is_human and not is_king_piece:
            # AI regular pieces move up
            directions = [(-1, 1), (-1, -1)]
        else:
            # Kings can move in all directions
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        # Check for captures first (forced moves)
        captures = []
        for dr, dc in directions:
            capture_row = row + 2 * dr
            capture_col = col + 2 * dc
            jump_row = row + dr
            jump_col = col + dc
            
            if (self.is_valid_position(capture_row, capture_col) and
                self.get_piece(capture_row, capture_col) == ' ' and
                self.is_valid_position(jump_row, jump_col)):
                
                jump_piece = self.get_piece(jump_row, jump_col)
                if ((is_human and self.is_ai_piece(jump_piece)) or
                    (not is_human and self.is_human_piece(jump_piece))):
                    captures.append((capture_row, capture_col, jump_row, jump_col))
        
        if captures:
            return captures
        
        # If no captures, check regular moves
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            if (self.is_valid_position(new_row, new_col) and
                self.get_piece(new_row, new_col) == ' '):
                moves.append((new_row, new_col))
        
        return moves
    
    def get_all_valid_moves(self, player):
        """Get all valid moves for a player"""
        all_moves = []
        captures = []
        
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if ((player == 'human' and self.is_human_piece(piece)) or
                    (player == 'ai' and self.is_ai_piece(piece))):
                    
                    moves = self.get_valid_moves(row, col)
                    for move in moves:
                        if len(move) == 4:  # Capture move
                            captures.append((row, col, move[0], move[1], move[2], move[3]))
                        else:  # Regular move
                            all_moves.append((row, col, move[0], move[1]))
        
        # Return captures if any exist, otherwise return regular moves
        return captures if captures else all_moves
    
    def make_move(self, from_row, from_col, to_row, to_col, capture_row=None, capture_col=None):
        """Make a move on the board"""
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '
        self.board[to_row][to_col] = piece
        
        # Handle capture
        if capture_row is not None and capture_col is not None:
            captured_piece = self.board[capture_row][capture_col]
            self.board[capture_row][capture_col] = ' '
            
            if self.is_human_piece(captured_piece):
                self.human_pieces -= 1
            else:
                self.ai_pieces -= 1
        
        # Handle king promotion
        if self.is_human_piece(piece) and to_row == 7:
            self.board[to_row][to_col] = 'K'  # Human king
        elif self.is_ai_piece(piece) and to_row == 0:
            self.board[to_row][to_col] = 'Q'  # AI king
    
    def get_human_move(self):
        """Get and validate human player's move"""
        while True:
            try:
                move_input = input("\nYour turn! Enter move (e.g., 'A3 to B4' or 'A3-B4'): ").strip()
                
                # Parse different input formats
                if ' to ' in move_input:
                    from_pos, to_pos = move_input.split(' to ')
                elif '-' in move_input:
                    from_pos, to_pos = move_input.split('-')
                else:
                    print("Invalid format! Use 'A3 to B4' or 'A3-B4'")
                    continue
                
                from_row, from_col = self.get_coordinates(from_pos.strip())
                to_row, to_col = self.get_coordinates(to_pos.strip())
                
                if from_row is None or to_row is None:
                    print("Invalid coordinates! Use format like 'A3'")
                    continue
                
                # Validate the move
                piece = self.get_piece(from_row, from_col)
                if not self.is_human_piece(piece):
                    print("That's not your piece!")
                    continue
                
                valid_moves = self.get_valid_moves(from_row, from_col)
                move_found = False
                capture_move = None
                
                for move in valid_moves:
                    if len(move) == 4:  # Capture move
                        if move[0] == to_row and move[1] == to_col:
                            move_found = True
                            capture_move = (move[2], move[3])
                            break
                    else:  # Regular move
                        if move[0] == to_row and move[1] == to_col:
                            move_found = True
                            break
                
                if not move_found:
                    print("Invalid move! Try again.")
                    continue
                
                return from_row, from_col, to_row, to_col, capture_move
                
            except (ValueError, IndexError):
                print("Invalid input! Use format like 'A3 to B4'")
    
    def get_ai_move(self):
        """AI makes a move using simple strategy"""
        print("\n🤖 AI is thinking...")
        time.sleep(1)  # Add some drama
        
        valid_moves = self.get_all_valid_moves('ai')
        
        if not valid_moves:
            return None
        
        # Simple AI strategy: prefer captures, then random move
        captures = [move for move in valid_moves if len(move) == 6]
        if captures:
            move = random.choice(captures)
            return move[0], move[1], move[2], move[3], (move[4], move[5])
        else:
            move = random.choice(valid_moves)
            return move[0], move[1], move[2], move[3], None
    
    def check_winner(self):
        """Check if there's a winner"""
        if self.human_pieces == 0:
            return 'ai'
        elif self.ai_pieces == 0:
            return 'human'
        
        # Check if current player has any valid moves
        current_moves = self.get_all_valid_moves(self.current_player)
        if not current_moves:
            return 'ai' if self.current_player == 'human' else 'human'
        
        return None
    
    def get_win_message(self, winner):
        """Get win/loss message"""
        if winner == 'human':
            win_messages = [
                "🎉 Congratulations! You've outsmarted the AI! Time to update your resume!",
                "🏆 Victory! You've proven that human strategy beats artificial intelligence!",
                "🎊 Amazing! You won! The AI is now questioning its programming!",
                "🌟 Fantastic! You've successfully captured all the AI pieces!",
                "🎯 Brilliant! You won! The AI is currently rebooting its strategy module!",
                "🚀 Outstanding! You've shown that old-school tactics still work!",
                "💪 Excellent! You won! The AI is now considering a career change!",
                "🎪 Spectacular! You've demonstrated superior checkers mastery!"
            ]
            return random.choice(win_messages)
        else:
            loss_messages = [
                "😊 Don't worry! The AI had a lucky day. You'll get it next time!",
                "🤗 That's okay! Even the best players have off games. You're still awesome!",
                "💙 No worries! The AI cheated by calculating millions of moves per second!",
                "😌 It happens to the best of us! The AI probably studied checkers theory!",
                "🤝 Don't feel bad! The AI has been practicing 24/7 while you have a life!",
                "💪 That's alright! The AI is just a soulless machine. You have creativity!",
                "😊 No problem! The AI probably used quantum computing. That's basically cheating!",
                "🌟 You're still a winner in my book! The AI just got lucky with its algorithms!"
            ]
            return random.choice(loss_messages)
    
    def play_game(self):
        """Main game loop"""
        print("🎮 Welcome to Checkers!")
        print("=" * 50)
        print("You are X (regular) and K (king)")
        print("AI is O (regular) and Q (king)")
        print("Enter moves like 'A3 to B4' or 'A3-B4'")
        print("=" * 50)
        
        while True:
            # Reset board for new game
            self.board = self.initialize_board()
            self.human_pieces = 12
            self.ai_pieces = 12
            self.current_player = 'human'
            self.game_count += 1
            
            print(f"\n🎮 Starting Game #{self.game_count}")
            
            # Game loop
            while True:
                self.display_board()
                
                if self.current_player == 'human':
                    move = self.get_human_move()
                    if move is None:
                        break
                    from_row, from_col, to_row, to_col, capture = move
                else:
                    move = self.get_ai_move()
                    if move is None:
                        break
                    from_row, from_col, to_row, to_col, capture = move
                    print(f"AI moves from {self.get_position_string(from_row, from_col)} to {self.get_position_string(to_row, to_col)}")
                
                self.make_move(from_row, from_col, to_row, to_col, capture[0] if capture else None, capture[1] if capture else None)
                
                # Check for winner
                winner = self.check_winner()
                if winner:
                    self.display_board()
                    
                    if winner == 'human':
                        print(f"\n{self.get_win_message('human')}")
                        self.human_wins += 1
                    else:
                        print(f"\n{self.get_win_message('ai')}")
                        self.ai_wins += 1
                    
                    break
                
                # Switch players
                self.current_player = 'ai' if self.current_player == 'human' else 'human'
            
            # Display game statistics
            print(f"\n📊 Game Statistics:")
            print(f"   Games Played: {self.game_count}")
            print(f"   Your Wins: {self.human_wins}")
            print(f"   AI Wins: {self.ai_wins}")
            print(f"   Ties: {self.game_count - self.human_wins - self.ai_wins}")
            
            # Ask to play again
            while True:
                play_again = input("\n🎮 Play again? (y/n): ").lower().strip()
                if play_again in ['y', 'yes']:
                    break
                elif play_again in ['n', 'no']:
                    print("\n👋 Thanks for playing! See you next time!")
                    return
                else:
                    print("Please enter 'y' or 'n'!")

def main():
    """Main function to start the game"""
    game = Checkers()
    game.play_game()

if __name__ == "__main__":
    main()
