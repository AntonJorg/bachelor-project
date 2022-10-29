class Reflect:
    """
    Defines methods for implementing TreeSearchAgent.reflect.

    These methods should:
        - Take no arguments
        - Evaluate the state of the search tree and/or the frontier
        - Possibly modify the search tree and/or the frontier
        - Return nothing
    """

    def iterative_deepening_reflect(self):
        if self.root.evaluated:
            action = self.get_minimax_move()
            self.best_move = action
            self.depth += 1

            # reset search tree
            self.last_iter_root = self.root.copy()
            self.root.reset()
            self.frontier.append(self.root)
