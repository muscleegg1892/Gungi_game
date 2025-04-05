import random
from board import board, captured_pieces, can_drop, get_highest_z
from player import move_piece, drop_piece
from piece import Piece

def random_ai_move(board, current_turn):
    """
    ランダムAIが次の手を選択して実行する。
    """
    # 盤上の駒を取得
    movable_pieces = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            z = get_highest_z(board, x, y)
            piece = board[y][x][z]
            if piece is not None and piece.owner == current_turn:
                movable_pieces.append((piece, x, y, z))

    # 持ち駒を取得
    captured = captured_pieces[current_turn]

    # ランダムに行動を選択
    if captured and random.choice([True, False]):  # 持ち駒を使うか盤上の駒を動かすかをランダムに選択
        # 持ち駒をランダムに選択
        piece = random.choice(captured)
        # 置ける場所を取得
        valid_positions = []
        for x in range(9):
            for y in range(9):
                z = get_highest_z(board, x, y)
                if can_drop(board, piece, x, y, z, current_turn):
                    valid_positions.append((x, y, z))
        
        # 置ける場所があればランダムに選択して置く
        if valid_positions:
            x, y, z = random.choice(valid_positions)
            success, _ = drop_piece(board, piece, x, y, z, current_turn)
            if success:
                print(f"AI: {piece.name}を({x}, {y}, {z})に打ちました")
                return True
    else:
        # 盤上の駒をランダムに選択
        if movable_pieces:
            piece, x, y, z = random.choice(movable_pieces)
            # 移動可能な場所を取得
            valid_moves = []
            for target_x in range(9):
                for target_y in range(9):
                    target_z = get_highest_z(board, target_x, target_y)
                    if piece.can_move(board,target_x, target_y, target_z):
                        valid_moves.append((target_x, target_y, target_z))
            
            # 移動可能な場所があればランダムに選択して移動
            if valid_moves:
                target_x, target_y, target_z = random.choice(valid_moves)
                if (target_x, target_y, target_z) == (x, y, z):
                    return False
                success, _ = move_piece(board, x, y, z, target_x, target_y, target_z, current_turn)
                if success:
                    print(f"AI: {piece.name}を({x}, {y}, {z})から({target_x}, {target_y}, {target_z})に移動しました")
                    return True

    print("AI: 有効な手がありませんでした")
    return False