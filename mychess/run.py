import os
import sys

from logging import getLogger

logger = getLogger(__name__)

_PATH_ = os.path.dirname(os.path.dirname(__file__))
# print(_PATH_)

# print(_PATH_ in sys.path)
if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

def setup(config):
    sys.setrecursionlimit(10000)
    config.opts.device_list = 0
    config.resource.create_directories()
    config.opts.piece_style = 'WOOD'
    config.opts.bg_style = 'WOOD'
    config.internet.distributed = False
    config.opts.light = False
    setup_logger(config.resource.play_log_path)  # in log/play.log

if __name__ == "__main__":
    from mychess.play_games import play
    from mychess.lib.logger import setup_logger
    from mychess.config import Config, PlayWithHumanConfig

    config = Config(config_type='mini')  # config = mini-config
    setup(config)  # set logger total_step
    pwhc = PlayWithHumanConfig()
    pwhc.update_play_config(config.play)  # update the config from configs/mini.py line 33: PlayConfig
    logger.info(f"AI move first : false")
    play.start(config)
