# django-history-example

## About this project

This is an example project to test the functionality of `django-simple-history`.

This uses Django with a SQLite database (for simplicity).


## Setup

This project uses:
- `poetry` for dependency managagement (https://python-poetry.org/)
- `precommit` to check commits to avoid committing sensitive data (https://pre-commit.com/)
- `ruff` for linting and formatting (https://docs.astral.sh/ruff/)
- `mypy` for checking type hints (https://mypy.readthedocs.io/en/stable/)

Make sure you have Python >= 3.12, `poetry` and `precommit` installed on your laptop. Then run `poetry install` to install relevant packages.

For linting and formatting: `make check-python-code` and `make format-python-code`. See the `Makefile` for more details (`make help`).

### Setting up the app

1. Clone the repo.
2. Run the migrations (which will create your SQLite database): `poetry run python manage.py migrate`.
3. Run the app: `make run`.
4. Go to http://localhost:8000 in the browser.

### Exploring the data

Explore in the shell: `poetry run python manage.py shell`.


## Populating the app with dummy data

There is a management command to populate the database with dummy data: `poetry run python manage.py generate_dummy_data`.


## Creating users

Create a superuser using `poetry run python manage.py createsuperuser`.

Create a regular user in the shell.


## Running the app

If you make database changes you will need to make migrations (`poetry run python manage.py makemigrations`) and run migrations (`poetry run python manage.py migrate`).

Then `make run` to run the app and go to http://localhost:8000 in the browser.

Go to http://localhost:8000/api/docs to see the API docs.
