from src.agents.treesearch_agent import TreeSearchAgent
from src.connectfour import ConnectFourState, apply_many

class MiniMaxAgent(TreeSearchAgent):
    def __init__(self, depth=None):
        super().__init__()
        self.depth = depth

    def select(self):
        return self.queue_select()

    def expand(self, node):
        return self.expand_next(node)

    def should_evaluate(self, node):
        return self.if_depth_reached(node)

    def evaluate(self, state):
        return self.count_consecutives(state)

    def should_backpropagate(self, node, value):
        return self.if_depth_reached_or_fully_expanded(node, value)

    def backpropagate(self, node, value):
        self.backpropagate_minimax(node, value)

    def reflect(self):
        pass

    def get_best_move(self):
        return self.get_minimax_move()

    def should_terminate(self):
        return self.when_fully_evaluated()


class IterativeDeepeningAgent(MiniMaxAgent):
    def __init__(self, search_time):
        super().__init__(depth=1)
        self.search_time = search_time
        self.best_move = None
        self.last_iter_root = None

    def search(self, state):
        self.depth = 1
        self.best_move = None
        return super().search(state)

    def should_terminate(self):
        return self.timed_termination()

    def reflect(self):
        return self.iterative_deepening_reflect()

    def get_best_move(self):
        return self.get_stored_best_move()


class IterativeDeepeningSimulationAgent(IterativeDeepeningAgent):
    def __init__(self, search_time, num_simulations=10):
        super().__init__(search_time)
        self.num_simulations = num_simulations

    def evaluate(self, state):
        return self.simulate_many(state)


class BeamSearchAgent(IterativeDeepeningAgent):
    def expand(self, node):
        return self.expand_next_beam(node)


if __name__ == "__main__":
    state = ConnectFourState(7, 6)

    agent = BeamSearchAgent(1)

    #state = apply_many(state, "33333345454")
    print(state)
    print(agent.search(state))
    agent.last_iter_root.print_tree(max_depth=2)
