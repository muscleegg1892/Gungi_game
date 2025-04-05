from piece import Piece


# 9x9x3のboard配列を初期化
board = [[[None for _ in range(3)] for _ in range(9)] for _ in range(9)]

# 先手と後手の持ち駒リスト
captured_pieces = {0: [],1: []}

# 除外駒リスト
excluded_pieces = {0: [],1: []}

# 手持ちの駒リスト（辞書型からリストのリストに変更）
hand_pieces = [
["師", "大", "中", "小", "小", "砲", "筒", "謀", "侍", "侍", "馬", "馬", "忍", "忍", "砦", "砦", "弓", "弓", "槍", "槍", "槍", "兵", "兵", "兵", "兵"],  # 先手
["師", "大", "中", "小", "小", "砲", "筒", "謀", "侍", "侍", "馬", "馬", "忍", "忍", "砦", "砦", "弓", "弓", "槍", "槍", "槍", "兵", "兵", "兵", "兵"]   # 後手
]


# ターンを切り替える
def switch_turn(current_turn):
    current_turn = 1 - current_turn
    print(f"現在のターン: {'先手' if current_turn == 0 else '後手'}")
    return current_turn


# 駒をボードに配置し、手持ちリストからその駒を削除する
def place_piece(board, hand_pieces, piece_name, owner, x, y, z):
    if piece_name in hand_pieces[owner]:
        board[y][x][z] = Piece(piece_name, owner, x, y, z)
        hand_pieces[owner].remove(piece_name)
        print(f"Placed {piece_name} at ({x}, {y}, {z}).")

# 除外する駒を除外駒に追加し、手持ちリストからその駒を削除する
def exclude_piece_from_hand(hand_pieces, piece_name, owner):
    if piece_name in hand_pieces[owner]:
        excluded_pieces[owner].append(Piece(piece_name, owner, -1, -1, -1))
        hand_pieces[owner].remove(piece_name)
        print(f"Excluded {piece_name} from hand.")

# 手持ちリストの余りを持ち駒リストに追加する
def add_captured_pieces(hand_pieces, captured_pieces, owner):
    for piece_name in hand_pieces[owner]:
        captured_pieces[owner].append(Piece(piece_name, owner, -1, -1, -1))
        print(f"Added {piece_name}to captured pieces.")



# 駒の初期配置
def setup1_pieces(board):
    """初期配置１"""
    # 先手（下側白）
    place_piece(board, hand_pieces, "兵", 0, 0, 6, 0)
    place_piece(board, hand_pieces, "砦", 0, 2, 6, 0)
    place_piece(board, hand_pieces, "侍", 0, 3, 6, 0)
    place_piece(board, hand_pieces, "兵", 0, 4, 6, 0)
    place_piece(board, hand_pieces, "侍", 0, 5, 6, 0)
    place_piece(board, hand_pieces, "砦", 0, 6, 6, 0)
    place_piece(board, hand_pieces, "兵", 0, 8, 6, 0)
    place_piece(board, hand_pieces, "忍", 0, 1, 7, 0)
    place_piece(board, hand_pieces, "槍", 0, 4, 7, 0)
    place_piece(board, hand_pieces, "忍", 0, 7, 7, 0)
    place_piece(board, hand_pieces, "大", 0, 3, 8, 0)
    place_piece(board, hand_pieces, "師", 0, 4, 8, 0)
    place_piece(board, hand_pieces, "中", 0, 5, 8, 0)
    # 特殊駒を除外
    exclude_piece_from_hand(hand_pieces, "砲", 0)
    exclude_piece_from_hand(hand_pieces, "弓", 0)
    exclude_piece_from_hand(hand_pieces, "弓", 0)
    exclude_piece_from_hand(hand_pieces, "筒", 0)
    exclude_piece_from_hand(hand_pieces, "謀", 0)

    # 後手（上側黒）
    place_piece(board, hand_pieces, "兵", 1, 0, 2, 0)
    place_piece(board, hand_pieces, "砦", 1, 2, 2, 0)
    place_piece(board, hand_pieces, "侍", 1, 3, 2, 0)
    place_piece(board, hand_pieces, "兵", 1, 4, 2, 0)
    place_piece(board, hand_pieces, "侍", 1, 5, 2, 0)
    place_piece(board, hand_pieces, "砦", 1, 6, 2, 0)
    place_piece(board, hand_pieces, "兵", 1, 8, 2, 0)
    place_piece(board, hand_pieces, "忍", 1, 1, 1, 0)
    place_piece(board, hand_pieces, "槍", 1, 4, 1, 0)
    place_piece(board, hand_pieces, "忍", 1, 7, 1, 0)
    place_piece(board, hand_pieces, "中", 1, 3, 0, 0)
    place_piece(board, hand_pieces, "師", 1, 4, 0, 0)
    place_piece(board, hand_pieces, "大", 1, 5, 0, 0)
    # 特殊駒を除外
    exclude_piece_from_hand(hand_pieces, "砲", 1)
    exclude_piece_from_hand(hand_pieces, "弓", 1)
    exclude_piece_from_hand(hand_pieces, "弓", 1)
    exclude_piece_from_hand(hand_pieces, "筒", 1)
    exclude_piece_from_hand(hand_pieces, "謀", 1)

    # 残りの手持ちリストを持ち駒リストに追加
    for owner in range(len(hand_pieces)):
        add_captured_pieces(hand_pieces, captured_pieces, owner)

def setup2_pieces(board):
    """初期配置２"""
    # 先手（下側白）
    place_piece(board, hand_pieces, "兵", 0, 0, 6, 0)
    place_piece(board, hand_pieces, "砦", 0, 2, 6, 0)
    place_piece(board, hand_pieces, "侍", 0, 3, 6, 0)
    place_piece(board, hand_pieces, "兵", 0, 4, 6, 0)
    place_piece(board, hand_pieces, "侍", 0, 5, 6, 0)
    place_piece(board, hand_pieces, "砦", 0, 6, 6, 0)
    place_piece(board, hand_pieces, "兵", 0, 8, 6, 0)
    place_piece(board, hand_pieces, "忍", 0, 1, 7, 0)
    place_piece(board, hand_pieces, "弓", 0, 2, 7, 0)
    place_piece(board, hand_pieces, "槍", 0, 4, 7, 0)
    place_piece(board, hand_pieces, "弓", 0, 6, 7, 0)
    place_piece(board, hand_pieces, "馬", 0, 7, 7, 0)
    place_piece(board, hand_pieces, "大", 0, 3, 8, 0)
    place_piece(board, hand_pieces, "師", 0, 4, 8, 0)
    place_piece(board, hand_pieces, "中", 0, 5, 8, 0)
    # 特殊駒を除外
    exclude_piece_from_hand(hand_pieces, "砲", 0)
    exclude_piece_from_hand(hand_pieces, "弓", 0)
    exclude_piece_from_hand(hand_pieces, "弓", 0)
    exclude_piece_from_hand(hand_pieces, "筒", 0)
    exclude_piece_from_hand(hand_pieces, "謀", 0)

    # 後手（上側黒）
    place_piece(board, hand_pieces, "兵", 1, 0, 2, 0)
    place_piece(board, hand_pieces, "砦", 1, 2, 2, 0)
    place_piece(board, hand_pieces, "侍", 1, 3, 2, 0)
    place_piece(board, hand_pieces, "兵", 1, 4, 2, 0)
    place_piece(board, hand_pieces, "侍", 1, 5, 2, 0)
    place_piece(board, hand_pieces, "砦", 1, 6, 2, 0)
    place_piece(board, hand_pieces, "兵", 1, 8, 2, 0)
    place_piece(board, hand_pieces, "忍", 1, 1, 1, 0)
    place_piece(board, hand_pieces, "弓", 1, 2, 1, 0)
    place_piece(board, hand_pieces, "槍", 1, 4, 1, 0)
    place_piece(board, hand_pieces, "弓", 1, 6, 1, 0)
    place_piece(board, hand_pieces, "馬", 1, 7, 1, 0)
    place_piece(board, hand_pieces, "中", 1, 3, 0, 0)
    place_piece(board, hand_pieces, "師", 1, 4, 0, 0)
    place_piece(board, hand_pieces, "大", 1, 5, 0, 0)
    # 特殊駒を除外
    exclude_piece_from_hand(hand_pieces, "砲", 1)
    exclude_piece_from_hand(hand_pieces, "弓", 1)
    exclude_piece_from_hand(hand_pieces, "弓", 1)
    exclude_piece_from_hand(hand_pieces, "筒", 1)
    exclude_piece_from_hand(hand_pieces, "謀", 1)

    # 残りの手持ちリストを持ち駒リストに追加
    for owner in range(len(hand_pieces)):
        add_captured_pieces(hand_pieces, captured_pieces, owner)

def setup3_pieces():
    """初期配置3"""
    # 残りの手持ちリストを持ち駒リストに追加
    for owner in range(len(hand_pieces)):
        add_captured_pieces(hand_pieces, captured_pieces, owner)

#指定されたx, yの位置で、zの値がNoneではない一番高い数字を取得する。
def get_highest_z(board, x, y):
    for z in range(2, -1, -1):  # zを2から0まで逆順にループ
        if board[y][x][z] is not None:
            return z
    return 0  # 全てNoneの場合

# 持ち駒を置ける場所を判断する関数
def can_drop(board, piece, x, y, z, current_turn):
    for i in range(3):
            # 自分の師の上にツケられない（重ねられない）ようにする
            if board[y][x][i] is not None and board[y][x][i].name == "師" and board[y][x][i].owner == current_turn:
                return False
    # 謀は3段目に打てる
    if not piece.name == "謀":
        # 3段目に駒を置けないようにする（謀以外）
        if z >= 1:
            return False
    else:
        if z >= 2:
            return False
    # 一番進んでいる駒を取得
    if current_turn == 0:
        top_y = 8
    else:
        top_y = 0
    for a in range(len(board[0])):
        for b in range(len(board)):
            if board[b][a][get_highest_z(board, a, b)] is not None:
                if board[b][a][get_highest_z(board, a, b)].owner == current_turn:
                    if current_turn == 0 and top_y > b:
                        top_y = b
                    elif current_turn == 1 and top_y < b:
                        top_y = b
    if not piece.name == "謀":
        # 一番進んでいる駒のy座標以下の確認と空か所有者が同じかの確認
        if current_turn == 0 and top_y <= y:
            if board[y][x][z] is None:
                return True
            elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
                return True
        elif current_turn == 1 and top_y >= y:
            if board[y][x][z] is None:
                return True
            elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
                return True
    else:
        if current_turn == 0 and top_y <= y and z == 0:
            if board[y][x][z] is None:
                return True
            elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
                return True
        elif board[y][x][z] is not None and current_turn == 0 and top_y <= y and z == 1:
            if board[y][x][z - 1] is None:
                return True
            elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
                return True
        elif current_turn == 1 and top_y >= y and z == 0:
            if board[y][x][z] is None:
                return True
            elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
                return True
        elif board[y][x][z] is not None and current_turn == 1 and top_y >= y and z == 1:
            if board[y][x][z - 1] is None:
                return True
            elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
                return True

    return False

# 持ち駒を置ける場所を判断する関数
def can_setdrop(board, piece, x, y, z, current_turn):
    for i in range(3):
            # 自分の師の上にツケられない（重ねられない）ようにする
            if board[y][x][i] is not None and board[y][x][i].name == "師" and board[y][x][i].owner == current_turn:
                return False
    # 3段目まで置ける
    if z >= 2:
        return False
    # 一番進んでいる駒を取得
    if current_turn == 0:
        top_y = 6
    else:
        top_y = 2
    # 一番進んでいる駒のy座標以下の確認と空か所有者が同じかの確認
    if current_turn == 0 and top_y <= y:
        if board[y][x][z] is None:
            return True
        elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
            return True
    elif current_turn == 1 and top_y >= y:
        if board[y][x][z] is None:
            return True
        elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
            return True

    if current_turn == 0 and top_y <= y and z == 0:
        if board[y][x][z] is None:
            return True
        elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
            return True
    elif board[y][x][z] is not None and current_turn == 0 and top_y <= y and z == 1:
        if board[y][x][z - 1] is None:
            return True
        elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
            return True
    elif current_turn == 1 and top_y >= y and z == 0:
        if board[y][x][z] is None:
            return True
        elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
            return True
    elif board[y][x][z] is not None and current_turn == 1 and top_y >= y and z == 1:
        if board[y][x][z - 1] is None:
            return True
        elif board[y][x][z].owner == current_turn and board[y][x][z + 1] is None:
            return True
    return False


# 師の場所を探す
def king_place(board, current_turn):
    for y in range(len(board)):
        for x in range(len(board[0])):
            z = get_highest_z(board, x, y)
            if board[y][x][z] is not None and board[y][x][z].name == "師" and board[y][x][z].owner != current_turn:
                return x, y, z
    return None

# 王手チェック
def checkmate(board, current_turn):
    king_position = king_place(board, current_turn)
    if king_position is None:
        print("エラー: 王の位置が見つかりませんでした")
        return False  # 王がいない場合は王手ではないとみなす
    king_x, king_y, king_z = king_position
    for y in range(len(board)):
        for x in range(len(board[0])):
            z = get_highest_z(board, x, y)
            if board[y][x][z] is not None and board[y][x][z].owner == current_turn:
                if board[y][x][z].can_move(board, king_x, king_y, king_z):
                    return True

# 勝者チェック
def check_winer(board, current_turn):
    if king_place(board, current_turn) is None:
        return True
    return False