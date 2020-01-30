## MAT-API

Moringa Attendance Tracker


## Description

The **mat-api** is the backbone of an application for viewing classroom attendance.
The api provides features for registering users(students and TMs) and viewing attendance records for students.


## Development set up


-   Check that python 3.7.x is installed:

    ```
    python --version
    >> Python 3.7.x
    ```

-   Install pipenv:

    ```
    pip3 install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.11.26
    ```
-   Check that postgres is installed:

    ```
    postgres --version
    >> postgres (PostgreSQL) 10.1
    ```
-  Database
    * Swith to postgres account (in terminal)
        ```
        sudo su - postgres
        ```
    * Run PostgreSQL command line client.
        ```
        psql
        ```
    * Create a database user with a password.
        ```
        CREATE USER mat_owner with password 'password12345';
        ```
    * Create a database instance.
        ```
        CREATE DATABASE mat_db owner mat_owner encoding 'utf-8';
        ```  

- Clone the mat-api repo and cd into it
    ```
    git clone https://gitlab.com/Moringa-School/mat-api.git
    ```
- Create  virtual environment
    ```
    pipenv --python 3.7

    ```
- Turn off a virtual environment  
    ```
    exit
    ```

- Spawn a shell in a virtual environment
    ```
    pipenv shell
    ```
- Install dependencies
    ```
   pipenv install 
    ```
- Create Application environment variables and save them in .env file 
    ```
    DJANGO_READ_DOT_ENV_FILE=True
    DJANGO_DEBUG=True
    DATABASE_URL='postgresql://localhost/mat_db?user=mat_owner&password=password12345'
    SECRET_KEY='super_secret'
    ```

- Add the variables in the .env file to path
    ```
    source .env
    ```
- Running migrations

    - Initial migration commands
        ```
        make migrations
        
        make migrate
        ```



- Run application.
    ```
    make serve
    ```

- Running tests and generating report

    On command line run:

    ```
    pytest
    ```

    To further view the lines not tested or covered if there is any,

    A `htmlcov` directory will be created, get the `index.html` file by entering the directory and view it in your browser.


### Merge Request Process

-   A contributor shall identify a task to be done from [Asana](https://app.asana.com/0/1118828205403923/board). 
- If there is a bug , feature or chore that has not been included among the tasks, the contributor can add it only after consulting the owner of this repository and the task being accepted.
-   The Contributor shall then create a branch off the `development` branch where they are expected to undertake the task they have chosen.
-   After undertaking the task, a fully detailed pull request shall be submitted to the owners of this repository for review.
-   If there any changes requested ,it is expected that these changes shall be effected and the pull request resubmitted for review.Once all the changes are accepted, the pull request shall be closed and the changes merged into `development` by the owners of this repository.



## Built with
- Python version  3
- Django (DRF)
- Postgres
 ```


