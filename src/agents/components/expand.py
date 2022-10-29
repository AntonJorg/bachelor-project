from src.tree import TreeSearchNode
from src.connectfour import result

class Expand:
    """
    Defines methods for implementing TreeSearchAgent.expand.

    These methods should:
        - Take a TreeSearchNode
        - Return a TreeSearchNode
        - Modify tree structure and frontier
        - Not modify node data unrelated to tree structure
    """

    def expand_next(self, node: TreeSearchNode, dfs: bool = False) -> TreeSearchNode:
        """
        
        """
        # do not try to expand terminal states
        if node.state.is_terminal:
            return node

        action = node.unexpanded_actions.pop()
        state = result(node.state, action)

        # add node to queue for further expansion if in dfs mode
        if dfs and node.unexpanded_actions:
            self.frontier.append(node)

        leaf = node.add_child(state, action)
        self.frontier.append(leaf)

        return leaf

    def expand_next_depth_limited(self, node: TreeSearchNode, dfs: bool = False) -> TreeSearchNode:
        """
        
        """
        # depth limiting
        if node.depth == self.depth:
            return node

        return self.expand_next(node, dfs)

    def expand_next_alpha_beta(self, node: TreeSearchNode) -> TreeSearchNode:
        """
        
        """
        # alpha beta pruning
        # uses strict inequalities to prevent suboptimal moves from having equal
        # utility to the optimal move
        if node.children:
            if node.is_max_node and node.children[-1].utility > node.beta or \
                not node.is_max_node and node.children[-1].utility < node.alpha:
                
                node.unexpanded_actions.clear()
                return node

        return self.expand_next_depth_limited(node, dfs=True)

    def expand_next_beam(self, node: TreeSearchNode) -> TreeSearchNode:
        """
        
        """
        # beam search on root
        if node.parent is None and not node.children:
            node.unexpanded_actions = self.filter_unexpanded_actions(node)

        leaf = self.expand_next_alpha_beta(node)

        # beam search on leaf nodes
        if leaf.unexpanded_actions:
            leaf.unexpanded_actions = self.filter_unexpanded_actions(leaf)

        return leaf

    def expand_all_depth_limited(self, node: TreeSearchNode) -> TreeSearchNode:
        """
        
        """
        if node.state.is_terminal:
            return node

        if node.depth == self.depth:
            return node
        
        while node.unexpanded_actions:
            action = node.unexpanded_actions.pop()
            state = result(node.state, action)
            leaf = node.add_child(state, action)
            self.frontier.append(leaf)

        # return last child for evaluate function
        return leaf