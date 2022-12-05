from src.games import NimState

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
