import os
from tqdm import tqdm

from src.connectfour import ConnectFourState, result


dir_path = os.path.join("data", "processed")

move_strings = []

for filename in ["winning", "losing", "drawing"]:
    with open(os.path.join(dir_path, filename + ".data"), "r") as f:
        move_strings.extend(f.read().splitlines())


print("Verifying that no move sequences in the dataset are unapplicable...")

for move_string in tqdm(move_strings):
    state = ConnectFourState(7, 6)

    for move in move_string:
        action = int(move)
        assert action in state.applicable_actions
        state = result(state, action)
        assert state.utility == 0.5
    
print("Verification complete!")
