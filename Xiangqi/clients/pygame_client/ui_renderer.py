"""
Xiangqi UI and Rendering
Handles drawing the board, pieces, and user interface elements
"""

import pygame
import os
from common.constants import (
    BOARD_OFFSET_X, BOARD_OFFSET_Y, SQUARE_SIZE,
    BOARD_COLOR, LINE_COLOR, PALACE_COLOR, RIVER_COLOR,
    RED_PIECE_COLOR, BLACK_PIECE_COLOR, HIGHLIGHT_COLOR,
    SCREEN_WIDTH, SCREEN_HEIGHT
)


class UI:
    """Handles rendering of the game board and pieces"""

    def __init__(self, screen, board):
        """
        Initialize the UI

        Args:
            screen: Pygame screen surface
            board: Board object
        """
        self.screen = screen
        self.board = board
        self.font = pygame.font.Font(None, 48)
        self.status_font = pygame.font.Font(None, 32)
        self.piece_images = {}
        self._load_piece_images()

    def _load_piece_images(self):
        """Load all piece images"""
        piece_types = ['general', 'advisor', 'elephant', 'horse', 'chariot', 'cannon', 'soldier']
        colors = ['red', 'black']

        for color in colors:
            for piece_type in piece_types:
                filename = f"assets/images/{color}_{piece_type}.png"
                if os.path.exists(filename):
                    image = pygame.image.load(filename)
                    # Scale image to fit the square size
                    scaled_image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                    self.piece_images[f"{color}_{piece_type}"] = scaled_image
                else:
                    print(f"Warning: Image not found: {filename}")

    def draw_board(self):
        """Draw the Xiangqi board"""
        self.screen.fill(BOARD_COLOR)

        # Draw vertical lines
        for col in range(9):
            x = BOARD_OFFSET_X + col * SQUARE_SIZE
            # Lines don't cross the river for some columns
            if col == 0 or col == 8:
                # Full length lines on the sides
                pygame.draw.line(
                    self.screen, LINE_COLOR,
                    (x, BOARD_OFFSET_Y),
                    (x, BOARD_OFFSET_Y + 9 * SQUARE_SIZE),
                    2
                )
            else:
                # Top half (black side)
                pygame.draw.line(
                    self.screen, LINE_COLOR,
                    (x, BOARD_OFFSET_Y),
                    (x, BOARD_OFFSET_Y + 4 * SQUARE_SIZE),
                    2
                )
                # Bottom half (red side)
                pygame.draw.line(
                    self.screen, LINE_COLOR,
                    (x, BOARD_OFFSET_Y + 5 * SQUARE_SIZE),
                    (x, BOARD_OFFSET_Y + 9 * SQUARE_SIZE),
                    2
                )

        # Draw horizontal lines
        for row in range(10):
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE
            pygame.draw.line(
                self.screen, LINE_COLOR,
                (BOARD_OFFSET_X, y),
                (BOARD_OFFSET_X + 8 * SQUARE_SIZE, y),
                2
            )

        # Draw palace diagonals
        self._draw_palace_diagonals()

        # Draw river
        self._draw_river()

        # Draw board border
        pygame.draw.rect(
            self.screen, LINE_COLOR,
            (BOARD_OFFSET_X, BOARD_OFFSET_Y,
             8 * SQUARE_SIZE, 9 * SQUARE_SIZE),
            3
        )

    def _draw_palace_diagonals(self):
        """Draw diagonal lines in the palaces"""
        # Black palace (top)
        top_palace_x = BOARD_OFFSET_X + 3 * SQUARE_SIZE
        top_palace_y = BOARD_OFFSET_Y

        pygame.draw.line(
            self.screen, LINE_COLOR,
            (top_palace_x, top_palace_y),
            (top_palace_x + 2 * SQUARE_SIZE, top_palace_y + 2 * SQUARE_SIZE),
            2
        )
        pygame.draw.line(
            self.screen, LINE_COLOR,
            (top_palace_x + 2 * SQUARE_SIZE, top_palace_y),
            (top_palace_x, top_palace_y + 2 * SQUARE_SIZE),
            2
        )

        # Red palace (bottom)
        bottom_palace_x = BOARD_OFFSET_X + 3 * SQUARE_SIZE
        bottom_palace_y = BOARD_OFFSET_Y + 7 * SQUARE_SIZE

        pygame.draw.line(
            self.screen, LINE_COLOR,
            (bottom_palace_x, bottom_palace_y),
            (bottom_palace_x + 2 * SQUARE_SIZE, bottom_palace_y + 2 * SQUARE_SIZE),
            2
        )
        pygame.draw.line(
            self.screen, LINE_COLOR,
            (bottom_palace_x + 2 * SQUARE_SIZE, bottom_palace_y),
            (bottom_palace_x, bottom_palace_y + 2 * SQUARE_SIZE),
            2
        )

    def _draw_river(self):
        """Draw the river in the middle of the board"""
        river_y = BOARD_OFFSET_Y + 4 * SQUARE_SIZE + SQUARE_SIZE // 2
        river_font = pygame.font.Font(None, 36)

        # Draw "楚河" (Chu River) on the left
        chu_text = river_font.render("楚河", True, RIVER_COLOR)
        self.screen.blit(chu_text, (BOARD_OFFSET_X + SQUARE_SIZE, river_y - 15))

        # Draw "漢界" (Han Boundary) on the right
        han_text = river_font.render("漢界", True, RIVER_COLOR)
        self.screen.blit(han_text, (BOARD_OFFSET_X + 5 * SQUARE_SIZE, river_y - 15))

    def draw_pieces(self):
        """Draw all pieces on the board"""
        for row in range(10):
            for col in range(9):
                piece = self.board.get_piece(row, col)
                if piece:
                    self._draw_piece(piece, row, col)

    def _draw_piece(self, piece, row, col):
        """
        Draw a single piece

        Args:
            piece: Piece object
            row: Row position
            col: Column position
        """
        x = BOARD_OFFSET_X + col * SQUARE_SIZE
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE

        # Get the piece image key
        image_key = f"{piece.color}_{piece.piece_type}"

        # Draw piece image if available, otherwise fallback to text
        if image_key in self.piece_images:
            image = self.piece_images[image_key]
            # Center the image on the intersection
            image_rect = image.get_rect(center=(x, y))
            self.screen.blit(image, image_rect)
        else:
            # Fallback to drawing text (original method)
            color = RED_PIECE_COLOR if piece.color == 'red' else BLACK_PIECE_COLOR
            pygame.draw.circle(self.screen, (240, 220, 180), (x, y), SQUARE_SIZE // 3)
            pygame.draw.circle(self.screen, color, (x, y), SQUARE_SIZE // 3, 3)

            text_color = RED_PIECE_COLOR if piece.color == 'red' else BLACK_PIECE_COLOR
            text = self.font.render(str(piece), True, text_color)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)

    def highlight_square(self, position, color):
        """
        Highlight a square on the board

        Args:
            position: Tuple (row, col)
            color: RGB color tuple
        """
        row, col = position
        x = BOARD_OFFSET_X + col * SQUARE_SIZE
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE

        # Draw semi-transparent highlight
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(color)
        self.screen.blit(s, (x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2))

    def draw_status(self, status_text):
        """
        Draw game status text

        Args:
            status_text: Status message to display
        """
        text = self.status_font.render(status_text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 30))

        # Draw background for text
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (255, 255, 200), bg_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect, 2)

        self.screen.blit(text, text_rect)

    def screen_to_board(self, pos):
        """
        Convert screen coordinates to board coordinates

        Args:
            pos: Tuple (x, y) in screen coordinates

        Returns:
            Tuple (col, row) in board coordinates
        """
        x, y = pos
        col = round((x - BOARD_OFFSET_X) / SQUARE_SIZE)
        row = round((y - BOARD_OFFSET_Y) / SQUARE_SIZE)

        # Clamp to board boundaries
        col = max(0, min(8, col))
        row = max(0, min(9, row))

        return col, row

    def board_to_screen(self, row, col):
        """
        Convert board coordinates to screen coordinates

        Args:
            row: Row on board
            col: Column on board

        Returns:
            Tuple (x, y) in screen coordinates
        """
        x = BOARD_OFFSET_X + col * SQUARE_SIZE
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE
        return x, y

    def draw_thinking_animation(self, frame):
        """
        Draw a creative thinking animation

        Args:
            frame: Animation frame number
        """
        import math

        # Position at top center of screen
        center_x = SCREEN_WIDTH // 2
        center_y = 50

        # Create a pulsing effect
        pulse = abs(math.sin(frame * 0.1)) * 0.3 + 0.7

        # Draw animated text
        thinking_text = "AI is thinking"
        dots = "." * ((frame // 10) % 4)
        full_text = thinking_text + dots

        text_surface = self.status_font.render(full_text, True, (50, 50, 150))
        text_rect = text_surface.get_rect(center=(center_x, center_y))

        # Background with pulse effect
        bg_width = text_rect.width + 60
        bg_height = text_rect.height + 20
        bg_rect = pygame.Rect(
            center_x - bg_width // 2,
            center_y - bg_height // 2,
            bg_width,
            bg_height
        )

        # Pulsing background
        bg_alpha = int(200 * pulse)
        bg_surface = pygame.Surface((bg_width, bg_height))
        bg_surface.set_alpha(bg_alpha)
        bg_surface.fill((200, 220, 255))
        self.screen.blit(bg_surface, bg_rect)

        # Border with animation
        pygame.draw.rect(self.screen, (50, 50, 150), bg_rect, 2)

        # Draw text
        self.screen.blit(text_surface, text_rect)

        # Draw rotating circles around the text
        num_circles = 8
        radius = 15
        orbit_radius = bg_width // 2 + 20

        for i in range(num_circles):
            angle = (frame * 0.05) + (i * 2 * math.pi / num_circles)
            x = center_x + math.cos(angle) * orbit_radius
            y = center_y + math.sin(angle) * orbit_radius

            # Fade circles based on position
            fade = (math.sin(angle + frame * 0.1) + 1) / 2
            alpha = int(150 * fade)

            # Create circle with transparency
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            color_with_alpha = (100, 100, 200, alpha)
            pygame.draw.circle(circle_surface, color_with_alpha, (radius, radius), radius)

            self.screen.blit(circle_surface, (x - radius, y - radius))

        # Draw brain/thought icon (stylized Chinese character for "thought" 思)
        icon_font = pygame.font.Font(None, 36)
        icon = icon_font.render("💭", True, (80, 80, 180))
        if not icon.get_width() > 5:  # Fallback if emoji not supported
            icon = icon_font.render("◎", True, (80, 80, 180))

        icon_x = center_x - bg_width // 2 - 30
        icon_rect = icon.get_rect(center=(icon_x, center_y))
        self.screen.blit(icon, icon_rect)
