import os.path
import sys
from datetime import datetime
from logging import getLogger

from mychess.config import Config
from mychess.environment.env import CChessEnv
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
        self.chessmans = None
        self.env = CChessEnv()
        self.screen_width = 720
        self.height = 577
        self.width = 521
        self.chessman_w = 57
        self.chessman_h = 57
        self.disp_record_num = 15  # the num of records to display
        self.rec_labels = [None] * self.disp_record_num

    def start(self, human_first=True):
        pass
        screen, board_background, widget_background = self.init_screen()
        self.env.reset()

        self.chessmans = pygame.sprite.Group()  # 声明精灵组
        creat_sprite_group(self.chessmans, self.env.board.chessmans_hash, self.chessman_w, self.chessman_h)  # 棋盘放置棋子
        pygame.display.update()

        # update all the sprites
        self.chessmans.update()
        self.chessmans.draw(screen)
        pygame.display.update()
        framerate = pygame.time.Clock()

        # 用于记录当前选中的棋子
        current_chessman = None

        while not self.env.board.is_end():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.env.board.print_record()  # 打印记录
                    game_id = datetime.now().strftime("%Y%m%d-%H%M%S")
                    path = os.path.join(self.config.resource.play_record_dir,
                                        self.config.resource.play_record_filename_tmpl % game_id)
                    self.env.board.save_record(path)
                    sys.exit()
                    pass
                elif event.type == MOUSEBUTTONDOWN:  # 处理鼠标事件
                    if human_first == self.env.red_to_move:
                        pass
                        pressed_array = pygame.mouse.get_pressed()
                        if pressed_array[0]:
                            mouse_x, mouse_y = pygame.mouse.get_pos()
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
                                else:  # 其它情况： 第二个点是空白处 or 对方棋子
                                    move = str(current_chessman.chessman.col_num) + str(
                                        current_chessman.chessman.row_num) + \
                                           str(col_num) + str(row_num)  # a string
                                    success = current_chessman.move(col_num, row_num)  # 调用 move, return true or false
                                    self.history.append(move)  # 更新记录
                                    if success:
                                        self.chessmans.remove(chessman_sprite)
                                        chessman_sprite.kill()
                                        current_chessman.is_selected = False
                                        current_chessman = None
                                        self.history.append(self.env.get_state())
                            elif current_chessman != None and chessman_sprite is None:
                                move = str(current_chessman.chessman.col_num) + str(
                                    current_chessman.chessman.row_num) + str(col_num) + str(row_num)
                                success = current_chessman.move(col_num, row_num, self.chessman_w,
                                                                self.chessman_h)  # chessman sprite的move
                                self.history.append(move)
                                if success:
                                    current_chessman.is_selected = False
                                    current_chessman = None
                                    self.history.append(self.env.get_state())

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
        t_rect.y = 10
        widget_background.blit(t, t_rect)

        screen.blit(board_background, (0, 0))
        screen.blit(widget_background, (self.width, 0))
        pygame.display.flip()
        return screen, board_background, widget_background
