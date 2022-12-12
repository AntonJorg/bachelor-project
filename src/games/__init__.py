from typing import Union

from src.games.connectfour import ConnectFourState
from src.games.nim import NimState
from src.games.twenty48 import Twenty48EnvironmentState, Twenty48State

GameState = Union[ConnectFourState, NimState, Twenty48State, Twenty48EnvironmentState]

states = (
    ConnectFourState,
    NimState
)
