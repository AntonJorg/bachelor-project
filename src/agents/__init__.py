from src.agents.minimax_agents import *
from src.agents.mcts_agents import *
from src.agents.random_agents import *
from src.agents.maximizer_agents import *

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
    ProgressivePruningMCTSAgent,
    RandomDistributionAgent,
    ExpectiMaxAgent,
    MaximizerMCTSAgent
)