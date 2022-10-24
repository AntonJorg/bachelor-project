from src.agents.treesearch_agent import TreeSearchAgent
from src.connectfour import ConnectFourState

class MCTSAgent(TreeSearchAgent):
    def __init__(self, search_time):
        super().__init__()
        self.search_time = search_time

    def select(self):
        return self.uct_select()

    def expand(self, node):
        return self.expand_next(node)

    def should_evaluate(self, node):
        return True

    def evaluate(self, state):
        return self.simulate(state)

    def should_backpropagate(self, node, value):
        return True

    def backpropagate(self, node, value):
        self.backpropagate_sum(node, value)

    def reflect(self):
        pass

    def get_best_move(self):
        return self.most_robust_child()

    def should_terminate(self):
        return self.timed_termination()


class MCTSEvaluationAgent(MCTSAgent):
    def evaluate(self, state):
        return self.count_consecutives(state)


if __name__ == "__main__":
    agent = MCTSAgent(2.0)
    state = ConnectFourState(7, 6)

    print("Action:", agent.search(state))
    agent.root.print_tree(max_depth=2)