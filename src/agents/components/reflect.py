class Reflect:
    """
    Defines methods for implementing TreeSearchAgent.reflect.

    These methods should:
        - Take no arguments
        - Evaluate the state of the search tree and/or the frontier
        - Possibly modify the search tree and/or the frontier
        - Return nothing
    """

    def iterative_deepening_reflect(self, n=1):
        """
        
        """
        def deepest_node(node):
            if node.children:
                return max(deepest_node(c) for c in node.children)
            else:
                return node.depth

        if self.root.eval is not None:
            # log before increase to reflect last completed search
            self.search_info["depth"] = min(self.depth, deepest_node(self.root))

            action = self.get_minimax_move()
            self.best_move = action
            self.depth += n

            # reset search tree
            self.last_iter_root = self.root.copy()
            self.root.reset()
            self.frontier.append(self.root)

    def fractional_pruning(self, frequency=100):
        """
        
        """
        # TODO: Make 
        def recurse(node):
            node.children = [c for c in node.children if \
                c.count >= node.count / (node.branching_factor + self.pruning_factor)]

            for c in node.children:
                if not c.unexpanded_actions:
                    recurse(c)

        if not self.root.count % frequency:
            recurse(self.root)
