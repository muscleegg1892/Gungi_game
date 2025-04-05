import pygame
from game_ui import draw_board, draw_pieces, draw_labels, draw_captured_pieces, draw_excluded_pieces, handle_page_events, BOARD_X, BOARD_Y, SIZE, draw_possible_moves, captured_pages, excluded_pages, draw_selected_piece, draw_selected_captured_piece, draw_possible_drop_positions, show_checkmate_message, show_winer_message, select_setup, draw_possible_setdrop_positions, draw_setup_finish_button, handle_setup_finish_events, show_start_message
from board import board, setup1_pieces, setup2_pieces, setup3_pieces,  get_highest_z, captured_pieces, checkmate, check_winer
from player import move_piece, drop_piece, setdrop_piece

# Pygameの初期化
pygame.init()
pygame.mixer.init()
def BGM():
    # 音楽ファイルを読み込み
    BGM = pygame.mixer.music.load("sound\BGM.mp3")
    pygame.mixer.music.set_volume(0.5)
    # 音楽をループ再生（-1は無限ループ）
    pygame.mixer.music.play(-1)
def checkmate_BGM():
    # 音楽ファイルを読み込み
    BGM = pygame.mixer.music.load("sound\王手BGM.mp3")
    pygame.mixer.music.set_volume(0.5)
    # 音楽をループ再生（-1は無限ループ）
    pygame.mixer.music.play(-1)

# 効果音ファイル読み込み
click_sound = pygame.mixer.Sound("sound\決定ボタン.mp3")
play_sound = pygame.mixer.Sound("sound\「始め」.mp3")
drop_sound = pygame.mixer.Sound("sound\将棋・駒を強めに指す03.mp3")
end_sound = pygame.mixer.Sound("sound\end.mp3")
end_sound.set_volume(1)
checkmate_sound = pygame.mixer.Sound("sound\王手.wav")



# ウィンドウの設定
WIDTH = 800
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("軍議")

# 色の設定
WHITE = (255, 255, 255) # 白
BLACK = (0, 0, 0) # 黒


# メインプログラム
def main():
    print("軍議プログラム開始")
    BGM()
    now_BGM = 0
    # 駒の選択状態を管理する変数
    selected_piece = None
    selected_x, selected_y, selected_z = -1, -1, -1
    selected_captured_piece = None
    captured_x, captured_y = -1, -1
    current_turn = 0  # ターンの初期化
    

    # メインループ
    running = True

    # 初期配置を選択
    result = select_setup()
    if result is None:  
        running = False
    elif result == 1:
        setup1_pieces(board)
        click_sound.play()
    elif result == 2:
        setup2_pieces(board)
        click_sound.play()
    elif result == 3:
        setup3_pieces()
        click_sound.play()
        # セットアップループ
        setup = True
        end = True
        # 師を配置
        for i in range(2):
            if end == False:
                break
            king = True
            if i == 0:
                selected_captured_piece = captured_pieces[0][0]
                captured_x = 15
                captured_y = 675
            else:
                selected_captured_piece = captured_pieces[1][0]
                captured_x = 15
                captured_y = 40
            while king:
                # 画面を黒で塗りつぶす
                screen.fill(BLACK)
                # 盤面の描画
                draw_board()
                # 数字と漢数字の描画
                draw_labels()
                # 持ち駒の描画
                draw_captured_pieces(current_turn)
                # 移動可能なマスを描画
                if selected_captured_piece is not None:
                    draw_possible_setdrop_positions(board, selected_captured_piece, current_turn)
                    # 選択した持ち駒を強調表示
                    draw_selected_captured_piece(captured_x, captured_y)
                # 駒の描画
                draw_pieces()
                # 除外駒の描画
                draw_excluded_pieces()
                # 画面を更新
                pygame.display.update()

                # イベント処理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        setup = False
                        king = False
                        end = False
                    # 持ち駒と除外駒のページ切り替え
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        handle_page_events(event)

                        x, y = event.pos
                        board_x = (x - BOARD_X) // SIZE
                        board_y = (y - BOARD_Y) // SIZE

                        # 範囲チェックを追加
                        if 0 <= board_x < len(board[0]) and 0 <= board_y < len(board):
                            board_z = get_highest_z(board, board_x, board_y)
                            
                            if selected_captured_piece is not None:
                                # 持ち駒を置く
                                result, current_turn = setdrop_piece(board, selected_captured_piece, board_x, board_y, board_z, current_turn)
                                if result == True:
                                    drop_sound.play()
                                    # 画面を黒で塗りつぶす
                                    screen.fill(BLACK)
                                    # 盤面の描画
                                    draw_board()
                                    # 数字と漢数字の描画
                                    draw_labels()
                                    # 移動可能なマスを描画
                                    draw_possible_setdrop_positions(board, selected_captured_piece, current_turn)
                                    # 持ち駒の描画
                                    draw_captured_pieces(current_turn)
                                    # 選択した持ち駒を強調表示
                                    draw_selected_captured_piece(captured_x, captured_y)
                                    # 駒の描画
                                    draw_pieces()
                                    # 除外駒の描画
                                    draw_excluded_pieces()
                                    # 画面を更新
                                    pygame.display.update()
                                    king = False
                                    selected_captured_piece = None
                                    captured_x, captured_y = -1, -1

        # 師以外を配置
        setup_complete = 0
        while setup:
            # 画面を黒で塗りつぶす
            screen.fill(BLACK)
            # 盤面の描画
            draw_board()
            # 数字と漢数字の描画
            draw_labels()
            # 持ち駒の描画
            draw_captured_pieces(current_turn)
            # 移動可能なマスを描画
            if selected_captured_piece is not None:
                draw_possible_setdrop_positions(board, selected_captured_piece, current_turn)
                # 選択した持ち駒を強調表示
                draw_selected_captured_piece(captured_x, captured_y)
            # 駒の描画
            draw_pieces()
            # 除外駒の描画
            draw_excluded_pieces()
            # セットアップ完了ボタンの描画
            draw_setup_finish_button(current_turn)
            # 両方セットアップ完了
            if setup_complete == 2:
                setup = False
            # 画面を更新
            pygame.display.update()

            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    setup = False
                # 持ち駒と除外駒のページ切り替え
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    handle_page_events(event)
                    if handle_setup_finish_events(event) == True:
                        setup_complete  += 1
                        current_turn = 1 - current_turn
                        print(f"準備完了ボタンが押されました。現在は: {setup_complete}")


                    x, y = event.pos
                    board_x = (x - BOARD_X) // SIZE
                    board_y = (y - BOARD_Y) // SIZE

                    # 範囲チェックを追加
                    if 0 <= board_x < len(board[0]) and 0 <= board_y < len(board):
                        board_z = get_highest_z(board, board_x, board_y)
                        
                        if selected_captured_piece is not None:
                            # 持ち駒を置く
                            result, current_turn = setdrop_piece(board, selected_captured_piece, board_x, board_y, board_z, current_turn)
                            if result == True:
                                drop_sound.play()
                                # 画面を黒で塗りつぶす
                                screen.fill(BLACK)
                                # 盤面の描画
                                draw_board()
                                # 数字と漢数字の描画
                                draw_labels()
                                # 移動可能なマスを描画
                                draw_possible_setdrop_positions(board, selected_captured_piece, current_turn)
                                # 持ち駒の描画
                                draw_captured_pieces(current_turn)
                                # 選択した持ち駒を強調表示
                                draw_selected_captured_piece(captured_x, captured_y)
                                # 駒の描画
                                draw_pieces()
                                # 除外駒の描画
                                draw_excluded_pieces()
                                # 画面を更新
                                pygame.display.update()
                                # 片方はセットアップ完了
                                if setup_complete == 1:
                                    current_turn = 1 - current_turn
                            # 選択状態をリセット
                            selected_captured_piece = None
                            captured_x, captured_y = -1, -1

                    else:
                        if selected_captured_piece is None:
                            # 持ち駒を選択
                            if HEIGHT - SIZE - 50 <= y <= HEIGHT - 10 and current_turn == 0:  # 先手の持ち駒エリア
                                index = (x - 15) // (SIZE + 5) + captured_pages[0] * 13
                                if 0 <= index < len(captured_pieces[0]):
                                    selected_captured_piece = captured_pieces[0][index]
                                    captured_x = 15 + (index - captured_pages[0] * 13) * (SIZE + 5)
                                    captured_y = HEIGHT - SIZE - 20
                                    print(captured_x,captured_y,index)
                            elif 10 <= y <= 10 + SIZE + 40 and current_turn == 1:  # 後手の持ち駒エリア
                                index = (x - 15) // (SIZE + 5) + captured_pages[1] * 13
                                if 0 <= index < len(captured_pieces[1]):
                                    selected_captured_piece = captured_pieces[1][index]
                                    captured_x = 15 + (index - captured_pages[1] * 13) * (SIZE + 5)
                                    captured_y = 40
                                    print(captured_x,captured_y,index)
                        else:
                            # 持ち駒の選択を解除
                            selected_captured_piece = None
                            captured_x, captured_y = -1, -1

    current_turn = 0  # ターンの初期化
    start = True



    # 対戦開始
    while running:
        # 画面を黒で塗りつぶす
        screen.fill(BLACK)
        # 盤面の描画
        draw_board()
        # 数字と漢数字の描画
        draw_labels()
        # 持ち駒の描画
        draw_captured_pieces(current_turn)
        # 移動可能なマスを描画
        if selected_piece is not None:
            draw_possible_moves(board, selected_piece, selected_x, selected_y, selected_z)
            # 選択した駒の強調表示
            draw_selected_piece(selected_x, selected_y)
        elif selected_captured_piece is not None:
            draw_possible_drop_positions(board, selected_captured_piece, current_turn)
            # 選択した持ち駒を強調表示
            draw_selected_captured_piece(captured_x, captured_y)
        # 駒の描画
        draw_pieces()
        # 除外駒の描画
        draw_excluded_pieces()
        # 画面を更新
        pygame.display.update()
        # 対局開始メッセージ
        if start == True:
            show_start_message()
            play_sound.play()
            start = False

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 持ち駒と除外駒のページ切り替え
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_page_events(event)

                x, y = event.pos
                board_x = (x - BOARD_X) // SIZE
                board_y = (y - BOARD_Y) // SIZE

                # 範囲チェックを追加
                if 0 <= board_x < len(board[0]) and 0 <= board_y < len(board):
                    board_z = get_highest_z(board, board_x, board_y)
                    
                    if selected_piece is None and selected_captured_piece is None:
                        # 駒を選択
                        if board[board_y][board_x][board_z] is not None and board[board_y][board_x][board_z].owner == current_turn:
                            selected_piece = board[board_y][board_x][board_z]
                            selected_x, selected_y , selected_z = board_x, board_y, board_z

                    elif selected_piece is not None:
                        # 駒を移動
                        if (selected_x, selected_y, selected_z) != (board_x, board_y, board_z):
                            result, current_turn = move_piece(board, selected_x, selected_y, selected_z, board_x, board_y, board_z, current_turn)
                            if result == True:
                                drop_sound.play()
                                # 画面を黒で塗りつぶす
                                screen.fill(BLACK)
                                # 盤面の描画
                                draw_board()
                                # 数字と漢数字の描画
                                draw_labels()
                                # 持ち駒の描画
                                draw_captured_pieces(current_turn)
                                # 移動可能なマスを描画
                                if selected_piece is not None:
                                    draw_possible_moves(board, selected_piece, selected_x, selected_y, selected_z)
                                    # 選択した駒の強調表示
                                    draw_selected_piece(selected_x, selected_y)
                                elif selected_captured_piece is not None:
                                    draw_possible_drop_positions(board, selected_captured_piece, current_turn)
                                    # 選択した持ち駒を強調表示
                                    draw_selected_captured_piece(captured_x, captured_y)
                                # 駒の描画
                                draw_pieces()
                                # 選択した持ち駒を強調表示
                                if selected_captured_piece is not None:
                                    draw_selected_captured_piece(captured_x, captured_y)
                                # 除外駒の描画
                                draw_excluded_pieces()
                                # 画面を更新
                                pygame.display.update()
                                # 王手チェック
                                if checkmate(board, 1 - current_turn):
                                    print(f"{current_turn}が王手された")
                                    checkmate_sound.play()
                                    show_checkmate_message()
                                    checkmate_BGM()
                                    now_BGM = 1
                                elif checkmate(board, current_turn):
                                    print(f"{1 - current_turn}王手はそのまま")
                                # 勝者チェック
                                elif check_winer(board, 1 - current_turn):
                                    print(f"{1 - current_turn}の勝利")
                                    pygame.mixer.music.stop()
                                    end_sound.play()
                                    show_winer_message(1 - current_turn)
                                    running = False
                                elif now_BGM == 1:
                                    BGM()
                                    now_BGM = 0
                                
                            elif result is None:
                                running = False
                                break

                        # 選択状態をリセット
                        selected_piece = None
                        selected_x, selected_y, selected_z = -1, -1, -1
                    
                    elif selected_captured_piece is not None:
                        # 持ち駒を置く
                        result, current_turn = drop_piece(board, selected_captured_piece, board_x, board_y, board_z, current_turn)
                        if result == True:
                            drop_sound.play()
                            # 画面を黒で塗りつぶす
                            screen.fill(BLACK)
                            # 盤面の描画
                            draw_board()
                            # 数字と漢数字の描画
                            draw_labels()
                            # 持ち駒の描画
                            draw_captured_pieces(current_turn)
                            # 移動可能なマスを描画
                            if selected_piece is not None:
                                draw_possible_moves(board, selected_piece, selected_x, selected_y, selected_z)
                                # 選択した駒の強調表示
                                draw_selected_piece(selected_x, selected_y)
                            elif selected_captured_piece is not None:
                                draw_possible_drop_positions(board, selected_captured_piece, current_turn)
                                # 選択した持ち駒を強調表示
                                draw_selected_captured_piece(captured_x, captured_y)
                            # 駒の描画
                            draw_pieces()
                            # 選択した持ち駒を強調表示
                            if selected_captured_piece is not None:
                                draw_selected_captured_piece(captured_x, captured_y)
                            # 除外駒の描画
                            draw_excluded_pieces()
                            # 画面を更新
                            pygame.display.update()
                            # 王手チェック
                            if checkmate(board, 1 - current_turn):
                                print(f"{current_turn}王手")
                                checkmate_sound.play()
                                show_checkmate_message()
                                checkmate_BGM()
                                now_BGM = 1
                            elif now_BGM == 1:
                                BGM()
                                now_BGM = 0
                        # 選択状態をリセット
                        selected_captured_piece = None
                        captured_x, captured_y = -1, -1

                else:
                    if selected_captured_piece is None:
                        # 持ち駒を選択
                        if HEIGHT - SIZE - 50 <= y <= HEIGHT - 10 and current_turn == 0:  # 先手の持ち駒エリア
                            index = (x - 15) // (SIZE + 5) + captured_pages[0] * 13
                            if 0 <= index < len(captured_pieces[0]):
                                selected_captured_piece = captured_pieces[0][index]
                                captured_x = 15 + (index - captured_pages[0] * 13) * (SIZE + 5)
                                captured_y = HEIGHT - SIZE - 20
                            # 選択状態をリセット
                            selected_piece = None
                            selected_x, selected_y, selected_z = -1, -1, -1
                        elif 10 <= y <= 10 + SIZE + 40 and current_turn == 1:  # 後手の持ち駒エリア
                            index = (x - 15) // (SIZE + 5) + captured_pages[1] * 13
                            if 0 <= index < len(captured_pieces[1]):
                                selected_captured_piece = captured_pieces[1][index]
                                captured_x = 15 + (index - captured_pages[1] * 13) * (SIZE + 5)
                                captured_y = 40
                            # 選択状態をリセット
                            selected_piece = None
                            selected_x, selected_y, selected_z = -1, -1, -1
                    else:
                        # 持ち駒の選択を解除
                        selected_captured_piece = None
                        captured_x, captured_y = -1, -1
    

    # Pygameの終了処理
    pygame.quit()
    print("軍議プログラム終了")

if __name__ == "__main__":
    main()

