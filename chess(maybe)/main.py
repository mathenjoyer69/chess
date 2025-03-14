from time import sleep
import pygame
import chess
import pyautogui
import tkinter as tk

def on_close():
    global autoplay_online_bool, analysis, autoplay_bool
    autoplay_online_bool = autoplay_online_bool.get()
    analysis = analysis.get()
    autoplay_bool = autoplay_bool.get()
    root.destroy()

root = tk.Tk()

autoplay_online_bool = tk.BooleanVar(value=False)
analysis = tk.BooleanVar(value=False)
autoplay_bool = tk.BooleanVar(value=False)

autoplay_online_label = tk.Label(root,text="click this if you want the bot to be able to move pieces on chess.com")
autoplay_online_label.pack()
check_autoplay_online = tk.Checkbutton(root, text="Autoplay Online", variable=autoplay_online_bool)
check_autoplay_online.pack(pady=5)

analysis_label = tk.Label(root,text="the analysis is for chess.com click it if you play on the analysis board. if you play online dont click it")
analysis_label.pack()
check_analysis = tk.Checkbutton(root, text="Analysis", variable=analysis)
check_analysis.pack(pady=5)

autoplay_label = tk.Label(root,text="the bot will play the move on the pygame chess screen that will open up as soon as you close this window")
autoplay_label.pack()
check_autoplay = tk.Checkbutton(root, text="Autoplay", variable=autoplay_bool)
check_autoplay.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

print(autoplay_online_bool,autoplay_bool,analysis)
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
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
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

def autoplay_online(move1,analysis):
    move_str = str(move1)
    if analysis:
        coordinates = {"a1":(435,905),"a2":(435,805),"a3":(435,705),"a4":(435,605),"a5":(435,505),"a6":(435,405),"a7":(435,305),"a8":(435,205),
                       "b1":(535,905),"b2":(535,805),"b3":(535,705),"b4":(535,605),"b5":(535,505),"b6":(535,405),"b7":(535,305),"b8":(535,205),
                       "c1":(635,905),"c2":(635,805),"c3":(635,705),"c4":(635,605),"c5":(635,505),"c6":(635,405),"c7":(635,305),"c8":(635,205),
                       "d1":(735,905),"d2":(735,805),"d3":(735,705),"d4":(735,605),"d5":(735,505),"d6":(735,405),"d7":(735,305),"d8":(735,205),
                       "e1":(835,905),"e2":(835,805),"e3":(835,705),"e4":(835,605),"e5":(835,505),"e6":(835,405),"e7":(835,305),"e8":(835,205),
                       "f1":(935,905),"f2":(935,805),"f3":(935,705),"f4":(935,605),"f5":(935,505),"f6":(935,405),"f7":(935,305),"f8":(935,205),
                       "g1":(1035,905),"g2":(1035,805),"g3":(1035,705),"g4":(1035,605),"g5":(1035,505),"g6":(1035,405),"g7":(1035,305),"g8":(1035,205),
                       "h1":(1135,905),"h2":(1135,805),"h3":(1135,705),"h4":(1135,605),"h5":(1135,505),"h6":(1135,405),"h7":(1135,305),"h8":(1135,205),
                      }
    else:
        coordinates = {"a1":(275,905),"a2":(275,805),"a3":(275,705),"a4":(275,605),"a5":(275,505),"a6":(275,405),"a7":(275,305),"a8":(275,205),
                       "b1":(375,905),"b2":(375,805),"b3":(375,705),"b4":(375,605),"b5":(375,505),"b6":(375,405),"b7":(375,305),"b8":(375,205),
                       "c1":(475,905),"c2":(475,805),"c3":(475,705),"c4":(475,605),"c5":(475,505),"c6":(475,405),"c7":(475,305),"c8":(475,205),
                       "d1":(575,905),"d2":(575,805),"d3":(575,705),"d4":(575,605),"d5":(575,505),"d6":(575,405),"d7":(575,305),"d8":(575,205),
                       "e1":(675,905),"e2":(675,805),"e3":(675,705),"e4":(675,605),"e5":(675,505),"e6":(675,405),"e7":(675,305),"e8":(675,205),
                       "f1":(775,905),"f2":(775,805),"f3":(775,705),"f4":(775,605),"f5":(775,505),"f6":(775,405),"f7":(775,305),"f8":(775,205),
                       "g1":(875,905),"g2":(875,805),"g3":(875,705),"g4":(875,605),"g5":(875,505),"g6":(875,405),"g7":(875,305),"g8":(875,205),
                       "h1":(975,905),"h2":(975,805),"h3":(975,705),"h4":(975,605),"h5":(975,505),"h6":(975,405),"h7":(975,305),"h8":(975,205),
}
    first_mouse = move_str[:2]
    last_mouse = move_str[2:]
    first_m_coords = coordinates[first_mouse]
    last_m_coords = coordinates[last_mouse]
    print(first_m_coords,last_m_coords)
    pyautogui.moveTo(first_m_coords)
    sleep(1)
    pyautogui.dragTo(last_m_coords,button="left")

running = True
selected_square = None
flipped = True
counter = 0

while running and not autoplay_online_bool:
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
                if board.piece_at(selected_square) and board.piece_at(selected_square).piece_type == chess.PAWN:
                    if chess.square_rank(square) == 7 or chess.square_rank(square) == 0:
                        move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                    else:
                        move = chess.Move(selected_square, square)
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
        elif event.type == pygame.KEYDOWN and not autoplay_bool:
            if event.key == pygame.K_SPACE:
                if counter % 2 != 0:
                    best_move = get_best_move()
                    print(f"ai chose: {best_move}")
                else:
                    print("its white's turn")
            elif event.key == pygame.K_d:
                autoplay_bool = not autoplay_bool
                if autoplay_bool:
                    print("autoplay on")
                else:
                    print("autoplay off")
        if autoplay_bool:
            if counter % 2 != 0:
                counter += 1
                best_move = get_best_move()
                print(best_move)
                board.push(best_move)
                flipped = not flipped

while running and autoplay_online_bool:
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
                if board.piece_at(selected_square) and board.piece_at(selected_square).piece_type == chess.PAWN:
                    if chess.square_rank(square) == 7 or chess.square_rank(square) == 0:
                        move = chess.Move(selected_square, square, promotion=chess.QUEEN)
                    else:
                        move = chess.Move(selected_square, square)
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
        elif event.type == pygame.KEYDOWN and not autoplay_bool:
            if event.key == pygame.K_SPACE:
                if counter % 2 != 0:
                    best_move = get_best_move()
                    print(f"ai chose: {best_move}")
                    board.push(best_move)
                    sleep(1)
                    autoplay_online(best_move,analysis)
                    flipped = not flipped
                    counter += 1
                else:
                    print("its white's turn")
        if autoplay_bool:
            if counter % 2 != 0:
                counter += 1
                best_move = get_best_move()
                print(best_move)
                sleep(1)
                board.push(best_move)
                flipped = not flipped
                sleep(1)
                autoplay_online(best_move,analysis)

pygame.quit()
