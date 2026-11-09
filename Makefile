# Usage:
#   make all                     download data, run tests, execute every notebook
#   make all PYTHON=/path/to/python   use a specific interpreter
PYTHON ?= python
export PYTHONPATH := $(CURDIR)/src$(if $(PYTHONPATH),:$(PYTHONPATH))
NOTEBOOKS := $(sort $(wildcard notebooks/*.ipynb))

.PHONY: all data data-lazada prepare test notebooks figures

all: data data-lazada prepare test notebooks

data:
	$(PYTHON) scripts/download_data.py

data-lazada:
	$(PYTHON) scripts/download_data.py --lazada

prepare:
	$(PYTHON) scripts/prepare_data.py

test:
	$(PYTHON) -m pytest -q

# Executes every chapter top to bottom. Results go to runs/ (not committed),
# so the notebooks in notebooks/ stay as published.
notebooks:
	$(PYTHON) -m nbconvert --to notebook --execute --ExecutePreprocessor.timeout=1800 --output-dir runs $(NOTEBOOKS)

# Saves the charts used in the README and case study to images/ (from the published notebooks).
figures:
	$(PYTHON) scripts/export_figures.py
