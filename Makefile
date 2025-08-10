.PHONY: help install test build clean release run run-server

help: ## Show this help message
	@echo "TermEmoji - Terminal-based Emoji Battle Royale Game"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	python -m pip install --upgrade pip
	@if [ "$(OS)" = "Windows_NT" ]; then \
		python -m pip install windows-curses; \
	fi
	python -m pip install -e .

test: ## Run tests
	python -c "import sys; print('Python version:', sys.version)"
	python -c "import curses; print('Curses available')"
	python -c "from main import main; print('Main module imports successfully')"
	python -c "from server import main as server_main; print('Server module imports successfully')"
	python -c "from characters import CHARACTERS; print(f'Found {len(CHARACTERS)} characters')"

build: ## Build the package
	python setup.py sdist bdist_wheel

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -name "*.pyc" -delete

release: clean build ## Create a release build
	python build_release.py

run: ## Run the game
	python main.py

run-server: ## Run the server
	python server.py --host 0.0.0.0 --port 8765

install-dev: ## Install development dependencies
	python -m pip install --upgrade pip
	@if [ "$(OS)" = "Windows_NT" ]; then \
		python -m pip install windows-curses; \
	fi
	python -m pip install setuptools wheel twine

publish: build ## Publish to PyPI (requires credentials)
	twine upload dist/*

check: ## Check package for issues
	python setup.py check
	twine check dist/*

format: ## Format code (if you have black installed)
	black *.py

lint: ## Lint code (if you have flake8 installed)
	flake8 *.py

all: clean install test build ## Run all checks and build
