import random
import time
from math import sqrt, log

from src.connectfour import ConnectFour, ConnectFourState


class TreeSearchAgent:
    def __init__(self,
                 game: ConnectFour,
                 select: callable,
                 expand: callable,
                 evaluate: callable,
                 backpropagate: callable,
                 should_backpropagate: callable,
                 should_terminate: callable,
                 get_best_move: callable):

        # environment dynamics
        self.game = game

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

        while not self.should_terminate(self):
            self.state = self.initial_state.copy()
            node = self.select(self, root)
            leaf = self.expand(self, node)
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

    def __repr__(self):
        return f"Node(action={self.generating_action}, utility={self.utility}, count={self.count})"


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

    agent.game.result(agent.state, best_child.generating_action)

    return uct_select(agent, best_child)


def expand_next(agent, node):
    if agent.state.is_terminal():
        return node
    action = node.unexpanded_actions.pop()
    agent.game.result(agent.state, action)

    leaf = TreeSearchNode(node, action, agent.state)

    node.children.append(leaf)

    return leaf


def simulate(agent, node):
    s = agent.state.copy()

    while not s.is_terminal():
        action = random.choice(s.applicable_actions)
        agent.game.result(s, action)

    return s.utility()


def most_robust_child(agent, node: TreeSearchNode):
    return sorted(node.children, key=lambda c: c.count)[-1].generating_action


def timed_termination(agent: TreeSearchAgent):
    return time.time() - agent.start_time > agent.search_time_allowed


def backpropagate_sum(agent, node, value):
    if node is not None:
        node.utility += value
        node.count += 1
        backpropagate_sum(agent, node.parent, value)

# minimax components


def random_agent(): return TreeSearchAgent(
    game=ConnectFour(),
    select=no_op,
    expand=no_op,
    evaluate=no_op,
    backpropagate=no_op,
    should_backpropagate=no_op,
    should_terminate=always,
    get_best_move=random_move
)


def mcts_agent(): return TreeSearchAgent(
    game=ConnectFour(),
    select=uct_select,
    expand=expand_next,
    evaluate=simulate,
    backpropagate=backpropagate_sum,
    should_backpropagate=always,
    should_terminate=timed_termination,
    get_best_move=most_robust_child
)


def minimax_agent(): return TreeSearchAgent(
    game=ConnectFour(),
    select=no_op,
    expand=no_op,
    evaluate=no_op,
    backpropagate=no_op,
    should_backpropagate=no_op,
    should_terminate=always,
    get_best_move=random_move
)
