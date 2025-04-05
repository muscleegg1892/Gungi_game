from piece import Piece
from board import switch_turn, excluded_pieces, captured_pieces, can_drop, can_setdrop
from game_ui import stack_or_take_dialog, swap_or_keep_dialog

# 駒を移動する関数
def move_piece(board, x1, y1, z1, x2, y2, z2, current_turn):
    # ボード範囲外のチェック
    if not (0 <= x2 < len(board[0]) and 0 <= y2 < len(board) and 0 <= z2 < len(board[0][0])): 
        print("移動先がボードの範囲外です")
        return False, current_turn

    piece = board[y1][x1][z1]
    if piece is None:
        print("選択された位置に駒がありません")
        return False, current_turn

    if not piece.can_move(board, x2, y2, z2):
        print(f"{piece.name}は({x2}, {y2}, {z2})に移動できません")
        return False, current_turn

    # 移動先に駒がある場合
    if board[y2][x2][z2] is not None:
        # z2が2の場合は取る動作のみ許可
        if z2 == 2 and board[y2][x2][z2].owner == current_turn:
            print("この位置ではツケることはできません")
            return False, current_turn
        
        # ツケるか取るかの判定
        if board[y2][x2][z2].owner == current_turn:
            board[y1][x1][z1] = None
            board[y2][x2][z2 + 1] = piece
            piece.x, piece.y, piece.z = x2, y2, z2 + 1
            print(f"{piece.name}を({x2}, {y2}, {z2 + 1})に移動（ツケ）")

            # 謀の特殊処理
            if z2 == 1:
                for index2 in range(len(captured_pieces[current_turn])):
                    if captured_pieces[current_turn][index2].name == board[y2][x2][z2 - 1].name:
                        break
                # ふたつ下の駒だけが相手の駒だった場合
                if (board[y2][x2][z2 - 1] is not None and
                    piece.name == "謀" and
                    board[y2][x2][z2 - 1].owner != piece.owner and
                    captured_pieces[current_turn][index2].name == board[y2][x2][z2 - 1].name):
                    result = swap_or_keep_dialog()
                    if result == True:
                        # 入れ替え処理
                        print(f"{captured_pieces[current_turn][index2].name}と{board[y2][x2][z2 - 1].name}を入れ替えました")
                        board[y2][x2][z2 - 1] = captured_pieces[current_turn][index2]
                        board[y2][x2][z2 - 1].x = x2
                        board[y2][x2][z2 - 1].y = y2
                        board[y2][x2][z2 - 1].z = z2 - 1
                        captured_pieces[current_turn].remove(captured_pieces[current_turn][index2])
                        excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][z2 - 1].name, 1 - current_turn, -1, -1, -1))
                    elif result == None:
                        return None, current_turn

        else:
            # 三段は取る動作のみ
            if z2 == 2:
                index = 0
                for i in range(z2 + 1):
                    if board[y2][x2][i] is not None and board[y2][x2][i].owner != piece.owner:
                        # 除外駒リストに追加
                        excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][i].name, 1 - current_turn, -1, -1, -1))
                        print(f"{piece.name}が{board[y2][x2][i].name}を取りました")
                        board[y2][x2][i] = None  # 除外された駒を削除
                    elif board[y2][x2][i] is not None:
                        board[y2][x2][index] = board[y2][x2][i]
                        board[y2][x2][index].z = index
                        if index != i:
                            board[y2][x2][i] = None
                            print(f"{board[y2][x2][index].name}を{board[y2][x2][index].z}に移動")
                        index += 1
                board[y1][x1][z1] = None
                board[y2][x2][index] = piece
                piece.x, piece.y, piece.z = x2, y2, index
                print(f"{piece.name}を({x1}, {y1}, {z1})から({x2}, {y2}, {index})に移動しました")
            # 相手の師だった場合、取る
            elif board[y2][x2][z2].name == "師":
                index = 0
                for i in range(z2 + 1):
                    if board[y2][x2][i] is not None and board[y2][x2][i].owner != piece.owner:
                        # 除外駒リストに追加
                        excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][i].name, 1 - current_turn, -1, -1, -1))
                        print(f"{piece.name}が{board[y2][x2][i].name}を取りました")
                        board[y2][x2][i] = None  # 除外された駒を削除
                    elif board[y2][x2][i] is not None:
                        board[y2][x2][index] = board[y2][x2][i]
                        board[y2][x2][index].z = index
                        if index != i:
                            board[y2][x2][i] = None
                            print(f"{board[y2][x2][index].name}を{board[y2][x2][index].z}に移動")
                        index += 1
                board[y1][x1][z1] = None
                board[y2][x2][index] = piece
                piece.x, piece.y, piece.z = x2, y2, index
                print(f"{piece.name}を({x1}, {y1}, {z1})から({x2}, {y2}, {index})に移動しました")
            else:
                result = stack_or_take_dialog()
                if result == "stack":
                    board[y1][x1][z1] = None
                    board[y2][x2][z2 + 1] = piece
                    piece.x, piece.y, piece.z = x2, y2, z2 + 1
                    print(f"{piece.name}を({x1}, {y1}, {z1})から({x2}, {y2}, {z2 + 1})に移動（ツケ）")
                    # 謀の特殊処理
                    if z2 == 0:
                        for index in range(len(captured_pieces[current_turn])):
                            if captured_pieces[current_turn][index].name == board[y2][x2][z2].name:
                                break
                        if (piece.name == "謀" and
                            board[y2][x2][z2].owner != piece.owner and
                            captured_pieces[current_turn][index].name == board[y2][x2][z2].name):
                            result = swap_or_keep_dialog()
                            if result == True:
                                # 入れ替え処理
                                print(f"{captured_pieces[current_turn][index].name}と{board[y2][x2][z2].name}を入れ替えました")
                                board[y2][x2][z2] = captured_pieces[current_turn][index]
                                board[y2][x2][z2].x = x2
                                board[y2][x2][z2].y = y2
                                board[y2][x2][z2].z = z2
                                captured_pieces[current_turn].remove(captured_pieces[current_turn][index])
                                excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][z2].name, 1 - current_turn, -1, -1, -1))
                            elif result == None:
                                return None, current_turn
                    else:
                        for index1 in range(len(captured_pieces[current_turn])):
                            if captured_pieces[current_turn][index1].name == board[y2][x2][z2].name:
                                break
                        for index2 in range(len(captured_pieces[current_turn])):
                            if captured_pieces[current_turn][index2].name == board[y2][x2][z2 - 1].name:
                                print(f"{captured_pieces[current_turn][index2].name}")
                                break
                        
                        # 下の駒が両方相手の駒だった場合
                        if (board[y2][x2][z2 - 1] is not None and
                            piece.name == "謀" and
                            board[y2][x2][z2].owner != piece.owner and
                            captured_pieces[current_turn][index1].name == board[y2][x2][z2].name and
                            board[y2][x2][z2 - 1].owner != piece.owner and
                            captured_pieces[current_turn][index2].name == board[y2][x2][z2 - 1].name):
                            result = swap_or_keep_dialog()
                            if result == True:
                                # 入れ替え処理
                                print(f"{captured_pieces[current_turn][index1].name}と{board[y2][x2][z2].name}を入れ替えました")
                                board[y2][x2][z2] = captured_pieces[current_turn][index1]
                                board[y2][x2][z2].x = x2
                                board[y2][x2][z2].y = y2
                                board[y2][x2][z2].z = z2
                                captured_pieces[current_turn].remove(captured_pieces[current_turn][index1])
                                excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][z2].name, 1 - current_turn, -1, -1, -1))
                                print(f"{captured_pieces[current_turn][index2 -1].name}と{board[y2][x2][z2 - 1].name}を入れ替えました")
                                board[y2][x2][z2 - 1] = captured_pieces[current_turn][index2 - 1]
                                board[y2][x2][z2 - 1].x = x2
                                board[y2][x2][z2 - 1].y = y2
                                board[y2][x2][z2 - 1].z = z2 - 1
                                captured_pieces[current_turn].remove(captured_pieces[current_turn][index2 - 1])
                                excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][z2 - 1].name, 1 - current_turn, -1, -1, -1, -1, -1, -1))
                            elif result == None:
                                return None, current_turn
                        # ひとつ下の駒だけが相手の駒だった場合
                        elif (board[y2][x2][z2 - 1] is not None and
                            piece.name == "謀" and
                            board[y2][x2][z2].owner != piece.owner and
                            captured_pieces[current_turn][index1].name == board[y2][x2][z2].name and
                            board[y2][x2][z2 - 1].owner == piece.owner):
                            result = swap_or_keep_dialog()
                            if result == True:
                                # 入れ替え処理
                                print(f"{captured_pieces[current_turn][index1].name}と{board[y2][x2][z2].name}を入れ替えました")
                                board[y2][x2][z2] = captured_pieces[current_turn][index1]
                                board[y2][x2][z2].x = x2
                                board[y2][x2][z2].y = y2
                                board[y2][x2][z2].z = z2
                                captured_pieces[current_turn].remove(captured_pieces[current_turn][index1])
                                excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][z2].name, 1 - current_turn, -1, -1, -1))
                            elif result == None:
                                return None, current_turn
                        # ふたつ下の駒だけが相手の駒だった場合
                        elif (board[y2][x2][z2 - 1] is not None and
                            piece.name == "謀" and
                            board[y2][x2][z2].owner == piece.owner and
                            board[y2][x2][z2 - 1].owner != piece.owner and
                            captured_pieces[current_turn][index2].name == board[y2][x2][z2 - 1].name):
                            result = swap_or_keep_dialog()
                            if result == True:
                                # 入れ替え処理
                                print(f"{captured_pieces[current_turn][index2].name}と{board[y2][x2][z2 - 1].name}を入れ替えました")
                                board[y2][x2][z2 - 1] = captured_pieces[current_turn][index2]
                                board[y2][x2][z2 - 1].x = x2
                                board[y2][x2][z2 - 1].y = y2
                                board[y2][x2][z2 - 1].z = z2 - 1
                                captured_pieces[current_turn].remove(captured_pieces[current_turn][index2])
                                excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][z2 - 1].name, 1 - current_turn, -1, -1, -1))
                            elif result == None:
                                return None, current_turn
                # クローズした場合
                elif result == None:
                    return None, current_turn
                # 取る場合
                elif result == "take":
                    index = 0
                    for i in range(z2 + 1):
                        if board[y2][x2][i] is not None and board[y2][x2][i].owner != piece.owner:
                            # 除外駒リストに追加
                            excluded_pieces[1 - current_turn].append(Piece(board[y2][x2][i].name, 1 - current_turn, -1, -1, -1))
                            print(f"{piece.name}が{board[y2][x2][i].name}を取りました")
                            board[y2][x2][i] = None  # 除外された駒を削除
                        elif board[y2][x2][i] is not None:
                            board[y2][x2][index] = board[y2][x2][i]
                            board[y2][x2][index].z = index
                            if index != i:
                                board[y2][x2][i] = None
                                print(f"{board[y2][x2][index].name}を{board[y2][x2][index].z}に移動")
                            index += 1
                    board[y1][x1][z1] = None
                    board[y2][x2][index] = piece
                    piece.x, piece.y, piece.z = x2, y2, index
                    print(f"{piece.name}を({x1}, {y1}, {z1})から({x2}, {y2}, {index})に移動しました")
                elif result == "cancel":
                    print("キャンセル")
                    return False, current_turn
    # 移動先に駒がない場合
    else:
        board[y1][x1][z1] = None
        board[y2][x2][z2] = piece
        piece.x, piece.y, piece.z = x2, y2, z2
        print(f"{piece.name}を({x1}, {y1}, {z1})から({x2}, {y2}, {z2})に移動しました")

    # ターンを交代
    current_turn = switch_turn(current_turn)
    return True, current_turn

# 持ち駒を打つ（新）関数
def drop_piece(board, piece, x, y, z, current_turn):
    if not can_drop(board, piece, x, y, z, current_turn):
        print(f"{piece.name}は({x}, {y}, {z})に打てません")
        return False, current_turn
    else:
        if board[y][x][z] is None:
            board[y][x][z] = piece
            captured_pieces[piece.owner].remove(piece)
            piece.x = x
            piece.y = y
            piece.z = z
            print(f"{piece.name}を({x}, {y}, {z})に打ちました")
        elif board[y][x][z].owner == piece.owner:
            board[y][x][z + 1] = piece
            captured_pieces[piece.owner].remove(piece)
            piece.x = x
            piece.y = y
            piece.z = z + 1
            print(f"{piece.name}を({x}, {y}, {z + 1})に打ちました")

            # 謀の特殊処理
            if z == 1:
                for index2 in range(len(captured_pieces[current_turn])):
                    if captured_pieces[current_turn][index2].name == board[y][x][z - 1].name:
                        break
                # ふたつ下の駒だけが相手の駒だった場合
                if (board[y][x][z - 1] is not None and
                    piece.name == "謀" and
                    board[y][x][z - 1].owner != piece.owner and
                    captured_pieces[current_turn][index2].name == board[y][x][z - 1].name):
                    if swap_or_keep_dialog():
                        # 入れ替え処理
                        print(f"{captured_pieces[current_turn][index2].name}と{board[y][x][z - 1].name}を入れ替えました")
                        board[y][x][z - 1] = captured_pieces[current_turn][index2]
                        board[y][x][z - 1].x = x
                        board[y][x][z - 1].y = y
                        board[y][x][z - 1].z = z - 1
                        captured_pieces[current_turn].remove(captured_pieces[current_turn][index2])
                        excluded_pieces[1 - current_turn].append(Piece(board[y][x][z - 1].name, 1 - current_turn, -1, -1, -1))
        current_turn = switch_turn(current_turn)
        return True, current_turn

# セットアップ持ち駒を打つ（新）関数
def setdrop_piece(board, piece, x, y, z, current_turn):
    if not can_setdrop(board, piece, x, y, z, current_turn):
        print(f"{piece.name}は({x}, {y}, {z})に打てません")
        return False, current_turn
    else:
        if board[y][x][z] is None:
            board[y][x][z] = piece
            captured_pieces[piece.owner].remove(piece)
            piece.x = x
            piece.y = y
            piece.z = z
            print(f"{piece.name}を({x}, {y}, {z})に打ちました")
        elif board[y][x][z].owner == piece.owner:
            board[y][x][z + 1] = piece
            captured_pieces[piece.owner].remove(piece)
            piece.x = x
            piece.y = y
            piece.z = z + 1
            print(f"{piece.name}を({x}, {y}, {z + 1})に打ちました")

        current_turn = switch_turn(current_turn)
        return True, current_turn
