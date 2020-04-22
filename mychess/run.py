import os
import sys

_PATH_ = os.path.dirname(os.path.dirname(__file__))
print(_PATH_)

# print(_PATH_ in sys.path)
if _PATH_ not in sys.path:
    sys.path.append(_PATH_)

if __name__ == "__main__":

    sys.setrecursionlimit(10000)
    from mychess import manager
    manager.start()
