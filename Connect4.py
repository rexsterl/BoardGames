import random
import time


class Connect4:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
        self.human_symbol = "X"
        self.ai_symbol = "O"
        self.current_player = "human"  # human or ai
        self.game_count = 0
        self.human_wins = 0
        self.ai_wins = 0

    def display_board(self):
        print("\n" + "=" * 50)
        print("   " + "   ".join(str(c + 1) for c in range(self.cols)))
        print("  +" + "+".join(["---"] * self.cols) + "+")
        for r in range(self.rows):
            print("  |" + "|".join(f" {self.board[r][c]} " for c in range(self.cols)) + "|")
            print("  +" + "+".join(["---"] * self.cols) + "+")
        print("=" * 50)

    def get_valid_columns(self):
        return [c for c in range(self.cols) if self.board[0][c] == " "]

    def drop_piece(self, column, symbol):
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][column] == " ":
                self.board[r][column] = symbol
                return r, column
        return None

    def undo_piece(self, column):
        for r in range(self.rows):
            if self.board[r][column] != " ":
                self.board[r][column] = " "
                return

    def check_winner_symbol(self, symbol):
        # Horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if all(self.board[r][c + i] == symbol for i in range(4)):
                    return True
        # Vertical
        for c in range(self.cols):
            for r in range(self.rows - 3):
                if all(self.board[r + i][c] == symbol for i in range(4)):
                    return True
        # Diagonal down-right
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if all(self.board[r + i][c + i] == symbol for i in range(4)):
                    return True
        # Diagonal up-right
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if all(self.board[r - i][c + i] == symbol for i in range(4)):
                    return True
        return False

    def board_full(self):
        return all(self.board[0][c] != " " for c in range(self.cols))

    def evaluate_position(self):
        # Simple heuristic: center preference + count potential lines
        score = 0
        center_col = self.cols // 2
        center_count = sum(1 for r in range(self.rows) if self.board[r][center_col] == self.ai_symbol)
        score += center_count * 3

        def score_window(window):
            s = 0
            ai = window.count(self.ai_symbol)
            hu = window.count(self.human_symbol)
            empty = window.count(" ")
            if ai == 4:
                s += 100000
            elif ai == 3 and empty == 1:
                s += 50
            elif ai == 2 and empty == 2:
                s += 10
            if hu == 3 and empty == 1:
                s -= 60
            elif hu == 2 and empty == 2:
                s -= 12
            return s

        # Horizontal windows
        for r in range(self.rows):
            for c in range(self.cols - 3):
                window = [self.board[r][c + i] for i in range(4)]
                score += score_window(window)
        # Vertical windows
        for c in range(self.cols):
            for r in range(self.rows - 3):
                window = [self.board[r + i][c] for i in range(4)]
                score += score_window(window)
        # Diagonal down-right
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += score_window(window)
        # Diagonal up-right
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                window = [self.board[r - i][c + i] for i in range(4)]
                score += score_window(window)

        return score

    def get_human_move(self):
        while True:
            try:
                move = input("\nYour turn! Choose column (1-7): ").strip()
                if not move.isdigit():
                    print("Please enter a number!")
                    continue
                col = int(move) - 1
                if col < 0 or col >= self.cols:
                    print("Please enter a number between 1 and 7!")
                    continue
                if self.board[0][col] != " ":
                    print("That column is full! Try another.")
                    continue
                return col
            except ValueError:
                print("Please enter a valid number!")

    def get_ai_move(self, max_depth=4):
        print("\n🤖 AI is thinking...")
        time.sleep(1)

        valid_cols = self.get_valid_columns()
        if not valid_cols:
            return None

        best_score = float("-inf")
        best_col = random.choice(valid_cols)

        alpha = float("-inf")
        beta = float("inf")

        for col in valid_cols:
            self.drop_piece(col, self.ai_symbol)
            score = self.minimax(depth=1, maximizing=False, alpha=alpha, beta=beta, max_depth=max_depth)
            self.undo_piece(col)
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)
        return best_col

    def minimax(self, depth, maximizing, alpha, beta, max_depth):
        if self.check_winner_symbol(self.ai_symbol):
            return 1_000_000 - depth
        if self.check_winner_symbol(self.human_symbol):
            return -1_000_000 + depth
        if self.board_full() or depth == max_depth:
            return self.evaluate_position()

        valid_cols = self.get_valid_columns()
        if not valid_cols:
            return 0

        if maximizing:
            value = float("-inf")
            for col in valid_cols:
                self.drop_piece(col, self.ai_symbol)
                value = max(value, self.minimax(depth + 1, False, alpha, beta, max_depth))
                self.undo_piece(col)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float("inf")
            for col in valid_cols:
                self.drop_piece(col, self.human_symbol)
                value = min(value, self.minimax(depth + 1, True, alpha, beta, max_depth))
                self.undo_piece(col)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def announce_result(self, winner_symbol):
        if winner_symbol == self.human_symbol:
            messages = [
                "🎉 Nice! You connected four and beat the bot!",
                "🏆 Victory! The AI is rethinking its life choices.",
                "🎊 You win! Gravity and strategy on your side!",
            ]
            print(random.choice(messages))
        elif winner_symbol == self.ai_symbol:
            messages = [
                "🤖 The AI connects four! Better luck next time.",
                "🧠 Bot wins. Time to sharpen those tactics!",
                "📈 The algorithm found a line. You got this next time!",
            ]
            print(random.choice(messages))
        else:
            print("🤝 It's a tie! No more space left.")

    def play_game(self):
        print("🎮 Welcome to Connect 4!")
        print("=" * 50)
        print("You are X. AI is O.")
        print("Drop by choosing a column 1-7.")
        print("=" * 50)

        while True:
            # Reset for new game
            self.board = [[" " for _ in range(self.cols)] for _ in range(self.rows)]
            self.current_player = "human"
            self.game_count += 1

            print(f"\n🎮 Starting Game #{self.game_count}")

            while True:
                self.display_board()
                if self.current_player == "human":
                    col = self.get_human_move()
                    self.drop_piece(col, self.human_symbol)
                else:
                    col = self.get_ai_move()
                    if col is None:
                        break
                    self.drop_piece(col, self.ai_symbol)
                    print(f"AI drops in column {col + 1}")

                # Check for end conditions
                if self.check_winner_symbol(self.human_symbol):
                    self.display_board()
                    self.announce_result(self.human_symbol)
                    self.human_wins += 1
                    break
                if self.check_winner_symbol(self.ai_symbol):
                    self.display_board()
                    self.announce_result(self.ai_symbol)
                    self.ai_wins += 1
                    break
                if self.board_full():
                    self.display_board()
                    self.announce_result(None)
                    break

                self.current_player = "ai" if self.current_player == "human" else "human"

            # Stats
            print(f"\n📊 Game Statistics:")
            print(f"   Games Played: {self.game_count}")
            print(f"   Your Wins: {self.human_wins}")
            print(f"   AI Wins: {self.ai_wins}")
            print(f"   Ties: {self.game_count - self.human_wins - self.ai_wins}")

            # Replay prompt
            while True:
                play_again = input("\n🎮 Play again? (y/n): ").lower().strip()
                if play_again in ["y", "yes"]:
                    break
                elif play_again in ["n", "no"]:
                    print("\n👋 Thanks for playing! See you next time!")
                    return
                else:
                    print("Please enter 'y' or 'n'!")


def main():
    game = Connect4()
    game.play_game()


if __name__ == "__main__":
    main()


