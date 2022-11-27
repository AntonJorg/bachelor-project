import cProfile

from src.agents import MCTSAgent, IterativeDeepeningSimulationAgent
from src.games import ConnectFourState, CheckersState, NimState

state = CheckersState()
agent = MCTSAgent(2)


with cProfile.Profile() as pr:
    print(agent.search(state))

pr.print_stats(sort="cumtime")