import pygame
from Board import *

# fade multiple surfaces on the screen
def fade(*surfacencoords: tuple):
    for alpha in range(0, 257, 6):
        for snc in surfacencoords:
            surface, coordinates = snc
            surface.set_alpha(alpha)
            screen.blit(surface, coordinates)
            pygame.time.delay(30)
        pygame.display.flip()

# board initialisations
game_board = Board()

# pygame initialisations
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Othello/Reversi")

bBoard = pygame.image.load("Othello-Reversi-Game/images/Othello_Black_Side_Board.png")
black_disc = pygame.image.load("Othello-Reversi-Game/images/Black_Disc.png")
white_disc = pygame.image.load("Othello-Reversi-Game/images/White_Disc.png")

blackDiscCounter = pygame.image.load("Othello-Reversi-Game/images/Large_Black_Disc.png")
whiteDiscCounter = pygame.image.load("Othello-Reversi-Game/images/Large_White_Disc.png")

possibleBlackMove = pygame.image.load("Othello-Reversi-Game/images/Black_Disc.png")
possibleWhiteMove = pygame.image.load("Othello-Reversi-Game/images/White_Disc.png")
pygame.Surface.set_alpha(possibleBlackMove, 50)
pygame.Surface.set_alpha(possibleWhiteMove, 50)

endScreenBlack = pygame.image.load("Othello-Reversi-Game/images/End_Screen_Black.png")
endScreenWhite = pygame.image.load("Othello-Reversi-Game/images/End_Screen_White.png")
endScreenDraw = pygame.image.load("Othello-Reversi-Game/images/End_Screen_Draw.png")
endPrompt  = pygame.image.load("Othello-Reversi-Game/images/End_Prompt.png")

discCountFont = pygame.font.Font("Othello-Reversi-Game/Gotham-Font/GothamLight.ttf", 40)

screen.blit(bBoard, (0,0))
screen.blit(blackDiscCounter, (775, 475))
screen.blit(whiteDiscCounter, (950, 475))
pygame.display.flip()

running = True
turn = Board.BLACK
shown_moves = False
possible_moves = []
last_move = (20, 20)
game_end = False
hasBlackForfeited = False
hasWhiteForfeited = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            mx -= 100
            my -= 100
            r = my // 75
            c = mx // 75
            if (r,c) in possible_moves:
                last_move = (r, c)
                game_board.set_discs(r, c, turn)
                shown_moves = False
                possible_moves.remove((r,c))
                for pos in possible_moves:
                    row, col = pos
                    x = 100 + 75 * col
                    y = 100 + 75 * row
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x+4, y+4, 67, 67))
                turn *= -1
        elif game_end and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                game_end = False
                # fade out the screen
                game_board.reset_board()
                dummy_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                dummy_surface.fill((255, 255, 255))
                fade((dummy_surface, (0, 0)))

                screen.blit(bBoard, (0,0))
                screen.blit(blackDiscCounter, (775, 475))
                screen.blit(whiteDiscCounter, (950, 475))
                last_move = (20, 20)

    if not game_end:           
        # display all the dics present on the board
        for row in range(8):
            for col in range(8):
                if game_board.board[row, col] == Board.BLACK:
                    x = 100 + 75 * col
                    y = 100 + 75 * row
                    screen.blit(black_disc, (x,y))

                elif game_board.board[row, col] == Board.WHITE:
                    x = 100 + 75 * col
                    y = 100 + 75 * row
                    screen.blit(white_disc, (x,y))
        
        # mark the last move made
        r, c = last_move
        pygame.draw.circle(screen, (255, 0, 0), (c * 75 + 100 + 75/2, r * 75 + 100 + 75/2), 5)

        if turn == Board.BLACK and not shown_moves:
            possible_moves = list(game_board.all_legal_moves(Board.BLACK))
            if possible_moves == []:
                turn *= -1
                hasBlackForfeited = True
            else:
                hasBlackForfeited = False
            for pos in possible_moves:
                r, c = pos
                screen.blit(possibleBlackMove, (100 + 75 * c, 100 + 75 * r))
            
            shown_moves = not hasBlackForfeited

        elif turn == Board.WHITE and not shown_moves:
            possible_moves = list(game_board.all_legal_moves(Board.WHITE))
            if possible_moves == []:
                hasWhiteForfeited = True
                turn *= -1
            else:
                hasWhiteForfeited = False
            for pos in possible_moves:
                r, c = pos
                screen.blit(possibleWhiteMove, (100 + 75 * c, 100 + 75 * r))
            
            shown_moves = not hasWhiteForfeited

        if hasBlackForfeited is True and hasWhiteForfeited is True:
            if game_board.black_disc_count > game_board.white_disc_count:
                fade((endScreenBlack, (725, 250)))
            elif game_board.black_disc_count < game_board.white_disc_count:
                fade((endScreenWhite, (725, 250)))
            else:
                fade((endScreenDraw, (725, 250)))
            fade((endPrompt, (877, 420)))
            game_end = True

        # blit the scores during the game
        dummy_surface = pygame.Surface((60, 40))
        dummy_surface.fill((255, 255, 255))
        screen.blit(dummy_surface, (885, 510))
        screen.blit(dummy_surface, (1060, 510))

        black_disc_count = discCountFont.render(f"{game_board.black_disc_count}", False, (0, 0, 0))
        white_disc_count = discCountFont.render(f"{game_board.white_disc_count}", False, (0, 0, 0))
        screen.blit(black_disc_count, (885, 510))
        screen.blit(white_disc_count, (1060, 510))
        
        pygame.display.flip()

pygame.quit()