import random
import time
from math import sqrt, log

from src.connectfour import ConnectFourState, result, reverse


class TreeSearchAgent:
    def __init__(self,
                 select: callable,
                 expand: callable,
                 evaluate: callable,
                 backpropagate: callable,
                 should_backpropagate: callable,
                 should_terminate: callable,
                 get_best_move: callable):

        # control functions

        self.select = select
        self.expand = expand
        self.evaluate = evaluate
        self.backpropagate = backpropagate
        self.should_backpropagate = should_backpropagate
        self.should_terminate = should_terminate
        self.get_best_move = get_best_move

    def search(self, state):
        self.reset()

        root = TreeSearchNode(state, None, None)

        while not self.should_terminate(root):
            node = self.select(root)
            leaf = self.expand(node)
            # include check here?
            value = self.evaluate(leaf)
            if self.should_backpropagate(leaf, value):
                self.backpropagate(leaf, value)

        return self.get_best_move(root), root

    def reset(self):
        for v in self.__dict__.values():
            if hasattr(v, "reset"):
                v.reset()


class TreeSearchNode:
    def __init__(self, state, parent, generating_action):
        self.state = state
        self.parent = parent
        self.generating_action = generating_action
        self.unexpanded_actions = state.applicable_actions
        self.children = []

        self.utility = 0
        self.count = 0
        self.evaluated = False

    def __repr__(self):
        return f"Node(action={self.generating_action}, utility={self.utility}, count={self.count}, {self.evaluated})"

    def print_tree(self, depth=0):
        print(depth * "--", self)
        for c in self.children:
            c.print_tree(depth + 1)


def no_op(*args):
    pass


def always(*args):
    return True


def never(*args):
    return False


def random_move(agent, root):
    return random.choice(agent.initial_state.applicable_actions)


# select functions

def uct_select(root):
    if root.unexpanded_actions or root.state.is_terminal:
        return root

    def uct(node):
        if node.state.moves % 2:
            exploit = node.utility / node.count
        else:
            exploit = (node.count - node.utility) / node.count

        explore = sqrt(2) * sqrt(log(root.count) / node.count)

        return exploit + explore

    best_child = sorted(root.children, key=uct)[-1]

    return uct_select(best_child)


def dfs_select(agent, root):
    # TODO: A node should have at most one unevaluated child, how to utilize this?
    unevaluated_children = [c for c in root.children if not c.evaluated]

    if not unevaluated_children or agent.state.is_terminal():
        return root

    child = unevaluated_children[0]

    result(agent.state, child.generating_action)

    return dfs_select(agent, child)


# expand functions

def expand_next(node):
    if node.state.is_terminal:
        return node

    action = node.unexpanded_actions.pop()
    state = result(node.state, action)

    leaf = TreeSearchNode(state, node, action)
    node.children.append(leaf)

    return leaf


# evaluate functions

def utility(node):
    if node.state.is_terminal:
        return agent.state.utility
    else:
        return None


def simulate(node):
    state = node.state

    while not state.is_terminal:
        action = random.choice(state.applicable_actions)
        state = result(state, action)

    return state.utility

# backpropagate functions


def backpropagate_sum(node, value):
    if node is not None:
        node.utility += value
        node.count += 1
        backpropagate_sum(node.parent, value)


def backpropagate_minimax(node, value):
    node.utility = state.utility
    node.evaluated = True

    def bp(node):
        if all(c.evaluated for c in node.children) and not node.unexpanded_actions:
            if node.state.moves % 2:  # current player = min, last player = max
                node.utility = max(c.utility for c in node.children)
            else:
                node.utility = min(c.utility for c in node.children)

            node.evaluated = True

            if node.parent:
                bp(node.parent)

    bp(node.parent)


# should_backpropagate functions

def when_terminal(node, value):
    return node.state.is_terminal()


# should_terminate functions

class timed_termination:
    def __init__(self, search_time):
        self.start_time = None
        self.search_time = search_time

    def __call__(self, *args):
        return time.time() - self.start_time > self.search_time

    def reset(self):
        self.start_time = time.time()


def when_fully_evaluated(agent, root):
    return root.evaluated


# get_best_move functions

def get_minimax_move(root: TreeSearchNode) -> int:
    if root.state.moves % 2:
        return sorted(root.children, key=lambda c: c.utility)[0].generating_action
    else:
        return sorted(root.children, key=lambda c: c.utility)[-1].generating_action


def most_robust_child(root: TreeSearchNode) -> int:
    return sorted(root.children, key=lambda c: c.count)[-1].generating_action


def random_agent(t): return TreeSearchAgent(
    select=no_op,
    expand=no_op,
    evaluate=no_op,
    backpropagate=no_op,
    should_backpropagate=no_op,
    should_terminate=always,
    get_best_move=random_move
)


def mcts_agent(t): return TreeSearchAgent(
    select=uct_select,
    expand=expand_next,
    evaluate=simulate,
    backpropagate=backpropagate_sum,
    should_backpropagate=always,
    should_terminate=timed_termination(t),
    get_best_move=most_robust_child
)


def minimax_agent(t): return TreeSearchAgent(
    select=dfs_select,
    expand=expand_next,
    evaluate=utility,
    backpropagate=backpropagate_minimax,
    should_backpropagate=when_terminal,
    should_terminate=when_fully_evaluated,
    get_best_move=get_minimax_move
)


if __name__ == "__main__":
    agent = mcts_agent(1)
