# e-learning-platform
A simple E-learning platform for delivering learning media content.

## How to setup the project 
-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.6.5
    ```

-   Install pipenv:

    ```
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.6.25
    ```
-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
    ```
-   Clone the  repo and cd into it:

    ```
    git clone https://github.com/kimbugp/e-learning-platform
    ```

-   Install dependencies:

    ```
    pipenv install
    ```

-   Install dev dependencies to setup development environment:

    ```
    pipenv install --dev
    ```
-   Make a copy of the .env.sample file and rename it to .env and update the variables accordingly:

-   Activate a virtual environment:

    ```
    pipenv shell
    ```

-   Apply migrations:

    ```
    python manage.py migrate
    ```
*   Run the application:

    ```
    python manage.py runserver
    ```