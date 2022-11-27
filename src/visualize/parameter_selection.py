import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
sb.set()

out_folder = os.path.join("latex", "images")

dir_path = os.path.join("experiments", "pp_tuning")

sub_dirs = os.listdir(dir_path)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 5))

observations = []

for sub_dir in sub_dirs:
	path = os.path.join(dir_path, sub_dir, "data.json")
	param = float(sub_dir.split("=")[-1])
	with open(path, "r") as f:
		d = json.load(f)
		observations.append((param, (d["agent1_wins"] + d["draws"] / 2) / d["iterations"]))

observations.sort()
x, wr = list(zip(*observations))
x, wr, baseline = np.array(x), np.array(wr), np.ones(len(x)) / 2
idx = np.argmax(wr)
idx_sel = 15

sb.lineplot(x=x, y=wr, ax=ax1)
ax1.plot(x, baseline, linestyle="--")
ax1.scatter(x[idx], wr[idx], label=f"WR({x[idx]:.1f})={wr[idx]:.2f}",
	marker="^", c="r", zorder=2, s=100)
ax1.scatter(x[idx_sel], wr[idx_sel], label=f"Selected",
	c="b", zorder=2, s=100)
ax1.set_ylim(0, 1)
ax1.set_title("Progressive Pruning MCTS")
ax1.set_xlabel("Pruning Factor")
ax1.set_ylabel("Winrate vs MCTS")
ax1.legend()

dir_path = os.path.join("experiments", "sim_tuning")

sub_dirs = os.listdir(dir_path)

for sub_dir in sub_dirs:
	path = os.path.join(dir_path, sub_dir, "data.json")
	param = float(sub_dir.split("=")[-1])
	with open(path, "r") as f:
		d = json.load(f)
		observations.append((param, (d["agent1_wins"] + d["draws"] / 2) / d["iterations"]))

observations.sort()
x, wr = list(zip(*observations))
x, wr, baseline = np.array(x), np.array(wr), np.ones(len(x)) / 2
idx = np.argmax(wr)

sb.lineplot(x=x, y=wr, ax=ax2)
ax2.plot(x, baseline, linestyle="--")
ax2.scatter(x[idx], wr[idx], label=f"WR({x[idx]:.0f})={wr[idx]:.2f}",
	marker="^", c="r", zorder=2, s=100)
ax2.set_ylim(0, 1)
ax2.set_title("Iterative Deepening w/ Simulation")
ax2.set_xlabel("Number of simulations per evaluation")
ax2.set_ylabel("Winrate vs Iterative Deepening")
ax2.legend()


file = "connectfour_parameter_selection.pdf"
plt.savefig(os.path.join(out_folder, file))
