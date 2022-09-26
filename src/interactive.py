from connectfour import ConnectFour
from src.treesearch import mcts_agent

if __name__ == "__main__":
    c4 = ConnectFour()

    state = c4.initial_state(7, 6)

    agent = mcts_agent()

    print(state)

    while not state.utility():
        action = agent.search(state)
        c4.result(state, action)

        print(state)
        # state.visualize()
