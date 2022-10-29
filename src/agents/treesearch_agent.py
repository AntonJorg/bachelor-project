import time
from abc import ABC, abstractmethod
from collections import deque, defaultdict

from src.tree import TreeSearchNode
from src.connectfour import ConnectFourState
from src.agents.components import components


class TreeSearchAgent(ABC, *components):
    """
    The TreeSearchAgent implements the General Tree Search Algorithm
    in self.search, and also defines all methods called in self.search
    as abstract methods to be implemented in subclasses.
    """
    def __init__(self):
        self.root = None
        self.frontier = deque()
        
        self.start_time = None
        self.search_time = None

        self.depth = None

        self.search_info = defaultdict(float)

    def search(self, state):
        """
        General Tree Search Algorithm
        """

        if state.is_terminal:
            raise ValueError("Cannot search terminal states!")

        self.search_info.clear()

        self.frontier.clear()
        self.root = TreeSearchNode(state, None, None)
        self.frontier.append(self.root)

        self.start_time = time.time()

        while not self.should_terminate():
            node = self.select()
            
            leaf = self.expand(node)

            value = None
            if self.should_evaluate(leaf):
                value = self.evaluate(leaf.state)

            if self.should_backpropagate(leaf, value):
                self.backpropagate(leaf, value)
     
            self.reflect()

        return self.get_best_move(), self.search_info

    @abstractmethod 
    def should_terminate(self) -> bool:
        """
        Determines when the search algorithm terminates. This should
        not happen before the search has progressed to a point where
        self.get_best_move has a valid answer, i.e. can return an
        applicable action.
        """
        pass

    @abstractmethod
    def select(self) -> TreeSearchNode:
        """
        Selects where in the search tree the search should continue.
        This can either be based on the search tree itself, or the frontier.
        """
        pass

    @abstractmethod 
    def expand(self, node: TreeSearchNode) -> TreeSearchNode:
        """
        Takes the node returned from self.select, and decides
        which child nodes to expand and add to the search 
        tree and frontier.
        """
        pass

    @abstractmethod 
    def should_evaluate(self, node: TreeSearchNode) -> bool:
        """
        Whether or not to call self.evaluate on node.
        """
        pass

    @abstractmethod 
    def evaluate(self, state: ConnectFourState) -> float:
        """
        Returns an estimate of the value of state. The estimate
        can be deterministic or stochastic, but should be a float.
        """
        pass

    @abstractmethod 
    def should_backpropagate(self, node: TreeSearchNode, value: float) -> bool:
        """
        Whether or not to backpropagate value through node. Only determines when
        to call self.backpropagate, not how far up the tree the backpropagation
        continues.
        """
        pass

    @abstractmethod 
    def backpropagate(self, node: TreeSearchNode, value: float) -> None:
        """
        Propagates the value returned from self.evaluate up through the
        search tree, starting at node. Should modify the values of nodes
        in the tree, but not the tree structure.
        """
        pass

    @abstractmethod 
    def reflect(self) -> None:
        """
        If a specific algorithm needs to modify the search tree and/or frontier
        during the search, this function is where it should happen.
        """
        pass

    @abstractmethod 
    def get_best_move(self) -> int:
        """
        Using information from the search tree, the frontier, or other available sources,
        return the action that the agent should take.
        """
        pass
 

