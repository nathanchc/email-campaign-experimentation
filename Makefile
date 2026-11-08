.PHONY: data data-lazada prepare test

data:
	python scripts/download_data.py

data-lazada:
	python scripts/download_data.py --lazada

prepare:
	python scripts/prepare_data.py

test:
	pytest -q
