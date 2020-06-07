import getpass
import os


# 返回项目根目录的绝对路径
def _project_dir():
    # print(os.path.abspath(__file__), _project_dir(), sep = '\n')
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _data_dir():
    return os.path.join(_project_dir(), "data")


# print(_data_dir())
# exit()

class Config:
    def __init__(self, config_type="mini", search_num=200):
        self.opts = Options()
        self.resource = ResourceConfig()

        if config_type == "mini":
            import configs.mini as c
        # elif config_type == "normal":
        #     import configs.normal as c
        # elif config_type == 'distribute':
        #     import cchess_alphazero.configs.distribute as c
        else:
            raise RuntimeError('unknown config_type: %s' % (config_type))

        self.model = c.ModelConfig()
        self.play = c.PlayConfig()
        self.play_data = c.PlayDataConfig()
        self.trainer = c.TrainerConfig()  # configs/mini.py TrainerConfig
        self.eval = c.EvaluateConfig()

        self.opts.device_list = 0
        self.resource.create_directories()
        self.opts.piece_style = 'WOOD'
        self.opts.bg_style = 'WOOD'
        # self.internet.distributed = False
        self.opts.light = False

        self.play.simulation_num_per_move = search_num  # MCTS number per move.
        self.play.c_puct = 1  # balance parameter of value network and policy network in MCTS.
        self.play.search_threads = 2  # balance parameter of speed and accuracy in MCTS.
        self.play.noise_eps = 0
        self.play.tau_decay_rate = 0
        self.play.dirichlet_alpha = 0.2  # random parameter in self-play.


class PlayWithHumanConfig:
    def __init__(self):
        self.simulation_num_per_move = 800  # MCTS number per move.
        self.c_puct = 1  # balance parameter of value network and policy network in MCTS.
        self.search_threads = 10  # balance parameter of speed and accuracy in MCTS.
        self.noise_eps = 0
        self.tau_decay_rate = 0
        self.dirichlet_alpha = 0.2  # random parameter in self-play.

    def update_play_config(self, pc):
        pc.simulation_num_per_move = self.simulation_num_per_move
        pc.c_puct = self.c_puct
        pc.search_threads = self.search_threads
        pc.noise_eps = self.noise_eps
        pc.tau_decay_rate = self.tau_decay_rate
        pc.dirichlet_alpha = self.dirichlet_alpha

class Options:
    new = False
    light = True
    device_list = '0'
    bg_style = 'CANVAS'
    piece_style = 'WOOD'
    random = 'none'
    log_move = False
    use_multiple_gpus = False
    gpu_num = 1
    evaluate = False
    has_history = False

class ResourceConfig:
    def __init__(self):
        self.project_dir = os.environ.get("PROJECT_DIR", _project_dir())
        self.data_dir = os.environ.get("DATA_DIR", _data_dir())
        self.model_dir = os.environ.get("MODEL_DIR", os.path.join(self.data_dir, "model"))

        self.model_best_config_path = os.path.join(self.model_dir, "model_best_config.json")
        self.model_best_weight_path = os.path.join(self.model_dir, "model_best_weight.h5")
        self.sl_best_config_path = os.path.join(self.model_dir, "sl_best_config.json")
        self.sl_best_weight_path = os.path.join(self.model_dir, "sl_best_weight.h5")
        self.eleeye_path = os.path.join(self.model_dir, 'ELEEYE')

        self.next_generation_model_dir = os.path.join(self.model_dir, "next_generation")
        self.next_generation_config_path = os.path.join(self.next_generation_model_dir, "next_generation_config.json")
        self.next_generation_weight_path = os.path.join(self.next_generation_model_dir, "next_generation_weight.h5")
        self.rival_model_config_path = os.path.join(self.model_dir, "rival_config.json")
        self.rival_model_weight_path = os.path.join(self.model_dir, "rival_weight.h5")

        self.play_data_dir = os.path.join(self.data_dir, "play_data")
        self.play_data_filename_tmpl = "play_%s.json"
        self.self_play_game_idx_file = os.path.join(self.data_dir, "play_data_idx")
        self.play_record_filename_tmpl = "record_%s.qp"
        self.play_record_dir = os.path.join(self.data_dir, "play_record")

        self.log_dir = os.path.join(self.project_dir, "logs")
        self.main_log_path = os.path.join(self.log_dir, "main.log")
        self.opt_log_path = os.path.join(self.log_dir, "opt.log")
        self.play_log_path = os.path.join(self.log_dir, "play.log")
        self.sl_log_path = os.path.join(self.log_dir, "sl.log")
        self.eval_log_path = os.path.join(self.log_dir, "eval.log")

        self.sl_data_dir = os.path.join(self.data_dir, "sl_data")
        self.sl_data_gameinfo = os.path.join(self.sl_data_dir, "gameinfo.csv")
        self.sl_data_move = os.path.join(self.sl_data_dir, "moves.csv")
        self.sl_onegreen = os.path.join(self.sl_data_dir, "onegreen.json")

        self.font_path = os.path.join(self.project_dir, 'mychess', 'play_games', 'PingFang.ttc')

    def create_directories(self):
        dirs = [self.project_dir, self.data_dir, self.model_dir, self.play_data_dir, self.log_dir,
                self.play_record_dir, self.next_generation_model_dir, self.sl_data_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
