import pygame
import chess

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (255, 255, 255)
GREEN = (118, 150, 86)
DARK_BROWN = (79, 55, 42)
LIGHT_BROWN = (237, 204, 155)
PIECE_IMAGES = {}

PIECES = {'p': 'bp.png', 'r': 'br.png', 'n': 'bn.png', 'b': 'bb.png', 'q': 'bq.png', 'k': 'bk.png', 'P': 'p.png', 'R': 'r.png', 'N': 'n.png', 'B': 'b.png', 'Q': 'q.png', 'K': 'k.png'}

for piece, filename in PIECES.items():
    PIECE_IMAGES[piece] = pygame.image.load(f'assets/{filename}')
    PIECE_IMAGES[piece] = pygame.transform.scale(PIECE_IMAGES[piece], (SQUARE_SIZE, SQUARE_SIZE))

board = chess.Board()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")


def evaluate_board(board):
    piece_values = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3, chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}
    value = 0
    max = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                value += piece_values[piece.piece_type]
            else:
                value -= piece_values[piece.piece_type]

    return value


def minimax(board, depth, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        max_eval = -10000
        for move in board.legal_moves:
            board.push(move)
            #eval2 = evaluate_board(board)
            eval, _ = minimax(board, depth - 1, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        #print(board.legal_moves)
        for move in board.legal_moves:
            board.push(move)
            eval2 = evaluate_board(board)
            #if eval2 > 0:
                #print(eval2,move)
            eval, _ = minimax(board, depth - 1, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move


def get_best_move():
    _, best_move = minimax(board, 3, board.turn)
    return best_move


def draw_board(flipped):
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            actual_row = 7 - row if flipped else row
            actual_col = 7 - col if flipped else col
            pygame.draw.rect(screen, color,(actual_col * SQUARE_SIZE, actual_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(flipped):
    for row in range(ROWS):
        for col in range(COLS):
            actual_row = 7 - row if flipped else row
            actual_col = 7 - col if not flipped else col

            square = chess.square(actual_col, actual_row)
            piece = board.piece_at(square)
            if piece:
                piece_symbol = piece.symbol()
                screen.blit(PIECE_IMAGES[piece_symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))


def get_square_from_pos(pos, flipped):
    x, y = pos
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    actual_row = 7 - row if flipped else row
    actual_col = 7 - col if not flipped else col
    return actual_row, actual_col


running = True
selected_square = None
flipped = True
counter = 0

while running:
    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()

    if not board.legal_moves:
        running = False
        if counter % 2 == 0:
            print("black won")
        else:
            print("white won")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_from_pos(pygame.mouse.get_pos(), flipped)
            square = chess.square(col, row)
            if selected_square is None:
                if board.piece_at(square):
                    selected_square = square
            else:
                move = chess.Move(selected_square, square)
                if move in board.legal_moves:
                    board.push(move)
                    flipped = not flipped
                    counter += 1
                else:
                    print("illegal move")
                selected_square = None
            print(f"you clicked {board.piece_at(square)}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if counter % 2 != 0:
                    best_move = get_best_move()
                    print(f"ai chose: {best_move}")
                else:
                    print("its white's turn")

pygame.quit()
