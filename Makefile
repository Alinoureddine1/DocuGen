.PHONY: setup test clean run

setup:
	python -m venv venv
	. venv/Scripts/activate && pip install -e ".[dev]"
	. venv/Scripts/activate && python -m docugen.nltk_downloader

test:
	python -m unittest discover tests

clean:
	rm -rf venv
	rm -rf output
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

run:
	python -m docugen.docugen $(ARGS)