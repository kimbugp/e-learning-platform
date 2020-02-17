[![Build Status](https://travis-ci.com/kimbugp/e-learning-platform.svg?branch=develop)](https://travis-ci.com/kimbugp/e-learning-platform)
# e-learning-platform

## Mirest platform
A simple E-learning platform for delivering learning media content.
The Mirest e-learning is an online platform a learning management tools for both students and instructors

## Link 
    https://mirest.herokuapp.com/ 

## Structure
    An instructor signs up and manages courses with the content on the platform under different categories
    Students sign-up and search through the application for useful courses which they enrol onto.
    
## Features.

- Instructor signup
- Courses creation and management
- Creation and management of modules
- Management of content in modules
- Course enrollment by students
- View of courses by students
- Rating of course


## How to setup the project 
-   Clone the  repo and cd into it:

    ```
    git clone https://github.com/kimbugp/e-learning-platform
    ```

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.6.5
    ```

-   Install virtualenv:

    ```
    pip install virtualenv
    ```

-   Check virtualenv is installed:
    ```
    virtualenv --version
    >> 16.5.0
    ```
-   Create virtual environment:

    ```
    virtualenv venv
    ```

-   Activate virtual environment:

    ```
    source venv/bin/activate install
    ```

-   Install dev dependencies to setup development environment:

    ```
    pip install -r requirements.txt
    ```

-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
    ```

-   Make a copy of the .env.sample file and rename it to .env and update the variables accordingly:


-   Apply migrations:

    ```
    python manage.py migrate
    ```
-   Load sample data:

    ```
    python manage.py loaddata app/authentication/fixtures/all.json
    ```
-   Run the application:

    ```
    python manage.py runserver
    ```

- Running tests:

    ```
    python manage.py test
    ```