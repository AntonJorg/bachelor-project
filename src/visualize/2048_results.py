import os
import json
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

sb.set()

folder = os.path.join("experiments", "twenty48")

utilities = {}
percentages = {}

for exp in os.listdir(folder):
    with open(os.path.join(folder, exp, "data.json"), "r") as f:
        data = json.load(f)

    key = exp[:exp.find("Agent")]

    boards = data["boards"].values()
    utils = list(data["utilities"].values())

    max_tiles = []

    for board in boards:
        max_tiles.append(max(max(row) for row in board))

    l = min(max_tiles)
    h = max(max_tiles)

    percentage_reached = []
    for v in range(l, h + 1):
        temp = [val for val in max_tiles if val >= v]
        percentage_reached.append((v, len(temp)))

    percentages[key] = percentage_reached
    utilities[key] = utils

labels = ['1024', '2048', '4096']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5), gridspec_kw={"width_ratios": [1, 2]})

rects1 = ax1.bar(1, np.mean(utilities["IDExpectiMax"]), width, label='ExpectiMax')
rects2 = ax1.bar(1.5, np.mean(utilities["MaximizerMCTS"]), width, label='MCTS')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax1.set_ylabel('Average score')
ax1.set_title('Average score')
ax1.set_xticks((1, 1.5), ("ExpectiMax", "MCTS"))
#ax1.legend()

ax1.bar_label(rects1, padding=3)
ax1.bar_label(rects2, padding=3)



rects1 = ax2.bar(x - width/2, tuple(v[1] for v in percentages["IDExpectiMax"])[1:], width, label='ExpectiMax')
rects2 = ax2.bar(x + width/2, tuple(v[1] for v in percentages["MaximizerMCTS"])[1:], width, label='MCTS')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax2.set_ylabel('Percentage of games that reached tile')
ax2.set_title('Tiles Reached')
ax2.set_xticks(x, labels)
ax2.legend()

ax2.bar_label(rects1, padding=3)
ax2.bar_label(rects2, padding=3)

fig.suptitle("2048 results, $n=100$")
fig.tight_layout()

plt.savefig(os.path.join("latex", "images", "2048_results.pdf"))