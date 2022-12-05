from typing import Union

from src.games.connectfour import ConnectFourState
from src.games.nim import NimState
from src.games.checkers import CheckersState
# import env state as normal state since env is the first state in the game
from src.games.twenty48 import Twenty48EnvironmentState, Twenty48State

states = (
    ConnectFourState,
    NimState,
    Twenty48State
)

# Only for typing
# TODO: Consider if this should be an abstract base class?
GameState = Union[ConnectFourState, NimState, CheckersState, Twenty48State, Twenty48EnvironmentState]