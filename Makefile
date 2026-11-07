.PHONY: data prepare test

data:
	python scripts/download_data.py

prepare:
	python scripts/prepare_data.py

test:
	pytest -q
