from math import log, sqrt
import random

from src.agents.mcts_agents import MCTSAgent
from src.agents.minimax_agents import IterativeDeepeningAgent


class MaximizerMCTSAgent(MCTSAgent):
    """
    
    """
    def select(self, node=None):
        if node is None:
            node = self.root

        if node.unexpanded_actions or node.state.is_terminal:
            return node

        if not node.is_max_node:
            return self.select(random.choice(node.children))

        c = node.cumulative_utility / node.count

        def uct(child):
            exploit = child.cumulative_utility / child.count

            explore = c * sqrt(log(node.count) / child.count)

            return exploit + explore

        best_child = sorted(node.children, key=uct)[-1]

        return self.select(best_child)

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


class IDExpectiMaxAgent(IterativeDeepeningAgent):
    """
    
    """
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
