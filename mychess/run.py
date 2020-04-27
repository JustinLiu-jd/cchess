import os
import sys

import pygame

_PATH_ = os.path.dirname(os.path.dirname(__file__))
# print(_PATH_)

# print(_PATH_ in sys.path)
if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

if __name__ == "__main__":
    from mychess import manager

    pygame.init()
    manager.start()
