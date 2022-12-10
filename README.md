# A Generalized Approach to Search Algorithms in Games

## About
This project seeks to generalize adversarial tree search algorithms (agents) by introducing a common framework that they can all inherit from. The framework consists of several *component functions*, that when specified describe an agent uniquely. This modularity allows for quick experimentation by swapping out component functions, as well as easier separation of configuration from code, for example by specifying agents in `yaml`/`json` files.

The hope is that this will allow for easier innovation, experimentation, development, and education in the field.

The framework is called Extended General Tree Search (EGTS), and pseudocode can be seen below:

```python
def TreeSearch(State):
    global Parameters = ... # Dictionary accessible from all functions
    Frontier = ... # LIFO / FIFO / Priority Queue
    Root = Node(State)

    while not ShouldTerminate(Root):
        # Choose node for expansion using either treetraversal or
        # the frontier
        Node = Select(Root, Frontier)

        # Generate new state with applicable action
        # If Node is fully expanded, Leaf = Node
        Leaf = Expand(Node)

        # Some agents (e.g. MiniMax) do not need to evaluate all states
        if ShouldEvaluate(Leaf):
            Value = Evaluate(Leaf.State)

        # Backprop w/o evaluation is useful for proactive pruning
        if ShouldBackPropagate(Leaf, Value):
            Backpropagate(Leaf, Value)

        # For removing nodes from the tree, i.e. retroactive pruning
        if ShouldTrim(Root):
            Trim(Root, Frontier)

    # Decide best move based on root and its children, or values
    # stored in Parameters
    return GetBestMove(Root)
```

## Usage

Agents are specified in the `agents` module, using component functions from `agents.components`. If you create a new agent and want to use it in the experiment scripts, it needs to be added to the `agents` list in `agents.__init__`. 

Example usage of the adversarial experiment script:
```
python src/run_experiment.py ConnectFour IterativeDeepeningAgent MCTSAgent 50 -t 2 -swap
```
First argument specifies the game to be played, followed by the two agents, and the number of games. The `-t` option sets the search time for each move, and `-swap` makes the agents take turns being Max- and Min-player. 


## Further Work

- [ ] Clarify responsibilities and permissions of component functions
- [ ] Add support for nested agents
- [ ] Add support for ensemble methods
- [ ] Move agent definitions into config files (keeping ability to inherit)

## Credentials 
Author: Anton Thestrup Jørgensen, s194268

Supervisor: Thomas Bolander

Technical University of Denmark, DTU Compute

