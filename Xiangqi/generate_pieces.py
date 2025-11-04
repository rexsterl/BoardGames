#!/usr/bin/env python3
"""
Generate Xiangqi piece images
Creates PNG images for all pieces with traditional styling
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Piece size
PIECE_SIZE = 80
PIECE_RADIUS = 35

# Colors
RED_COLOR = (200, 0, 0)
BLACK_COLOR = (0, 0, 0)
BACKGROUND = (240, 220, 180)
CIRCLE_BG = (250, 240, 220)

# Piece characters
pieces_red = {
    'general': '帥',
    'advisor': '仕',
    'elephant': '相',
    'horse': '傌',
    'chariot': '俥',
    'cannon': '炮',
    'soldier': '兵'
}

pieces_black = {
    'general': '將',
    'advisor': '士',
    'elephant': '象',
    'horse': '馬',
    'chariot': '車',
    'cannon': '砲',
    'soldier': '卒'
}


def find_chinese_font():
    """Find a suitable Chinese font on the system"""
    # List of possible Chinese font paths
    font_paths = [
        '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',
        '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        'C:\\Windows\\Fonts\\msyh.ttc',  # Windows
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path

    # If no font found, try system fonts
    return pygame.font.match_font('notosanscjk,notoserifcjk,wqy,droid')


def create_piece_image(piece_char, color_rgb, filename, font):
    """Create a single piece image"""
    # Create surface with transparency
    surface = pygame.Surface((PIECE_SIZE, PIECE_SIZE), pygame.SRCALPHA)

    # Draw piece background circle (lighter color)
    pygame.draw.circle(surface, CIRCLE_BG,
                      (PIECE_SIZE // 2, PIECE_SIZE // 2),
                      PIECE_RADIUS)

    # Draw piece border circle
    pygame.draw.circle(surface, color_rgb,
                      (PIECE_SIZE // 2, PIECE_SIZE // 2),
                      PIECE_RADIUS, 3)

    # Draw inner circle (for decorative effect)
    pygame.draw.circle(surface, color_rgb,
                      (PIECE_SIZE // 2, PIECE_SIZE // 2),
                      PIECE_RADIUS - 5, 1)

    # Draw piece character
    text = font.render(piece_char, True, color_rgb)
    text_rect = text.get_rect(center=(PIECE_SIZE // 2, PIECE_SIZE // 2))
    surface.blit(text, text_rect)

    # Save the image
    pygame.image.save(surface, filename)
    print(f"Created: {filename}")


def main():
    """Generate all piece images"""
    # Create output directory
    output_dir = "assets/images"
    os.makedirs(output_dir, exist_ok=True)

    # Find and load Chinese font
    font_path = find_chinese_font()
    if font_path:
        print(f"Using font: {font_path}")
        try:
            font = pygame.font.Font(font_path, 48)
        except Exception as e:
            print(f"Error loading font {font_path}: {e}")
            print("Falling back to system font")
            font = pygame.font.SysFont('notosanscjk,notoserifcjk,wqy,droid,sans', 48)
    else:
        print("No Chinese font found, using system default")
        font = pygame.font.SysFont('sans', 48)

    # Generate red pieces
    print("\nGenerating red pieces...")
    for piece_type, piece_char in pieces_red.items():
        filename = os.path.join(output_dir, f"red_{piece_type}.png")
        create_piece_image(piece_char, RED_COLOR, filename, font)

    # Generate black pieces
    print("\nGenerating black pieces...")
    for piece_type, piece_char in pieces_black.items():
        filename = os.path.join(output_dir, f"black_{piece_type}.png")
        create_piece_image(piece_char, BLACK_COLOR, filename, font)

    print(f"\nAll pieces generated successfully in {output_dir}/")
    pygame.quit()


if __name__ == "__main__":
    main()
