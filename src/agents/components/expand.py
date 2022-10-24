from src.tree import TreeSearchNode
from src.connectfour import result

class Expand:
    def expand_next(self, node: TreeSearchNode) -> TreeSearchNode:
        # do not try to expand terminal states
        if node.state.is_terminal:
            return node

        # depth limiting
        if self.depth is not None and node.depth == self.depth:
            return node

        # alpha beta pruning
        if node.children:
            if node.is_max_node and node.children[-1].utility >= node.beta or \
                not node.is_max_node and node.children[-1].utility <= node.alpha:
                
                node.unexpanded_actions.clear()
                return node

        action = node.unexpanded_actions.pop()
        state = result(node.state, action)

        # add node to queue for further expansion if needed
        if node.unexpanded_actions:
            self.frontier.append(node)

        leaf = node.add_child(state, action)
        self.frontier.append(leaf)

        return leaf

    def expand_next_beam(self, node: TreeSearchNode) -> TreeSearchNode:
        # beam search on root
        if node.parent is None and not node.children:
            node.unexpanded_actions = self.filter_unexpanded_actions(node)

        # do not try to expand terminal states
        if node.state.is_terminal:
            return node

        # depth limiting
        if self.depth is not None and node.depth == self.depth:
            return node

        # alpha beta pruning
        if node.children:
            if node.is_max_node and node.children[-1].utility >= node.beta or \
                not node.is_max_node and node.children[-1].utility <= node.alpha:
                
                node.unexpanded_actions.clear()
                return node

        action = node.unexpanded_actions.pop()
        state = result(node.state, action)

        # add node to queue for further expansion if needed
        if node.unexpanded_actions:
            self.frontier.append(node)

        leaf = node.add_child(state, action)
        self.frontier.append(leaf)

        # beam search on leaf nodes
        leaf.unexpanded_actions = self.filter_unexpanded_actions(leaf)

        return leaf

    def expand_all(self, node: TreeSearchNode) -> TreeSearchNode:
        if node.state.is_terminal:
            return node

        if self.depth is not None and node.depth == self.depth:
            return node
        
        while node.unexpanded_actions:
            action = node.unexpanded_actions.pop()
            state = result(node.state, action)
            leaf = node.add_child(state, action)
            self.frontier.append(leaf)

        # return last child for evaluate function
        return leaf