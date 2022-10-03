from typing import List
import matplotlib.pyplot as plt


class ConnectFourState:
    """
    Represents the Connect 4 board as two binary numbers; the piece mask
    and the player mask. Each bit in the numbers correspond to a field on 
    the board as such:

    .  .  .  .  .  .  .
    5 12 19 26 33 40 47
    4 11 18 25 32 39 46
    3 10 17 24 31 38 45
    2  9 16 23 30 37 44
    1  8 15 22 29 36 43
    0  7 14 21 28 35 42 

    Bitboard representation for a 7x6 board. The bits marked by dots
    are used for denoting a full row.

    The piece mask describes which fields contain a piece, and the
    player mask describes which of those pieces belong to the current
    player.

    Though the move count could be inferred from the piece mask,
    this state also keeps a separate move count.
    """

    def __init__(self, width, height, piece_mask=0, player_mask=0, moves=0):
        self.width = width
        self.height = height

        self.piece_mask = piece_mask
        self.player_mask = player_mask

        self.moves = moves

        self.applicable_actions = self._init_applicable_actions()
        self.utility = self._init_utility()
        self.is_terminal = self._init_is_terminal()

    def __repr__(self):
        board = "Board:\n"
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width):
                idx = i + j * (self.height + 1)
                if self.piece_mask & 1 << idx:

                    # TODO: REFACTOR

                    if (self.player_mask & 1 << idx):
                        if self.moves % 2:
                            board += "2 "
                        else:
                            board += "1 "
                    else:
                        if self.moves % 2:
                            board += "1 "
                        else:
                            board += "2 "
                else:
                    board += ". "
            board += "\n"
        board += f"Applicable actions: {self.applicable_actions}\n"
        board += f"Piece mask : {bin(self.piece_mask)}\n"
        board += f"Player mask: {bin(self.player_mask)}\n"
        board += f"Moves made : {str(self.moves)}\n"
        board += f"Winner     : {self.utility}"
        return board

    def _init_applicable_actions(self) -> List[int]:
        """
        Returns the actions that are applicable in the current
        state, ie. the actions corresponding to non-full rows.
        """
        a = self.height - 1
        b = self.height + 1
        return [i for i in range(self.width) if not self.piece_mask & (1 << a + i * b)]

    def _init_utility(self) -> int:
        """
        Returns the utility of terminal states according to the
        following cases:

            Player 1 win: 1.0
            Player 2 win: 0.0
            Draw        : 0.5

        Even though the utility function is theoretically
        only defined on terminal states, this implementation does not
        check if that is the case, but will simply return 0.5 for
        non-terminal states, as there is no winner.
        """
        # the winner can only be the previous player to move
        pieces = self.player_mask ^ self.piece_mask
        utility_of_win = self.moves % 2

        # check horizontal win
        shift = self.height + 1
        m = pieces & pieces >> shift
        if m & m >> 2 * shift > 0:
            return utility_of_win

        # check vertical win
        m = pieces & pieces >> 1
        if m & m >> 2 > 0:
            return utility_of_win

        # check diagonal win
        shift = self.height
        m = pieces & pieces >> shift
        if m & m >> 2 * shift > 0:
            return utility_of_win

        # check antidiagonal win
        shift = self.height + 2
        m = pieces & pieces >> shift
        if m & m >> 2 * shift > 0:
            return utility_of_win

        # if no win is detected
        return 0.5

    def _init_is_terminal(self) -> bool:
        """
        Return True in terminal states, false otherwise.
        A state is terminal if there is a winner, or there are no applicable actions.
        """
        return not self.applicable_actions or self.utility != 0.5

#    def copy(self) -> 'ConnectFourState':
#        """
#        Return a copy of the state.
#        """
#        new = ConnectFourState(self.width, self.height)
#        new.piece_mask = self.piece_mask
#        new.player_mask = self.player_mask
#        new.moves = self.moves
#
#        return new

    def visualize(self, savepath=None):
        plt.axis([0, 10 * self.width, 0, 10 * self.height])
        plt.axis("off")
        plt.gca().set_aspect('equal', adjustable='box')

        r = plt.Rectangle((0, 0), 10 * self.width, 10 *
                          self.height, color="grey")
        plt.gca().add_artist(r)

        for i in range(self.height - 1, -1, -1):
            for j in range(self.width):
                idx = i + j * (self.height + 1)
                if self.piece_mask & 1 << idx:

                    # TODO: REFACTOR

                    if (self.player_mask & 1 << idx):
                        if self.moves % 2:
                            c = "r"
                        else:
                            c = "b"
                    else:
                        if self.moves % 2:
                            c = "b"
                        else:
                            c = "r"
                else:
                    c = "w"

                c = plt.Circle((5 + 10 * j, 5 + 10 * i), radius=4, color=c)
                plt.gca().add_artist(c)

        plt.show()


def result(state: ConnectFourState, action: int) -> ConnectFourState:
    """

    """
    player_mask = state.player_mask ^ state.piece_mask
    piece_mask = state.piece_mask | state.piece_mask + \
        (1 << action * (state.height + 1))

    return ConnectFourState(state.width, state.height, piece_mask, player_mask, state.moves + 1)


def reverse(state: ConnectFourState, action: int) -> ConnectFourState:
    """
    Modifies the state object to contain the result of un-making
    the given action. Also returns state for convenience.
    """
    col_mask = 2**(state.height + 1) - 1 << action * (state.height + 1)

    # remove most significant bit in column
    state.piece_mask &= ~col_mask | (
        state.piece_mask & state.piece_mask >> 1)

    state.player_mask ^= state.piece_mask
    state.moves -= 1

    return state


def apply_many(state: ConnectFourState, action_string: str) -> ConnectFourState:
    """
    Applies the result function for each action in action_string.
    Useful for generating positions.
    """
    for char in action_string:
        action = int(char)
        state = result(state, action)
    return state


if __name__ == "__main__":

    state = ConnectFourState(7, 6)

    print(state)

    while not state.is_terminal():
        action = int(input("Enter move: ")) - 1
        result(state, action)

        print(state)
