# ADACS SS20B SStevenson COMPAS

## Setup
### To run on your local machine

1. Clone the repository.
2. Install python packges using [python poetry](https://python-poetry.org/):
Run `poetry install --no-dev` for minimum install. This only installs required production packages.
Run `poetry install` to also install development packages such as testing tools.

3. Create a copy from `src/.env.template` and rename it to `src/.env` and ENSURE ALL DB CONNECTION CONFIG OPTIONS ARE COMMENTED OUT/REMOVED (to use the django sqlite db server)

4. [Download](https://redis.io/download) and install Redis
5. In a new terminal, run Redis server `redis-server`
6. In a new terminal, run Celery worker in
    ```
    cd src
    poetry run celery -A compas.celery worker --loglevel=info
    ```
7. In a new terminal `cd src`
8. Initialise the DB with `poetry run python manage.py migrate`
    - Optional: load test data with `poetry run python manage.py loaddata compasweb/fixtures/test_data.json`
9. Start the development server.
  Run `poetry run python manage.py runserver` and open the [development server](http://localhost:8000/).

### To run the application using docker-compose

1. Clone the repository.
2. Create a copy from `.env.template` and rename it to `.env`
    - To use MySQL db in production environment, uncomment the database connection details and modify usernames + passwords as necessary, otherwise leave uncommented to use sqlite db
      ```
      DB_ENGINE=django.db.backends.mysql
      MYSQL_DATABASE=<name of your MySQL DB>
      MYSQL_USER=<username to log in to DB>
      MYSQL_PASSWORD=<password>
      MYSQL_HOST=<MySQL default hostname>
      MYSQL_ROOT_PASSWORD=<root password>
      DB_PORT=<MySQL Server port>
      ```
      (Note: if you modify the port, you'll need to also change it in `docker-compose.yml`).
    - Modify `DJANGO_SECRET_KEY` however you prefer
    - Uncomment `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`
      ```
      CELERY_BROKER_URL=redis://redis:6379
      CELERY_RESULT_BACKEND=redis://redis:6379
      ```
    - Modify COMPAS IO settings
      ```
      COMPAS_EXECUTABLE_PATH=/app/COMPAS/bin/COMPAS
      COMPAS_INPUT_DIR_PATH=/files/jobs/
      COMPAS_LOGS_OUTPUT_DIR_PATH=/files/jobs/
      ```
    - Keep everything else as is
3. If you're running it on your local machine, Run `ROOT_SUBDIRECTORY_PATH="" COMPAS_HOST="" docker-compose up --build` and open the [development server](http://localhost:8080).
4. Alternatively, if you're running on a production server
    - Set the value of COMPAS_HOST to your IP address or domain name if you're not running it locally. Ex. `https://compasportal.com/`
    - Optional: You can set the value of `ROOT_SUBDIRECTORY_PATH`. This is the part that appears after your server IP/domain name. Ex. `live/compasweb`. `ROOT_SUBDIRECTORY_PATH` needs to be set in `.env` as well

    - Application URL would be `<IP address/Domain><ROOT_SUBDIRECTORY_PATH>`. Ex. `https://compasportal.com/live/compasweb`

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
