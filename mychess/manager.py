import sys
from logging import getLogger

from mychess.config import Config, PlayWithHumanConfig
from mychess.lib.logger import setup_logger
from mychess.play_games import play
from mychess.play_games.colorAndUIModule import *

logger = getLogger(__name__)


class game():
    def __init__(self):
        self.winstyle = 0
        self.screen_width = 720
        self.height = 577
        self.buttonToLR = 310

    def init_screen(self):
        bestdepth = pygame.display.mode_ok([self.screen_width, self.height], self.winstyle, 32)
        # screen
        screen = pygame.display.set_mode([self.screen_width, self.height], self.winstyle, bestdepth)
        pygame.display.set_caption("中国象棋")
        # background
        background = pygame.Surface([self.screen_width, self.height])
        background.fill((140, 220, 254))
        # font
        font_file = 'mychess/play_games/PingFang.ttc'  # PingFang.ttc
        font = pygame.font.Font(font_file, 16)

        button0 = myButton(Rect(0, 0, 100, 40), '玩家对弈')
        button1 = myButton(Rect(0, 0, 100, 40), '人机模式')
        button2 = myButton(Rect(0, 0, 100, 40), '复盘模式')
        button0.set_rect(self.screen_width // 2, self.height // 6 * 2)
        button1.set_rect(self.screen_width // 2, self.height // 6 * 3)
        button2.set_rect(self.screen_width // 2, self.height // 6 * 4)
        background.blit(button0.get_Surface(), button0.get_rect())
        background.blit(button1.get_Surface(), button1.get_rect())
        background.blit(button2.get_Surface(), button2.get_rect())

        buttonList = [button0, button1, button2]

        screen.blit(background, (0, 0))
        pygame.display.update()
        return screen, background, buttonList


def setup(config):
    sys.setrecursionlimit(10000)
    config.opts.device_list = 0
    config.resource.create_directories()
    config.opts.piece_style = 'WOOD'
    config.opts.bg_style = 'WOOD'
    config.internet.distributed = False
    config.opts.light = False
    setup_logger(config.resource.play_log_path)  # in log/play.log


def start():
    while True:
        newGame = game()
        screen, background, buttonList = newGame.init_screen()
        clock = pygame.time.Clock()
        running = True
        mode = 0  # 游戏模式
        level = 0  # 人机模式的难度
        while running:  # loop listening for end of game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        pass
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        button0 = buttonList[0]
                        t_rect = button0.get_rect()
                        if t_rect[0] <= mouse_x <= t_rect[0] + t_rect[2]:
                            button1 = buttonList[1]
                            button2 = buttonList[2]
                            t_rect1 = button1.get_rect()
                            t_rect2 = button2.get_rect()
                            if t_rect[1] <= mouse_y <= t_rect[1] + t_rect[3]:
                                print(f'选中 {button0.get_text()} 模式')
                                # logger.info(f'选中 {button0.get_text()} 模式')
                            elif t_rect1[1] <= mouse_y <= t_rect1[1] + t_rect[3]:
                                print(f'选中 {button1.get_text()} 模式')
                                # logger.info(f'选中 {button0.get_text()} 模式')
                            elif t_rect2[1] <= mouse_y <= t_rect2[1] + t_rect[3]:
                                print(f'选中 {button2.get_text()} 模式')
                                # logger.info(f'选中 {button0.get_text()} 模式')

        config = Config(config_type='mini')  # config = mini-config
        setup(config)  # set logger total_step
        pwhc = PlayWithHumanConfig()
        pwhc.update_play_config(config.play)  # update the config from configs/mini.py line 33: PlayConfig
        logger.info(f"AI move first : false")

        play.start(config)
