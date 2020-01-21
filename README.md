## MAT-API

Moringa Attendance Tracker


## Description

The **mat-api** is the backbone of an application for viewing classroom attendance.
The api provides features for registering users(students and TMs) and viewing attendance records for students.


## Development set up


-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.6.5
    ```

-   Install pipenv:

    ```
    pip install pipenv
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

- Clone the mat-api repo and cd into it
    ```
    git clone https://gitlab.com/Moringa-School/mat-api.git
    ```

- spawn a shell in a virtual environment
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
    DATABASE_URL='url_here'
    SECRET_KEY='super_secret'
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

- Running Tests

 [TODO]


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


