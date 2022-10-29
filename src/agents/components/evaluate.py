import random
from math import exp, ceil

from src.connectfour import ConnectFourState, result, apply_many


class Evaluate:
    """
    Defines methods for implementing TreeSearchAgent.evaluate.

    These methods should:
        - Take a ConnectFourState
        - Return an estimate of the utility of the state, as a float
        - Not have any side effects
        - Not have to be deterministic
    """
    
    def evaluate_utility(self, state):
        if state.is_terminal:
            return state.utility
        else:
            return None

    def simulate(self, state):
        while not state.is_terminal:
            action = random.choice(state.applicable_actions)
            state = result(state, action)

        return state.utility

    def simulate_many(self, state):        
        values = (self.simulate(state) for _ in range(self.num_simulations))
        return sum(values) / self.num_simulations

    def count_consecutives(self, state):
        if state.is_terminal:
            return state.utility

        if state.moves % 2:
            other_pieces = state.player_mask
            current_pieces = state.player_mask ^ state.piece_mask
        else:
            current_pieces = state.player_mask
            other_pieces = state.player_mask ^ state.piece_mask


        shifts = [state.height + 1, 1, state.height, state.height + 2]

        # count 2 connected
        current_two = 0
        other_two = 0
        for shift in shifts:
            current_two += (current_pieces & current_pieces >> shift).bit_count()
            other_two += (other_pieces & other_pieces >> shift).bit_count()
        
        # count three connected
        current_three = 0
        other_three = 0
        for shift in shifts:
            m = current_pieces & current_pieces >> shift
            current_three += (m & m >> shift).bit_count()
            m = other_pieces & other_pieces >> shift
            other_three += (m & m >> shift).bit_count()

        col_mask = 2**(state.height) - 1
        weights = list(range(ceil(state.width / 2))) + list(reversed(range(state.width // 2)))
        weights = (w + 1 for w in weights)

        current_position = 0
        other_position = 0
        for i, weight in enumerate(weights):
            current_position += (current_pieces & col_mask << i * (state.height + 1)).bit_count() * weight
            other_position += (other_pieces & col_mask << i * (state.height + 1)).bit_count() * weight

        score = (current_position - other_position) * .01 + (current_two - other_two) * .1 + current_three - other_three    

        return 1 / (1 + exp(-score))


if __name__ == "__main__":
    ev = Evaluate()

    for action in range(7):
        state = ConnectFourState(7, 6)
        state = result(state, action)
        print(state)
        print(ev.count_consecutives(state))