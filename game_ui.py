import pygame
import time
from board import board, captured_pieces, excluded_pieces, can_drop, can_setdrop
from piece import Piece

pygame.init()

# 画面の大きさ
WIDTH = 800
HEIGHT = 750
# 画面の大きさを指定して画面を作成
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# タイトルを指定
pygame.display.set_caption("軍議")

# フォントの設定
fontBold = "Noto_Sans_JP/static/NotoSansJP-Bold.ttf"
fontTama = "玉ねぎ楷書「激」無料版v7\玉ねぎ楷書激無料版v7改.ttf"

# 色の設定
WHITE = (255, 255, 255) # 白
BLACK = (0, 0, 0) # 黒
LIGHT_GREEN = (144, 238, 144) # 黄緑色
RED = (255, 0, 0) # 赤

# マス目の大きさ
SIZE = 55

# マス目の色
BOARD_COLOR = (255, 220, 150)
LINE_COLOR = (0, 0, 0)  # 線の色

# 持ち駒エリアの色
CAPTURED_AREA_COLOR = (200, 200, 200)

# 将棋盤のサイズ
BOARD_SIZE = SIZE * 9

# 将棋盤の左上の位置
BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2

# 初期配置を選択
def select_setup():
    # スタート画面の背景
    image = pygame.image.load("image\First_screen.jpg")
    scaled_image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(scaled_image, (0, 0))
    # タイトル
    font = pygame.font.Font(fontTama, 200)
    # 黒い縁取りを描画
    for offset_x, offset_y in [(-10, 0), (10, 0), (0, -10), (0, 10)]:  # 上下左右に少しずらして描画
        text_outline = font.render("軍議", True, BLACK)
        text_rect_outline = text_outline.get_rect(center=(WIDTH // 2, BOARD_Y // 2 + 100))
    screen.blit(text_outline, (text_rect_outline.x + offset_x, text_rect_outline.y + offset_y))

    text = font.render("軍議", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, BOARD_Y // 2 + 100))
    screen.blit(text, text_rect)

    font = pygame.font.Font(fontBold, 36)
    text = font.render("初期配置を選んでください", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 20), 2)  # 黒い枠を追加
    screen.blit(text, text_rect)

    # 1ボタン
    yes_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 50, 120, 50)
    pygame.draw.rect(screen, WHITE, yes_button)
    pygame.draw.rect(screen, BLACK, yes_button, 2)
    yes_text = font.render("初級", True, (0, 0, 0))
    yes_text_rect = yes_text.get_rect(center=yes_button.center)
    screen.blit(yes_text, yes_text_rect)

    # 2ボタン
    no_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 120, 120, 50)
    pygame.draw.rect(screen, WHITE, no_button)
    pygame.draw.rect(screen, BLACK, no_button, 2)
    no_text = font.render("中級", True, (0, 0, 0))
    no_text_rect = no_text.get_rect(center=no_button.center)
    screen.blit(no_text, no_text_rect)

    # 3ボタン
    third_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 190, 120, 50)
    pygame.draw.rect(screen, WHITE, third_button)
    pygame.draw.rect(screen, BLACK, third_button, 2)
    third_text = font.render("上級", True, (0, 0, 0))
    third_text_rect = third_text.get_rect(center=third_button.center)
    screen.blit(third_text, third_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return 1
                elif no_button.collidepoint(event.pos):
                    return 2
                elif third_button.collidepoint(event.pos):
                    return 3






# 盤面の描画
def draw_board():
    for y in range(9):
        for x in range(9):
            rect = pygame.Rect(BOARD_X + x * SIZE, BOARD_Y + y * SIZE, SIZE, SIZE)
            pygame.draw.rect(screen, BOARD_COLOR, rect)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)
    # 線を描画
    for i in range(10):
        pygame.draw.line(screen, LINE_COLOR, (BOARD_X + i * SIZE, BOARD_Y), (BOARD_X + i * SIZE, BOARD_Y + BOARD_SIZE), 2)
        pygame.draw.line(screen, LINE_COLOR, (BOARD_X, BOARD_Y + i * SIZE), (BOARD_X + BOARD_SIZE, BOARD_Y + i * SIZE), 2)



# 数字と漢数字のリスト
NUMBERS = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
ARABIC_NUMBERS = ["9", "8", "7", "6", "5", "4", "3", "2", "1"]
# 数字と漢数字の描画
def draw_labels():
    font = pygame.font.Font(fontBold, 20)
    # 上側の数字（逆順）
    for i, num in enumerate(ARABIC_NUMBERS):
        text = font.render(num, True, WHITE)
        screen.blit(text, (BOARD_X + i * SIZE + SIZE // 2 - text.get_width() // 2, BOARD_Y - SIZE // 2 - text.get_height() // 2 + 15))
    # 右側の漢数字（そのまま）
    for i, num in enumerate(NUMBERS):
        text = font.render(num, True, WHITE)
        screen.blit(text, (BOARD_X + BOARD_SIZE + SIZE // 2 - text.get_width() // 2 - 15, BOARD_Y + i * SIZE + SIZE // 2 - text.get_height() // 2))

# 画像を読み込む
def load_piece_image(path, size):
    try:
        return pygame.transform.scale(pygame.image.load(path), (size, size))
    except FileNotFoundError:
        print(f"Error: File not found - {path}")
        # 画像が見つからない場合はデフォルトの色付き矩形を返す
        surface = pygame.Surface((size, size))
        surface.fill((255, 0, 0))  # 赤色で代替
        return surface

# 黒駒の画像を読み込む
black_piece_images = {
    "師": load_piece_image("image/piece/Black_Sui.png", SIZE),
    "大": load_piece_image("image/piece/Black_Taisyo.png", SIZE),
    "中": load_piece_image("image/piece/Black_Chujo.png", SIZE),
    "小": load_piece_image("image/piece/Black_Shosho.png", SIZE),
    "侍": load_piece_image("image/piece/Black_Samurai.png", SIZE),
    "槍": load_piece_image("image/piece/Black_Yari.png", SIZE),
    "馬": load_piece_image("image/piece/Black_Kiba.png", SIZE),
    "忍": load_piece_image("image/piece/Black_Shinobi.png", SIZE),
    "砦": load_piece_image("image/piece/Black_Toride.png", SIZE),
    "兵": load_piece_image("image/piece/Black_Hyo.png", SIZE),
    "砲": load_piece_image("image/piece/Black_Odutu.png", SIZE),
    "弓": load_piece_image("image/piece/Black_Yumi.png", SIZE),
    "筒": load_piece_image("image/piece/Black_Tutu.png", SIZE),
    "謀": load_piece_image("image/piece/Black_Bosho.png", SIZE),
}

# 白駒の画像を読み込む
white_piece_images = {
    "師": load_piece_image("image/piece/White_Sui.png", SIZE),
    "大": load_piece_image("image/piece/White_Taisyo.png", SIZE),
    "中": load_piece_image("image/piece/White_Chujo.png", SIZE),
    "小": load_piece_image("image/piece/White_Shosho.png", SIZE),
    "侍": load_piece_image("image/piece/White_Samurai.png", SIZE),
    "槍": load_piece_image("image/piece/White_Yari.png", SIZE),
    "馬": load_piece_image("image/piece/White_Kiba.png", SIZE),
    "忍": load_piece_image("image/piece/White_Shinobi.png", SIZE),
    "砦": load_piece_image("image/piece/White_Toride.png", SIZE),
    "兵": load_piece_image("image/piece/White_Hyo.png", SIZE),
    "砲": load_piece_image("image/piece/White_Odutu.png", SIZE),
    "弓": load_piece_image("image/piece/White_Yumi.png", SIZE),
    "筒": load_piece_image("image/piece/White_Tutu.png", SIZE),
    "謀": load_piece_image("image/piece/White_Bosho.png", SIZE),
}

# ターンを表示する関数
def draw_turn(current_turn, sent_text, gote_text):
    font = pygame.font.Font(fontBold, 20)
    text = font.render("あなたの番です", True, RED)
    if current_turn == 0:
        screen.blit(text, (15 + sent_text.get_width() + 10, HEIGHT - SIZE - 45))
    else:
        screen.blit(text, (15 + gote_text.get_width() + 10, 15))

# 移動可能なマスを描画する関数
def draw_possible_moves(board, piece, x, y, z):
    for i in range(len(board[0])):
        for j in range(len(board)):
            for k in range(len(board[0][0])):
                if piece.can_move(board, i, j, k) and (i, j) != (x, y):
                    rect = pygame.Rect(BOARD_X + i * SIZE, BOARD_Y + j * SIZE, SIZE, SIZE)
                    pygame.draw.rect(screen, LIGHT_GREEN, rect)
                    # 線を再描画
                    pygame.draw.rect(screen, LINE_COLOR, rect, 1)

# 持ち駒を置くことが可能なマスを描画する関数
def draw_possible_drop_positions(board, piece, current_turn):
    for z in range(2):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_drop(board, piece, x, y, z, current_turn):
                    rect = pygame.Rect(BOARD_X + x * SIZE, BOARD_Y + y * SIZE, SIZE, SIZE)
                    pygame.draw.rect(screen, LIGHT_GREEN, rect)
                    # 線を再描画
                    pygame.draw.rect(screen, LINE_COLOR, rect, 1)

# セットアップ持ち駒を置くことが可能なマスを描画する関数
def draw_possible_setdrop_positions(board, piece, current_turn):
    for z in range(2):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_setdrop(board, piece, x, y, z, current_turn):
                    rect = pygame.Rect(BOARD_X + x * SIZE, BOARD_Y + y * SIZE, SIZE, SIZE)
                    pygame.draw.rect(screen, LIGHT_GREEN, rect)
                    # 線を再描画
                    pygame.draw.rect(screen, LINE_COLOR, rect, 1)


# 選択された駒を強調表示する関数
def draw_selected_piece(x, y):
    rect = pygame.Rect(BOARD_X + x * SIZE, BOARD_Y + y * SIZE, SIZE, SIZE)
    pygame.draw.rect(screen, RED, rect, 5)

# 選択された持ち駒を強調表示する関数
def draw_selected_captured_piece(x, y):
    rect = pygame.Rect(x, y, SIZE, SIZE)
    pygame.draw.rect(screen, RED, rect, 5)

# 持ち駒のページ位置
captured_pages = [0, 0]  # [先手, 後手]

# 除外エリアのページ位置
excluded_pages = [0, 0]  # [先手, 後手]

# ページボタンの描画
def draw_page_buttons():
    font = pygame.font.Font(fontBold, 30)
    # 先手のページボタン右（持ち駒）
    if (captured_pages[0] + 1) * 13 < len(captured_pieces[0]):
        right_button = font.render("➡", True, BLACK)
        screen.blit(right_button, (WIDTH - 40, HEIGHT - SIZE - 50))
    if captured_pages[0] > 0:
        left_button = font.render("⬅", True, BLACK)
        screen.blit(left_button, (WIDTH - 80, HEIGHT - SIZE - 50))
    # 後手のページボタン右
    if (captured_pages[1] + 1) * 13 < len(captured_pieces[1]):
        right_button = font.render("➡", True, BLACK)
        screen.blit(right_button, (WIDTH - 40, 10))
    if captured_pages[1] > 0:
        left_button = font.render("⬅", True, BLACK)
        screen.blit(left_button, (WIDTH - 80, 10))

    # 先手のページボタン（下）（除外駒）
    if excluded_pages[0] > 0:
        up_button = font.render("⬆", True, BLACK)
        screen.blit(up_button, (10 + SIZE, BOARD_Y + BOARD_SIZE - 80))
    if (excluded_pages[0] + 1) * 8 < len(excluded_pieces[0]):
        down_button = font.render("⬇", True, BLACK)
        screen.blit(down_button, (10 + SIZE, BOARD_Y + BOARD_SIZE - 40))
    # 後手のページボタン（下）
    if excluded_pages[1] > 0:
        up_button = font.render("⬆", True, BLACK)
        screen.blit(up_button, (WIDTH - SIZE - 50 + SIZE, BOARD_Y + BOARD_SIZE - 80))
    if (excluded_pages[1] + 1) * 8 < len(excluded_pieces[1]):
        down_button = font.render("⬇", True, BLACK)
        screen.blit(down_button, (WIDTH - SIZE - 50 + SIZE, BOARD_Y + BOARD_SIZE - 40))

# ページイベントの処理
def handle_page_events(event):
    global captured_pages
    global excluded_pages
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        # 先手のページボタンがクリックされた場合（持ち駒）
        if WIDTH - 40 <= x <= WIDTH - 10 and HEIGHT - SIZE - 50 <= y <= HEIGHT - SIZE - 20:
            if (captured_pages[0] + 1) * 13 < len(captured_pieces[0]):  # 次のページが存在する場合のみ
                captured_pages[0] += 1
        elif WIDTH - 80 <= x <= WIDTH - 50 and HEIGHT - SIZE - 50 <= y <= HEIGHT - SIZE - 20:
            if captured_pages[0] > 0:  # 前のページが存在する場合のみ
                captured_pages[0] -= 1
        # 後手のページボタンがクリックされた場合
        if WIDTH - 40 <= x <= WIDTH - 10 and 10 <= y <= 40:
            if (captured_pages[1] + 1) * 13 < len(captured_pieces[1]):  # 次のページが存在する場合のみ
                captured_pages[1] += 1
        elif WIDTH - 80 <= x <= WIDTH - 50 and 10 <= y <= 40:
            if captured_pages[1] > 0:  # 前のページが存在する場合のみ
                captured_pages[1] -= 1
        
        # 先手のページボタンがクリックされた場合（除外エリア）
        if 10 + SIZE <= x <= 10 + SIZE + 30 and BOARD_Y + BOARD_SIZE - 80 <= y <= BOARD_Y + BOARD_SIZE - 50:
            if excluded_pages[0] > 0:  # 前のページが存在する場合のみ
                excluded_pages[0] -= 1
        elif 10 + SIZE <= x <= 10 + SIZE + 30 and BOARD_Y + BOARD_SIZE - 40 <= y <= BOARD_Y + BOARD_SIZE - 10:
            if (excluded_pages[0] + 1) * 8 < len(excluded_pieces[0]):  # 次のページが存在する場合のみ
                excluded_pages[0] += 1
        # 後手のページボタンがクリックされた場合
        if WIDTH - SIZE - 50 + SIZE <= x <= WIDTH - SIZE - 50 + SIZE + 30 and BOARD_Y + BOARD_SIZE - 80 <= y <= BOARD_Y + BOARD_SIZE - 50:
            if excluded_pages[1] > 0:  # 前のページが存在する場合のみ
                excluded_pages[1] -= 1
        elif WIDTH - SIZE - 50 + SIZE <= x <= WIDTH - SIZE - 50 + SIZE + 30 and BOARD_Y + BOARD_SIZE - 40 <= y <= BOARD_Y + BOARD_SIZE - 10:
            if (excluded_pages[1] + 1) * 8 < len(excluded_pieces[1]):  # 次のページが存在する場合のみ
                excluded_pages[1] += 1
        
        

# 駒の描画
def draw_pieces():
    for y in range(9):
        for x in range(9):
            for z in range(3):
                piece = board[y][x][z]
                if piece is not None:
                    if piece.owner == 0:
                        match z:
                            case 0:
                                screen.blit(white_piece_images[piece.name], (BOARD_X + x * SIZE, BOARD_Y + y * SIZE))
                            case 1:
                                screen.blit(white_piece_images[piece.name], (BOARD_X + x * SIZE - 5, BOARD_Y + y * SIZE - 5))
                            case 2:
                                screen.blit(white_piece_images[piece.name], (BOARD_X + x * SIZE - 10, BOARD_Y + y * SIZE - 10))
                    else:
                        match z:
                            case 0:
                                screen.blit(black_piece_images[piece.name], (BOARD_X + x * SIZE, BOARD_Y + y * SIZE))
                            case 1:
                                screen.blit(black_piece_images[piece.name], (BOARD_X + x * SIZE - 5, BOARD_Y + y * SIZE - 5))
                            case 2:
                                screen.blit(black_piece_images[piece.name], (BOARD_X + x * SIZE - 10, BOARD_Y + y * SIZE - 10))



# 持ち駒の描画（ページ対応）
def draw_captured_pieces(current_turn):
    # 先手の持ち駒エリアを塗りつぶす
    pygame.draw.rect(screen, CAPTURED_AREA_COLOR, (10, HEIGHT - SIZE - 50, WIDTH - 20, SIZE + 40))
    # 後手の持ち駒エリアを塗りつぶす
    pygame.draw.rect(screen, CAPTURED_AREA_COLOR, (10, 10, WIDTH - 20, SIZE + 40))
    # 持ち駒エリアの左上に「持ち駒」という文字を表示
    font = pygame.font.Font(fontBold, 20)
    sente_text = font.render("先手の持ち駒", True, (0, 0, 0))
    gote_text = font.render("後手の持ち駒", True, (0, 0, 0))
    screen.blit(sente_text, (15, HEIGHT - SIZE - 45))
    screen.blit(gote_text, (15, 15))

    # ターン表示
    draw_turn(current_turn, sente_text, gote_text)

    # 先手の持ち駒を表示
    start_index = captured_pages[0] * 13
    for i, piece in enumerate(captured_pieces[0][start_index:start_index + 13]):
        x = 15 + i * (SIZE + 5)
        y = HEIGHT - SIZE - 20
        screen.blit(white_piece_images[piece.name], (x, y))
    # 後手の持ち駒を表示
    start_index = captured_pages[1] * 13
    for i, piece in enumerate(captured_pieces[1][start_index:start_index + 13]):
        x = 15 + i * (SIZE + 5)
        y = 40
        screen.blit(black_piece_images[piece.name], (x, y))
    # ページボタンの描画
    draw_page_buttons()


# 除外エリアの描画（ページ対応）
def draw_excluded_pieces():
    # 左側の除外エリアを塗りつぶす
    pygame.draw.rect(screen, CAPTURED_AREA_COLOR, (10, BOARD_Y, SIZE + 40, BOARD_SIZE))
    # 右側の除外エリアを塗りつぶす
    pygame.draw.rect(screen, CAPTURED_AREA_COLOR, (WIDTH - SIZE - 50, BOARD_Y, SIZE + 40, BOARD_SIZE))
    # 除外エリアの左上に「除外駒」という文字を表示
    font = pygame.font.Font(fontBold, 20)
    left_text = font.render("除外駒", True, (0, 0, 0))  # 先手の除外された駒
    right_text = font.render("除外駒", True, (0, 0, 0))  # 後手の除外された駒
    screen.blit(left_text, (15, BOARD_Y + 5))
    screen.blit(right_text, (WIDTH - SIZE - 45, BOARD_Y + 5))
    # 先手の除外された駒を表示
    start_index = excluded_pages[0] * 8
    for i, piece in enumerate(excluded_pieces[0][start_index:start_index + 8]):
        screen.blit(white_piece_images[piece.name], (15, BOARD_Y + 30 + i * SIZE))
    # 後手の除外された駒を表示
    start_index = excluded_pages[1] * 8
    for i, piece in enumerate(excluded_pieces[1][start_index:start_index + 8]):
        screen.blit(black_piece_images[piece.name], (WIDTH - SIZE - 45, BOARD_Y + 30 + i * SIZE))
    # ページボタンの描画
    draw_page_buttons()

# ツケるか取るかの選択
def stack_or_take_dialog():
    font = pygame.font.Font(fontBold, 36)
    text = font.render("ツケるか取るか", True, (255, 0, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 20), 2)  # 黒い枠を追加
    screen.blit(text, text_rect)
    # YESボタン
    yes_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 50, 120, 50)
    pygame.draw.rect(screen, WHITE, yes_button)
    pygame.draw.rect(screen, BLACK, yes_button, 2)
    yes_text = font.render("ツケる", True, (0, 0, 0))
    yes_text_rect = yes_text.get_rect(center=yes_button.center)
    screen.blit(yes_text, yes_text_rect)
    # NOボタン
    no_button = pygame.Rect(WIDTH // 2 + 40, HEIGHT // 2 + 50, 80, 50)
    pygame.draw.rect(screen, WHITE, no_button)
    pygame.draw.rect(screen, BLACK, no_button, 2)
    no_text = font.render("取る", True, (0, 0, 0))
    no_text_rect = no_text.get_rect(center=no_button.center)
    screen.blit(no_text, no_text_rect)
    # キャンセルボタン
    cancel_button = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 2 - text.get_height() // 2 - 40, 30, 32)
    pygame.draw.rect(screen, WHITE, cancel_button)
    pygame.draw.rect(screen, BLACK, cancel_button, 2)
    cancel_text = font.render("×", True, (0, 0, 0))
    cancel_text_rect = cancel_text.get_rect(center=cancel_button.center)
    screen.blit(cancel_text, cancel_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return "stack"
                elif no_button.collidepoint(event.pos):
                    return "take"
                elif cancel_button.collidepoint(event.pos):
                    return "cancel"

def swap_or_keep_dialog():
    font = pygame.font.Font(fontBold, 36)
    text = font.render("寝返りますか？", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, text_rect.inflate(20, 20), 2)
    screen.blit(text, text_rect)
    # YESボタン
    yes_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 50, 120, 50)
    pygame.draw.rect(screen, WHITE, yes_button)
    pygame.draw.rect(screen, BLACK, yes_button, 2)
    yes_text = font.render("寝返る", True, (0, 0, 0))
    yes_text_rect = yes_text.get_rect(center=yes_button.center)
    screen.blit(yes_text, yes_text_rect)
    # NOボタン
    no_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 50, 120, 50)
    pygame.draw.rect(screen, WHITE, no_button)
    pygame.draw.rect(screen, BLACK, no_button, 2)
    no_text = font.render("いいえ", True, (0, 0, 0))
    no_text_rect = no_text.get_rect(center=no_button.center)
    screen.blit(no_text, no_text_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return True
                elif no_button.collidepoint(event.pos):
                    return False

# 王手の表示
def show_checkmate_message():
    font = pygame.font.Font(fontTama, 300)
    text = font.render("大手", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(2)


def show_winer_message(current_turn):
    font = pygame.font.Font(fontTama, 150)
    winer_text = f"{'先手' if current_turn == 0 else '後手'}の勝利"
    text = font.render(winer_text, True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(5)


# セットアップ完了ボタン
def draw_setup_finish_button(current_turn):
    if current_turn == 0:
        # ボタンの位置とサイズ
        sente_button_center = (WIDTH - SIZE - 50 + SIZE // 2, BOARD_Y + BOARD_SIZE + 30)
        sente_button_radius = 25
        # 円形ボタンを描画
        pygame.draw.circle(screen, (0, 255, 0), sente_button_center, sente_button_radius)  # 緑色
        pygame.draw.circle(screen, (0, 0, 0), sente_button_center, sente_button_radius, 2)  # 黒い枠
        # ボタンのテキスト
        font = pygame.font.Font(fontBold, 20)
        text = font.render("完了", True, (0, 0, 0))
        sente_text_rect = text.get_rect(center=sente_button_center)
        screen.blit(text, sente_text_rect)
    else:
        gote_button_center = (WIDTH - SIZE - 50 + SIZE // 2, 120)
        gote_button_radius = 25
        pygame.draw.circle(screen, (0, 255, 0), gote_button_center, gote_button_radius)  # 緑色
        pygame.draw.circle(screen, (0, 0, 0), gote_button_center, gote_button_radius, 2)  # 黒い枠
        font = pygame.font.Font(fontBold, 20)
        text = font.render("完了", True, (0, 0, 0))
        gote_text_rect = text.get_rect(center=gote_button_center)
        screen.blit(text, gote_text_rect)
    


def handle_setup_finish_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos

    # 準備完了ボタンがクリックされた場合
    sente_button_center = (WIDTH - SIZE - 50 + SIZE // 2, BOARD_Y + BOARD_SIZE + 30)
    sente_button_radius = 25
    gote_button_center = (WIDTH - SIZE - 50 + SIZE // 2, 120)
    gote_button_radius = 25
    if (x - sente_button_center[0]) ** 2 + (y - sente_button_center[1]) ** 2 <= sente_button_radius ** 2:
        return True
    elif (x - gote_button_center[0]) ** 2 + (y - gote_button_center[1]) ** 2 <= gote_button_radius ** 2:
        return True

# 対局の表示
def show_start_message():
    font = pygame.font.Font(fontTama, 150)
    text = font.render("対局開始", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    # 白い縁取りを描画
    for offset_x, offset_y in [(-5, 0), (5, 0), (0, -5), (0, 5), (-5, -5), (-5, 5), (5, -5), (5, 5)]:
        text_outline = font.render("対局開始", True, WHITE)
        screen.blit(text_outline, (text_rect.x + offset_x, text_rect.y + offset_y))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(2)
