from typing import Union

from src.games.connectfour import ConnectFourState
from src.games.nim import NimState

states = (
    ConnectFourState,
    NimState
)

# Only for typing
# TODO: Consider if this should be an abstract base class?
GameState = Union[ConnectFourState, NimState]