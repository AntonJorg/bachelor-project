from bisect import insort
from collections import deque

from src.agents.treesearch_agent import TreeSearchAgent
from src.connectfour import ConnectFourState, apply_many
from src.tree import TreeSearchNode

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


class MCTSFrontierAgent(MCTSAgent):


    class EvaluationQueue:
        def __init__(self, evaluate):
            self._data = []
            self.evaluate = evaluate

        def __repr__(self):
            return f"EvaluationQueue(len={len(self)})"

        def __len__(self):
            return len(self._data)

        def append(self, item: TreeSearchNode):
            x = (self.evaluate(item), item)
            self._data.append(x)

        def pop(self):
            return self._data.pop()[1]

        def clear(self):
            self._data.clear()

    pass



if __name__ == "__main__":
    agent = MCTSFrontierAgent(2)
    frontier = MCTSFrontierAgent.PriorityEvaluationQueue(agent.count_consecutives)
    state = ConnectFourState(7, 6)

    frontier.append(state)

    state = apply_many(state, "3")
    frontier.append(state)

    state = apply_many(state, "3")
    frontier.append(state)

    state = apply_many(state, "0")
    frontier.append(state)

    state = apply_many(state, "3")
    frontier.append(state)

    print(frontier)
    print(frontier.pop())
    print(frontier)

