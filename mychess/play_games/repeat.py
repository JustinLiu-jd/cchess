import os.path

from mychess.play_games.play import *

logger = getLogger(__name__)
main_dir = os.path.split(os.path.abspath(__file__))[0]  # play_games/


def repeatMode(record: str):
    print(record)
    config = Config(config_type='mini')
    sys.setrecursionlimit(10000)
    setup_logger(config.resource.play_log_path)  # in log/play.log
    game = repeatGame(config, savedRecord=record)
    game.start()

    pass


class repeatGame:
    def __init__(self, config: Config, savedRecord: str):
        self.config = config
        self.savedRecord = savedRecord
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
        self.disp_cnt_num = 8  # the num of records to display in Green
        self.rec_labels = [None] * self.disp_record_num
        self.has_resign = 0
        self.history = []
        self.cnt = 0
        self.chooseToStart = 0

    def load_model(self):
        self.model = CChessModel(self.config)  # in cchess_ahphazero/agent/model.py

        # load_best_model_weight(self.model) : return model.load(model.config.resource.model_best_config_path, model.config.resource.model_best_weight_path);
        if self.config.opts.new or not load_best_model_weight(self.model):
            self.model.build()

    def init_screen(self):
        bestdepth = pygame.display.mode_ok([self.screen_width, self.height], self.winstyle, 32)
        screen = pygame.display.set_mode([self.screen_width, self.height], self.winstyle, bestdepth)
        pygame.display.set_caption("中国象棋-复盘模式")

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
        t_rect.y = 40
        widget_background.blit(t, t_rect)

        button_withdraw = myButton(Rect(0, 0, 70, 20), '悔棋', bkgColor=button_color)
        button_resign = myButton(Rect(0, 0, 70, 20), '认输', bkgColor=red)
        tem = self.screen_width - self.width
        button_withdraw.set_rect(tem // 7 * 2, 20)
        button_resign.set_rect(tem // 7 * 5, 20)
        # widget_background.blit(button_withdraw.get_Surface(), button_withdraw.get_rect())
        # widget_background.blit(button_resign.get_Surface(), button_resign.get_rect())

        f_button = myButton(Rect(0, 0, 50, 20), '下一步', bkgColor=button_color)
        b_button = myButton(Rect(0, 0, 50, 20), '上一步', bkgColor=button_color)
        c_button = myButton(Rect(0, 0, 50, 20), '选择', bkgColor=button_color)
        b_button.set_rect(tem // 10 * 2, 20)
        f_button.set_rect(tem // 10 * 5, 20)
        c_button.set_rect(tem // 10 * 8, 20)
        widget_background.blit(b_button.get_Surface(), b_button.get_rect())
        widget_background.blit(f_button.get_Surface(), f_button.get_rect())
        widget_background.blit(c_button.get_Surface(), c_button.get_rect())

        buttonList = [button_withdraw, button_resign, b_button, f_button, c_button]

        screen.blit(board_background, (0, 0))
        screen.blit(widget_background, (self.width, 0))
        pygame.display.flip()
        return screen, board_background, widget_background, buttonList

    def start(self, human_first=True):
        savedRecord = self.savedRecord
        screen, board_background, widget_background, buttonList = self.init_screen()
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
        temList = savedRecord.split()
        moveList = []
        for t in temList:
            if t[-1] != '.':
                moveList.append(t)
        for move in moveList:
            print(move)
        self.cnt = 0  # 值为0时，一步都不走; 值为1时，执行moveList[0]    即执行moveList[self.cnt - 1]

        while not self.chooseToStart:
            for event in pygame.event.get():  # 处理事件
                if event.type == pygame.QUIT:  # 退出
                    # 因为只是观看历史棋局 目前无操作 所以直接退出即可
                    sys.exit()
                elif event.type == VIDEORESIZE:
                    pass
                elif event.type == MOUSEBUTTONDOWN:  # 处理鼠标事件
                    pressed_array = pygame.mouse.get_pressed()
                    if pressed_array[0]:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        # buttonList[2:5] 分别是前一步 后一步 和 选择 按钮
                        if buttonList[2].isInRect(mouse_x, mouse_y, self.width):  # 由于固定在widget上,x坐标上有偏移
                            self.cnt = max(0, self.cnt - 1)
                        elif buttonList[3].isInRect(mouse_x, mouse_y, self.width):  # 由于固定在widget上,x坐标上有偏移
                            if self.cnt + 1 > len(moveList):
                                break
                            self.cnt = min(len(moveList), self.cnt + 1)
                            move = moveList[self.cnt - 1]
                            if move[-1] == u"降":
                                break
                            old_x, old_y, x, y = self.env.board.record_to_move(move, self.cnt % 2)
                            current_chessman = select_sprite_from_group(self.chessmans, old_x, old_y)
                            chessman_sprite = select_sprite_from_group(self.chessmans, x, y)
                            moveString = str(old_x) + str(old_y) + str(x) + str(y)
                            success = current_chessman.move(x, y)
                            if self.cnt % 2 == 0:
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

                        elif buttonList[4].isInRect(mouse_x, mouse_y, self.width):  # 由于固定在widget上,x坐标上有偏移
                            chooseToStart = 1

            self.draw_widget(screen, widget_background, buttonList)
            # clear/erase the last drawn sprites
            self.chessmans.clear(screen, board_background)  # draw a background over the Sprites
            # update all the sprites
            self.chessmans.update()
            self.chessmans.draw(screen)
            pygame.display.update()

        # for move in moveList:
        #     self.cnt += 1  # self.cnt % 2 == 1: 红方行; 否则黑方行动
        #     old_x, old_y, x, y = self.env.board.record_to_move(move, self.cnt % 2)
        #     current_chessman = select_sprite_from_group(self.chessmans, old_x, old_y)
        #     chessman_sprite = select_sprite_from_group(self.chessmans, x, y)
        #     moveString = str(old_x) + str(old_y) + str(x) + str(y)
        #     success = current_chessman.move(x, y)
        #     if self.cnt % 2 == 0:
        #         moveString = flip_move(moveString)
        #     self.history.append(moveString)
        #
        #     # print(f'old_x:{old_x}, old_y:{old_y}, x:{x}, y:{y}\t success:{success}')
        #     if success:
        #         if chessman_sprite != None:
        #             self.chessmans.remove(chessman_sprite)
        #             chessman_sprite.kill()
        #         self.history.append(self.env.get_state())
        #     else:
        #         logger.error('record to move did not success')
        # for i in self.history:
        #     print('print history after repeat mode init:', i)
        #
        # # self.draw_widget(screen, widget_background)
        # framerate.tick(60)  # 20
        # # clear/erase the last drawn sprites
        # self.chessmans.clear(screen, board_background)  # draw a background over the Sprites
        # # update all the sprites
        # self.chessmans.update()
        # self.chessmans.draw(screen)
        # pygame.display.update()

        while not self.env.board.is_end():
            break
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

    def draw_widget(self, screen, widget_background, buttonList: list):
        white_rect = Rect(0, 0, self.screen_width - self.width, self.height)
        widget_background.fill((255, 255, 255), white_rect)

        if self.chooseToStart:
            pygame.draw.line(widget_background, (255, 0, 0), (10, 285), (self.screen_width - self.width - 10, 285))

        if buttonList == None:
            logger.error('buttonList is not defined! line in play_games/repeat.py: draw widget')
            sys.exit()

        if not self.chooseToStart:
            # 上一步 下一步 选择 三个按钮
            for button in buttonList[2:5]:
                widget_background.blit(button.get_Surface(), button.get_rect())
        else:
            # 撤回 认输 两个按钮
            for button in buttonList[0:2]:
                widget_background.blit(button.get_Surface(), button.get_rect())

        self.draw_records(screen, widget_background)
        if self.chooseToStart:
            self.draw_evaluation(screen, widget_background)

    def draw_records(self, screen, widget_background):
        text = '着法记录'
        self.draw_label(screen, widget_background, text, 40, 16, 10)  # 10, 16, 10
        repeatedRecords = self.env.board.record.split('\n')
        if len(repeatedRecords) == 1 and len(repeatedRecords[0]) == 0:
            repeatedRecords = []
        records = self.savedRecord.split('\n')
        # print('records:')
        # for i in records:
        #     print(i)
        # tem = []
        # for t in repeatedRecords:
        #     if t[-1] != '.':
        #         tem.append(t)
        # repeatedRecords = tem
        # tem = []
        # for t in records:
        #     if t[-1] != '.':
        #         tem.append(t)
        # records = tem
        font_file = self.config.resource.font_path
        font = pygame.font.Font(font_file, 12)

        len1 = len(repeatedRecords)
        len2 = len(records)
        # 已复现的moves <= 8行
        if len1 <= self.disp_cnt_num:
            recordList = repeatedRecords[0: len1]
            toRepeatRecordList = records[len1: self.disp_record_num]
        # 还没复现的moves <= 15 - 8 行
        elif len2 - len1 <= self.disp_record_num - self.disp_cnt_num:
            recordList = repeatedRecords[len2 - self.disp_record_num: len1]
            toRepeatRecordList = records[len1: len2]
        # 其它情况
        else:
            recordList = repeatedRecords[-self.disp_cnt_num: len1]
            toRepeatRecordList = records[len1: len1 + (self.disp_record_num - self.disp_cnt_num)]

        # for i in recordList:
        #     print('recordList:', i)
        # print('len1:', len1, 'records[len1]:', records[len1])
        # for i in repeatedRecords:
        #     print('repeatedRecords:', i, 'len(i):', len(i))
        # for i in toRepeatRecordList:
        #     print('toRepeatRecordList:', i)
        i = 0
        for record in recordList:
            self.rec_labels[i] = font.render(record, True, green, (255, 255, 255))
            t_rect = self.rec_labels[i].get_rect()
            t_rect.y = 65 + i * 15  # 35 + i * 35
            t_rect.x = 10
            t_rect.width = self.screen_width - self.width
            widget_background.blit(self.rec_labels[i], t_rect)
            i += 1

        if i and self.cnt % 2:
            record = records[len1 - 1]
            record = ' ' * (len(record) + 7) + record[-4:]
            tem = font.render(record, True, gray)
            t_rect = tem.get_rect()
            t_rect.x = 10
            t_rect.y = 65 + (i - 1) * 15  # 35 + i * 35
            t_rect.width = self.screen_width - self.width
            widget_background.blit(tem, t_rect)

        for record in toRepeatRecordList:
            self.rec_labels[i] = font.render(record, True, gray, (255, 255, 255))
            t_rect = self.rec_labels[i].get_rect()
            t_rect.y = 65 + i * 15  # 35 + i * 35
            t_rect.x = 10
            t_rect.width = self.screen_width - self.width
            widget_background.blit(self.rec_labels[i], t_rect)
            i += 1
        screen.blit(widget_background, (self.width, 0))

    def draw_evaluation(self, screen, widget_background):
        title_label = 'CC-Zero信息'

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
