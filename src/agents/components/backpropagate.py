from src.tree import TreeSearchNode

class Backpropagate:
    def backpropagate_sum(self, node: TreeSearchNode, value: float) -> None:
        if node is not None:
            node.utility += value
            node.count += 1
            self.backpropagate_sum(node.parent, value)

    def backpropagate_minimax(self, node: TreeSearchNode, value: float) -> None:
        
        def bp(node):
            max_child_utility = max(c.utility for c in node.children) if node.children else None
            min_child_utility = min(c.utility for c in node.children) if node.children else None

            if node.is_max_node:
                node.alpha = max(node.alpha, max_child_utility)
            else:
                node.beta = min(node.beta, min_child_utility)

            if all(c.evaluated for c in node.children) and not node.unexpanded_actions:
        
                node.utility = max_child_utility if node.is_max_node else min_child_utility
                
                node.evaluated = True

                if node.parent is not None:
                    bp(node.parent)

        if value is None:
            # alpha beta cutoff happened
            bp(node)
        else:
            node.utility = value
            node.evaluated = True

            if node.parent is not None:
                bp(node.parent)