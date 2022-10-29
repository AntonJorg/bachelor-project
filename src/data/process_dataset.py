import os
from tqdm import tqdm

file_path = os.path.join("data", "original", "positions.data")

with open(file_path, "r") as f:
    lines = f.read().splitlines()

winning = []
losing = []
drawing = []

for line in tqdm(lines):
    position = line.strip().split(",")

    # last element either win, draw or loss, convert to utility value
    utility = position.pop()

    columns = []

    for i in range(7):
        column = position[(6 * i):(6 * (i + 1))]
        column = [p for p in column if p != "b"]
        column.reverse()
        columns.append(column)

    def recursive_solve(columns, player):
        if not any(columns):
            return ""

        playable = [i for i, c in enumerate(columns) if len(c) and c[-1] == player]

        player = "o" if player == "x" else "x"

        for i in playable:
            a = columns[i].pop()
            move = recursive_solve(columns, player)
            columns[i].append(a)

            if move is not None:
                return str(i) + move
        else:
            return None

    move_string = recursive_solve(columns, "x")

    if move_string is None:

        for i in range(7):
            print(position[(6 * i):(6 * (i + 1))])
        print(player)
        print(moves)
        for c in columns:
            print(c)
        raise RuntimeError("No valid moves found!")

    if utility == "win":
        winning.append(move_string)
    elif utility == "loss":
        losing.append(move_string)
    else:
        drawing.append(move_string)

print(f"Processed {len(winning) + len(losing) + len(drawing)} positions.")
print(f"{len(winning)} winning positions")
print(f"{len(losing)} losing positions")
print(f"{len(drawing)} drawing positions")

dir_path = os.path.join("data", "processed")

with open(os.path.join(dir_path, "winning.data"), "w+") as f:
    f.write("\n".join(winning))

with open(os.path.join(dir_path, "losing.data"), "w+") as f:
    f.write("\n".join(losing))

with open(os.path.join(dir_path, "drawing.data"), "w+") as f:
    f.write("\n".join(drawing))