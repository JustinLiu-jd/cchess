import argparse
import multiprocessing as mp
from mychess.lib.logger import setup_logger
from mychess.config import Config, PlayWithHumanConfig
from logging import getLogger

logger = getLogger(__name__)

CMD_LIST = ['play', 'history']              # 增加了history
RANDOM_LIST = ['none', 'small', 'medium', 'large']

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="what to do", choices=CMD_LIST)
    parser.add_argument("--random", help="choose a style of randomness", choices=RANDOM_LIST, default="none")
    parser.add_argument("--type", help="use normal setting", default="mini")
    parser.add_argument("--ucci", help="play with ucci engine instead of self play", action="store_true")
    # parser.add_argument("--new", help="run from new best model", action="store_true")
    parser.add_argument("--total-step", help="set TrainerConfig.start_total_steps", type=int)
    parser.add_argument("--ai-move-first", help="set human or AI move first", action="store_true")
    # parser.add_argument("--cli", help="play with AI with CLI, default with GUI", action="store_true")
    parser.add_argument("--gpu", help="device list", default="0")
    # parser.add_argument("--onegreen", help="train sl work with onegreen data", action="store_true")
    # parser.add_argument("--skip", help="skip games", default=0, type=int)
    # parser.add_argument("--piece-style", help="choose a style of piece", choices=PIECE_STYLE_LIST, default="WOOD")
    # parser.add_argument("--bg-style", help="choose a style of board", choices=BG_STYLE_LIST, default="WOOD")
    # parser.add_argument("--distributed", help="whether upload/download file from remote server", action="store_true")
    # parser.add_argument("--elo", help="whether to compute elo score", action="store_true")
    return parser

def setup(config: Config, args):
    # config.opts.new = args.new
    if args.total_step is not None:
        config.trainer.start_total_steps = args.total_step      # configs/mini.py line 60: self.start_total_steps = 0
    config.opts.device_list = args.gpu
    config.resource.create_directories()
    if args.cmd == 'self':
        setup_logger(config.resource.main_log_path)  # in log/main.log
    elif args.cmd == 'play':
        setup_logger(config.resource.play_log_path)     # in log/play.log


def start():
    parser = create_parser()
    args = parser.parse_args()
    config_type = args.type         # default 'mini'
    # print(config_type)
    # exit()
    config = Config(config_type=config_type)        # config = mini-config
    setup(config, args)     # set logger total_step

    logger.info('Config type: %s' % (config_type))
    # config.opts.piece_style = args.piece_style
    # config.opts.bg_style = args.bg_style
    config.opts.piece_style = 'WOOD'
    config.opts.bg_style = 'WOOD'
    config.internet.distributed = False
    print(config.opts.piece_style, config.opts.bg_style, 'from manager.py line 64')

    # use multiple GPU
    gpus = config.opts.device_list.split(',')
    if len(gpus) > 1:
        config.opts.use_multiple_gpus = True
        config.opts.gpu_num = len(gpus)
        logger.info(f"User GPU {config.opts.device_list}")

    if args.cmd == 'play':
        from mychess.play_games import play
        config.opts.light = False

        pwhc = PlayWithHumanConfig()
        pwhc.update_play_config(config.play)        # update the config from configs/mini.py line 33: PlayConfig
        logger.info(f"AI move first : {args.ai_move_first}")
        play.start(config, not args.ai_move_first)

    # elif args.cmd == 'self':
        #     if args.ucci:
        #         import mychess.worker.play_with_ucci_engine as self_play
        #     else:
        #         if mp.get_start_method() == 'spawn':
        #             import mychess.worker.self_play_windows as self_play
        #         else:
        #             from mychess.worker import self_play
        #     return self_play.start(config)
        # elif args.cmd == 'opt':
        #     from cchess_alphazero.worker import optimize
        #     return optimize.start(config)



