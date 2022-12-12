from src.games import NimState

# calculates the game tree complexity of Nim with initial heap sizes
#   {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
if __name__ == "__main__":
    state = NimState()
    
    print(state)

    tt = dict()

    def f(state):
        if state.is_terminal:
            return 1

        v = tt.get(tuple(sorted(state.array)))

        if v is None:
            retval = sum(f(state.result(a)) for a in state.applicable_actions)
            tt[tuple(sorted(state.array))] = retval
            return retval
        else:
            return v 

    print(f(state))
