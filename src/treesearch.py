import random
import time
from collections import deque
from math import sqrt, log, exp

from src.connectfour import ConnectFourState, result, reverse


class TreeSearchAgent:
    """
    The TreeSearchAgent implements the general tree search algorithm
    INSERT NAME, and takes a callable for each function specified
    in the algorithm, which determine the agents behavior.
    """
    def __init__(self,
                 select: callable,
                 expand: callable,
                 evaluate: callable,
                 should_evaluate: callable,
                 backpropagate: callable,
                 should_backpropagate: callable,
                 reflect: callable,
                 should_terminate: callable,
                 get_best_move: callable):

        # control functions
        self.select = select
        self.expand = expand
        self.evaluate = evaluate
        self.should_evaluate = should_evaluate
        self.backpropagate = backpropagate
        self.should_backpropagate = should_backpropagate
        self.reflect = reflect
        self.should_terminate = should_terminate
        self.get_best_move = get_best_move

    def search(self, state):
        """
        General Tree Search Algorithm
        """

        root = TreeSearchNode(state, None, None)

        self.reset(root)

        while not self.should_terminate(root):

            node = self.select(root)

            leaf = self.expand(node)
        
            if self.should_evaluate(leaf):
                value = self.evaluate(leaf.state)

                if self.should_backpropagate(leaf, value):
                    self.backpropagate(leaf, value)

            self.reflect(root)

        return self.get_best_move(root), root

    def reset(self, root):
        for v in self.__dict__.values():
            if hasattr(v, "reset"):
                v.reset(root)


class TreeSearchNode:
    """
    Generic doubly linked tree data structure.
    """
    def __init__(self, state: ConnectFourState, parent: 'TreeSearchNode', generating_action: int, depth: int =0):
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
        self.alpha = -float('inf')
        self.beta = float('inf')

        
    def __repr__(self):
        return f"Node(action={self.generating_action}, utility={self.utility}, count={self.count}, evaluated={self.evaluated}, depth={self.depth})"

    def print_tree(self, depth: int =0):
        print(depth * "--", self)
        for c in self.children:
            c.print_tree(depth + 1)

    def add_child(self, state: ConnectFourState, generating_action: int) -> 'TreeSearchNode':
        """
        
        """
        child = TreeSearchNode(state, self, generating_action, self.depth + 1)
        self.children.append(child)

        return child

    def reset(self):
        self.__init__(self.state, self.parent, self.generating_action, self.depth)


# generic functions
def no_op(*args) -> None:
    """
    No operation. Used as placeholder when a function in the general
    algorithm is not used in a specific algorithm.
    """
    pass


def always(*args) -> True:
    """
    Used for constructing algorithms where termination, backpropagation, and/or
    evaluation always happens.
    """
    return True


def never(*args) -> False:
    """
    Used for constructing algorithms where termination, backpropagation, and/or
    evaluation never happens.
    """
    return False


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


def dfs_select(node, depth=5):
    if not depth:
        return node
    # TODO: A node should have at most one unevaluated child, how to utilize this?
    unevaluated_children = [c for c in node.children if not c.evaluated]

    if not unevaluated_children or node.state.is_terminal:
        return node

    child = unevaluated_children[0]

    return dfs_select(child, depth - 1)


# expand functions

def expand_next(node):
    if node.state.is_terminal:
        return node

    action = node.unexpanded_actions.pop()
    state = result(node.state, action)

    leaf = node.add_child(state, action)

    return leaf


# evaluate functions

def utility(state):
    if state.is_terminal:
        return state.utility
    else:
        return None


def simulate(state):
    while not state.is_terminal:
        action = random.choice(state.applicable_actions)
        state = result(state, action)

    return state.utility


def simulate_many(number):

    def _simulate_many(state):
        values = (simulate(state) for _ in range(number))
        return sum(values) / number

    return _simulate_many        

def count_consecutives(state):
    if state.is_terminal:
        return state.utility

    current_pieces = state.player_mask
    other_pieces = state.player_mask ^ state.piece_mask


    shifts = [state.height + 1, 1, state.height, state.height + 2]

    # count 2 connected
    current_two = 0
    other_two = 0
    for shift in shifts:
        current_two += (current_pieces & current_pieces >> shift).bit_count()
        other_two += (other_pieces & other_pieces >> shift).bit_count()
    
    # count three connected
    current_three = 0
    other_three = 0
    for shift in shifts:
        m = current_pieces & current_pieces >> shift
        current_three += (m & m >> shift).bit_count()
        m = other_pieces & other_pieces >> shift
        other_three += (m & m >> shift).bit_count()

    score = (current_two - other_two) * .01 + current_three - other_three    

    return 1 / (1 + exp(-score))

# should_evaluate functions

# backpropagate functions


def backpropagate_sum(node, value):
    if node is not None:
        node.utility += value
        node.count += 1
        backpropagate_sum(node.parent, value)


def backpropagate_minimax(node, value):
    node.utility = value
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
    return node.state.is_terminal


# should_terminate functions
class timed_termination:
    def __init__(self, search_time):
        self.start_time = None
        self.search_time = search_time

    def __call__(self, *args):
        return time.time() - self.start_time > self.search_time

    def reset(self, *args):
        self.start_time = time.time()


def when_fully_evaluated(root):
    return root.evaluated


# get_best_move functions
def get_minimax_move(root: TreeSearchNode) -> int:
    if root.state.moves % 2:
        m = min(c.utility for c in root.children)        
    else:
        m = max(c.utility for c in root.children)

    # consider all moves that maximize/minimize utility
    optimal_nodes = (c for c in root.children if c.utility == m)

    return random.choice(optimal_nodes).generating_action


def most_robust_child(root: TreeSearchNode) -> int:
    return sorted(root.children, key=lambda c: c.count)[-1].generating_action


def random_move(root):
    return random.choice(root.state.applicable_actions)


class iterative_deepening_context:
    def __init__(self):
        self.frontier = deque()
        self.best_action = None
        self.depth = 1

    def update_best_action(self, action):
        self.best_action = action
        self.depth += 1
        self.frontier = deque()

    def reset(self):
        self.__init__()        


class queue_select:
    def __init__(self, context):
        self.context = context

    def __call__(self, *args):
        return self.context.frontier.pop()

    def reset(self, root):
        self.context.reset()
        self.context.frontier.append(root)


class queue_depth_limited_expand:
    def __init__(self, context):
        self.context = context

    def __call__(self, node: TreeSearchNode):
        if node.depth == self.context.depth or node.state.is_terminal:
            return node
        else:
            while node.unexpanded_actions:
                action = node.unexpanded_actions.pop()
                state = result(node.state, action)
                child = node.add_child(state, action)
                self.context.frontier.append(child)

            # return last child for evaluate function
            return child
            

def if_depth_reached(context):
    if isinstance(context, int):
        def _if_depth_reached(node, value=0):
            return node.depth == context
    else:
        def _if_depth_reached(node, value=0):
            return node.depth == context.depth

    return _if_depth_reached


def iterative_deepening_reflect(context):

    def _iterative_deepening_reflect(root):
        if root.evaluated:
            # root node reached, all children evaluated
            action = get_minimax_move(root)
            context.update_best_action(action)

            # reset search tree
            root.reset()
            context.frontier.append(root)
        
    return _iterative_deepening_reflect


def iterative_deepening_agent(search_time: float):
    context = iterative_deepening_context()
    return TreeSearchAgent(
        select=queue_select(context),
        expand=queue_depth_limited_expand(context),
        evaluate=count_consecutives,
        should_evaluate=if_depth_reached(context),
        backpropagate=backpropagate_minimax,
        should_backpropagate=always,
        reflect=iterative_deepening_reflect(context),
        should_terminate=timed_termination(search_time),
        get_best_move= lambda *args: context.best_action)


def iterative_deepening_simulation_agent(search_time: float):
    context = iterative_deepening_context()
    return TreeSearchAgent(
        select=queue_select(context),
        expand=queue_depth_limited_expand(context),
        evaluate=simulate_many(10),
        should_evaluate=if_depth_reached(context),
        backpropagate=backpropagate_minimax,
        should_backpropagate=always,
        reflect=iterative_deepening_reflect(context),
        should_terminate=timed_termination(search_time),
        get_best_move= lambda *args: context.best_action)


def random_agent(t): return TreeSearchAgent(
    select=no_op,
    expand=no_op,
    evaluate=no_op,
    should_evaluate=no_op,
    backpropagate=no_op,
    should_backpropagate=no_op,
    reflect=no_op,
    should_terminate=always,
    get_best_move=random_move
)


def mcts_agent(t): return TreeSearchAgent(
    select=uct_select,
    expand=expand_next,
    evaluate=simulate,
    should_evaluate=always,
    backpropagate=backpropagate_sum,
    should_backpropagate=always,
    reflect=no_op,
    should_terminate=timed_termination(t),
    get_best_move=most_robust_child
)

def mcts_agent_with_evaluation(t): return TreeSearchAgent(
    select=uct_select,
    expand=expand_next,
    evaluate=count_consecutives,
    should_evaluate=always,
    backpropagate=backpropagate_sum,
    should_backpropagate=always,
    reflect=no_op,
    should_terminate=timed_termination(t),
    get_best_move=most_robust_child
)

def minimax_agent(*args): return TreeSearchAgent(
    select=dfs_select,
    expand=expand_next,
    evaluate=count_consecutives,
    should_evaluate=if_depth_reached(6),
    backpropagate=backpropagate_minimax,
    should_backpropagate=if_depth_reached(6),
    reflect=no_op,
    should_terminate=when_fully_evaluated,
    get_best_move=get_minimax_move
)


if __name__ == "__main__":
    agent = iterative_deepening_agent(1)

    state = ConnectFourState(7, 6)

    print(state)

    action, root = agent.search(state)

    print(action)
    print(root.children)
