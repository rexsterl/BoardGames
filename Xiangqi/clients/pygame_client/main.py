#!/usr/bin/env python3
"""
Xiangqi (Chinese Chess) - Pygame Client
Desktop GUI implementation
"""

import pygame
import sys
from engine.game_engine import GameEngine
from clients.pygame_client.ui_renderer import UI
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class XiangqiGame:
    """Main game class that manages the game loop and state"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Xiangqi - Chinese Chess")
        self.clock = pygame.time.Clock()

        # Initialize game engine
        self.engine = GameEngine()
        self.game_id = self.engine.new_game(ai_enabled=True, ai_color='black', ai_depth=3)
        self.board = self.engine.get_board(self.game_id)

        # Initialize UI
        self.ui = UI(self.screen, self.board)

        self.running = True
        self.selected_piece = None
        self.valid_moves = []
        self.ai_should_move = False
        self.ai_thinking = False
        self.thinking_animation_frame = 0
        self.ai_delay_frames = 0  # Delay before AI starts computing

    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)

    def handle_click(self, pos):
        """Handle mouse clicks on the board"""
        # Don't allow clicks while AI is thinking
        if self.ai_should_move:
            return

        # Convert screen coordinates to board coordinates
        col, row = self.ui.screen_to_board(pos)

        if self.selected_piece:
            # Try to move the selected piece
            if (row, col) in self.valid_moves:
                result = self.engine.make_move(
                    self.game_id,
                    self.selected_piece,
                    (row, col)
                )

                if result['success']:
                    self.selected_piece = None
                    self.valid_moves = []

                    # Schedule AI move (will happen after rendering)
                    if not self.engine.is_game_over(self.game_id):
                        self.ai_should_move = True
            else:
                # Deselect if clicking elsewhere
                self.selected_piece = None
                self.valid_moves = []

        # Select a piece if it belongs to the current player
        if self.board.is_valid_position(row, col):
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.board.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = self.engine.get_valid_moves(self.game_id, row, col)

    def update(self):
        """Update game state"""
        # Update thinking animation frame
        if self.ai_thinking:
            self.thinking_animation_frame += 1

        # Execute AI move if scheduled
        if self.ai_should_move:
            if not self.ai_thinking:
                # Start showing the thinking animation
                self.ai_thinking = True
                self.thinking_animation_frame = 0
                self.ai_delay_frames = 10  # Show animation for 10 frames before computing
            elif self.ai_delay_frames > 0:
                # Count down delay frames
                self.ai_delay_frames -= 1
            else:
                # Delay complete, now compute AI move
                result = self.engine.make_ai_move(self.game_id)
                self.ai_should_move = False
                self.ai_thinking = False

    def render(self):
        """Render the game"""
        self.ui.draw_board()
        self.ui.draw_pieces()

        # Highlight selected piece and valid moves
        if self.selected_piece:
            self.ui.highlight_square(self.selected_piece, (255, 255, 0))
            for move in self.valid_moves:
                self.ui.highlight_square(move, (0, 255, 0))

        # Draw game status
        status = self.engine.get_game_status(self.game_id)
        self.ui.draw_status(status)

        # Draw thinking animation if AI is thinking
        if self.ai_thinking:
            self.ui.draw_thinking_animation(self.thinking_animation_frame)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.render()  # Render first so player move is visible
            self.update()  # Then update (AI moves after rendering)
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    game = XiangqiGame()
    game.run()


if __name__ == "__main__":
    main()
