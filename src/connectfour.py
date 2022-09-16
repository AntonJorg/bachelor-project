from typing import List
import matplotlib.pyplot as plt


class ConnectFourState:
    """
    Bitboard representation for a 7x6 board. The bits marked by dots
    are used for denoting a full row.

    .  .  .  .  .  .  .
    5 12 19 26 33 40 47
    4 11 18 25 32 39 46
    3 10 17 24 31 38 45
    2  9 16 23 30 37 44
    1  8 15 22 29 36 43
    0  7 14 21 28 35 42 




    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.piece_mask = 0
        self.player_mask = 0

        self.moves = 0

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
        board += f"Applicable actions: {[i + 1 for i in self.applicable_actions]}\n"
        board += f"Piece mask : {bin(self.piece_mask)}\n"
        board += f"Player mask: {bin(self.player_mask)}\n"
        board += f"Moves made : {str(self.moves)}\n"
        board += f"Winner     : {self.utility()}"
        return board

    @property
    def applicable_actions(self) -> List[int]:
        return [i for i in range(7) if not self.piece_mask & (1 << 5 + i * 7)]

    def utility(self) -> int:
        # the winner can only be the previous player to move
        pieces = self.player_mask ^ self.piece_mask
        previous_player = 1 if self.moves % 2 else -1

        # horizontal
        m = pieces & pieces >> 7
        if m & m >> 14 > 0:
            return previous_player

        # vertical
        m = pieces & pieces >> 1
        if m & m >> 2 > 0:
            return previous_player

        # diagonal
        m = pieces & pieces >> 6
        if m & m >> 12 > 0:
            return previous_player

        # antidiagonal
        m = pieces & pieces >> 8
        if m & m >> 16 > 0:
            return previous_player

        return 0

    def visualize(self, savepath=None):

        # set axis limits of plot (x=0 to 20, y=0 to 20)
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


class ConnectFour:
    @staticmethod
    def initial_state(width=7, height=6):
        return ConnectFourState(width, height)

    @staticmethod
    def result(state: ConnectFourState, action: int) -> ConnectFourState:
        state.player_mask ^= state.piece_mask
        state.piece_mask |= state.piece_mask + \
            (1 << action * (state.height + 1))

        state.moves += 1

        return state

    @staticmethod
    def reverse(state: ConnectFourState, action: int) -> ConnectFourState:
        col_mask = 2**(state.height + 1) - 1 << action * (state.height + 1)

        # remove most significant bit in column
        state.piece_mask &= ~col_mask | (
            state.piece_mask & state.piece_mask >> 1)

        state.player_mask ^= state.piece_mask
        state.moves -= 1

        return state

    def apply_many(self, state: ConnectFourState, action_string: str) -> ConnectFourState:
        for char in action_string:
            action = int(char)
            self.result(state, action)
        return state


if __name__ == "__main__":
    c4 = ConnectFour()

    state = c4.initial_state(5, 4)

    c4.apply_many(state, "0123321001233210")

    state.visualize()

    print(state)

    while not state.utility():
        action = int(input("Enter move: ")) - 1
        c4.result(state, action)

        print(state)
        state.visualize()