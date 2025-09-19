import random
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human_symbol = None
        self.ai_symbol = None
        self.current_player = None
        self.game_count = 0
        self.human_wins = 0
        self.ai_wins = 0
        self.last_winner = None
        
    def display_board(self):
        """Display the current game board"""
        print("\n" + "="*25)
        print("   1 | 2 | 3 ")
        print("  -----------")
        print(f"   4 | 5 | 6 ")
        print("  -----------")
        print("   7 | 8 | 9 ")
        print("="*25)
        print("\nCurrent Board:")
        print(f"   {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("  -----------")
        print(f"   {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("  -----------")
        print(f"   {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("="*25)
    
    def choose_symbol(self):
        """Let human player choose X or O"""
        while True:
            choice = input("\nChoose your symbol (X or O): ").upper().strip()
            if choice in ['X', 'O']:
                self.human_symbol = choice
                self.ai_symbol = 'O' if choice == 'X' else 'X'
                print(f"\nYou chose {self.human_symbol}! AI will be {self.ai_symbol}")
                return
            else:
                print("Please enter X or O only!")
    
    def determine_first_player(self):
        """Determine who goes first based on game rules"""
        if self.game_count == 0:
            # First game: human always goes first
            self.current_player = 'human'
            print(f"\n🎮 First game! You go first with {self.human_symbol}")
        else:
            # Subsequent games: loser goes first
            if self.last_winner == 'human':
                self.current_player = 'ai'
                print(f"\n🤖 You won last game! AI goes first with {self.ai_symbol}")
            else:
                self.current_player = 'human'
                print(f"\n🎮 You lost last game! You go first with {self.human_symbol}")
    
    def get_human_move(self):
        """Get and validate human player's move"""
        while True:
            try:
                move = input(f"\nYour turn! Enter position (1-9): ").strip()
                if not move.isdigit():
                    print("Please enter a number!")
                    continue
                    
                move = int(move) - 1  # Convert to 0-based index
                
                if move < 0 or move > 8:
                    print("Please enter a number between 1 and 9!")
                    continue
                    
                if self.board[move] != ' ':
                    print("That position is already taken! Try again.")
                    continue
                    
                return move
            except ValueError:
                print("Please enter a valid number!")
    
    def get_ai_move(self):
        """AI makes move using minimax algorithm"""
        print(f"\n🤖 AI is thinking...")
        time.sleep(1)  # Add some drama
        
        # Use minimax to find best move
        best_score = float('-inf')
        best_move = 0
        
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = self.ai_symbol
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '  # Undo move
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax algorithm for AI decision making"""
        result = self.check_winner()
        
        if result == self.ai_symbol:
            return 10 - depth
        elif result == self.human_symbol:
            return -10 + depth
        elif result == 'tie':
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.ai_symbol
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = self.human_symbol
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score
    
    def make_move(self, position, symbol):
        """Make a move on the board"""
        self.board[position] = symbol
    
    def check_winner(self):
        """Check if there's a winner or tie"""
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                return self.board[i]
        
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                return self.board[i]
        
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return self.board[2]
        
        # Check for tie
        if ' ' not in self.board:
            return 'tie'
        
        return None
    
    def get_win_message(self, winner):
        """Get humorous win message or supportive loss message"""
        if winner == 'human':
            win_messages = [
                "🎉 Congratulations! You've achieved the impossible! Even a goldfish could do better than the AI!",
                "🏆 Victory! You've proven that humans still have some advantages over machines... barely!",
                "🎊 Amazing! You won! The AI is now questioning its life choices!",
                "🌟 Fantastic! You've successfully outsmarted a computer! Time to update your resume!",
                "🎯 Brilliant! You won! The AI is currently downloading more RAM to process this defeat!",
                "🚀 Outstanding! You've proven that sometimes the old ways are the best ways!",
                "💪 Excellent! You won! The AI is now considering a career change to professional losing!",
                "🎪 Spectacular! You've shown that human intuition beats artificial intelligence... this time!"
            ]
            return random.choice(win_messages)
        else:
            loss_messages = [
                "😊 Don't worry! The AI had a lucky day. You'll get it next time!",
                "🤗 That's okay! Even the best players have off games. You're still awesome!",
                "💙 No worries! The AI cheated by thinking faster than you. That's not fair!",
                "😌 It happens to the best of us! The AI probably studied your moves in advance!",
                "🤝 Don't feel bad! The AI has been practicing 24/7 while you have a life!",
                "💪 That's alright! The AI is just a soulless machine. You have heart and soul!",
                "😊 No problem! The AI probably used quantum computing. That's basically cheating!",
                "🌟 You're still a winner in my book! The AI just got lucky with its random number generator!"
            ]
            return random.choice(loss_messages)
    
    def play_game(self):
        """Main game loop"""
        print("🎮 Welcome to Tic-Tac-Toe!")
        print("=" * 50)
        
        while True:
            # Reset board for new game
            self.board = [' ' for _ in range(9)]
            self.game_count += 1
            
            # Choose symbols (only on first game)
            if self.game_count == 1:
                self.choose_symbol()
            
            # Determine who goes first
            self.determine_first_player()
            
            # Game loop
            while True:
                self.display_board()
                
                if self.current_player == 'human':
                    move = self.get_human_move()
                    self.make_move(move, self.human_symbol)
                else:
                    move = self.get_ai_move()
                    self.make_move(move, self.ai_symbol)
                    print(f"AI chose position {move + 1}")
                
                # Check for winner
                winner = self.check_winner()
                if winner:
                    self.display_board()
                    
                    if winner == 'tie':
                        print("\n🤝 It's a tie! You're both equally matched!")
                        self.last_winner = None
                    elif winner == self.human_symbol:
                        print(f"\n{self.get_win_message('human')}")
                        self.human_wins += 1
                        self.last_winner = 'human'
                    else:
                        print(f"\n{self.get_win_message('ai')}")
                        self.ai_wins += 1
                        self.last_winner = 'ai'
                    
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
    game = TicTacToe()
    game.play_game()

if __name__ == "__main__":
    main()