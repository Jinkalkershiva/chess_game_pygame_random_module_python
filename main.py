import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Chess piece class
class ChessPiece:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

# Initialize the board
board = [[None for _ in range(8)] for _ in range(8)]
current_player = 'white'
selected_piece = None
selected_pos = None
valid_moves = []

def init_board():
    for col in range(8):
        board[1][col] = ChessPiece('black', 'pawn', 'images/black_pawn.png')
        board[6][col] = ChessPiece('white', 'pawn', 'images/white_pawn.png')
    
    piece_positions = {
        'rook': [(0, 0), (0, 7), (7, 0), (7, 7)],
        'knight': [(0, 1), (0, 6), (7, 1), (7, 6)],
        'bishop': [(0, 2), (0, 5), (7, 2), (7, 5)],
        'queen': [(0, 3), (7, 3)],
        'king': [(0, 4), (7, 4)]
    }
    
    for type, positions in piece_positions.items():
        for row, col in positions:
            color = 'black' if row == 0 else 'white'
            board[row][col] = ChessPiece(color, type, f'images/{color}_{type}.png')

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    if selected_pos:
        pygame.draw.rect(screen, YELLOW, (selected_pos[1] * SQUARE_SIZE, selected_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
    
    for move in valid_moves:
        pygame.draw.rect(screen, GREEN, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                screen.blit(piece.image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def get_valid_moves(piece, row, col):
    moves = []
    directions = {
        'rook': [(1, 0), (-1, 0), (0, 1), (0, -1)],
        'bishop': [(1, 1), (1, -1), (-1, 1), (-1, -1)],
        'queen': [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)],
        'knight': [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
        'king': [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    }
    
    if piece.type in directions:
        for dr, dc in directions[piece.type]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    moves.append((r, c))
                    break
                else:
                    break
                if piece.type in ['knight', 'king']:
                    break
                r += dr
                c += dc
    elif piece.type == 'pawn':
        direction = -1 if piece.color == 'white' else 1
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))
        for dc in [-1, 1]:
            if 0 <= row + direction < 8 and 0 <= col + dc < 8 and board[row + direction][col + dc]:
                if board[row + direction][col + dc].color != piece.color:
                    moves.append((row + direction, col + dc))
    return moves

def make_random_move():
    global current_player
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == 'black':
                valid = get_valid_moves(piece, row, col)
                if valid:
                    moves.append((piece, row, col, valid))
    if moves:
        piece, row, col, valid = random.choice(moves)
        new_row, new_col = random.choice(valid)
        board[new_row][new_col] = piece
        board[row][col] = None
        piece.has_moved = True
        current_player = 'white'

def handle_click(pos):
    global selected_piece, selected_pos, valid_moves, current_player
    if current_player == 'black':
        return
    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    if selected_piece is None:
        piece = board[row][col]
        if piece and piece.color == current_player:
            selected_piece = piece
            selected_pos = (row, col)
            valid_moves = get_valid_moves(piece, row, col)
    else:
        if (row, col) in valid_moves:
            board[row][col] = selected_piece
            board[selected_pos[0]][selected_pos[1]] = None
            selected_piece.has_moved = True
            current_player = 'black'
        selected_piece = None
        selected_pos = None
        valid_moves = []

def main():
    init_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(pygame.mouse.get_pos())
        if current_player == 'black':
            make_random_move()
        draw_board()
        draw_pieces()
        pygame.display.flip()

if __name__ == "__main__":
    main()
