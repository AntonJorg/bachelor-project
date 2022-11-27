from src.agents.treesearch_agent import TreeSearchAgent
from src.games import ConnectFourState, NimState, CheckersState

class MiniMaxAgent(TreeSearchAgent):
    """
    
    """
    def __init__(self, depth=None):
        super().__init__()
        self.depth = depth

    def __repr__(self):
        return type(self).__name__

    def select(self):
        return self.queue_select()

    def expand(self, node):
        return self.expand_all_depth_limited(node)

    def should_evaluate(self, node):
        return self.if_depth_reached(node)

    def evaluate(self, state):
        return self.static_evaluation(state)

    def should_backpropagate(self, node, value):
        return self.if_depth_reached(node, value)

    def backpropagate(self, node, value):
        self.backpropagate_minimax(node, value)

    def reflect(self):
        pass

    def get_best_move(self):
        return self.get_minimax_move()

    def should_terminate(self):
        return self.when_fully_evaluated()


class AlphaBetaAgent(MiniMaxAgent):
    """
    
    """
    def should_backpropagate(self, node, value):
        return self.if_depth_reached_or_fully_expanded(node, value)

    def expand(self, node):
        return self.expand_next_alpha_beta(node)


class IterativeDeepeningAgent(MiniMaxAgent):
    """
    
    """
    def __init__(self, search_time):
        super().__init__(depth=1)
        self.search_time = search_time
        self.best_move = None
        self.last_iter_root = None

    def __repr__(self):
        return type(self).__name__ + f"+st={self.search_time}"

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


class IterativeDeepeningAlphaBetaAgent(IterativeDeepeningAgent, AlphaBetaAgent):
    """
    
    """
    pass


class IterativeDeepeningSimulationAgent(IterativeDeepeningAgent):
    """
    
    """
    def __init__(self, search_time, num_simulations=62):
        super().__init__(search_time)
        self.num_simulations = int(num_simulations)

    def __repr__(self):
        return super().__repr__() + f"+ns={self.num_simulations}"

    def evaluate(self, state):
        return self.simulate_many(state)


class BeamSearchAgent(IterativeDeepeningAlphaBetaAgent):
    """
    
    """
    def expand(self, node):
        return self.expand_next_beam(node)


class BestFirstMiniMaxAgent(MiniMaxAgent):
    def __init__(self, search_time):
        super().__init__(self)
        self.search_time = search_time

    def __repr__(self):
        return type(self).__name__ + f"+st={self.search_time}"

    def select(self):
        return self.principal_variation_select()

    def expand(self, node):
        return self.expand_next(node)

    def should_evaluate(self, node):
        return True

    def should_backpropagate(self, node, value):
        return True

    def should_terminate(self):
        return self.timed_termination()

if __name__ == "__main__":
    state = CheckersState()

    agent = IterativeDeepeningSimulationAgent(.5)
    #state = apply_many(state, "23223311120223313114")
    print(state)
    print(agent.search(state))
    agent.last_iter_root.print_tree()
    