import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
sb.set()

out_folder = os.path.join("latex", "images")

dir_path = os.path.join("experiments", "nim_time")

sub_dirs = os.listdir(dir_path)

fig, ax = plt.subplots(ncols=1, figsize=(6, 5))

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

sb.lineplot(x=x, y=wr, ax=ax)
ax.plot(x, baseline, linestyle="--")
ax.scatter(x[idx], wr[idx], label=f"WR({x[idx]:.1f})={wr[idx]:.2f}",
	marker="^", c="r", zorder=2, s=100)
ax.set_ylim(0, 1)
ax.set_title("Progressive Pruning MCTS")
ax.set_xlabel("Pruning Factor")
ax.set_ylabel("Winrate vs MCTS")
ax.legend()

ax.set_xscale("log")

file = "time_performance.pdf"
plt.savefig(os.path.join(out_folder, file))
