import os
import argparse
import logging
import json
from datetime import datetime
from tqdm import tqdm

from src.connectfour import ConnectFourState, result
from src.treesearch import random_agent, mcts_agent, minimax_agent


parser = argparse.ArgumentParser(description='Run a number of Connect Four games for \
                                            two agents, saving the results.')
parser.add_argument('agent0', help="The first agent to make a move.", choices=[
                    "random", "mcts", "minimax"])
parser.add_argument('agent1', help="The second agent to make a move.", choices=[
                    "random", "mcts", "minimax"])
parser.add_argument(
    'iterations', help="The number of games to play.", type=int)
parser.add_argument(
    '-t', help="The time available to the agents for taking an action.", type=float, default=1)

args = parser.parse_args()


time_string = datetime.now().strftime("%y%m%d-%H%M%S")
base_filename = os.path.join("logs", time_string)


logging.basicConfig(
    filename=f'{base_filename}.log',
    encoding='utf-8',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


print("STARTING EXPERIMENT...")
print("Configuration:")
print(args)
print("Logs will be stored in:")
print(f"{base_filename}.log")
print(f"{base_filename}.json")
print("Progress:")

agent_dict = {
    "random": random_agent,
    "mcts": mcts_agent,
    "minimax": minimax_agent
}


agents = [agent_dict[args.agent0](args.t), agent_dict[args.agent1](args.t)]
agent0_wins = 0
agent1_wins = 0
draws = 0
games = []

pbar = tqdm(range(args.iterations))

# TODO: Implement multiprocessing https://www.youtube.com/watch?v=X7vBbelRXn0

for i in pbar:

    logging.info(f"STARTING GAME {i}")

    state = ConnectFourState(7, 6)

    logging.info(state)

    actions = []

    while not state.is_terminal:
        agent_idx = state.moves % 2
        action, root = agents[agent_idx].search(state)
        state = result(state, action)
        actions.append(str(action))
        logging.info(f"Root: {root}")
        logging.info("Children:")
        for c in root.children:
            logging.info(c)
        logging.info(f"Agent {agent_idx} took action {action}")
        logging.info(state)

    games.append("".join(actions))

    if state.utility == 1:
        agent0_wins += 1
    elif state.utility == 0:
        agent1_wins += 1
    else:
        draws += 1

logging.info("Results:")
logging.info(
    f"Player 1: {agent0_wins / args.iterations * 100:.2f}% ({agent0_wins} wins)")
logging.info(
    f"Player 2: {agent1_wins / args.iterations * 100:.2f}% ({agent1_wins} wins)")
logging.info(f"Draws   : {draws / args.iterations * 100:.2f}% ({draws} games)")

with open(f'{base_filename}.json', 'w') as json_file:
    json.dump(
        {
            "p1_wins": agent0_wins,
            "p2_wins": agent1_wins,
            "draws": draws,
            "iterations": args.iterations,
            "games": games
        },
        json_file)
