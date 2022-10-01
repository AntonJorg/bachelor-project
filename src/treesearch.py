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

        # additional variables

        self.start_time = None
        self.search_time_allowed = 2
        self.state = None
        self.initial_state = None

    def search(self, state):
        self.state = state.copy()
        self.initial_state = state.copy()
        self.start_time = time.time()

        root = TreeSearchNode(None, None, self.state)

        while not self.should_terminate(self, root):
            self.state = self.initial_state.copy()
            node = self.select(self, root)
            leaf = self.expand(self, node)
            # include check here?
            value = self.evaluate(self, leaf)
            if self.should_backpropagate(self, leaf, value):
                self.backpropagate(self, leaf, value)

        return self.get_best_move(self, root), root


class TreeSearchNode:
    def __init__(self, parent, generating_action, state):
        self.parent = parent
        self.generating_action = generating_action
        self.unexpanded_actions = state.applicable_actions
        self.children = []

        self.utility = 0
        self.count = 0
        self.c = sqrt(2)
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


# mcts components

def uct_select(agent, root):
    if root.unexpanded_actions or agent.state.is_terminal():
        return root

    def uct(node):
        if agent.state.moves % 2:
            exploit = (node.count - node.utility) / node.count

        else:
            exploit = node.utility / node.count

        explore = sqrt(2) * sqrt(log(root.count) / node.count)

        return exploit + explore

    best_child = sorted(root.children, key=uct)[-1]

    result(agent.state, best_child.generating_action)

    return uct_select(agent, best_child)


def expand_next(agent, node):
    if agent.state.is_terminal():
        return node

    action = node.unexpanded_actions.pop()
    result(agent.state, action)

    leaf = TreeSearchNode(node, action, agent.state)

    node.children.append(leaf)

    return leaf


def simulate(agent, node):
    s = agent.state.copy()

    while not s.is_terminal():
        action = random.choice(s.applicable_actions)
        result(s, action)

    return s.utility()


def most_robust_child(agent, node: TreeSearchNode):
    return sorted(node.children, key=lambda c: c.count)[-1].generating_action


def timed_termination(agent: TreeSearchAgent, root):
    return time.time() - agent.start_time > agent.search_time_allowed


def backpropagate_sum(agent, node, value):
    if node is not None:
        node.utility += value
        node.count += 1
        backpropagate_sum(agent, node.parent, value)

# minimax components


def dfs_select(agent, root):
    # TODO: A node should have at most one unevaluated child, how to utilize this?
    unevaluated_children = [c for c in root.children if not c.evaluated]

    if not unevaluated_children or agent.state.is_terminal():
        return root

    child = unevaluated_children[0]

    result(agent.state, child.generating_action)

    return dfs_select(agent, child)


def backpropagate_minimax(agent, node, value):
    node.utility = agent.state.utility()
    node.evaluated = True

    def bp(node):
        if all(c.evaluated for c in node.children) and not node.unexpanded_actions:
            if agent.state.moves % 2:  # current player = min, last player = max
                node.utility = max(c.utility for c in node.children)
            else:
                node.utility = min(c.utility for c in node.children)

            node.evaluated = True

            if node.parent:
                reverse(agent.state, node.generating_action)
                bp(node.parent)

    bp(node.parent)


def when_terminal(agent, node, value):
    return agent.state.is_terminal()


def utility(agent, node):
    if agent.state.is_terminal():
        return agent.state.utility()
    else:
        return None


def when_fully_evaluated(agent, root):
    return root.evaluated


def get_minimax_move(agent, root):
    if agent.initial_state.moves % 2:
        return sorted(root.children, key=lambda c: c.utility)[0].generating_action
    else:
        return sorted(root.children, key=lambda c: c.utility)[-1].generating_action


def random_agent(): return TreeSearchAgent(
    select=no_op,
    expand=no_op,
    evaluate=no_op,
    backpropagate=no_op,
    should_backpropagate=no_op,
    should_terminate=always,
    get_best_move=random_move
)


def mcts_agent(): return TreeSearchAgent(
    select=uct_select,
    expand=expand_next,
    evaluate=simulate,
    backpropagate=backpropagate_sum,
    should_backpropagate=always,
    should_terminate=timed_termination,
    get_best_move=most_robust_child
)


def minimax_agent(): return TreeSearchAgent(
    select=dfs_select,
    expand=expand_next,
    evaluate=utility,
    backpropagate=backpropagate_minimax,
    should_backpropagate=when_terminal,
    should_terminate=when_fully_evaluated,
    get_best_move=get_minimax_move
)
