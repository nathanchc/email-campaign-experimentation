.PHONY: data test

data:
	python scripts/download_data.py

test:
	pytest -q
