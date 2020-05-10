import os.path
import sys
from collections import defaultdict
from datetime import datetime
from logging import getLogger
from threading import Thread
from time import sleep

import mychess.environment.static_env as senv
from mychess.agent.model import CChessModel
from mychess.agent.player import CChessPlayer, VisitState
# from mychess.agent.api import CChessModelAPI
from mychess.config import Config
# from mychess.environment.chessboard import Chessboard
from mychess.environment.env import CChessEnv
from mychess.environment.lookup_tables import Winner, ActionLabelsRed, flip_move
from mychess.lib.logger import setup_logger
from mychess.lib.model_helper import load_best_model_weight
from mychess.play_games.MySQLTool import *
from mychess.play_games.colorAndUIModule import *
from mychess.play_games.tool import *

# from mychess.lib.tf_util import set_session_config

logger = getLogger(__name__)
main_dir = os.path.split(os.path.abspath(__file__))[0]  # play_games/


def start(config: Config, human_move_first=True):
    # global PIECE_STYLE
    # PIECE_STYLE = config.opts.piece_style
    sys.setrecursionlimit(10000)
    setup_logger(config.resource.play_log_path)  # in log/play.log
    play = PlayWithHuman(config)
    play.start(human_move_first)  # to line 101

class PlayWithHuman:
    def __init__(self, config: Config):
        self.config = config
        self.env = CChessEnv()
        self.model = None
        self.pipe = None
        self.ai = None
        self.winstyle = 0
        self.chessmans = None
        self.human_move_first = True
        self.screen_width = 720
        self.height = 577
        self.width = 521
        self.chessman_w = 58
        self.chessman_h = 58
        self.disp_record_num = 15  # the num of records to display
        self.rec_labels = [None] * self.disp_record_num
        self.nn_value = 0
        self.mcts_moves = {}
        self.history = []
        self.has_resign = 0
        self.path = None

    def load_model(self):
        self.model = CChessModel(self.config)       # in cchess_ahphazero/agent/model.py

        # load_best_model_weight(self.model) : return model.load(model.config.resource.model_best_config_path, model.config.resource.model_best_weight_path);
        if self.config.opts.new or not load_best_model_weight(self.model):
            self.model.build()


    def start(self, human_first=True):

        screen, board_background, widget_background, buttonList = self.init_screen()
        self.env.reset()
        # chessmans sprite group
        self.chessmans = pygame.sprite.Group()
        creat_sprite_group(self.chessmans,
                           self.env.board.chessmans_hash,
                           self.chessman_w,
                           self.chessman_h)  # 棋盘放置棋子
        pygame.display.update()

        # update all the sprites
        self.chessmans.update()
        self.chessmans.draw(screen)
        pygame.display.update()
        framerate = pygame.time.Clock()

        self.load_model()
        self.pipe = self.model.get_pipes()  # agent/model.get_pipes()
        self.ai = CChessPlayer(self.config,
                               search_tree=defaultdict(VisitState),
                               pipes=self.pipe,
                               enable_resign=True,
                               debugging=True)  # ai的config 是 self.config.play
        self.human_move_first = human_first

        labels = ActionLabelsRed
        labels_n = len(ActionLabelsRed)

        if human_first:
            self.env.board.calc_chessmans_moving_list()

        ai_worker = Thread(target=self.ai_move, name="ai_worker")
        ai_worker.daemon = True
        ai_worker.start()

        # 用于记录当前选中的棋子
        current_chessman = None

        while not self.env.board.is_end() and not self.has_resign:
            for event in pygame.event.get():  # 处理事件
                if event.type == pygame.QUIT:  # 退出
                    self.env.board.print_record()  # 打印记录
                    self.ai.close(wait=False)
                    game_id = datetime.now().strftime("%Y%m%d-%H%M%S")
                    self.path = os.path.join(self.config.resource.play_record_dir,
                                             self.config.resource.play_record_filename_tmpl % game_id)
                    self.env.board.save_record(self.path)
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    pass
                elif event.type == MOUSEBUTTONDOWN:         # 处理鼠标事件
                    if human_first == self.env.red_to_move:  # 判断是不是该自己走棋/操作
                        pressed_array = pygame.mouse.get_pressed()
                        # for index in range(len(pressed_array)):
                        if pressed_array[0]:
                            mouse_x, mouse_y = pygame.mouse.get_pos()

                            # 处理认输和悔棋
                            if buttonList[0].isInRect(mouse_x, mouse_y, self.width):
                                logger.info('click withdraw')
                                record = self.env.board.record
                                sep = '\n'
                                # reset
                                self.env.reset()
                                self.chessmans.empty()
                                creat_sprite_group(self.chessmans,
                                                   self.env.board.chessmans_hash,
                                                   self.chessman_w,
                                                   self.chessman_h)  # 棋盘放置棋子
                                self.history = [self.env.get_state()]

                                moveList = self.env.board.getMoveList(record, sep)
                                if len(moveList) == 0:
                                    break
                                cnt = 0
                                for move in moveList:
                                    if move[-1] == '.':
                                        continue
                                    cnt += 1  # cnt % 2 == 1: 红方行; 否则黑方行动
                                    # print(move)
                                    old_x, old_y, x, y = self.env.board.record_to_move(move, cnt % 2)
                                    current_chessman = select_sprite_from_group(self.chessmans, old_x, old_y)
                                    chessman_sprite = select_sprite_from_group(self.chessmans, x, y)
                                    moveString = str(old_x) + str(old_y) + str(x) + str(y)
                                    success = current_chessman.move(x, y)
                                    if cnt % 2 == 0:
                                        moveString = flip_move(moveString)
                                    self.history.append(moveString)

                                    # print(f'old_x:{old_x}, old_y:{old_y}, x:{x}, y:{y}\t success:{success}')
                                    if success:
                                        if chessman_sprite != None:
                                            self.chessmans.remove(chessman_sprite)
                                            chessman_sprite.kill()
                                        self.history.append(self.env.get_state())
                                    else:
                                        logger.error('record to move did not success')
                                for i in self.history:
                                    print('print history after withdraw:', i)
                                break

                            if buttonList[1].isInRect(mouse_x, mouse_y, self.width):
                                logger.info('click resign')
                                self.has_resign = 1
                                break

                            col_num, row_num = translate_hit_area(mouse_x, mouse_y, self.chessman_w, self.chessman_h)
                            chessman_sprite = select_sprite_from_group(self.chessmans, col_num, row_num)

                            if current_chessman is None and chessman_sprite != None:  # 从未选中棋子->选中棋子
                                if chessman_sprite.chessman.is_red == self.env.red_to_move:  # 点击的是己方棋子
                                    current_chessman = chessman_sprite
                                    chessman_sprite.is_selected = True  # 设置当前棋子为选中
                            elif current_chessman != None and chessman_sprite != None:  # 选中第二枚棋子
                                if chessman_sprite.chessman.is_red == self.env.red_to_move:  # 第二枚是己方的棋子， 更新已选中的棋子
                                    current_chessman.is_selected = False
                                    current_chessman = chessman_sprite
                                    chessman_sprite.is_selected = True
                                else:                                                           # 其它情况： 第二个点是空白处 or 对方棋子
                                    move = str(current_chessman.chessman.col_num) + str(current_chessman.chessman.row_num) +\
                                           str(col_num) + str(row_num)                          # a string
                                    success = current_chessman.move(col_num, row_num)         # 调用 move, return true or false
                                    self.history.append(move)               # 更新记录
                                    if success:
                                        self.chessmans.remove(chessman_sprite)
                                        chessman_sprite.kill()
                                        current_chessman.is_selected = False
                                        current_chessman = None
                                        self.history.append(self.env.get_state())
                            elif current_chessman != None and chessman_sprite is None:
                                move = str(current_chessman.chessman.col_num) + str(
                                    current_chessman.chessman.row_num) + str(col_num) + str(row_num)
                                success = current_chessman.move(col_num, row_num)  # chessman sprite的move
                                self.history.append(move)
                                if success:
                                    current_chessman.is_selected = False
                                    current_chessman = None
                                    self.history.append(self.env.get_state())

            self.draw_widget(screen, widget_background, buttonList)
            framerate.tick(60)  # 20
            # clear/erase the last drawn sprites
            self.chessmans.clear(screen, board_background)  # draw a background over the Sprites

            # update all the sprites
            self.chessmans.update()
            self.chessmans.draw(screen)
            pygame.display.update()

        self.ai.close(wait=False)

        if self.has_resign == 1:
            self.env.board.winner = Winner.black

        logger.info(f"Winner is {self.env.board.winner} !!!")
        self.env.board.print_record()
        game_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.path = os.path.join(self.config.resource.play_record_dir,
                                 self.config.resource.play_record_filename_tmpl % game_id)
        self.env.board.save_record(self.path)
        conn = set_conn()
        success = insert_a_record(conn, self.env.board.winner, self.path)
        if success:
            print('insert to database success')
        else:
            print('insert to database fail')
        conn.close()
        sleep(3)

    def init_screen(self):
        bestdepth = pygame.display.mode_ok([self.screen_width, self.height], self.winstyle, 32)
        screen = pygame.display.set_mode([self.screen_width, self.height], self.winstyle, bestdepth)
        pygame.display.set_caption("中国象棋")

        # create the background, tile the background image
        bgdtile = load_image(f'{self.config.opts.bg_style}.GIF')
        bgdtile = pygame.transform.scale(bgdtile, (self.width, self.height))
        board_background = pygame.Surface([self.width, self.height])
        board_background.blit(bgdtile, (0, 0))
        widget_background = pygame.Surface([self.screen_width - self.width, self.height])
        white_rect = Rect(0, 0, self.screen_width - self.width, self.height)
        widget_background.fill((255, 255, 255), white_rect)

        # create text label
        font_file = self.config.resource.font_path  # PingFang.ttc
        font = pygame.font.Font(font_file, 16)
        font_color = (0, 0, 0)
        font_background = (255, 255, 255)
        t = font.render("着法记录", True, font_color, font_background)
        t_rect = t.get_rect()
        t_rect.x = 10
        t_rect.y = 40  # 10
        widget_background.blit(t, t_rect)

        button_withdraw = myButton(Rect(0, 0, 70, 20), '悔棋', bkgColor=button_color)
        button_resign = myButton(Rect(0, 0, 70, 20), '认输', bkgColor=red)
        tem = self.screen_width - self.width
        button_withdraw.set_rect(tem // 7 * 2, 20)
        button_resign.set_rect(tem // 7 * 5, 20)
        widget_background.blit(button_withdraw.get_Surface(), button_withdraw.get_rect())
        widget_background.blit(button_resign.get_Surface(), button_resign.get_rect())
        buttonList = [button_withdraw, button_resign]

        screen.blit(board_background, (0, 0))
        screen.blit(widget_background, (self.width, 0))
        pygame.display.flip()
        return screen, board_background, widget_background, buttonList

    def ai_move(self):
        ai_move_first = not self.human_move_first
        self.history = [self.env.get_state()]  # 当前棋盘的fen表示    # 其实是棋盘初始化后 对自己的初始化
        no_act = None
        while not self.env.done:  # 棋局没结束
            if ai_move_first == self.env.red_to_move:  # 判断是不是ai走棋
                labels = ActionLabelsRed
                labels_n = len(ActionLabelsRed)

                self.ai.search_results = {}
                state = self.env.get_state()
                logger.info(f"state = {state}")  # logger 当前搜索的局面
                _, _, _, check = senv.done(state, need_check=True)  # if check == false: game not end
                # 对历史中对每一个局面计算 no_act表
                if not check and state in self.history[:-1]:  # self.history[:-1] 是历史中出现过的局面
                    no_act = []  # 禁止走步表 列表
                    free_move = defaultdict(int)  # 一个字典

                    for i in range(len(self.history) - 1):
                        if self.history[i] == state:
                            # 如果走了下一步是将军或捉：禁止走那步
                            if senv.will_check_or_catch(state, self.history[i + 1]):
                                no_act.append(self.history[i + 1])

                            # 否则当作闲着处理
                            else:
                                free_move[state] += 1
                                if free_move[state] >= 2:
                                    # 作和棋处理
                                    self.env.winner = Winner.draw
                                    self.env.board.winner = Winner.draw
                                    break
                    if no_act:
                        logger.debug(f"no_act = {no_act}")
                print('computer starts thinking!!!')
                action, policy = self.ai.action(state, self.env.num_halfmoves, no_act)
                print('computer finishs thinking!!!')

                if action is None:
                    logger.info("AI has resigned!")
                    return
                self.history.append(action)
                for i in self.history:
                    print('print history:', i)
                if not self.env.red_to_move:
                    action = flip_move(action)

                key = self.env.get_state()
                p, v = self.ai.debug[key]
                logger.info(f"check = {check}, NN value = {v:.3f}")
                self.nn_value = v

                logger.info("MCTS results:")
                self.mcts_moves = {}
                for move, action_state in self.ai.search_results.items():
                    move_cn = self.env.board.make_single_record(int(move[0]), int(move[1]), int(move[2]), int(move[3]))
                    logger.info(f"move: {move_cn}-{move}, visit count: {action_state[0]}, Q_value: {action_state[1]:.3f}, Prior: {action_state[2]:.3f}")
                    self.mcts_moves[move_cn] = action_state

                x0, y0, x1, y1 = int(action[0]), int(action[1]), int(action[2]), int(action[3])
                chessman_sprite = select_sprite_from_group(self.chessmans, x0, y0)
                sprite_dest = select_sprite_from_group(self.chessmans, x1, y1)
                if sprite_dest:
                    self.chessmans.remove(sprite_dest)
                    sprite_dest.kill()
                chessman_sprite.move(x1, y1, self.chessman_w, self.chessman_h)
                self.history.append(self.env.get_state())

    def draw_widget(self, screen, widget_background, buttonList: list):
        white_rect = Rect(0, 0, self.screen_width - self.width, self.height)
        widget_background.fill((255, 255, 255), white_rect)
        pygame.draw.line(widget_background, (255, 0, 0), (10, 285), (self.screen_width - self.width - 10, 285))
        screen.blit(widget_background, (self.width, 0))

        if buttonList == None:
            print('error, buttonList is not defined!')
            logger.error('buttonList is not defined! line in play_games/play.py: draw widget')
            sys.exit()
        widget_background.blit(buttonList[0].get_Surface(), buttonList[0].get_rect())
        widget_background.blit(buttonList[1].get_Surface(), buttonList[1].get_rect())

        self.draw_records(screen, widget_background)
        self.draw_evaluation(screen, widget_background)

    def draw_records(self, screen, widget_background):
        text = '着法记录'
        self.draw_label(screen, widget_background, text, 40, 16, 10)  # 10, 16, 10
        records = self.env.board.record.split('\n')
        font_file = self.config.resource.font_path
        font = pygame.font.Font(font_file, 12)

        i = 0
        for record in records[-self.disp_record_num:]:
            self.rec_labels[i] = font.render(record, True, (0, 0, 0), (255, 255, 255))
            t_rect = self.rec_labels[i].get_rect()
            # t_rect.centerx = (self.screen_width - self.width) / 2
            t_rect.y = 65 + i * 15  # 35 + i * 35
            t_rect.x = 10
            t_rect.width = self.screen_width - self.width
            widget_background.blit(self.rec_labels[i], t_rect)
            i += 1
        screen.blit(widget_background, (self.width, 0))

    def draw_evaluation(self, screen, widget_background):
        title_label = 'CC-Zero信息'
        self.draw_label(screen, widget_background, title_label, 300, 16, 10)
        info_label = f'MCTS搜索次数：{self.config.play.simulation_num_per_move}'
        self.draw_label(screen, widget_background, info_label, 335, 14, 10)
        eval_label = f"当前局势评估: {self.nn_value:.3f}"
        self.draw_label(screen, widget_background, eval_label, 360, 14, 10)
        label = f"MCTS搜索结果:"
        self.draw_label(screen, widget_background, label, 395, 14, 10)
        label = f"着法 访问计数 动作价值 先验概率"
        self.draw_label(screen, widget_background, label, 415, 12, 10)
        i = 0
        tmp = copy.deepcopy(self.mcts_moves)
        for mov, action_state in tmp.items():
            label = f"{mov}"
            self.draw_label(screen, widget_background, label, 435 + i * 20, 12, 10)
            label = f"{action_state[0]}"
            self.draw_label(screen, widget_background, label, 435 + i * 20, 12, 70)
            label = f"{action_state[1]:.2f}"
            self.draw_label(screen, widget_background, label, 435 + i * 20, 12, 100)
            label = f"{action_state[2]:.3f}"
            self.draw_label(screen, widget_background, label, 435 + i * 20, 12, 150)
            i += 1

    def draw_label(self, screen, widget_background, text, y, font_size, x=None):
        font_file = self.config.resource.font_path
        font = pygame.font.Font(font_file, font_size)
        label = font.render(text, True, (0, 0, 0), (255, 255, 255))
        t_rect = label.get_rect()
        t_rect.y = y
        if x != None:
            t_rect.x = x
        else:
            t_rect.centerx = (self.screen_width - self.width) / 2
        widget_background.blit(label, t_rect)
        screen.blit(widget_background, (self.width, 0))
