from math import sqrt, log

from src.tree import TreeSearchNode


class Select:
    """
    Defines methods for implementing TreeSearchAgent.select.

    These methods should:
        - Be callable with no arguments
        - Base their selection on self.root or self.frontier
        - Return a TreeSearchNode
        - Have no side effects
    """

    def uct_select(self, node: TreeSearchNode = None) -> TreeSearchNode:
        if node is None:
            node = self.root

        if node.unexpanded_actions or node.state.is_terminal:
            return node

        def uct(child):
            if child.is_max_node:
                exploit = (child.count - child.utility) / child.count
            else:
                exploit = child.utility / child.count

            explore = sqrt(2) * sqrt(log(node.count) / child.count)

            return exploit + explore

        best_child = sorted(node.children, key=uct)[-1]

        return self.uct_select(best_child)

    def partial_expansion_select(self, node: TreeSearchNode = None) -> TreeSearchNode:
        if node is None:
            node = self.root

        if not node.children or node.state.is_terminal:
            return node

        def uct(child):
            if child.is_max_node:
                exploit = (child.count - child.utility) / child.count
            else:
                exploit = child.utility / child.count

            explore = sqrt(2) * sqrt(log(node.count) / child.count)

            return exploit + explore

        ucb_child = 0.5 + sqrt(2) * sqrt(log(node.count) / (1 + len(node.children)))

        ucts = (uct(c) for c in node.children)
        
        if max(ucts) > ucb_child:
            best_child = sorted(node.children, key=uct)[-1]
            return self.partial_expansion_select(best_child)
        else:
            return node

    def queue_select(self) -> TreeSearchNode:
        return self.frontier.pop()

    def frontier_aided_uct_select(self) -> TreeSearchNode:

        if True:
            return self.uct_select()
        else:
            return self.uct_select()
