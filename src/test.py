from src.agents import *
from src.games import *

a = IDExpectiMaxAgent(1)

s = Twenty48State()

ac, si = a.search(s)
print(si)

exit()

if __name__ == "__main__":
    from src.agents import MaximizerMCTSAgent, IDExpectiMaxAgent, RandomDistributionAgent
    agent = MaximizerMCTSAgent(1)

    state = Twenty48State()
    env = RandomDistributionAgent()

    print(state)
    
    while not state.is_terminal:
        action, single_search_info = agent.search(state)
    
        state = state.result(action)
    
        print(single_search_info)
        print(state)

        if state.is_terminal:
            break
        
        effect, _ = env.search(state)
        state = state.result(effect)

exit()

if __name__ == "__main__":

    a = StaticWeightedMCTSAgent(1)
    s = ConnectFourState()

    print(a.search(s))

    for agent in agents[:12]:
        print(agent.__name__)
        for state in states[:2]:
            s = state()
            a = agent(search_time=1)
            print("   ", state.__name__)
            print("   ", a.search(s))