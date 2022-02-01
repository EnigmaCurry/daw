install:
	poetry install

clean:
	rm -rf dist daw.egg-info build __pycache__ daw/*.so daw/*.c

run:
	poetry run python -m daw.main ${PROJECT}

test:
	poetry run pytest --doctest-modules --verbose

