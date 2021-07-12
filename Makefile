PHONY: .serve

serve:
	poetry run uvicorn app.main:app --reload
