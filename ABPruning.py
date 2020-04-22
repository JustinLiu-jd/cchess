
class ABPruning:
    def __init__(self):
        self.depth = 2
        self.strategy = 1

    def comptuteNextMove(self, curr_state):
        evalResult = self.recurseEvaluation(curr_state, self.depth, float('-inf'), float('inf'))



    def recurseEvaluation(self, state, depth, alpha, beta):
        pass
        