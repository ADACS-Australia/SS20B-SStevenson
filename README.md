# ADACS SS20B SStevenson COMPAS

## Setup
### To run on your local machine

1. Clone the repository.
2. Install python packges using [python poetry](https://python-poetry.org/):
Run `poetry install --no-dev` for minimum install. This only installs required production packages.  
Run `poetry install` to also install development packages such as testing tools.

3. `cd src`
3. Initialise the DB with `poetry run python manage.py migrate`
    - Optional: load test data with `poetry run python manage.py loaddata compasweb/fixtures/test_data.json`
4. Start the development server.
  Run `poetry run python manage.py runserver` and open the [development server](http://localhost:8000/).

### To run the application using docker-compose

1. Clone the repository.
2. Run `ROOT_SUBDIRECTORY_PATH="" docker-compose up --build` and open the [development server](http://localhost:8080).
    - You can also have ROOT_SUBDIRECTORY_PATH in your environment. 

### Adding requirements

Requirements are managed using [python poetry](https://python-poetry.org/).

#### Add a production package
1. Run `poetry add hello` to add package `hello`
2. Run `poetry install`
3. Update requirements.txt with `poetry export -f requirements.txt --without-hashes > src/requirements.txt`. 

#### Add a development package
1. Run `poetry add --dev hello` to add development package `hello`
2. Follow the steps for production package aside from the 1st step

### Contributing

#### Installing black linter for use with arcanist:
1. Go to the top directory of where you have installed arcanist `cd arcanist_top_dir`
2. `git clone https://github.com/pinterest/arcanist-linters.git pinterest-linters`
3. Go to your repo `cd repo_dir`
4. `ln -s arcanist_top_dir/pinterest-linters .pinterest-linters`
