"""
Xiangqi Piece Representation
Defines the Piece class and piece types
"""


class Piece:
    """Represents a Xiangqi piece"""

    def __init__(self, piece_type, color, position):
        """
        Initialize a piece

        Args:
            piece_type: Type of piece ('general', 'advisor', 'elephant', 'horse', 'chariot', 'cannon', 'soldier')
            color: 'red' or 'black'
            position: Tuple (row, col)
        """
        self.piece_type = piece_type
        self.color = color
        self.position = position

    def __str__(self):
        """String representation of the piece"""
        piece_chars = {
            'red': {
                'general': '帥', 'advisor': '仕', 'elephant': '相',
                'horse': '傌', 'chariot': '俥', 'cannon': '炮', 'soldier': '兵'
            },
            'black': {
                'general': '將', 'advisor': '士', 'elephant': '象',
                'horse': '馬', 'chariot': '車', 'cannon': '砲', 'soldier': '卒'
            }
        }
        return piece_chars[self.color][self.piece_type]

    def to_dict(self):
        """Convert piece to dictionary for serialization"""
        return {
            'piece_type': self.piece_type,
            'color': self.color,
            'position': self.position
        }

    @classmethod
    def from_dict(cls, data):
        """Create piece from dictionary"""
        return cls(
            piece_type=data['piece_type'],
            color=data['color'],
            position=tuple(data['position'])
        )
