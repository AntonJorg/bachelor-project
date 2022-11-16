from src.agents import *
from src.games import *

if __name__ == "__main__":
    for state in states:
        print("GAME:", state.__name__.replace("State", ""))
        s = state()
        for agent in agents:
            print(agent.__name__)
            a = agent(1)
            print(a.search(s))