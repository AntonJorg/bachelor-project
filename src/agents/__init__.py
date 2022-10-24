from src.agents.minimax_agents import MiniMaxAgent
from src.agents.minimax_agents import IterativeDeepeningAgent
from src.agents.minimax_agents import IterativeDeepeningSimulationAgent
from src.agents.minimax_agents import BeamSearchAgent

from src.agents.mcts_agents import MCTSAgent
from src.agents.mcts_agents import MCTSEvaluationAgent

agents = (
    IterativeDeepeningAgent, 
    IterativeDeepeningSimulationAgent,
    BeamSearchAgent,
    MCTSAgent,
    MCTSEvaluationAgent
)