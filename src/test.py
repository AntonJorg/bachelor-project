from src.agents import *
from src.games import *

if __name__ == "__main__":    
    state = Twenty48EnvironmentState()

    env = RandomDistributionAgent()
    agent = IDExpectiMaxAgent(2)

    while not state.is_terminal:
        action, _ = env.search(state)
        state = state.result(action)
        print(state)
        if state.is_terminal:
            break
        action, d = agent.search(state)
        state = state.result(action)
        print("VAL", agent.last_iter_root.eval)
        print(d)