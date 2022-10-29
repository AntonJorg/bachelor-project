import random


class GetBestMove:
    """
    Defines methods for implementing TreeSearchAgent.get_best_move.

    These methods should:
        - Take no arguments
        - Return an action that is in agent.root.state.applicable_actions
        - Base its action choice on the search tree or information that TreeSearchAgent.reflect has stored
        - Have no side effects
    """

    def get_minimax_move(self) -> int:
        """
        
        """
        utils = (c.utility for c in self.root.children)

        m = min(utils) if self.root.state.moves % 2 else max(utils)
        
        # consider all moves that maximize/minimize utility
        optimal_nodes = [c for c in self.root.children if c.utility == m]

        return random.choice(optimal_nodes).generating_action

    def most_robust_child(self) -> int:
        """
        
        """
        return sorted(self.root.children, key=lambda c: c.count)[-1].generating_action

    def random_move(self):
        """
        
        """
        return random.choice(self.root.state.applicable_actions)

    def get_stored_best_move(self):
        """
        
        """
        return self.best_move
