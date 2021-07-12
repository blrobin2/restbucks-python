PHONY: .serve, .format

serve:
	poetry run uvicorn app.main:app --reload

format:
	poetry run autopep8 --in-place --recursive .

lint:
	poetry run flake8
