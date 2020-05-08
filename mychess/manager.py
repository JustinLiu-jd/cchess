import sys
from logging import getLogger

from mychess.config import Config, PlayWithHumanConfig
from mychess.lib.logger import setup_logger
from mychess.play_games import play
from mychess.play_games import pvp
from mychess.play_games.colorAndUIModule import *
from mychess.play_games.sqlTool import *

logger = getLogger(__name__)


class game():
    def __init__(self):
        self.winstyle = 0
        self.width = 521
        self.height = 577
        self.buttonToLR = 310
        self.boardImg = None
        self.page_num = 15  # 每一页显示多少条历史棋局
        self.current_page = 0  # 表示当前是第几页
        self.max_page = 1  # 总共有几页记录
        self.label_l = 300  # 每条记录的长度
        self.label_w = 24
        self.recordButtonL = 40  # 展示记录时每个按钮的长

    def init_screen(self):
        bestdepth = pygame.display.mode_ok([self.width, self.height], self.winstyle, 32)
        # screen
        screen = pygame.display.set_mode([self.width, self.height], self.winstyle, bestdepth)
        pygame.display.set_caption("中国象棋")
        # background
        background = pygame.Surface([self.width, self.height])
        self.boardImg = pygame.image.load('mychess/play_games/images/WOOD.GIF').convert()
        background.blit(self.boardImg, (0, 0))
        # font
        font_file = 'mychess/play_games/PingFang.ttc'  # PingFang.ttc
        font = pygame.font.Font(font_file, 16)

        button0 = myButton(Rect(0, 0, 100, 40), '玩家对弈', bkgColor=button_color)
        button1 = myButton(Rect(0, 0, 100, 40), '人机模式', bkgColor=button_color)
        button2 = myButton(Rect(0, 0, 100, 40), '复盘模式', bkgColor=button_color)
        button0.set_rect(self.width // 2, self.height // 6 * 2)
        button1.set_rect(self.width // 2, self.height // 6 * 3)
        button2.set_rect(self.width // 2, self.height // 6 * 4)
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
        # pygame.display.update()
        clock = pygame.time.Clock()
        running = True
        mode = 0  # 游戏模式
        level = 0  # 人机模式的难度
        while not mode:  # loop listening for end of game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                                print(f'选中 {button0.get_text()}')
                                # logger.info(f'选中 {button0.get_text()}')
                                mode = 1
                            elif t_rect1[1] <= mouse_y <= t_rect1[1] + t_rect[3]:
                                print(f'选中 {button1.get_text()}')
                                # logger.info(f'选中 {button0.get_text()}')
                                mode = 2
                            elif t_rect2[1] <= mouse_y <= t_rect2[1] + t_rect[3]:
                                print(f'选中 {button2.get_text()}')
                                # logger.info(f'选中 {button0.get_text()}')
                                mode = 3
        if mode == 1:
            pass
            config = Config(config_type='mini')
            setup(config)
            pvp.start(config)

        elif mode == 2:
            for i in range(len(buttonList)):
                buttonList[i].set_text(text=f'难度等级 {i + 1}')
                background.blit(buttonList[i].get_Surface(), buttonList[i].get_rect())
            screen.blit(background, (0, 0))
            pygame.display.update()
            while not level:  # loop listening for end of game
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
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
                                    print(f'选中 {button0.get_text()}')
                                    # logger.info(f'选中 {button0.get_text()}')
                                    level = 1
                                elif t_rect1[1] <= mouse_y <= t_rect1[1] + t_rect[3]:
                                    print(f'选中 {button1.get_text()}')
                                    # logger.info(f'选中 {button0.get_text()}')
                                    level = 2
                                elif t_rect2[1] <= mouse_y <= t_rect2[1] + t_rect[3]:
                                    print(f'选中 {button2.get_text()}')
                                    # logger.info(f'选中 {button0.get_text()}')
                                    level = 3
            if level == 1:
                pass
            elif level == 2:
                pass

            elif level == 3:
                config = Config(config_type='mini')  # config = mini-config
                setup(config)  # set logger total_step
                pwhc = PlayWithHumanConfig()
                pwhc.update_play_config(config.play)  # update the config from configs/mini.py line 33: PlayConfig
                logger.info(f"AI move first : false")
                play.start(config)


        elif mode == 3:
            background.blit(newGame.boardImg, (0, 0))
            label = myLabel(rect=Rect(0, 0, 150, 40), text="复盘模式", bkgColor=label_color)
            label.set_rect(newGame.width // 2, 50)
            background.blit(label.get_Surface(), label.get_rect())

            delta = newGame.label_l // 10
            xList = [delta, delta * 3, delta * 7]

            tList = ['编号', '赢者', '对弈日期']
            wordLabel = myLabel(Rect(0, 0, newGame.label_l, newGame.label_w), textList=tList, xList=xList,
                                bkgColor=white, font_size=14)
            wordLabel.set_rect(newGame.width // 2 - 50, 90)
            background.blit(wordLabel.get_Surface(), wordLabel.get_rect())

            conn = set_conn()
            total_record = get_len(conn)
            newGame.max_page = (total_record // newGame.page_num) + 1

            lis = get_page(conn, newGame.current_page)
            label_lis = []
            for record in lis:
                ID = str(record['uniID'])
                winner = 'Red' if record['whoWin'] == 'Winner.red' else (
                    'Black' if record['whoWin'] == 'Winner.black' else record['whoWin'])
                time = str(record['time'])
                tList = [ID, winner, time]
                tem_label = myLabel(Rect(0, 0, newGame.label_l, newGame.label_w), textList=tList, xList=xList,
                                    bkgColor=record_color, font_size=14)
                label_lis.append(tem_label)

            for i in range(len(label_lis)):
                lab = label_lis[i]
                lab.set_rect(newGame.width // 2 - 50, 120 + i * 27)
                background.blit(lab.get_Surface(), lab.get_rect())

            delete_buttons = []
            for i in range(len(label_lis)):
                tem_button = myButton(Rect(0, 0, newGame.recordButtonL, newGame.label_w), text="删除", bkgColor=red,
                                      font_size=14)
                tem_button.set_rect(newGame.width // 2 + 140, 120 + i * 27)
                delete_buttons.append(tem_button)
                background.blit(tem_button.get_Surface(), tem_button.get_rect())

            screen.blit(background, (0, 0))
            pygame.display.update()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                pass
