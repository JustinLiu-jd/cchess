from mychess.environment.chessboard import Chessboard

# print(-(1 << 30))

# 红方大写 黑方小写
# 棋子子力价值
pieceValues = {
    's': 6000, 'm': 120, 'e': 120, 'r': 600, 'k': 270, 'c': 285, 'p': 30,
    'S': 6000, 'M': 120, 'E': 120, 'R': 600, 'K': 270, 'C': 285, 'P': 30
}

# 棋子位置价值
posValues = {
    'R': [
        [-2, 10, 6, 14, 12, 14, 6, 10, -2],
        [8, 4, 8, 16, 8, 16, 8, 4, 8],
        [4, 8, 6, 14, 12, 14, 6, 8, 4],
        [6, 10, 8, 14, 14, 14, 8, 10, 6],
        [12, 16, 14, 20, 20, 20, 14, 16, 12],
        [12, 14, 12, 18, 18, 18, 12, 14, 12],
        [12, 18, 16, 22, 22, 22, 16, 18, 12],
        [12, 12, 12, 18, 18, 18, 12, 12, 12],
        [16, 20, 18, 24, 26, 24, 18, 20, 16],
        [14, 14, 12, 18, 16, 18, 12, 14, 14]
    ],
    'r': [
        [14, 14, 12, 18, 16, 18, 12, 14, 14],
        [16, 20, 18, 24, 26, 24, 18, 20, 16],
        [12, 12, 12, 18, 18, 18, 12, 12, 12],
        [12, 18, 16, 22, 22, 22, 16, 18, 12],
        [12, 14, 12, 18, 18, 18, 12, 14, 12],
        [12, 16, 14, 20, 20, 20, 14, 16, 12],
        [6, 10, 8, 14, 14, 14, 8, 10, 6],
        [4, 8, 6, 14, 12, 14, 6, 8, 4],
        [8, 4, 8, 16, 8, 16, 8, 4, 8],
        [-2, 10, 6, 14, 12, 14, 6, 10, -2]
    ],
    'K': [
        [0, -4, 0, 0, 0, 0, 0, -4, 0],
        [0, 2, 4, 4, -2, 4, 4, 2, 0],
        [4, 2, 8, 8, 4, 8, 8, 2, 4],
        [2, 6, 8, 6, 10, 6, 8, 6, 2],
        [4, 12, 16, 14, 12, 14, 16, 12, 4],
        [6, 16, 14, 18, 16, 18, 14, 16, 6],
        [8, 24, 18, 24, 20, 24, 18, 24, 8],
        [12, 14, 16, 20, 18, 20, 16, 14, 12],
        [4, 10, 28, 16, 8, 16, 28, 10, 4],
        [4, 8, 16, 12, 4, 12, 16, 8, 4]
    ],
    'k': [
        [4, 8, 16, 12, 4, 12, 16, 8, 4],
        [4, 10, 28, 16, 8, 16, 28, 10, 4],
        [12, 14, 16, 20, 18, 20, 16, 14, 12],
        [8, 24, 18, 24, 20, 24, 18, 24, 8],
        [6, 16, 14, 18, 16, 18, 14, 16, 6],
        [4, 12, 16, 14, 12, 14, 16, 12, 4],
        [2, 6, 8, 6, 10, 6, 8, 6, 2],
        [4, 2, 8, 8, 4, 8, 8, 2, 4],
        [0, 2, 4, 4, -2, 4, 4, 2, 0],
        [0, -4, 0, 0, 0, 0, 0, -4, 0]
    ],
    'C': [
        [0, 0, 2, 6, 6, 6, 2, 0, 0],
        [0, 2, 4, 6, 6, 6, 4, 2, 0],
        [4, 0, 8, 6, 10, 6, 8, 0, 4],
        [0, 0, 0, 2, 4, 2, 0, 0, 0],
        [-2, 0, 4, 2, 6, 2, 4, 0, -2],
        [0, 0, 0, 2, 8, 2, 0, 0, 0],
        [0, 0, -2, 4, 10, 4, -2, 0, 0],
        [2, 2, 0, -10, -8, -10, 0, 2, 2],
        [2, 2, 0, -4, -14, -4, 0, 2, 2],
        [6, 4, 0, -10, -12, -10, 0, 4, 6]
    ],
    'c': [
        [6, 4, 0, -10, -12, -10, 0, 4, 6],
        [2, 2, 0, -4, -14, -4, 0, 2, 2],
        [2, 2, 0, -10, -8, -10, 0, 2, 2],
        [0, 0, -2, 4, 10, 4, -2, 0, 0],
        [0, 0, 0, 2, 8, 2, 0, 0, 0],
        [-2, 0, 4, 2, 6, 2, 4, 0, -2],
        [0, 0, 0, 2, 4, 2, 0, 0, 0],
        [4, 0, 8, 6, 10, 6, 8, 0, 4],
        [0, 2, 4, 6, 6, 6, 4, 2, 0],
        [0, 0, 2, 6, 6, 6, 2, 0, 0]
    ],
    'P': [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, -2, 0, 4, 0, -2, 0, 0],
        [2, 0, 8, 0, 8, 0, 8, 0, 2],
        [6, 12, 18, 18, 20, 18, 18, 12, 6],
        [10, 20, 30, 34, 40, 34, 30, 20, 10],
        [14, 26, 42, 60, 80, 60, 42, 26, 14],
        [18, 36, 56, 80, 120, 80, 56, 36, 18],
        [0, 3, 6, 9, 12, 9, 6, 3, 0]
    ],
    'p': [
        [0, 3, 6, 9, 12, 9, 6, 3, 0],
        [18, 36, 56, 80, 120, 80, 56, 36, 18],
        [14, 26, 42, 60, 80, 60, 42, 26, 14],
        [10, 20, 30, 34, 40, 34, 30, 20, 10],
        [6, 12, 18, 18, 20, 18, 18, 12, 6],
        [2, 0, 8, 0, 8, 0, 8, 0, 2],
        [0, 0, -2, 0, 4, 0, -2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
}

# 红方为正，黑方为负
def caculate(board: Chessboard):
    val = 0
    for chess in board.chessmans_hash.values():
        if chess.is_alive:      # 棋子是否存活
            x, y = chess.position.x, chess.position.y
            if chess.is_red:
                piece_val = pieceValues[chess.fen]      # 棋子本身价值
                val += piece_val
                if chess.fen in posValues.keys():
                    val += posValues[chess.fen][y][x]   # 位置价值
                if chess.fen != 'S':        # 对'帅'特殊处理
                    val += int(len(chess.moving_list) * piece_val // 400)       # 灵活度价值
                    pass
            else:
                piece_val = pieceValues[chess.fen]
                val -= piece_val
                if chess.fen in posValues.keys():
                    # print(posValues[chess.fen])
                    val -= posValues[chess.fen][y][x]
                if chess.fen != 's':        # 对'将'特殊处理
                    val -= int(len(chess.moving_list) * piece_val // 400)
                    pass
    return val, None

def caculate_base_val(board: Chessboard):
    val = 0
    for chess in board.chessmans_hash.values():
        if chess.is_alive:
            x, y = chess.position.x, chess.position.y
            if chess.is_red:
                val += pieceValues[chess.fen]       # 棋子本身价值
                if chess.fen in posValues.keys():
                    val += posValues[chess.fen][y][x]   # 棋子位置价值
            else:
                val -= pieceValues[chess.fen]
                if chess.fen in posValues.keys():
                    val -= posValues[chess.fen][y][x]
    return val, None

def caculate_flex(board: Chessboard):
    val = 0
    for chess in board.chessmans_hash.values():
        if chess.is_alive:  # 棋子是否存活
            if chess.is_red:    # 棋子阵营判断
                if chess.fen != 'S':       # 对'帅'特殊处理
                    val += int(len(chess.moving_list) * pieceValues[chess.fen] // 100) # 棋子灵活性价值
            else:
                if chess.fen != 's':
                    val -= int(len(chess.moving_list) * pieceValues[chess.fen] // 100)
    return val, None

def minimax_AB(board: Chessboard, alpha, beta, dep, base_val = 0, isBlack = True):
    # print('dep: ', dep, 'is black: ', isBlack)

    if dep == 0 or not board.get_chessman_by_name('red_king').is_alive or not board.get_chessman_by_name('black_king').is_alive:
        # calculate value
        # flex_val, _ = caculate_flex(board)
        # total_value = base_val + flex_val
        total_value, _ = caculate(board)
        return -total_value, None     # 站在黑方视角，分数要最大化，故黑方的分数为正

    search_list = []        # 产生搜索空间
    for chessman in board.chessmans_hash.values():
        if chessman.is_alive:
            chessman.clear_moving_list()
            chessman.calc_moving_list()
            if isBlack != chessman.is_red:      # 判断是否是当前层可以移动的棋子
                # print('yes')
                # print(len(chessman.moving_list), chessman.name_cn)
                for dest in chessman.moving_list:
                    search_list.append([chessman.position, dest])
    # 排序
    sort_list(search_list)

    best_move = None

    for [src, des] in search_list:
        base_val_ = base_val        # 用于迭代计算
        x0, y0, x1, y1 = src.x, src.y, des.x, des.y
        # print(x0, y0, x1, y1)
        src_chess = board.chessmans[x0][y0]     # 起子点
        des_chess = board.chessmans[x1][y1]     # 落子点
        # print('a possible move: ', src_chess.name_cn, x0, y0, '\t', x1, y1)

        # move
        board.chessmans[x1][y1] = src_chess
        src_chess.minimax_move(x1, y1)
        if src_chess.fen in posValues.keys():       # 迭代计算位置价值
            # print(base_val_, posValues[src_chess.fen][y0][x0])
            base_val_ -= posValues[src_chess.fen][y0][x0]
            base_val_ += posValues[src_chess.fen][y1][x1]
        if des_chess != None:
            des_chess.set_alive(False)
            base_val_ -= pieceValues[des_chess.fen]     # 迭代计算棋子价值
            if des_chess.fen in posValues.keys():
                base_val_ -= posValues[des_chess.fen][y1][x1]       # 迭代计算位置加深==价值

        # print('AB move success')
        # Zobrist

        if isBlack:
            isBlackToMove = False
        else:
            isBlackToMove = True
        # 递归搜索
        tem_value, _ = minimax_AB(board, -beta, -alpha, dep - 1, base_val_, isBlackToMove)

        # rollback
        board.chessmans[x0][y0] = src_chess
        board.chessmans[x1][y1] = des_chess
        src_chess.minimax_move(x0, y0)
        if des_chess != None:
            des_chess.set_alive(True)
            board.add_chessman(des_chess, x1, y1)

        # Zobrist

        # print(-tem_value, dep)
        score = -tem_value
        if score > alpha:      # 更新最优着法
            alpha = score
            best_move = [src, des]
            # 剪枝
            if score >= beta:
                return beta, best_move

    return alpha, best_move

def sort_list(lis: list):
    pass