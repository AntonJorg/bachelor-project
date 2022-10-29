"""
This module defines classes for inheritance into TreeSearchAgent
solely for organizational purposes.

These classes should not be instantiated under normal use.
"""


from src.agents.components._select import Select
from src.agents.components.expand import Expand
from src.agents.components.evaluate import Evaluate
from src.agents.components.backpropagate import Backpropagate
from src.agents.components.reflect import Reflect
from src.agents.components.get_best_move import GetBestMove
from src.agents.components.control import Control


# collect all imports for easy inheritance
components = (Select, Expand, Evaluate, Backpropagate, Reflect, GetBestMove, Control)
