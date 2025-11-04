// Xiangqi Web Client
// API configuration
const API_BASE = window.location.origin + '/api';

// Game state
let gameState = {
    gameId: null,
    board: null,
    currentPlayer: null,
    selectedPiece: null,
    validMoves: [],
    status: ''
};

// Canvas configuration
const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');

const BOARD_OFFSET_X = 50;
const BOARD_OFFSET_Y = 50;
const SQUARE_SIZE = 60;
const BOARD_COLOR = '#f5deb3';
const LINE_COLOR = '#000000';
const RED_PIECE_COLOR = '#c00000';
const BLACK_PIECE_COLOR = '#000000';

// Piece characters
const PIECE_CHARS = {
    red: {
        general: '帥', advisor: '仕', elephant: '相',
        horse: '傌', chariot: '俥', cannon: '炮', soldier: '兵'
    },
    black: {
        general: '將', advisor: '士', elephant: '象',
        horse: '馬', chariot: '車', cannon: '砲', soldier: '卒'
    }
};

// Initialize game on load
document.addEventListener('DOMContentLoaded', () => {
    initGame();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('newGame').addEventListener('click', () => initGame());
    document.getElementById('aiMove').addEventListener('click', () => makeAIMove());
    canvas.addEventListener('click', handleCanvasClick);
}

async function initGame() {
    try {
        updateStatus('Creating new game...');

        const response = await fetch(`${API_BASE}/game/new`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ai_enabled: true,
                ai_color: 'black',
                ai_depth: 3
            })
        });

        const data = await response.json();

        if (data.success) {
            gameState.gameId = data.game_id;
            updateGameState(data.state);
            drawBoard();
        } else {
            updateStatus('Failed to create game');
        }
    } catch (error) {
        console.error('Error creating game:', error);
        updateStatus('Error creating game');
    }
}

function updateGameState(state) {
    if (!state) return;

    gameState.board = state.board_state.board;
    gameState.currentPlayer = state.board_state.current_player;
    gameState.status = state.board_state.status;
    gameState.selectedPiece = null;
    gameState.validMoves = [];

    updateStatus(gameState.status);
    drawBoard();

    // Enable/disable AI move button
    const aiButton = document.getElementById('aiMove');
    aiButton.disabled = gameState.currentPlayer !== 'black' || state.board_state.is_game_over;
}

function updateStatus(message) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = message;

    // Update status styling
    statusDiv.className = 'status-bar';
    if (message.includes('check!') && !message.includes('Checkmate')) {
        statusDiv.classList.add('check');
    } else if (message.includes('Checkmate')) {
        statusDiv.classList.add('checkmate');
    } else if (message.includes('Stalemate')) {
        statusDiv.classList.add('stalemate');
    }
}

function drawBoard() {
    // Clear canvas
    ctx.fillStyle = BOARD_COLOR;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw grid lines
    ctx.strokeStyle = LINE_COLOR;
    ctx.lineWidth = 2;

    // Vertical lines
    for (let col = 0; col < 9; col++) {
        const x = BOARD_OFFSET_X + col * SQUARE_SIZE;
        if (col === 0 || col === 8) {
            // Full length on sides
            ctx.beginPath();
            ctx.moveTo(x, BOARD_OFFSET_Y);
            ctx.lineTo(x, BOARD_OFFSET_Y + 9 * SQUARE_SIZE);
            ctx.stroke();
        } else {
            // Split by river
            ctx.beginPath();
            ctx.moveTo(x, BOARD_OFFSET_Y);
            ctx.lineTo(x, BOARD_OFFSET_Y + 4 * SQUARE_SIZE);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(x, BOARD_OFFSET_Y + 5 * SQUARE_SIZE);
            ctx.lineTo(x, BOARD_OFFSET_Y + 9 * SQUARE_SIZE);
            ctx.stroke();
        }
    }

    // Horizontal lines
    for (let row = 0; row < 10; row++) {
        const y = BOARD_OFFSET_Y + row * SQUARE_SIZE;
        ctx.beginPath();
        ctx.moveTo(BOARD_OFFSET_X, y);
        ctx.lineTo(BOARD_OFFSET_X + 8 * SQUARE_SIZE, y);
        ctx.stroke();
    }

    // Draw palace diagonals
    drawPalaceDiagonals();

    // Draw river text
    drawRiver();

    // Draw pieces
    if (gameState.board) {
        drawPieces();
    }

    // Highlight selected piece and valid moves
    if (gameState.selectedPiece) {
        highlightSquare(gameState.selectedPiece, 'rgba(255, 255, 0, 0.4)');
        gameState.validMoves.forEach(move => {
            highlightSquare(move, 'rgba(0, 255, 0, 0.4)');
        });
    }
}

function drawPalaceDiagonals() {
    ctx.strokeStyle = LINE_COLOR;
    ctx.lineWidth = 2;

    // Black palace (top)
    const topX = BOARD_OFFSET_X + 3 * SQUARE_SIZE;
    const topY = BOARD_OFFSET_Y;

    ctx.beginPath();
    ctx.moveTo(topX, topY);
    ctx.lineTo(topX + 2 * SQUARE_SIZE, topY + 2 * SQUARE_SIZE);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(topX + 2 * SQUARE_SIZE, topY);
    ctx.lineTo(topX, topY + 2 * SQUARE_SIZE);
    ctx.stroke();

    // Red palace (bottom)
    const bottomX = BOARD_OFFSET_X + 3 * SQUARE_SIZE;
    const bottomY = BOARD_OFFSET_Y + 7 * SQUARE_SIZE;

    ctx.beginPath();
    ctx.moveTo(bottomX, bottomY);
    ctx.lineTo(bottomX + 2 * SQUARE_SIZE, bottomY + 2 * SQUARE_SIZE);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(bottomX + 2 * SQUARE_SIZE, bottomY);
    ctx.lineTo(bottomX, bottomY + 2 * SQUARE_SIZE);
    ctx.stroke();
}

function drawRiver() {
    ctx.font = '24px Arial';
    ctx.fillStyle = '#4682b4';

    const riverY = BOARD_OFFSET_Y + 4.5 * SQUARE_SIZE;

    ctx.fillText('楚河', BOARD_OFFSET_X + SQUARE_SIZE, riverY);
    ctx.fillText('漢界', BOARD_OFFSET_X + 5 * SQUARE_SIZE, riverY);
}

function drawPieces() {
    for (let row = 0; row < 10; row++) {
        for (let col = 0; col < 9; col++) {
            const piece = gameState.board[row][col];
            if (piece) {
                drawPiece(piece, row, col);
            }
        }
    }
}

function drawPiece(piece, row, col) {
    const x = BOARD_OFFSET_X + col * SQUARE_SIZE;
    const y = BOARD_OFFSET_Y + row * SQUARE_SIZE;

    // Draw circle background
    ctx.fillStyle = '#f0e6d0';
    ctx.beginPath();
    ctx.arc(x, y, SQUARE_SIZE / 3, 0, 2 * Math.PI);
    ctx.fill();

    // Draw border
    ctx.strokeStyle = piece.color === 'red' ? RED_PIECE_COLOR : BLACK_PIECE_COLOR;
    ctx.lineWidth = 3;
    ctx.stroke();

    // Draw Chinese character
    ctx.font = 'bold 32px Arial';
    ctx.fillStyle = piece.color === 'red' ? RED_PIECE_COLOR : BLACK_PIECE_COLOR;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    const char = PIECE_CHARS[piece.color][piece.piece_type];
    ctx.fillText(char, x, y);
}

function highlightSquare(position, color) {
    const [row, col] = position;
    const x = BOARD_OFFSET_X + col * SQUARE_SIZE;
    const y = BOARD_OFFSET_Y + row * SQUARE_SIZE;

    ctx.fillStyle = color;
    ctx.fillRect(x - SQUARE_SIZE / 2, y - SQUARE_SIZE / 2, SQUARE_SIZE, SQUARE_SIZE);
}

function handleCanvasClick(event) {
    if (!gameState.gameId || gameState.currentPlayer !== 'red') return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Convert to board coordinates
    const col = Math.round((x - BOARD_OFFSET_X) / SQUARE_SIZE);
    const row = Math.round((y - BOARD_OFFSET_Y) / SQUARE_SIZE);

    if (row < 0 || row > 9 || col < 0 || col > 8) return;

    handleSquareClick(row, col);
}

async function handleSquareClick(row, col) {
    // If a piece is selected, try to move it
    if (gameState.selectedPiece) {
        const isValidMove = gameState.validMoves.some(
            move => move[0] === row && move[1] === col
        );

        if (isValidMove) {
            await makeMove(gameState.selectedPiece, [row, col]);
            return;
        } else {
            // Deselect
            gameState.selectedPiece = null;
            gameState.validMoves = [];
        }
    }

    // Select a piece if it belongs to current player
    const piece = gameState.board[row][col];
    if (piece && piece.color === gameState.currentPlayer) {
        await selectPiece(row, col);
    }

    drawBoard();
}

async function selectPiece(row, col) {
    try {
        const response = await fetch(
            `${API_BASE}/game/${gameState.gameId}/valid-moves?row=${row}&col=${col}`
        );
        const data = await response.json();

        gameState.selectedPiece = [row, col];
        gameState.validMoves = data.valid_moves;
    } catch (error) {
        console.error('Error getting valid moves:', error);
    }
}

async function makeMove(fromPos, toPos) {
    try {
        updateStatus('Making move...');

        const response = await fetch(`${API_BASE}/game/${gameState.gameId}/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                from_pos: fromPos,
                to_pos: toPos
            })
        });

        const data = await response.json();

        if (data.success) {
            updateGameState(data.state);

            // Automatically make AI move if game is not over
            if (!data.state.board_state.is_game_over && gameState.currentPlayer === 'black') {
                setTimeout(() => makeAIMove(), 500);
            }
        } else {
            updateStatus(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error making move:', error);
        updateStatus('Error making move');
    }
}

async function makeAIMove() {
    try {
        updateStatus('AI is thinking...');
        document.getElementById('aiMove').disabled = true;

        const response = await fetch(`${API_BASE}/game/${gameState.gameId}/ai-move`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            updateGameState(data.state);
        } else {
            updateStatus(`AI Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error making AI move:', error);
        updateStatus('Error making AI move');
    } finally {
        document.getElementById('aiMove').disabled = false;
    }
}
