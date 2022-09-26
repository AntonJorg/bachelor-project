from tqdm import tqdm
import logging
import json

from src.connectfour import ConnectFour
from src.treesearch import random_agent, mcts_agent, minimax_agent

logging.basicConfig(
    filename='example.log',
    encoding='utf-8',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

c4 = ConnectFour()

iterations = 20
agents = [mcts_agent(), mcts_agent()]
p1_wins = 0
p2_wins = 0
draws = 0
games = []

pbar = tqdm(range(iterations))

for i in pbar:

    logging.info(f"STARTING GAME {i}")

    state = c4.initial_state(7, 6)

    logging.info(state)

    actions = []

    while not state.is_terminal():
        agent_idx = state.moves % 2
        action, root = agents[agent_idx].search(state)
        c4.result(state, action)

        actions.append(str(action))
        logging.info(f"Root: {root}")
        logging.info("Children:")
        for c in root.children:
            logging.info(c)
        logging.info(f"Agent {agent_idx} took action {action}")
        logging.info(state)

    games.append("".join(actions))

    if state.utility() == 1:
        p1_wins += 1
    elif state.utility() == 0:
        p2_wins += 1
    else:
        draws += 1

logging.info("Results:")
logging.info(f"Player 1: {p1_wins / iterations * 100:.2f}% ({p1_wins} wins)")
logging.info(f"Player 2: {p2_wins / iterations * 100:.2f}% ({p2_wins} wins)")
logging.info(f"Draws   : {draws / iterations * 100:.2f}% ({draws} games)")

with open('example.json', 'w') as json_file:
    json.dump(
        {
            "p1_wins": p1_wins,
            "p2_wins": p2_wins,
            "draws": draws,
            "iterations": iterations,
            "games": games
        },
        json_file)
