install:
	poetry install

clean:
	rm -rf dist daw.egg-info build __pycache__ daw/*.so daw/*.c

run:
	poetry run python

test:
	poetry run pytest --doctest-modules --verbose

