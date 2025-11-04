# Xiangqi (Chinese Chess) Game

A playable 2D Chinese Chess game where a human player can compete against an AI opponent.

## Features

- Visual Chinese Chess board with traditional piece rendering
- Full legal move validation for all piece types
- Player vs Computer gameplay
- AI opponent using minimax algorithm with alpha-beta pruning
- Move highlighting and piece selection
- Game state display (check, checkmate, stalemate)
- Traditional board aesthetics with palace and river markings

## Tech Stack

### Backend
- Python 3.8+
- FastAPI for web API
- Uvicorn ASGI server
- WebSocket support for real-time updates

### Clients
- **Desktop**: Pygame for graphics and UI
- **Web**: HTML5 Canvas + JavaScript
- Both clients use the same game engine

### Deployment
- Caddy webserver (reverse proxy)
- Systemd service management
- Proxmox VM/LXC compatible

## Installation

1. Clone the repository

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Desktop Version (Pygame)

Run the game using the provided script:
```bash
./run.sh
```

Or manually with PYTHONPATH:
```bash
PYTHONPATH=. python3 main.py
```

### Web Version

Run the web server using the provided script:
```bash
./run-web.sh
```

Or manually with virtual environment:
```bash
source venv/bin/activate
PYTHONPATH=. python3 -m uvicorn server.api:app --host 127.0.0.1 --port 8000
```

Then open your browser to: **http://localhost:8000**

**For production deployment to Proxmox/Caddy, see [DEPLOYMENT.md](DEPLOYMENT.md)**

### Game Rules

- Red (human) moves first
- Click on a piece to select it (valid moves will be highlighted in green)
- Click on a highlighted square to move the selected piece
- The AI (black) will automatically make its move after yours
- Win by checkmating your opponent's General

### Piece Movement

- **General (帥/將)**: Moves one step orthogonally within the palace
- **Advisor (仕/士)**: Moves one step diagonally within the palace
- **Elephant (相/象)**: Moves two steps diagonally, cannot cross the river
- **Horse (傌/馬)**: Moves in an L-shape (one step orthogonal, one diagonal), can be blocked
- **Chariot (俥/車)**: Moves any distance orthogonally
- **Cannon (炮/砲)**: Moves like a chariot but must jump over one piece to capture
- **Soldier (兵/卒)**: Moves forward; can also move sideways after crossing the river

## Architecture

This project uses a **modular client-server architecture** that separates game logic from UI, enabling multiple front-end implementations.

### Project Structure

```
Xiangqi/
├── main.py                    # Entry point (launches pygame client)
├── run.sh                     # Convenience script with PYTHONPATH
│
├── engine/                    # Core game logic (UI-agnostic)
│   ├── game_engine.py        # Main game engine & API
│   ├── board.py              # Board state & move validation
│   ├── pieces.py             # Piece classes
│   ├── ai_player.py          # AI with minimax algorithm
│   └── __init__.py
│
├── clients/                   # UI implementations
│   └── pygame_client/        # Desktop client (pygame)
│       ├── main.py           # Game loop
│       ├── ui_renderer.py    # Rendering logic
│       ├── assets/           # Images, fonts
│       └── __init__.py
│
├── common/                    # Shared utilities
│   ├── constants.py          # Game constants
│   └── __init__.py
│
├── tests/                     # Test suite
│   └── test_stalemate_fix.py
│
└── server/                    # API server (for future web client)
    └── (to be implemented)
```

### Architecture Benefits

- **Separation of Concerns**: Game logic is completely independent of UI
- **Multiple Frontends**: Easy to add web, mobile, or CLI clients
- **Testability**: Engine can be tested without UI dependencies
- **Reusability**: Same engine for local and networked games
- **Scalability**: Future API server can handle multiple concurrent games

## Development

### Using the Game Engine

The game engine can be used programmatically:

```python
from engine.game_engine import GameEngine

# Create a game
engine = GameEngine()
game_id = engine.new_game(ai_enabled=True, ai_color='black')

# Make a move
result = engine.make_move(game_id, from_pos=(6, 0), to_pos=(5, 0))

# Get AI move
ai_move = engine.get_ai_move(game_id)

# Get game state
state = engine.get_game_state(game_id)
```

### AI Configuration

The AI search depth can be configured when creating a game:
```python
game_id = engine.new_game(ai_enabled=True, ai_color='black', ai_depth=4)
```

### Game Configuration

Board size, colors, and visual settings can be modified in `common/constants.py`.

### Running Tests

```bash
PYTHONPATH=. python3 tests/test_stalemate_fix.py
```

## Future Enhancements

### Engine
- Implement move history and undo functionality
- Add opening book for AI
- Implement game replay feature
- Add game serialization/deserialization

### Clients
- **Web Client**: HTML/JavaScript client with API server
  - Canvas/SVG board rendering
  - WebSocket for real-time updates
  - Mobile-responsive design
- **CLI Client**: Terminal-based interface
- Add sound effects to pygame client
- Create piece image assets (currently using Chinese characters)

### Server
- FastAPI/Flask REST API
- WebSocket support for live games
- Session management for multiple concurrent games
- Authentication and user profiles
- Game history and statistics

## License

This project is for educational purposes.
