import os.path
import sys
from datetime import datetime
from logging import getLogger
from time import sleep

from mychess.config import Config
from mychess.environment.env import CChessEnv
from mychess.environment.lookup_tables import Winner
from mychess.play_games.MySQLTool import *
from mychess.play_games.colorAndUIModule import *
from mychess.play_games.tool import *

logger = getLogger(__name__)
PIECE_STYLE = 'WOOD'


def start(config: Config):
    pass
    new = pvp(config)
    new.start()


class pvp:
    def __init__(self, config: Config):
        self.config = config
        self.winstyle = 0
        self.chessmans = None  # will be a sprite group
        self.env = CChessEnv()
        # self.history = []
        self.screen_width = 720
        self.height = 577
        self.width = 521
        self.chessman_w = 58
        self.chessman_h = 58
        self.disp_record_num = 30  # the num of records to display      # 15
        self.rec_labels = [None] * self.disp_record_num
        self.has_resign = 0
        self.path = None

    def start(self, human_first=True):
        screen, board_background, widget_background, buttonList = self.init_screen()
        self.env.reset()

        self.chessmans = pygame.sprite.Group()  # 声明精灵组
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

        # 用于记录当前选中的棋子
        current_chessman = None  # 指向的也是chessman sprite

        while not self.env.board.is_end() and not self.has_resign:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.env.board.print_record()  # 打印记录
                    game_id = datetime.now().strftime("%Y%m%d-%H%M%S")
                    self.path = os.path.join(self.config.resource.play_record_dir,
                                             self.config.resource.play_record_filename_tmpl % game_id)
                    self.env.board.save_record(self.path)
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:  # 处理鼠标事件
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # 处理认输和悔棋
                        if buttonList[0].isInRect(mouse_x, mouse_y, self.width):
                            logger.info('click withdraw')
                            record = self.env.board.record
                            if self.env.board.is_red_turn:
                                sep = '\n'
                            else:
                                sep = '\t'
                            # reset
                            self.env.reset()
                            self.chessmans.empty()
                            creat_sprite_group(self.chessmans,
                                               self.env.board.chessmans_hash,
                                               self.chessman_w,
                                               self.chessman_h)  # 棋盘放置棋子

                            moveList = self.env.board.getMoveList(record, sep)
                            if len(moveList) == 0:
                                break
                            cnt = 0
                            for move in moveList:
                                if move[-1] == '.':
                                    continue
                                cnt += 1
                                # print(move)
                                old_x, old_y, x, y = self.env.board.record_to_move(move, cnt % 2)
                                current_chessman = select_sprite_from_group(self.chessmans, old_x, old_y)
                                chessman_sprite = select_sprite_from_group(self.chessmans, x, y)
                                success = current_chessman.move(x, y)
                                # print(f'old_x:{old_x}, old_y:{old_y}, x:{x}, y:{y}\t success:{success}')
                                if success:
                                    if chessman_sprite != None:
                                        self.chessmans.remove(chessman_sprite)
                                        chessman_sprite.kill()
                                else:
                                    logger.error('record to move did not success')
                            break

                        if buttonList[1].isInRect(mouse_x, mouse_y, self.width):
                            logger.info('click resign')
                            self.has_resign = 1 if self.env.red_to_move else 2
                            break

                        col_num, row_num = translate_hit_area(mouse_x, mouse_y, self.chessman_w, self.chessman_h)
                        chessman_sprite = select_sprite_from_group(self.chessmans, col_num, row_num)

                        if current_chessman is None and chessman_sprite != None:  # 从未选中棋子->选中棋子
                            # print(f'chessman_sprite.chessman.is_red:{chessman_sprite.chessman.is_red}, self.env.red_to_move:{self.env.red_to_move}')
                            if chessman_sprite.chessman.is_red == self.env.red_to_move:  # 点击的是己方棋子
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True  # 设置当前棋子为选中
                        elif current_chessman != None and chessman_sprite != None:  # 选中第二枚棋子
                            # print(f'选中第二枚棋子: chessman_sprite.chessman.is_red:{chessman_sprite.chessman.is_red}, self.env.red_to_move:{self.env.red_to_move}')
                            if chessman_sprite.chessman.is_red == self.env.red_to_move:  # 第二枚是己方的棋子， 更新已选中的棋子
                                current_chessman.is_selected = False
                                current_chessman = chessman_sprite
                                chessman_sprite.is_selected = True
                            else:  # 其它情况： 第二个点是空白处 or 对方棋子
                                # move = str(current_chessman.chessman.col_num) + str(
                                #     current_chessman.chessman.row_num) + \
                                #        str(col_num) + str(row_num)  # a string
                                # self.history.append(move)  # 更新记录
                                success = current_chessman.move(col_num,
                                                                row_num)  # 调用 move, return true or false; function in play_games/tool.py
                                if success:
                                    self.chessmans.remove(chessman_sprite)
                                    chessman_sprite.kill()
                                    current_chessman.is_selected = False
                                    current_chessman = None
                                    # self.history.append(self.env.get_state())
                        elif current_chessman != None and chessman_sprite is None:
                            # move = str(current_chessman.chessman.col_num) + str(
                            #     current_chessman.chessman.row_num) + str(col_num) + str(row_num)
                            # self.history.append(move)
                            success = current_chessman.move(col_num, row_num)  # chessman sprite的move
                            if success:
                                current_chessman.is_selected = False
                                current_chessman = None
                                # self.history.append(self.env.get_state())

            self.draw_widget(screen, widget_background, buttonList)
            framerate.tick(60)
            # clear/erase the last drawn sprites
            self.chessmans.clear(screen, board_background)  # draw a background over the Sprites

            # update all the sprites
            self.chessmans.update()
            self.chessmans.draw(screen)
            pygame.display.update()

        if self.has_resign:
            if self.has_resign == 1:  # 红认输，则黑赢
                self.env.board.winner = Winner.black
            else:
                self.env.board.winner = Winner.red

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

        # 认输和悔棋按钮
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

    def draw_widget(self, screen, widget_background, buttonList: list):
        white_rect = Rect(0, 0, self.screen_width - self.width, self.height)  # 标出一个Rect
        widget_background.fill((255, 255, 255), white_rect)  # 填充白色

        if buttonList == None:
            print('error, buttonList is not defined!')
            logger.error('buttonList is not defined! line in play_games/pvp.py: draw widget')
            sys.exit()
        widget_background.blit(buttonList[0].get_Surface(), buttonList[0].get_rect())
        widget_background.blit(buttonList[1].get_Surface(), buttonList[1].get_rect())

        screen.blit(widget_background, (self.width, 0))
        self.draw_records(screen, widget_background)

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
