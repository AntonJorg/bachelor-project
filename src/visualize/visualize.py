import numpy as np
import matplotlib.pyplot as plt

from src.connectfour import ConnectFourState, apply_many
from src.agents.mcts_agents import MCTSAgent
from src.agents.minimax_agents import BestFirstMiniMaxAgent, IterativeDeepeningAlphaBetaAgent

def draw_state(state, savepath=None):
    plt.axis([0, 10 * state.width, 0, 10 * state.height])
    plt.axis("off")
    plt.gca().set_aspect('equal', adjustable='box')

    r = plt.Rectangle((0, 0), 10 * state.width, 10 *
                        state.height, color="grey")
    plt.gca().add_artist(r)

    for i in range(state.height - 1, -1, -1):
        for j in range(state.width):
            idx = i + j * (state.height + 1)
            if state.piece_mask & 1 << idx:

                # TODO: REFACTOR

                if (state.player_mask & 1 << idx):
                    if state.moves % 2:
                        c = "r"
                    else:
                        c = "b"
                else:
                    if state.moves % 2:
                        c = "b"
                    else:
                        c = "r"
            else:
                c = "w"

            c = plt.Circle((5 + 10 * j, 5 + 10 * i), radius=4, color=c)
            plt.gca().add_artist(c)

    plt.show()

def action_values(state, agent):
    best_action, _ = agent.search(state)

    values = np.zeros(state.width)

    if hasattr(agent, "last_iter_root"):
        root = agent.last_iter_root
    else:
        root = agent.root

    for c in root.children:
        value = c.cumulative_utility / c.count if c.count else c.eval
        values[c.generating_action] = value

    plt.bar(range(state.width), values)
    plt.ylim(0, 1)
    plt.show()



if __name__ == "__main__":
    state = ConnectFourState(7, 6)

    state = apply_many(state, "0022335")

    draw_state(state)

    agent = MCTSAgent(2)

    action_values(state, agent)