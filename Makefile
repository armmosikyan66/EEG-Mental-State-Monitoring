# Makefile for managing the project

.PHONY: init start clean

# Setup the project
init:
	@echo "Setting up the project..."
	python3 -m venv venv
	@echo "Activating virtual environment..."
	@. venv/bin/activate
	pip install -r requirements.txt

# Start the project
start:
	@echo "Starting the project..."
	python3 main.py

# Clean the project (e.g., remove temporary files, etc.)
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf venv
	@echo "Clean up completed."
