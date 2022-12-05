.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = ""
PROFILE = ""
PROJECT_NAME = ""
PYTHON_INTERPRETER = python3
MINIMAX_AGENTS = IterativeDeepeningAgent IterativeDeepeningAlphaBetaAgent IterativeDeepeningSimulationAgent BeamSearchAgent BestFirstMiniMaxAgent MCTSTreeMiniMaxAgent
MCTS_AGENTS = MCTSAgent MCTSEvaluationAgent PartialExpansionAgent StaticWeightedMCTSAgent MiniMaxWeightedMCTSAgent ProgressivePruningMCTSAgent

TOP_FOUR = IterativeDeepeningSimulationAgent BeamSearchAgent MCTSAgent PartialExpansionAgent

TIMES = 0.0625 0.125 0.25 0.5 1 2 4 8 16

N_COMPARISON = 250
N_TUNING = 200

N_2048 = 100

PP_ARGS := $(shell seq 1 .3333 15)
SIM_ARGS := $(shell seq 2 2 50) $(shell seq 54 4 150)

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Main entrypoint
run: requirements
	$(PYTHON_INTERPRETER) src/main.py

# Experiments
# Parameter Selection
progressive_pruning_parameter_selection: requirements
	for i in $(PP_ARGS) ; do \
		$(PYTHON_INTERPRETER) src/run_experiment.py MCTSAgent ProgressivePruningMCTSAgent $(N_TUNING) -loc pp_tuning -swap -arg2agent1 $$i ; \
	done

id_simulation_parameter_selection: requirements
	for i in $(SIM_ARGS) ; do \
		$(PYTHON_INTERPRETER) src/run_experiment.py IterativeDeepeningAgent IterativeDeepeningSimulationAgent $(N_TUNING) -loc sim_tuning -swap -arg2agent1 $$i ; \
	done

# Main Comparisons
minimax_connectfour: requirements
	for agent0 in $(MINIMAX_AGENTS) ; do \
		for agent1 in $(MINIMAX_AGENTS) ; do \
			$(PYTHON_INTERPRETER) src/run_experiment.py ConnectFour $$agent0 $$agent1 $(N_COMPARISON) -loc c4_minimax_agents; \
		done \
	done

mcts_connectfour: requirements
	for agent0 in $(MCTS_AGENTS) ; do \
		for agent1 in $(MCTS_AGENTS) ; do \
			$(PYTHON_INTERPRETER) src/run_experiment.py ConnectFour $$agent0 $$agent1 $(N_COMPARISON) -loc c4_mcts_agents; \
		done \
	done

top4_connectfour: requirements
	for agent0 in $(TOP_FOUR) ; do \
		for agent1 in $(TOP_FOUR) ; do \
			$(PYTHON_INTERPRETER) src/run_experiment.py ConnectFour $$agent0 $$agent1 $(N_COMPARISON) -loc c4_top_four; \
		done \
	done

top4_nim: requirements
	for agent0 in $(TOP_FOUR) ; do \
		for agent1 in $(TOP_FOUR) ; do \
			$(PYTHON_INTERPRETER) src/run_experiment.py Nim $$agent0 $$agent1 $(N_COMPARISON) -loc nim_top_four; \
		done \
	done

nim_time: requirements
	for time in $(TIMES) ; do \
			$(PYTHON_INTERPRETER) src/run_experiment.py Nim MCTSAgent PartialExpansionAgent $(N_COMPARISON) -loc nim_time -swap -t $$time; \
	done

c4_time: requirements
	for time in $(TIMES) ; do \
			$(PYTHON_INTERPRETER) src/run_experiment.py ConnectFour MCTSAgent PartialExpansionAgent $(N_COMPARISON) -loc c4_time -swap -t $$time; \
	done

2048_expectimax:
	$(PYTHON_INTERPRETER) src/run_2048_experiment.py IDExpectiMaxAgent $(N_2048) -t 2 -loc twenty48_temp

2048_mcts:
	$(PYTHON_INTERPRETER) src/run_2048_experiment.py MaximizerMCTSAgent $(N_2048) -t 2 -loc twenty48


# Cleanup
clear_logs:
	rm -r logs
	mkdir logs

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src


## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py

## Data
data: requirements
	$(PYTHON_INTERPRETER) src/data/get_dataset.py
	$(PYTHON_INTERPRETER) src/data/process_dataset.py

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')