deps:
	pip install -r requirements.txt

.PHONY: assets

assets:
	@echo "Running asset compiler."
	python ./assets/compiler.py
