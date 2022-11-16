import os
import json
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


minimax_index = {
	"IterativeDeepeningAgent": 0,
	"IterativeDeepeningAlphaBetaAgent": 1,
	"IterativeDeepeningSimulationAgent": 2,
	"BeamSearchAgent": 3,
	"BestFirstMiniMaxAgent": 4,
	"MCTSTreeMiniMaxAgent": 5
}

mcts_index = {
	"MCTSAgent": 0,
	"MCTSEvaluationAgent": 1,
	"PartialExpansionAgent": 2,
	"StaticWeightedMCTSAgent": 3,
	"MiniMaxWeightedMCTSAgent": 4,
	"ProgressivePruningMCTSAgent": 5
}


dir_path = os.path.join("experiments", "c4_minimax_agents")

minimax = np.zeros((6, 6))

for exp in os.listdir(dir_path):
	agent0, agent1 = exp.split("vs")
	agent0, agent1 = agent0.split("+")[0], agent1.split("+")[0]

	x, y = minimax_index[agent0], minimax_index[agent1]

	path = os.path.join(dir_path, exp, "data.json")
	with open(path, "r") as f:
		d = json.load(f)
		minimax[x, y] = (d["agent0_wins"] + d["draws"] / 2) / d["iterations"]


dir_path = os.path.join("experiments", "c4_mcts_agents")

mcts = np.zeros((6, 6))

for exp in os.listdir(dir_path):
	agent0, agent1 = exp.split("vs")
	agent0, agent1 = agent0.split("+")[0], agent1.split("+")[0]

	x, y = mcts_index[agent0], mcts_index[agent1]

	path = os.path.join(dir_path, exp, "data.json")
	with open(path, "r") as f:
		d = json.load(f)
		mcts[x, y] = (d["agent0_wins"] + d["draws"] / 2) / d["iterations"]


fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(13, 6))
cbar_ax = fig.add_axes([.93,.115,.03,.76])

a = np.random.rand(6, 6)

minimax_names = ("ID", "ID-AB", "ID-Sim", "BS", "BFMM", "MM-MCT")
mcts_names = ("MC", "MC-SR", "PE", "SW-MC", "MW-MC", "PP")

sb.heatmap(minimax, cmap="crest", vmin=0, vmax=1, xticklabels=minimax_names, 
	yticklabels=minimax_names, linewidth=.5, square=True, annot=True,
	fmt=".2f", ax=ax1, cbar=False)

sb.heatmap(mcts, cmap="crest", vmin=0, vmax=1, xticklabels=mcts_names, 
	yticklabels=mcts_names, linewidth=.5, square=True, annot=True,
	fmt=".2f", ax=ax2, cbar_ax=cbar_ax)

ax1.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

ax1.set_title("Minimax Agents")
ax1.set_ylabel("Max Player")
ax1.set_xlabel("Min Player")

ax1.xaxis.set_label_position("top")

ax2.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

ax2.set_title("MCTS Agents")
ax2.set_ylabel("Max Player")
ax2.set_xlabel("Min Player")

ax2.xaxis.set_label_position("top")

#plt.tight_layout()
plt.show()


def fold(array):
	out = np.zeros((6, 6))
	for i in range(1, 6):
		for j in range(0, i):
			v = (array[i, j] + 1 - array[j, i]) / 2
			out[i, j] = v
			out[j, i] = 1 - v

	return out

minimax = fold(minimax)
mcts = fold(mcts)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(13, 6))
cbar_ax = fig.add_axes([.93,.115,.03,.76])

a = np.random.rand(6, 6)

minimax_names = ("ID", "ID-AB", "ID-Sim", "BS", "BFMM", "MM-MCT")
mcts_names = ("MC", "MC-SR", "PE", "SW-MC", "MW-MC", "PP")

sb.heatmap(minimax, cmap="crest", vmin=0, vmax=1, xticklabels=minimax_names, 
	yticklabels=minimax_names, linewidth=.5, square=True, annot=True,
	fmt=".2f", ax=ax1, cbar=False)

sb.heatmap(mcts, cmap="crest", vmin=0, vmax=1, xticklabels=mcts_names, 
	yticklabels=mcts_names, linewidth=.5, square=True, annot=True,
	fmt=".2f", ax=ax2, cbar_ax=cbar_ax)

ax1.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

ax1.set_title("Minimax Agents")
ax1.set_ylabel("Max Player")
ax1.set_xlabel("Min Player")

ax1.xaxis.set_label_position("top")

ax2.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

ax2.set_title("MCTS Agents")
ax2.set_ylabel("Max Player")
ax2.set_xlabel("Min Player")

ax2.xaxis.set_label_position("top")

#plt.tight_layout()
plt.show()


minimax = np.sum(minimax, axis=1) / 5
mcts = np.sum(mcts, axis=1) / 5

sb.set()

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(13, 6))


minimax_names = ("ID", "ID-AB", "ID-Sim", "BS", "BFMM", "MM-MCT")
mcts_names = ("MC", "MC-SR", "PE", "SW-MC", "MW-MC", "PP")

bar1 = ax1.bar(range(1, 7), minimax)

bar2 = ax2.bar(range(1, 7), mcts)

ax1.set_title("Minimax Agents")
ax1.set_ylabel("Average Winrate")
ax1.set_xlabel("Agent")
ax1.set_xticks(range(1, 7))
ax1.set_xticklabels(minimax_names)
ax1.bar_label(bar1, (f"{val:.2f}" for val in minimax))
ax1.set_ylim(0, 1)

ax2.set_title("MCTS Agents")
ax2.set_ylabel("Average Winrate")
ax2.set_xlabel("Agent")
ax2.set_xticks(range(1, 7))
ax2.set_xticklabels(mcts_names)
ax2.bar_label(bar2, (f"{val:.2f}" for val in mcts))
ax2.set_ylim(0, 1)

#plt.tight_layout()
plt.show()

