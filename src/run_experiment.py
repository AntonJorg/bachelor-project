import os
import argparse
import logging
import json
import random
from datetime import datetime
from functools import partial
from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from src.connectfour import ConnectFourState, result
from src.agents import agents

agent_dict = {agent.__name__: agent for agent in agents}

# define command line arguments
parser = argparse.ArgumentParser(description='Run a number of Connect Four games for \
                                            two agents, saving the results.')
parser.add_argument('agent0', help="The first agent to make a move.", choices=agent_dict.keys())
parser.add_argument('agent1', help="The second agent to make a move.", choices=agent_dict.keys())
parser.add_argument(
    'iterations', help="The number of games to play.", type=int)
parser.add_argument(
    '-t', help="The time available to the agents for taking an action.", type=float, default=1)

# parse command line arguments
args = parser.parse_args()


# set up logging folder structure
time_string = datetime.now().strftime("%y%m%d-%H%M%S")
folder = os.path.join("logs", time_string)
os.mkdir(folder)
os.mkdir(os.path.join(folder, "games"))

print("STARTING EXPERIMENT...")
print("Configuration:")
print(args)
print("Logs will be stored in:", folder)
print("Progress:")


logging.basicConfig(
    encoding='utf-8',
    filemode="w",
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


# define function for running one game
def run_game(i, agent0, agent1, t):
    # make sure that a given game with given agents and time will be identical
    random.seed(i)

    # log each game to separate file
    log_file = os.path.join(folder, "games", f"game_{i}.log")
    logger = logging.getLogger()
    logger.handlers = []  # remove all handlers
    fh = logging.FileHandler(log_file)
    logger.addHandler(fh)

    logger.info(f"STARTING GAME {i}")
    logger.info(f"Agent 0: {agent0}")
    logger.info(f"Agent 1: {agent1}")

    agents = [agent_dict[agent0](t), agent_dict[agent1](t)]

    state = ConnectFourState(7, 6)

    logger.info(state)

    actions = []

    while not state.is_terminal:
        agent_idx = state.moves % 2
        agent = agents[agent_idx]
        action = agent.search(state)
        if action is None:
            print(state)
            print(agent.root)
            print(agent.root.children)
            print(agent.root.unexpanded_actions)
        state = result(state, action)
        actions.append(str(action))
        logger.info(f"Root: {agent.root}")
        logger.info("Children:")
        for c in agent.root.children:
            logger.info(c)
        logger.info(f"Agent {agent_idx} took action {action}")
        logger.info(state)

    game = "".join(actions)

    return i, state.utility, game


# insert all the constant arguments
thread_function = partial(run_game, agent0=args.agent0,
                          agent1=args.agent1, t=args.t)

# run games on multiple processes
results = process_map(thread_function, range(args.iterations))


# process results
agent0_wins = 0
agent1_wins = 0
draws = 0
games = {}

for i, utility, game in results:
    if utility == 1:
        agent0_wins += 1
    elif utility == 0:
        agent1_wins += 1
    else:
        draws += 1

    games[i] = game


# save results
with open(os.path.join(folder, "data.json"), 'w') as json_file:
    json.dump(
        {
            "p1_wins": agent0_wins,
            "p2_wins": agent1_wins,
            "draws": draws,
            "iterations": args.iterations,
            "games": games
        },
        json_file)
