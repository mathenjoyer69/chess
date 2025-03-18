from time import sleep
import pygame
import chess
import pyautogui
import tkinter as tk
import random


def on_close():
    global autoplay_online_bool, analysis, autoplay_bool, custom_board_bool,bot_vs_bot,player_color
    autoplay_online_bool = autoplay_online_bool.get()
    analysis = analysis.get()
    autoplay_bool = autoplay_bool.get()
    custom_board_bool = custom_board_bool.get()
    bot_vs_bot = bot_vs_bot.get()
    player_color = player_color.get()
    root.destroy()

root = tk.Tk()

autoplay_online_bool = tk.BooleanVar(value=False)
analysis = tk.BooleanVar(value=False)
autoplay_bool = tk.BooleanVar(value=False)
custom_board_bool = tk.BooleanVar(value=False)
bot_vs_bot = tk.BooleanVar(value=False)
player_color = tk.BooleanVar(value=False)

player_color_label = tk.Label(root,text="check this to be the white pieces")
player_color_label.pack()
check_player_color = tk.Checkbutton(root,text="color",variable=player_color)
check_player_color.pack(pady=5)

autoplay_online_label = tk.Label(root, text="enable bot to move pieces on chess.com")
autoplay_online_label.pack()
check_autoplay_online = tk.Checkbutton(root, text="Autoplay Online", variable=autoplay_online_bool)
check_autoplay_online.pack(pady=5)

analysis_label = tk.Label(root, text="makes the bot play in the analysis mode of chess.com")
analysis_label.pack()
check_analysis = tk.Checkbutton(root, text="Analysis", variable=analysis)
check_analysis.pack(pady=5)

autoplay_label = tk.Label(root, text="the bot will play on the pygame screen automatically")
autoplay_label.pack()
check_autoplay = tk.Checkbutton(root, text="Autoplay", variable=autoplay_bool)
check_autoplay.pack(pady=5)

custom_board_label = tk.Label(root, text="click this to create a custom board")
custom_board_label.pack()
check_custom_board = tk.Checkbutton(root, text="custom Board", variable=custom_board_bool)
check_custom_board.pack(pady=5)

bot_vs_bot_label = tk.Label(root,text="click this if you want the bot to play against it self(it doesnt work yet)")
bot_vs_bot_label.pack()
check_bot_vs_bot = tk.Checkbutton(root,text="bot vs bot",variable=bot_vs_bot)
check_bot_vs_bot.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

print(autoplay_online_bool,autoplay_bool,analysis,custom_board_bool,bot_vs_bot)
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

board = chess.Board() if not custom_board_bool else chess.Board(None)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess")


def evaluate_board(board):
    piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 10000}

    pawn_table = [
        0,  5,  10, 15,  15, 10, 5,  0,
        0,  10, 20, 25,  25, 20, 10, 0,
        0,  5,  10, 20,  20, 10, 5,  0,
        5,  5,  10, 15,  15, 10, 5,  5,
        5,  0,  5,  10,  10, 5,  0,  5,
        0,  0,  0,  -5,  -5, 0,  0,  0,
        0,  0,  0,  5,   5,  0,  0,  0,
        0,  0,  0,  0,   0,  0,  0,  0,
    ]

    knight_table = [
        -50, -40, -30, -30, -30, -30,-40, -50,
        -40, -20, -5,  -5,  -5,  -5, -20, -40,
        -30,  5,  10,  15,  15,  10,  5,  -30,
        -30,  0,  15,  20,  20,  15,  0,  -30,
        -30,  5,  15,  20,  20,  15,  5,  -30,
        -30,  0,  10,  15,  15,  10,  0,  -30,
        -40, -20,  5,   5,   5,   5, -20, -40,
        -50, -40, -30, -30, -30, -30,-40, -50,
    ]

    bishop_table = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,  5,   0,   0,   0,   0,   5,  -10,
        -10,  0,   5,   5,   5,   5,   0,  -10,
        -10,  0,   5,  10,  10,   5,   0,  -10,
        -10,  0,   5,  10,  10,   5,   0,  -10,
        -10,  0,   5,   5,   5,   5,   0,  -10,
        -10,  7,   0,   0,   0,   0,   7,  -10,
        -20, -10, -10, -10, -10, -10, -10, -20,
    ]

    rook_table = [
        0,  5,  10, 10, 10, 10,  5,  0,
        5,  5,  10, 10, 10, 10,  5,  5,
        10, 10, 20, 20, 20, 20, 10, 10,
        10, 10, 20, 20, 20, 20, 10, 10,
        10, 10, 20, 20, 20, 20, 10, 10,
        5,  5,  10, 10, 10, 10,  5,  5,
        0,  5,  10, 10, 10, 10,  5,  0,
        0,  0,  5,  5,  5,  5,   0,  0,
    ]

    queen_table = [
        -20, -10, -5,   0,  0, -5, -10, -20,
        -10,  0,   5,   5,  5,  5,  0,  -10,
        -5,   5,  10,  10, 10, 10,  5,  -5,
         0,   5,  10,  15, 15, 10,  5,   0,
         0,   5,  10,  15, 15, 10,  5,   0,
        -5,   5,  10,  10, 10, 10,  5,  -5,
        -10,  0,   5,   5,  5,  5,  0,  -10,
        -20, -10, -5,   0,  0, -5, -10, -20,
    ]

    king_table = [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -30, -30, -20, -20, -10,
         0,  -10, -10, -20, -20, -10, -10,  0,
         20,  20,  10,  0,   0,   10,  20,  20,
    ]

    value = 0
    for square in chess.SQUARES:
        piece1 = board.piece_at(square)
        if piece1:
            if piece1.color == chess.WHITE:
                value += piece_values[piece1.piece_type]

                if piece1.piece_type == chess.PAWN:
                    value += pawn_table[square]
                elif piece1.piece_type == chess.KNIGHT:
                    value += knight_table[square]
                elif piece1.piece_type == chess.BISHOP:
                    value += bishop_table[square]
                elif piece1.piece_type == chess.ROOK:
                    value += rook_table[square]
                elif piece1.piece_type == chess.QUEEN:
                    value += queen_table[square]
                elif piece1.piece_type == chess.KING:
                    value += king_table[square]

            if piece1.color == chess.BLACK:
                value -= piece_values[piece1.piece_type]

                if piece1.piece_type == chess.PAWN:
                    value -= pawn_table[chess.square_mirror(square)]
                if piece1.piece_type == chess.KNIGHT:
                    value -= knight_table[chess.square_mirror(square)]
                if piece1.piece_type == chess.BISHOP:
                    value -= bishop_table[chess.square_mirror(square)]
                if piece1.piece_type == chess.ROOK:
                    value -= rook_table[chess.square_mirror(square)]
                if piece1.piece_type == chess.QUEEN:
                    value -= queen_table[chess.square_mirror(square)]
                if piece1.piece_type == chess.KING:
                    value -= king_table[chess.square_mirror(square)]

    #value += 10 * (len(list(board.legal_moves)) if board.turn == chess.WHITE else -len(list(board.legal_moves)))

    if board.is_checkmate():
        return float('inf') if board.turn == chess.WHITE else float('-inf')

    return value


def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, False)
            if board.is_checkmate():
                board.pop()
                return max_eval,best_move
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 1, alpha, beta, True)
            if board.is_checkmate():
                board.pop()
                return min_eval,best_move
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def get_best_move(board):
    num_of_good_pieces = 0
    depth = 4
    for square in chess.SQUARES:
        if board.piece_at(square) != chess.PAWN and board.piece_at(square) != None and board.piece_at(square) != "K":
            print(board.piece_at(square))
            num_of_good_pieces += 1
    if num_of_good_pieces < 5:
        depth = 5
    if num_of_good_pieces < 4:
        depth = 6
    print("depth",depth)
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), board.turn)
    print(_)
    if best_move:
        return best_move
    else:
        if board.legal_moves:
            return random.choice(list(board.legal_moves))
        else:
            print("no legal moves")

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
    first_m_coordinates = coordinates[first_mouse]
    last_m_coordinates = coordinates[last_mouse]
    print(first_m_coordinates,last_m_coordinates)
    pyautogui.moveTo(first_m_coordinates)
    sleep(0.5)
    pyautogui.dragTo(last_m_coordinates,button="left")

running = True
selected_square = None
flipped = True

counter = 0
moves_played = []

while running and custom_board_bool:
    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_from_pos(pygame.mouse.get_pos(), flipped)
            selected_square = chess.square(col, row)
        elif event.type == pygame.KEYDOWN:
            if selected_square is not None:
                is_shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
                piece_color = chess.BLACK if is_shift_pressed else chess.WHITE
                if event.key == pygame.K_p:
                    board.set_piece_at(selected_square, chess.Piece(chess.PAWN, piece_color))
                elif event.key == pygame.K_r:
                    board.set_piece_at(selected_square, chess.Piece(chess.ROOK, piece_color))
                elif event.key == pygame.K_n:
                    board.set_piece_at(selected_square, chess.Piece(chess.KNIGHT, piece_color))
                elif event.key == pygame.K_b:
                    board.set_piece_at(selected_square, chess.Piece(chess.BISHOP, piece_color))
                elif event.key == pygame.K_q:
                    board.set_piece_at(selected_square, chess.Piece(chess.QUEEN, piece_color))
                elif event.key == pygame.K_k:
                    board.set_piece_at(selected_square, chess.Piece(chess.KING, piece_color))
                elif event.key == pygame.K_BACKSPACE:
                    board.remove_piece_at(selected_square)
                elif event.key == pygame.K_SPACE:
                    custom_board_bool = False
            else:
                print("select a square first😡")
while running and not autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
    keys = pygame.key.get_pressed()
    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()

    if not board.legal_moves:
        running = False
        if not board.is_check():
            print("draw")
            break
        if counter % 2 == 0:
            print("black won")
            break
        else:
            print("white won")
            break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_from_pos(pygame.mouse.get_pos(), flipped)
            square = chess.square(col, row)
            print(square)
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
                    moves_played.append(move)
                    print(move)
                    flipped = not flipped
                    counter += 1
                else:
                    print("illegal move")
                selected_square = None
            print(f"you clicked {board.piece_at(square)}")
        elif event.type == pygame.KEYDOWN and not autoplay_bool:
            if event.key == pygame.K_SPACE:
                if counter % 2 != 0:
                    best_move = get_best_move(board)
                    print(f"ai chose: {best_move}")
                else:
                    print("its white's turn")
            elif event.key == pygame.K_d:
                autoplay_bool = not autoplay_bool
                print("autoplay on")
            elif event.key == pygame.K_a:
                autoplay_online_bool = not autoplay_online_bool
                autoplay_bool = True
                print("autoplay online on")
        if autoplay_bool:
            if counter % 2 != 0:
                best_move = get_best_move(board)
                print(best_move)
                if board.legal_moves:
                    counter += 1
                    board.push(best_move)
                    moves_played.append(best_move)
                flipped = not flipped
if running and autoplay_online_bool:
    flipped = True
while running and autoplay_online_bool and not custom_board_bool and not bot_vs_bot:
    if moves_played:
        for i in moves_played:
            autoplay_online(i,analysis)
            sleep(1)
    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()

    if not board.legal_moves:
        running = False
        if not board.is_check():
            print("draw")
            break
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
                    autoplay_online(move,analysis)
                    counter += 1
                else:
                    print("illegal move")
                selected_square = None
            print(f"you clicked {board.piece_at(square)}")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if counter % 2 != 0:
                    best_move = get_best_move(board)
                    print(f"ai chose: {best_move}")
                    board.push(best_move)
                    sleep(1)
                    autoplay_online(best_move,analysis)
                    counter += 1
                else:
                    print("its white's turn")
                    best_move = get_best_move(board)
                    board.push(best_move)
                    sleep(1)
                    autoplay_online(best_move, analysis)

        if autoplay_bool:
            if counter % 2 != 0:
                counter += 1
                best_move = get_best_move(board)
                print(best_move)
                sleep(1)
                board.push(best_move)
                sleep(1)
                autoplay_online(best_move,analysis)
play = True
square_to_number = {"a1":0,"a2":8,"a3":16,"a4":24,"a5":32,"a6":40,"a7":48,"a8":56,
                    "b1":1,"b2":9,"b3":17,"b4":25,"b5":33,"b6":41,"b7":49,"b8":57,
                    "c1":2,"c2":10,"c3":18,"c4":26,"c5":34,"c6":42,"c7":50,"c8":58,
                    "d1":3,"d2":11,"d3":19,"d4":27,"d5":35,"d6":43,"d7":51,"d8":59,
                    "e1":4,"e2":12,"e3":20,"e4":28,"e5":36,"e6":44,"e7":52,"e8":60,
                    "f1":5,"f2":13,"f3":21,"f4":29,"f5":37,"f6":45,"f7":53,"f8":61,
                    "g1":6,"g2":14,"g3":22,"g4":30,"g5":38,"g6":46,"g7":54,"g8":62,
                    "h1":7,"h2":15,"h3":23,"h4":31,"h5":39,"h6":47,"h7":55,"h8":63}
moves = []
bot_counter = 0
if autoplay_online_bool:
    sleep(3)
while running and bot_vs_bot:
    k_in_a_row = 0
    draw_board(flipped)
    draw_pieces(flipped)
    pygame.display.flip()

    if board.is_checkmate():
        if counter % 2 == 0:
            print("black won")
        else:
            print("white won")
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play

    if play:
        best_move = get_best_move(board)
        move_str = str(best_move)
        move_1,move_2 = move_str[:2],move_str[2:]
        move_1_n,move_2_n = square_to_number[move_1],square_to_number[move_2]
        moves.append([move_1_n,move_2_n,move_str])
        if not autoplay_bool:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        board.push(best_move)
                        print(best_move)
        else:
            board.push(best_move)
            print(best_move)
        sleep(0.1)
        moves_played.append(best_move)
        if autoplay_online_bool:
            autoplay_online(best_move,analysis)
print(moves)
pygame.quit()
