"""
FastAPI server for Xiangqi game
Provides REST API and WebSocket support for web clients
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Tuple
import json

from engine.game_engine import GameEngine

app = FastAPI(title="Xiangqi API", version="1.0.0")

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game engine instance
engine = GameEngine()

# Active WebSocket connections
active_connections: dict[str, WebSocket] = {}


# Request/Response Models
class NewGameRequest(BaseModel):
    ai_enabled: bool = True
    ai_color: str = "black"
    ai_depth: int = 3


class MoveRequest(BaseModel):
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]


class MoveResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    move: Optional[dict] = None
    state: Optional[dict] = None


# API Endpoints
@app.get("/api")
async def root():
    """API root endpoint"""
    return {
        "name": "Xiangqi API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/game/new": "Create a new game",
            "GET /api/game/{game_id}/state": "Get game state",
            "POST /api/game/{game_id}/move": "Make a move",
            "GET /api/game/{game_id}/valid-moves": "Get valid moves for a position",
            "POST /api/game/{game_id}/ai-move": "Make AI move",
            "DELETE /api/game/{game_id}": "Delete a game",
            "WebSocket /ws/{game_id}": "Connect to game updates"
        }
    }


@app.post("/api/game/new")
async def create_game(request: NewGameRequest):
    """Create a new game"""
    try:
        game_id = engine.new_game(
            ai_enabled=request.ai_enabled,
            ai_color=request.ai_color,
            ai_depth=request.ai_depth
        )
        state = engine.get_game_state(game_id)
        return {
            "success": True,
            "game_id": game_id,
            "state": state
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/game/{game_id}/state")
async def get_game_state(game_id: str):
    """Get the current game state"""
    state = engine.get_game_state(game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")
    return state


@app.post("/api/game/{game_id}/move")
async def make_move(game_id: str, move: MoveRequest):
    """Make a move in the game"""
    result = engine.make_move(game_id, move.from_pos, move.to_pos)

    if not result['success']:
        return result

    # Notify WebSocket clients
    if game_id in active_connections:
        try:
            await active_connections[game_id].send_json({
                "type": "move",
                "data": result
            })
        except:
            pass

    return result


@app.get("/api/game/{game_id}/valid-moves")
async def get_valid_moves(game_id: str, row: int, col: int):
    """Get valid moves for a piece at the given position"""
    moves = engine.get_valid_moves(game_id, row, col)
    return {
        "position": [row, col],
        "valid_moves": moves
    }


@app.post("/api/game/{game_id}/ai-move")
async def make_ai_move(game_id: str):
    """Make the AI's move"""
    result = engine.make_ai_move(game_id)

    if not result['success']:
        return result

    # Notify WebSocket clients
    if game_id in active_connections:
        try:
            await active_connections[game_id].send_json({
                "type": "ai_move",
                "data": result
            })
        except:
            pass

    return result


@app.delete("/api/game/{game_id}")
async def delete_game(game_id: str):
    """Delete a game session"""
    success = engine.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")

    # Close WebSocket if exists
    if game_id in active_connections:
        try:
            await active_connections[game_id].close()
        except:
            pass
        del active_connections[game_id]

    return {"success": True, "message": "Game deleted"}


@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket endpoint for real-time game updates"""
    await websocket.accept()
    active_connections[game_id] = websocket

    try:
        # Send initial game state
        state = engine.get_game_state(game_id)
        if state:
            await websocket.send_json({
                "type": "initial_state",
                "data": state
            })

        # Keep connection alive and handle messages
        while True:
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
            await websocket.send_json({
                "type": "pong",
                "data": data
            })

    except WebSocketDisconnect:
        if game_id in active_connections:
            del active_connections[game_id]


# Mount static files (web client) - must be last
app.mount("/", StaticFiles(directory="clients/web_client", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
