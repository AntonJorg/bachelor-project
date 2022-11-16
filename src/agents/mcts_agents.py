from bisect import insort
from collections import deque

from src.agents.treesearch_agent import TreeSearchAgent
from src.games import ConnectFourState
from src.tree import TreeSearchNode


class MCTSAgent(TreeSearchAgent):
    def __init__(self, search_time):
        super().__init__()
        self.search_time = search_time

    def __repr__(self):
        return super().__repr__() + f"+st={self.search_time}"

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
        return self.static_evaluation(state)


class PartialExpansionAgent(MCTSAgent):
    def select(self):
        return self.partial_expansion_select()


class StaticWeightedMCTSAgent(MCTSAgent):
    def select(self):
        return self.partial_expansion_weighted_select()

    def evaluate(self, state):
        return self.evaluate_and_simulate(state)

    def backpropagate(self, node, value):
        self.store_eval_and_backpropagate_sum(node, value)

    def get_best_move(self):
        return self.weighted_eval_utility_move()


class MiniMaxWeightedMCTSAgent(MCTSAgent):
    def select(self):
        return self.partial_expansion_weighted_select()

    def evaluate(self, state):
        return self.evaluate_and_simulate(state)

    def backpropagate(self, node, value):
        self.backpropagate_sum_and_minimax(node, value)

    def get_best_move(self):
        return self.weighted_eval_utility_move()


class MCTSTreeMiniMaxAgent(MCTSAgent):
    def evaluate(self, state):
        return self.evaluate_and_simulate(state)

    def backpropagate(self, node, value):
        self.backpropagate_sum_and_minimax(node, value)

    def get_best_move(self):
        return self.get_minimax_move()


class ProgressivePruningMCTSAgent(MCTSAgent):
    def __init__(self, search_time, pruning_factor=6):
        super().__init__(search_time)
        self.pruning_factor = pruning_factor

    def __repr__(self):
        return super().__repr__() + f"+p={self.pruning_factor}"

    def reflect(self):
        self.fractional_pruning()


if __name__ == "__main__":
    agent = ProgressivePruningMCTSAgent(2, 1)

    state = ConnectFourState(7, 6)

    print(agent.search(state))
    agent.root.print_tree(max_depth=2)


    def f(node):
        if node.children:
            return max(f(c) for c in node.children)
        else:
            return node.depth

    print(f(agent.root))
    print(agent)