PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: run debug lint lint-strict clean install

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy .

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

clean:
	rm -rf __pycache__ MazeGen/__pycache__ .mypy_cache
	rm -rf dist/ *.egg-info/

install:
	$(PYTHON) -m pip install -r requirements.txt

build:
	$(PYTHON) -m build
