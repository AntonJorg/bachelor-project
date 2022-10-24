import time
from math import exp

from src.tree import TreeSearchNode
from src.connectfour import ConnectFourState, apply_many


class Control:
    # checks
    def if_depth_reached(self, node: TreeSearchNode, value: float = 0) -> bool:
        return node.depth == self.depth or node.state.is_terminal

    def if_depth_reached_or_fully_expanded(self, node: TreeSearchNode, value: float = 0) -> bool:
        return node.depth == self.depth or node.state.is_terminal or not node.unexpanded_actions

    def when_terminal(self, node, value=0):
        return node.state.is_terminal

    # should_terminate functions
    def timed_termination(self):
        if self.search_time is None:
            raise AttributeError("Subclass must set self.search_time to use self.timed_termination")
        
        return time.time() - self.start_time > self.search_time
    
    def when_fully_evaluated(self):
        return self.root.evaluated


    # filter functions
    def filter_unexpanded_actions(self, node: TreeSearchNode):
        # root case
        if not node.state.piece_mask:
            middle = node.state.width // 2
            if node.state.width % 2:
                return [middle]
            else:
                return [middle - 1, middle]

        
        played_rows = [i for i in range(node.state.width) if node.state.piece_mask & 1 << (node.state.height + 1) * i]

        beam = range(max(0, min(played_rows) - 1), min(node.state.width, max(played_rows) + 2))

        beam = [action for action in beam if action in node.state.applicable_actions]

        return sorted(beam, key=lambda x: -abs(x - node.state.width//2 + .1))


if __name__ == "__main__":
    state = ConnectFourState(7, 6)

    state = apply_many(state, "06")

    node = TreeSearchNode(state, None, None)

    ctrl = Control()

    print(ctrl.filter_unexpanded_actions(node))