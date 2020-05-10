import os.path

from mychess.play_games.play import *

logger = getLogger(__name__)
main_dir = os.path.split(os.path.abspath(__file__))[0]  # play_games/


def repeatMode(record: str):
    print(record)
    config = Config(config_type='mini')
    sys.setrecursionlimit(10000)
    setup_logger(config.resource.play_log_path)  # in log/play.log
    game = repeatGame(config)
    game.start(savedRecord=record)

    pass


class repeatGame:
    def __init__(self, config: Config):
        self.config = config
        self.env = CChessEnv()
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
        self.history = []

    def load_model(self):
        self.model = CChessModel(self.config)  # in cchess_ahphazero/agent/model.py

        # load_best_model_weight(self.model) : return model.load(model.config.resource.model_best_config_path, model.config.resource.model_best_weight_path);
        if self.config.opts.new or not load_best_model_weight(self.model):
            self.model.build()

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

    def start(self, human_first=True, savedRecord: str = ''):
        screen, board_background, widget_background = self.init_screen()
        self.env.reset()
        # chessmans sprite group
        self.chessmans = pygame.sprite.Group()
        creat_sprite_group(self.chessmans, self.env.board.chessmans_hash, self.chessman_w, self.chessman_h)  # 棋盘放置棋子
        pygame.display.update()

        # update all the sprites
        self.chessmans.update()
        self.chessmans.draw(screen)
        pygame.display.update()
        framerate = pygame.time.Clock()

        self.history = [self.env.get_state()]
        moveList = savedRecord.split()
        cnt = 0
        for move in moveList:
            if move[-1] == '.':
                continue
            cnt += 1  # cnt % 2 == 1: 红方行; 否则黑方行动
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
            print('print history after repeat mode init:', i)

        # self.draw_widget(screen, widget_background)
        framerate.tick(60)  # 20
        # clear/erase the last drawn sprites
        self.chessmans.clear(screen, board_background)  # draw a background over the Sprites
        # update all the sprites
        self.chessmans.update()
        self.chessmans.draw(screen)
        pygame.display.update()

        while not self.env.board.is_end():
            for event in pygame.event.get():  # 处理事件
                if event.type == pygame.QUIT:  # 退出
                    self.env.board.print_record()  # 打印记录
                    # self.ai.close(wait=False)
                    game_id = datetime.now().strftime("%Y%m%d-%H%M%S")
                    self.path = os.path.join(self.config.resource.play_record_dir,
                                             self.config.resource.play_record_filename_tmpl % game_id)
                    self.env.board.save_record(self.path)
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    pass
