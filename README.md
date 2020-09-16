# Running the application

If you're running the application for the first time, run the following commands:

1. Create a virtual environment with `python -m venv env`
2. Activate the environment: `env/Scripts/activate`
    - For mac users: `. env/bin/activate`
3. Install the libraries needed for the application: `pip install -r requirements.txt`
4. Go into the application directory with `cd application` 
5. Set up the database: `python database_setup.py`
6. Run the application with `set FLASK_APP=application` and `flask run`
    - For mac users: `export FLASK_APP=application` and `flask run`

If you already have a virtual environment and a database, follow these steps:

1. Activate the environment: `env/Scripts/activate`
    - For mac users: `. env/bin/activate`
2. Go into the application directory with `cd application`
3. Run the application with `set FLASK_APP=application` and `flask run`
    - For mac users: `export FLASK_APP=application` and `flask run`

To run the tests:

1. From the outer directory, go into the tests directory with `cd tests`
2. run `pytest` and watch it go~
