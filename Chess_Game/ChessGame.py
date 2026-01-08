import pygame as p
import ChessEngine
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

WIDTH = HEIGHT = 512
TIMER_WIDTH = 200
DIMENSIONS = 8
SQ_SIZE = HEIGHT// DIMENSIONS
MAX_FPS = 15
IMAGES = {}
FULLSCREEN = False

# Timer presets in seconds (minutes * 60)
TIMER_PRESETS = {
    "1": ("No Timer", None),
    "2": ("1 min", 60),
    "3": ("3 min", 180),
    "4": ("5 min", 300),
    "5": ("10 min", 600),
    "6": ("15 min", 900),
    "7": ("30 min", 1800)
}

# Try to load icon, but don't fail if it doesn't exist
try:
    icon_path = os.path.join(SCRIPT_DIR, "images", "icon.ico")
    icon = p.image.load(icon_path)
    p.display.set_icon(icon)
except:
    pass  # Icon is optional

p.display.set_caption("Chess Game")

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK' ]
    for piece in pieces:
        img_path = os.path.join(SCRIPT_DIR, "images", piece + ".png")
        IMAGES[piece] = p.transform.scale(p.image.load(img_path), (SQ_SIZE, SQ_SIZE))

def showTimerMenu(screen):
    """Display timer selection menu"""
    p.init()
    screen.fill(p.Color("white"))
    font = p.font.SysFont("Arial", 28, True)
    title_font = p.font.SysFont("Arial", 36, True)
    
    title = title_font.render("Select Time Control", True, p.Color("black"))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    y_offset = 120
    for key, (name, time) in TIMER_PRESETS.items():
        text = font.render(f"{key}. {name}", True, p.Color("black"))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
        y_offset += 50
    
    instruction = p.font.SysFont("Arial", 20).render("Press 1-7 to select", True, p.Color("gray"))
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT - 50))
    
    p.display.flip()
    
    # Wait for user selection
    selecting = True
    while selecting:
        for e in p.event.get():
            if e.type == p.QUIT:
                return None
            elif e.type == p.KEYDOWN:
                if e.unicode in TIMER_PRESETS:
                    return TIMER_PRESETS[e.unicode][1]
    return None

def formatTime(seconds):
    """Format seconds into MM:SS"""
    if seconds is None:
        return "--:--"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def main():
    global FULLSCREEN, WIDTH, HEIGHT, TIMER_WIDTH, SQ_SIZE
    p.init()
    
    # Show timer selection menu
    temp_screen = p.display.set_mode((WIDTH, HEIGHT))
    timer_duration = showTimerMenu(temp_screen)
    
    if timer_duration is None:
        return
    
    # Initialize with timer panel if timer is enabled
    use_timer = timer_duration is not None
    total_width = WIDTH + TIMER_WIDTH if use_timer else WIDTH
    
    # Start in windowed mode
    screen = p.display.set_mode((total_width, HEIGHT), p.RESIZABLE)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    
    # Timer variables
    white_time = timer_duration if timer_duration else 0
    black_time = timer_duration if timer_duration else 0
    last_time = p.time.get_ticks()
    timer_running = use_timer
    
    while running:
        # Update timer
        if timer_running and not gameOver:
            current_time = p.time.get_ticks()
            elapsed = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            if gs.whiteToMove:
                white_time -= elapsed
                if white_time <= 0:
                    white_time = 0
                    gameOver = True
                    timer_running = False
            else:
                black_time -= elapsed
                if black_time <= 0:
                    black_time = 0
                    gameOver = True
                    timer_running = False
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    # Only process clicks within the chess board
                    if row >= 0 and row < DIMENSIONS and col >= 0 and col < DIMENSIONS:
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 1 and (gs.board[row][col] == "--"): 
                            sqSelected = ()
                            playerClicks = []
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(move)
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    if use_timer:
                        white_time = timer_duration
                        black_time = timer_duration
                        last_time = p.time.get_ticks()
                        timer_running = True
                    gameOver = False
                if e.key == p.K_F11:
                    # Toggle fullscreen
                    FULLSCREEN = not FULLSCREEN
                    if FULLSCREEN:
                        # Get current display info and set fullscreen with scaling
                        info = p.display.Info()
                        screen = p.display.set_mode((info.current_w, info.current_h), p.FULLSCREEN | p.SCALED)
                    else:
                        screen = p.display.set_mode((total_width, HEIGHT), p.RESIZABLE)
        
        if moveMade:
            if animate:
                animatedMoves(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        
        drawGameState(screen, gs, validMoves, sqSelected)
        
        # Draw timer panel
        if use_timer:
            drawTimerPanel(screen, white_time, black_time, gs.whiteToMove)
        
        # Check game over conditions
        if gs.checkMate:
            gameOver = True
            timer_running = False
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            timer_running = False
            drawText(screen, 'Stalemate')
        elif use_timer and (white_time <= 0 or black_time <= 0):
            if white_time <= 0:
                drawText(screen, 'Black wins on time')
            else:
                drawText(screen, 'White wins on time')
        
        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color("yellow"))
            for moves in validMoves:
                if moves.startRow == r and moves.startCol == c:
                    screen.blit(s, (SQ_SIZE*moves.endCol, SQ_SIZE*moves.endRow))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animatedMoves(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, True, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, True, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

def drawTimerPanel(screen, white_time, black_time, white_to_move):
    """Draw the timer panel on the right side"""
    panel_x = WIDTH
    
    # Draw panel background
    p.draw.rect(screen, p.Color("lightgray"), p.Rect(panel_x, 0, TIMER_WIDTH, HEIGHT))
    
    # Draw black timer (top)
    black_bg_color = p.Color("yellow") if not white_to_move else p.Color("darkgray")
    p.draw.rect(screen, black_bg_color, p.Rect(panel_x + 10, 50, TIMER_WIDTH - 20, 100))
    p.draw.rect(screen, p.Color("black"), p.Rect(panel_x + 10, 50, TIMER_WIDTH - 20, 100), 3)
    
    # Black timer text
    font = p.font.SysFont("Arial", 40, True)
    black_label = p.font.SysFont("Arial", 24, True).render("BLACK", True, p.Color("black"))
    black_timer_text = font.render(formatTime(black_time), True, p.Color("black"))
    screen.blit(black_label, (panel_x + TIMER_WIDTH//2 - black_label.get_width()//2, 60))
    screen.blit(black_timer_text, (panel_x + TIMER_WIDTH//2 - black_timer_text.get_width()//2, 100))
    
    # Draw white timer (bottom)
    white_bg_color = p.Color("yellow") if white_to_move else p.Color("darkgray")
    p.draw.rect(screen, white_bg_color, p.Rect(panel_x + 10, HEIGHT - 150, TIMER_WIDTH - 20, 100))
    p.draw.rect(screen, p.Color("black"), p.Rect(panel_x + 10, HEIGHT - 150, TIMER_WIDTH - 20, 100), 3)
    
    # White timer text
    white_label = p.font.SysFont("Arial", 24, True).render("WHITE", True, p.Color("black"))
    white_timer_text = font.render(formatTime(white_time), True, p.Color("black"))
    screen.blit(white_label, (panel_x + TIMER_WIDTH//2 - white_label.get_width()//2, HEIGHT - 140))
    screen.blit(white_timer_text, (panel_x + TIMER_WIDTH//2 - white_timer_text.get_width()//2, HEIGHT - 100))
    
    # Draw controls help
    help_font = p.font.SysFont("Arial", 14)
    help_texts = [
        "Controls:",
        "Z - Undo move",
        "R - Reset game",
        "F11 - Fullscreen"
    ]
    y_pos = HEIGHT // 2 - 40
    for text in help_texts:
        rendered = help_font.render(text, True, p.Color("black"))
        screen.blit(rendered, (panel_x + 20, y_pos))
        y_pos += 25


if __name__ == "__main__":
    main()
