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
        if chess.is_alive:
            x, y = chess.position.x, chess.position.y
            if chess.is_red:
                val += pieceValues[chess.fen]
                if chess.fen in posValues.keys():
                    val += posValues[chess.fen][y][x]
                val += len(chess.moving_list) * 2
            else:
                val -= pieceValues[chess.fen]
                if chess.fen in posValues.keys():
                    # print(posValues[chess.fen])
                    val -= posValues[chess.fen][y][x]
                val -= len(chess.moving_list) * 2
    return val, None

def caculate_base_val(board: Chessboard):
    val = 0
    for chess in board.chessmans_hash.values():
        if chess.is_alive:
            x, y = chess.position.x, chess.position.y
            if chess.is_red:
                val += pieceValues[chess.fen]
                if chess.fen in posValues.keys():
                    val += posValues[chess.fen][y][x]
            else:
                val -= pieceValues[chess.fen]
                if chess.fen in posValues.keys():
                    val -= posValues[chess.fen][y][x]
    return val, None

def caculate_flex(board: Chessboard):
    val = 0
    for chess in board.chessmans_hash.values():
        if chess.is_alive:
            if chess.is_red:
                val += len(chess.moving_list) * 2
            else:
                val -= len(chess.moving_list) * 2
    return val, None

def minimax_AB(board: Chessboard, alpha, dep, base_val = 0, isBlack = False):
    # print('dep: ', dep, 'is black: ', isBlack)

    if dep == 0:
        # calculate value
        flex_val, _ = caculate_flex(board)
        total_value = base_val + flex_val
        if isBlack:             # 对于黑方，价值取反
            return -total_value, None
        else:
            return total_value, None

    search_list = []
    for chessman in board.chessmans_hash.values():
        chessman.clear_moving_list()
        chessman.calc_moving_list()
        if chessman.is_alive and isBlack != chessman.is_red:
            # print('yes')
            # print(len(chessman.moving_list), chessman.name_cn)
            for dest in chessman.moving_list:
                search_list.append([chessman.position, dest])

    best_move = None

    for [src, des] in search_list:
        base_val_ = base_val
        x0, y0, x1, y1 = src.x, src.y, des.x, des.y
        # print(x0, y0, x1, y1)
        src_chess = board.chessmans[x0][y0]
        des_chess = board.chessmans[x1][y1]
        # print('a possible move: ', src_chess.name_cn, x0, y0, '\t', x1, y1)
        # move
        board.chessmans[x1][y1] = src_chess
        src_chess.minimax_move(x1, y1)
        if src_chess.fen in posValues.keys():
            # print(base_val_, posValues[src_chess.fen][y0][x0])
            base_val_ -= posValues[src_chess.fen][y0][x0]
            base_val_ += posValues[src_chess.fen][y1][x1]
        if des_chess != None:
            des_chess.set_alive(False)
            base_val_ -= pieceValues[des_chess.fen]
            if des_chess.fen in posValues.keys():
                base_val_ -= posValues[des_chess.fen][y1][x1]

        # print('AB move success')
        # Zobrist

        if isBlack:
            tem_value, _ = minimax_AB(board, alpha, dep - 1, base_val_, False)
        else:
            tem_value, _ = minimax_AB(board, alpha, dep - 1, base_val_, True)

        # rollback
        board.chessmans[x0][y0] = src_chess
        board.chessmans[x1][y1] = des_chess
        src_chess.minimax_move(x0, y0)
        if des_chess != None:
            board.add_chessman(des_chess, x1, y1)
            des_chess.set_alive(True)

        # Zobrist

        # print(-tem_value, dep)
        if -tem_value > alpha:      # 负极大值搜索
            alpha = -tem_value
            best_move = [src, des]

    return alpha, best_move