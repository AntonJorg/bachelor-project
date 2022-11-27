from math import log, sqrt
import random

from src.agents.mcts_agents import TreeSearchAgent


class MaximizerMCTSAgent(TreeSearchAgent):
    def __init__(self, search_time):
        super().__init__()
        self.search_time = search_time

    def __repr__(self):
        return super().__repr__() + f"+st={self.search_time}"

    def select(self, node=None):
        if node is None:
            node = self.root

        if node.unexpanded_actions or node.state.is_terminal:
            return node

        if not node.is_max_node:
            return self.select(random.choice(node.children))

        c = max(c.cumulative_utility / c.count for c in node.children)

        def uct(child):
            exploit = child.cumulative_utility / child.count

            explore = c * sqrt(log(node.count) / child.count)

            return exploit + explore

        best_child = sorted(node.children, key=uct)[-1]

        return self.select(best_child)

    def expand(self, node):
        return self.expand_next(node)

    def should_evaluate(self, node):
        return True

    def evaluate(self, state):
        while not state.is_terminal:
            if hasattr(state, "cumulative_distribution"):
                action = random.choices(state.applicable_actions, 
                    cum_weights=state.cumulative_distribution, 
                    k=1)[0]
            else:
                action = random.choice(state.applicable_actions)
            state = state.result(action)
        return state.utility


    def should_backpropagate(self, node, value):
        return True

    def backpropagate(self, node, value):
        self.backpropagate_sum(node, value)

    def reflect(self):
        pass

    def get_best_move(self):
        for c in self.root.children:
            print(c.cumulative_utility / c.count)
        return self.most_robust_child()

    def should_terminate(self):
        return self.timed_termination()


class ExpectiMaxAgent(TreeSearchAgent):
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
        def bp(n):
            if n is None or len(n.unexpanded_actions) != 0 or any(c.eval is None for c in n.children):
                return

            if n.is_max_node:
                n.eval = max(c.eval for c in n.children)
            else:
                n.eval = sum(c.eval * w for c, w in zip(n.children, n.state.distribution[::-1])) / sum(n.state.distribution)

            if n.parent is not None:
                bp(n.parent)
           
        node.eval = value
        bp(node.parent)
        
    def reflect(self):
        pass

    def get_best_move(self):
        return self.get_minimax_move()

    def should_terminate(self):
        return self.when_fully_evaluated()


class IDExpectiMaxAgent(ExpectiMaxAgent):
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
        self.depth = 2 # always terminate on max layer
        self.best_move = None
        return super().search(state)

    def should_terminate(self):
        return self.timed_termination()

    def reflect(self):
        return self.iterative_deepening_reflect(n=2) # always terminate on max layer

    def get_best_move(self):
        return self.get_stored_best_move()


