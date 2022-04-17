BIN = .venv/bin/
CODE = cool_books

lint:
	$(BIN)flake8 --jobs 4 --statistics --show-source $(CODE) $(TEST)
	$(BIN)mypy $(CODE)
	$(BIN)black --target-version py36 --skip-string-normalization --line-length=119 --check $(CODE) $(TEST)

pretty:
	$(BIN)isort $(CODE) $(TEST)
	$(BIN)black --target-version py36 --skip-string-normalization --line-length=119 $(CODE) $(TEST)
	$(BIN)unify --in-place --recursive $(CODE) $(TEST)

plint: pretty lint

run-server:
	$(BIN)uvicorn cool_books.asgi:app --reload
