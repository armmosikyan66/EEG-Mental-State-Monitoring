.PHONY: init start clean

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

VENV=venv
PYTHON=$(VENV)/bin/python3

# Setup the project
init:
	@echo "Setting up the project..."
	python3 -m venv venv
	@echo "Activating virtual environment..."
	@. venv/bin/activate
	pip install -r requirements.txt

# Start the project
start:
	uvicorn main:app --reload --log-level debug --host localhost --port ${PORT}

# Clean the project (e.g., remove temporary files, etc.)
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf venv
	@echo "Clean up completed."
