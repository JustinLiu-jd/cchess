import copy
from logging import getLogger

import numpy as np

from mychess.environment.chessboard import Chessboard
from mychess.environment.lookup_tables import Fen_2_Idx, Winner

logger = getLogger(__name__)


class CChessEnv:

    def __init__(self, config=None):
        self.board = None
        self.winner = None
        self.num_halfmoves = 0
        self.config = config

    def reset(self, init=None):     # 可用于开启新的一局
        if self.config is None or not self.config.opts.light:       # will use heavy env
            # logger.info("Initialize heavy environment!")
            self.board = Chessboard()
            self.board.init_board()  # 摆放棋子, 放入二维数组和hash table中

        self.winner = None
        self.num_halfmoves = 0
        return self

    def update(self, board):
        self.board = board
        self.winner = None
        return self

    @property
    def done(self):
        return self.winner is not None

    @property
    def red_won(self):
        return self.winner == Winner.red

    @property
    def red_to_move(self):
        return self.board.is_red_turn

    @property
    def observation(self):
        if self.board.is_red_turn:
            return self.board.FENboard()
        else:
            return self.board.fliped_FENboard()

    def get_state(self):
        fen = self.observation
        foo = fen.split(' ')
        return foo[0]

    def step(self, action: str, check_over = True):
        if check_over and action is None:
            return

        if not self.board.move_action_str(action):
            logger.error("Move Failed, action=%s, is_red_turn=%d, board=\n%s" % (action, 
                self.red_to_move, self.board.screen))
            moves = self.board.legal_moves()
            logger.error(f"Legal moves: {moves}")
        self.num_halfmoves += 1

        if check_over and self.board.is_end():
            self.winner = self.board.winner

        self.board.clear_chessmans_moving_list()
        self.board.calc_chessmans_moving_list()

    def copy(self):
        env = copy.deepcopy(self)
        env.board = copy.deepcopy(self.board)
        return env

    def render(self, gui=False):
        if gui:
            pass
        else:
            self.board.print_to_cl()

    def input_planes(self):
        planes = self.fen_to_planes(self.observation)
        return planes

    def state_to_planes(self, state):
        planes = self.fen_to_planes(state)
        return planes

    def fen_to_planes(self, fen):
        '''
        e.g.
            rkemsmekr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RKEMSMEKR r - - 0 1
            rkemsmek1/8r/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RKEMSMEKR b - - 0 1
        '''
        planes = np.zeros(shape=(14, 10, 9), dtype=np.float32)
        foo = fen.split(' ')
        rows = foo[0].split('/')

        for i in range(len(rows)):
            row = rows[i]
            j = 0
            for letter in row:
                if letter.isalpha():
                    # 0 ~ 7 : upper, 7 ~ 14: lower
                    planes[Fen_2_Idx[letter] + int(letter.islower()) * 7][i][j] = 1
                    j += 1
                else:
                    j += int(letter)
        return planes

    def save_records(self, filename):
        self.board.save_record(filename)

