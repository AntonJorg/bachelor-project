from __future__ import annotations
from src.connectfour import ConnectFourState

class TreeSearchNode:
    """
    Generic doubly linked tree data structure.
    """
    def __init__(self, state: ConnectFourState, parent: 'TreeSearchNode', generating_action: int, depth: int =0, alpha=None, beta=None):
        # data structure
        self.parent = parent
        self.children = []
        self.depth = depth

        # game related information
        self.state = state
        self.generating_action = generating_action
        self.unexpanded_actions = state.applicable_actions.copy()

        # search related information        
        self.utility = 0
        self.count = 0
        self.evaluated = False
        self.alpha = -float('inf') if alpha is None else alpha
        self.beta = float('inf') if beta is None else beta
        self.is_max_node = not state.moves % 2

    def __repr__(self):
        return f"Node(action={self.generating_action}, utility={self.utility}, count={self.count}, evaluated={self.evaluated}, depth={self.depth})"

    def print_tree(self, max_depth: int = None, depth: int = 0):
        print(depth * "--", self)
        if max_depth is None or depth < max_depth:
            for c in self.children:
                c.print_tree(max_depth, depth + 1)

    def add_child(self, state: ConnectFourState, generating_action: int) -> 'TreeSearchNode':
        """
        
        """
        child = TreeSearchNode(state, self, generating_action, self.depth + 1, self.alpha, self.beta)
        self.children.append(child)

        return child

    def reset(self) -> None:
        self.__init__(self.state, self.parent, self.generating_action, self.depth)

    def copy(self) -> 'TreeSearchNode':
        node = TreeSearchNode(self.state, self.parent, self.generating_action)
        node.__dict__ = self.__dict__.copy()
        return node
