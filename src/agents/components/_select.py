from math import sqrt, log

from src.tree import TreeSearchNode


class Select:
    def uct_select(self, node=None):
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

    def queue_select(self):
        return self.frontier.pop()