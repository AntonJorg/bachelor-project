import os
import json
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


out_folder = os.path.join("latex", "images")

top_four_index = {
	"IterativeDeepeningSimulationAgent": 0,
	"BestFirstMiniMaxAgent": 1,
	"MCTSAgent": 2,
	"PartialExpansionAgent": 3
}

dir_path = os.path.join("experiments", "c4_top_four")

array = np.zeros((4, 4))

for exp in os.listdir(dir_path):
	agent0, agent1 = exp.split("vs")
	agent0, agent1 = agent0.split("+")[0], agent1.split("+")[0]

	x, y = top_four_index[agent0], top_four_index[agent1]

	path = os.path.join(dir_path, exp, "data.json")
	with open(path, "r") as f:
		d = json.load(f)
		array[x, y] = (d["agent0_wins"] + d["draws"] / 2) / d["iterations"]

fig = plt.figure()
names = ("ID-SIM", "BFMM", "MC", "PE")

sb.heatmap(array, cmap="crest", vmin=0, vmax=1, xticklabels=names, 
	yticklabels=names, linewidth=.5, square=True, annot=True,
	fmt=".2f")

plt.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

plt.title("Minimax Agents")
plt.ylabel("Max Player")
plt.xlabel("Min Player")

plt.gca().xaxis.set_label_position("top")

plt.tight_layout()

file = "connectfour_top_four_results.pdf"
plt.savefig(os.path.join(out_folder, file))


def fold(array):
	out = np.zeros((4, 4))
	for i in range(1, 4):
		for j in range(0, i):
			v = (array[i, j] + 1 - array[j, i]) / 2
			out[i, j] = v
			out[j, i] = 1 - v

	return out

array = fold(array)

fig = plt.figure()
names = ("ID-SIM", "BFMM", "MC", "PE")

sb.heatmap(array, cmap="crest", vmin=0, vmax=1, xticklabels=names, 
	yticklabels=names, linewidth=.5, square=True, annot=True,
	fmt=".2f")

plt.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

plt.title("Minimax Agents")
plt.ylabel("Max Player")
plt.xlabel("Min Player")

plt.gca().xaxis.set_label_position("top")

plt.tight_layout()

file = "connectfour_top_four_results_folded.pdf"
plt.savefig(os.path.join(out_folder, file))

array = np.sum(array, axis=1) / 3

sb.set()

fig = plt.figure()

bar1 = plt.bar(range(1, 5), array)

plt.gca().set_title("Minimax Agents")
plt.gca().set_ylabel("Average Winrate")
plt.gca().set_xlabel("Agent")
plt.gca().set_xticks(range(1, 5))
plt.gca().set_xticklabels(names)
plt.gca().bar_label(bar1, (f"{val:.2f}" for val in array))
plt.gca().set_ylim(0, 1)

#plt.tight_layout()

file = "connectfour_top_four_results_average.pdf"
plt.savefig(os.path.join(out_folder, file))





dir_path = os.path.join("experiments", "nim_top_four")

array = np.zeros((4, 4))

for exp in os.listdir(dir_path):
	agent0, agent1 = exp.split("vs")
	agent0, agent1 = agent0.split("+")[0], agent1.split("+")[0]

	x, y = top_four_index[agent0], top_four_index[agent1]

	path = os.path.join(dir_path, exp, "data.json")
	with open(path, "r") as f:
		d = json.load(f)
		array[x, y] = (d["agent0_wins"] + d["draws"] / 2) / d["iterations"]

fig = plt.figure()
names = ("ID-SIM", "BFMM", "MC", "PE")

sb.heatmap(array, cmap="crest", vmin=0, vmax=1, xticklabels=names, 
	yticklabels=names, linewidth=.5, square=True, annot=True,
	fmt=".2f")

plt.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

plt.title("Minimax Agents")
plt.ylabel("Max Player")
plt.xlabel("Min Player")

plt.gca().xaxis.set_label_position("top")

plt.tight_layout()

file = "nim_top_four_results.pdf"
plt.savefig(os.path.join(out_folder, file))


def fold(array):
	out = np.zeros((4, 4))
	for i in range(1, 4):
		for j in range(0, i):
			v = (array[i, j] + 1 - array[j, i]) / 2
			out[i, j] = v
			out[j, i] = 1 - v

	return out

array = fold(array)

fig = plt.figure()
names = ("ID-SIM", "BFMM", "MC", "PE")

sb.heatmap(array, cmap="crest", vmin=0, vmax=1, xticklabels=names, 
	yticklabels=names, linewidth=.5, square=True, annot=True,
	fmt=".2f")

plt.tick_params(axis="x", labelbottom = False, labeltop=True, top=True, bottom=False)

plt.title("Minimax Agents")
plt.ylabel("Max Player")
plt.xlabel("Min Player")

plt.gca().xaxis.set_label_position("top")

plt.tight_layout()

file = "nim_top_four_results_folded.pdf"
plt.savefig(os.path.join(out_folder, file))

array = np.sum(array, axis=1) / 3

sb.set()

fig = plt.figure()

bar1 = plt.bar(range(1, 5), array)

plt.gca().set_title("Minimax Agents")
plt.gca().set_ylabel("Average Winrate")
plt.gca().set_xlabel("Agent")
plt.gca().set_xticks(range(1, 5))
plt.gca().set_xticklabels(names)
plt.gca().bar_label(bar1, (f"{val:.2f}" for val in array))
plt.gca().set_ylim(0, 1.1)

plt.tight_layout()

file = "nim_top_four_results_average.pdf"
plt.savefig(os.path.join(out_folder, file))
