from src.agents.minimax_agents import *

from src.agents.mcts_agents import *

agents = (
    IterativeDeepeningAgent, 
    IterativeDeepeningAlphaBetaAgent,
    IterativeDeepeningSimulationAgent,
    BeamSearchAgent,
    BestFirstMiniMaxAgent,
    MCTSAgent,
    MCTSEvaluationAgent,
    PartialExpansionAgent,
    MiniMaxWeightedMCTSAgent,
    StaticWeightedMCTSAgent,
    MCTSTreeMiniMaxAgent,
    ProgressivePruningMCTSAgent
)