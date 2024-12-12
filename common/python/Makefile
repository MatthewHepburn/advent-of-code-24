.SILENT:

.DEFAULT_GOAL := help
# Allow us to import files from this directory in our solutions
PYTHONPATH:= $(shell realpath "../../common/python/")

help: ## Shows this help page
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: part_a_example
part_a_example: ## Solve part A with example input
	PYTHONPATH="${PYTHONPATH}" AOC_EXAMPLE_MODE=1 python solve_a.py

.PHONY: part_a
part_a: ## Solve part A with real input
	PYTHONPATH="${PYTHONPATH}" AOC_EXAMPLE_MODE=0 python solve_a.py

.PHONY: part_b_example
part_b_example: ## Solve part B with example input
	PYTHONPATH="${PYTHONPATH}" AOC_EXAMPLE_MODE=1 python solve_b.py

.PHONY: part_b
part_b: ## Solve part B with real input
	PYTHONPATH="${PYTHONPATH}" AOC_EXAMPLE_MODE=0 python solve_b.py
