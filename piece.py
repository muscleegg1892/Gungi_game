# 駒クラス
class Piece:
    # コンストラクタ
    def __init__(self, name, owner, x, y, z):
        self.name = name
        self.owner = owner
        self.x = x
        self.y = y
        self.z = z
    
    # 駒の移動可能な範囲を返す
    def can_move(self, board, x, y, z):

        for i in range(3):
            # 自分の師の上にツケられない（重ねられない）ようにする
            if board[y][x][i] is not None and board[y][x][i].name == "師" and board[y][x][i].owner == self.owner:
                return False
            # 自分より高い位置の駒に移動できないようにする
            if board[y][x][i] is not None and i > z:
                return False

        dx = x - self.x
        dy = y - self.y

        # 砲、筒、弓以外のとき
        if self.name not in ["砲", "筒", "弓"]:
            # 移動方向を確認
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
            current_x, current_y = self.x, self.y

            # 移動経路上の駒を確認
            while (current_x, current_y) != (x, y):
                current_x += step_x
                current_y += step_y
                # 範囲外チェックを追加
                if not (0 <= current_x < len(board[0]) and 0 <= current_y < len(board)):
                    break
                if (current_x, current_y) != (x, y) and board[current_y][current_x][0] is not None:
                    return False
        
        else:
            # 砲、筒の場合
            step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
            if self.name == "弓":
                current_x, current_y = self.x + step_x, self.y + step_y
                # 経路上に自分のzより高い駒がある場合は移動不可
                for z_level in range(self.z + 1, len(board[0][0])):
                    if board[current_y][current_x][z_level] is not None:
                        return False
                current_x -= step_x
            else:
                current_x, current_y = self.x, self.y

            # 移動経路上の駒を確認
            while (current_x, current_y) != (x, y):
                current_x += step_x
                current_y += step_y
                # 範囲外チェックを追加
                if not (0 <= current_x < len(board[0]) and 0 <= current_y < len(board)):
                    break
                # 経路上に自分のzより高い駒がある場合は移動不可
                for z_level in range(self.z + 1, len(board[0][0])):
                    if board[current_y][current_x][z_level] is not None:
                        return False
                # 前方以外は飛び越えられない
                if (current_x, current_y) != (x, y) and board[current_y][current_x][0] is not None and (self.owner == 0 and dy > 0 or self.owner == 1 and dy < 0 or dy == 0 and dx != 0)  :
                    return False

        if self.name == "師":
            match self.z:
                case 0:
                    return ((dx == 0 and abs(dy) == 1) or (abs(dx) == 1 and dy == 0) or (abs(dx) == abs(dy) and 0 <= abs(dx) <= 1)) and (z <= self.z)
                case 1:
                    return ((dx == 0 and 0 <= abs(dy) <= 2) or (0 <= abs(dx) <= 2 and dy == 0) or (abs(dx) == abs(dy) and 0 <= abs(dx) <= 2)) and (z <= self.z)
                case 2:
                    return ((dx == 0 and 0 <= abs(dy) <= 3) or (0 <= abs(dx) <= 3 and dy == 0) or (abs(dx) == abs(dy) and 0 <= abs(dx) <= 3)) and (z <= self.z)
        elif self.name == "大":
            match self.z:
                case 0:
                    return ((dx == 0 or dy == 0) or (abs(dx) == abs(dy) and 0 <= abs(dx) <= 1)) and (z <= self.z)
                case 1:
                    return ((dx == 0 or dy == 0) or (abs(dx) == abs(dy) and 0 <= abs(dx) <= 2)) and (z <= self.z)
                case 2:
                    return ((dx == 0 or dy == 0) or (abs(dx) == abs(dy) and 0 <= abs(dx) <= 3)) and (z <= self.z)
        elif self.name == "中":
            match self.z:
                case 0:
                    return ((abs(dx) == abs(dy)) or (dx == 0 and 0 <= abs(dy) <= 1) or (0 <= abs(dx) <= 1 and dy == 0)) and (z <= self.z)
                case 1:
                    return ((abs(dx) == abs(dy)) or (dx == 0 and 0 <= abs(dy) <= 2) or (0 <= abs(dx) <= 2 and dy == 0)) and (z <= self.z)
                case 2:
                    return ((abs(dx) == abs(dy)) or (dx == 0 and 0 <= abs(dy) <= 3) or (0 <= abs(dx) <= 3 and dy == 0)) and (z <= self.z)
        elif self.name == "小":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and 0 <= abs(dy) <= 1) or (0 <= abs(dx) <= 1 and dy == 0) or (abs(dx) == abs(dy) and -1 <= dy <= 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= abs(dy) <= 2) or (0 <= abs(dx) <= 2 and dy == 0) or (abs(dx) == abs(dy) and -2 <= dy <= 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <= abs(dy) <= 3) or (0 <= abs(dx) <= 3 and dy == 0) or (abs(dx) == abs(dy) and -3 <= dy <= 0)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and 0 <= abs(dy) <= 1) or (0 <= abs(dx) <= 1 and dy == 0) or (abs(dx) == abs(dy) and 0 <= dy <= 1)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= abs(dy) <= 2) or (0 <= abs(dx) <= 2 and dy == 0) or (abs(dx) == abs(dy) and 0 <= dy <= 2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <= abs(dy) <= 3) or (0 <= abs(dx) <= 3 and dy == 0) or (abs(dx) == abs(dy) and 0 <= dy <= 3)) and (z <= self.z)
        elif self.name == "侍":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and abs(dy) == 1) or (abs(dx) == abs(dy) and -1 <= dy <= 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= abs(dy) <= 2) or (abs(dx) == abs(dy) and -2 <= dy <= 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <= abs(dy) <= 3) or (abs(dx) == abs(dy) and -3 <= dy <= 0)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and abs(dy) == 1) or (abs(dx) == abs(dy) and 0 <= dy <= 1)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= abs(dy) <= 2) or (abs(dx) == abs(dy) and 0 <= dy <= 2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <=abs(dy) <= 3) or (abs(dx) == abs(dy) and 0 <= dy <= 3)) and (z <= self.z)
        elif self.name == "槍":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and -2 <= dy <= 0) or (dx == 0 and 0 <= dy <= 1) or (abs(dx) == abs(dy) and -1 <= dy <= 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and -3 <= dy <= 0) or (dx == 0 and 0 <= dy <= 2) or (abs(dx) == abs(dy) and -2 <= dy <= 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and -4 <= dy <= 0) or (dx == 0 and 0 <= dy <= 3) or (abs(dx) == abs(dy) and -3 <= dy <= 0)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and 0 <= dy <= 2) or (dx == 0 and -1 <= dy <= 0) or (abs(dx) == abs(dy) and 0 <= dy <= 1)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= dy <= 3) or (dx == 0 and -2 <= dy <= 0) or (abs(dx) == abs(dy) and 0 <= dy <= 2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <= dy <= 4) or (dx == 0 and -3 <= dy <= 0) or (abs(dx) == abs(dy) and 0 <= dy <= 3)) and (z <= self.z)
        elif self.name == "馬":
            match self.z:
                case 0:
                    return ((dx == 0 and 0 <= abs(dy) <= 2) or (0 <= abs(dx) <= 1 and dy == 0)) and (z <= self.z)
                case 1:
                    return ((dx == 0 and 0 <= abs(dy) <= 3) or (0 <= abs(dx) <= 2 and dy == 0)) and (z <= self.z)
                case 2:
                    return ((dx == 0 and 0 <= abs(dy) <= 4) or (0 <= abs(dx) <= 3 and dy == 0)) and (z <= self.z)
        elif self.name == "忍":
            match self.z:
                case 0:
                    return ((abs(dx) == abs(dy) and 0 <= abs(dy) <= 2)) and (z <= self.z)
                case 1:
                    return ((abs(dx) == abs(dy) and 0 <= abs(dy) <= 3)) and (z <= self.z)
                case 2:
                    return ((abs(dx) == abs(dy) and 0 <= abs(dy) <= 4)) and (z <= self.z)
        elif self.name == "砦":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and -1 <= dy <= 0) or (0 <= abs(dx) <= 1 and dy == 0) or (abs(dx) == abs(dy) and 0 <= dy <= 1)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and -2 <= dy <= 0) or (0 <= abs(dx) <= 2 and dy == 0) or (abs(dx) == abs(dy) and 0 <= dy <= 2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and -3 <= dy <= 0) or (0 <= abs(dx) <= 3 and dy == 0) or (abs(dx) == abs(dy) and 0 <= dy <= 3)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and 0 <= dy <= 1) or (0 <= abs(dx) <= 1 and dy == 0) or (abs(dx) == abs(dy) and -1 <= dy <= 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= dy <= 2) or (0 <= abs(dx) <= 2 and dy == 0) or (abs(dx) == abs(dy) and -2 <= dy <= 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <= dy <= 3) or (0 <= abs(dx) <= 3 and dy == 0) or (abs(dx) == abs(dy) and -3 <= dy <= 0)) and (z <= self.z)
        elif self.name == "兵":
            match self.z:
                case 0:
                    return ((dx == 0 and abs(dy) == 1)) and (z <= self.z)
                case 1:
                    return ((dx == 0 and 0 <= abs(dy) <= 2)) and (z <= self.z)
                case 2:
                    return ((dx == 0 and 0 <= abs(dy) <= 3)) and (z <= self.z)
        elif self.name == "砲":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and dy == -3) or (dx == 0 and 0 <= dy <= 1) or (0 <= abs(dx) <= 1 and dy == 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and -4 <= dy <= -3) or (dx == 0 and 0 <= dy <= 2) or (0 <= abs(dx) <= 2 and dy == 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and -5 <= dy <= -3) or (dx == 0 and 0 <= dy <= 3) or (0 <= abs(dx) <= 3 and dy == 0)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and dy == 3) or (dx == 0 and -1 <= dy <= 0) or (0 <= abs(dx) <= 1 and dy == 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 3 <= dy <= 4) or (dx == 0 and -2 <= dy <= 0) or (0 <= abs(dx) <= 2 and dy == 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 3 <= dy <= 5) or (dx == 0 and -3 <= dy <= 0) or (0 <= abs(dx) <= 3 and dy == 0)) and (z <= self.z)
        elif self.name == "弓":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and dy == -2) or (dx == 0 and 0 <= dy <= 1) or (abs(dx) + 1 == abs(dy) and dy == -2)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and -3 <= dy <= -2) or (dx == 0 and 0 <= dy <= 2) or (abs(dx) + 1 == abs(dy) and -3 <= dy <= -2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and -4 <= dy <= -2) or (dx == 0 and 0 <= dy <= 3) or (abs(dx) + 1 == abs(dy) and -4 <= dy <= -2)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and dy == 2) or (dx == 0 and -1 <= dy <= 0) or (abs(dx) + 1 == abs(dy) and dy == 2)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 2 <= dy <= 3) or (dx == 0 and -2 <= dy <= 0) or (abs(dx) + 1 == abs(dy) and 2 <= dy <= 3)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 2 <= dy <= 4) or (dx == 0 and -3 <= dy <= 0) or (abs(dx) + 1 == abs(dy) and 2 <= dy <= 4)) and (z <= self.z)
        elif self.name == "筒":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and dy == -2) or (abs(dx) == abs(dy) and 0 <= dy <= 1)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and -3 <= dy <= -2) or (abs(dx) == abs(dy) and 0 <= dy <= 2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and -4 <= dy <= -2) or (abs(dx) == abs(dy) and 0 <= dy <= 3)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and dy == 2) or (abs(dx) == abs(dy) and -1 <= dy <= 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 2 <= dy <= 3) or (abs(dx) == abs(dy) and -2 <= dy <= 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 2 <= dy <= 4) or (abs(dx) == abs(dy) and -3 <= dy <= 0)) and (z <= self.z)
        elif self.name == "謀":
            if self.owner == 0:
                match self.z:
                    case 0:
                        return ((dx == 0 and 0 <= dy <= 1) or (abs(dx) == abs(dy) and -1 <= dy <= 0)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and 0 <= dy <= 2) or (abs(dx) == abs(dy) and -2 <= dy <= 0)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and 0 <= dy <= 3) or (abs(dx) == abs(dy) and -3 <= dy <= 0)) and (z <= self.z)
            else:
                match self.z:
                    case 0:
                        return ((dx == 0 and -1 <= dy <= 0) or (abs(dx) == abs(dy) and 0 <= dy <= 1)) and (z <= self.z)
                    case 1:
                        return ((dx == 0 and -2 <= dy <= 0) or (abs(dx) == abs(dy) and 0 <= dy <= 2)) and (z <= self.z)
                    case 2:
                        return ((dx == 0 and -3 <= dy <= 0) or (abs(dx) == abs(dy) and 0 <= dy <= 3)) and (z <= self.z)