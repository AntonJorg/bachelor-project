from src.agents import *
from src.games import *

# test all adversarial agents on all compatible environments
if __name__ == "__main__":
    for state in states:
        print(state.__name__)
        for agent in agents:
            s = state()
            a = agent(search_time=1)
            print("   ", agent.__name__)
            print("   ", a.search(s))
