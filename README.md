# Student Explorer

## Development Environment

### Application Setup

To follow these instructions, you will need to have [Docker](https://www.docker.com/) installed. For those new to the
technology, the [documentation](https://docs.docker.com/) includes a detailed introduction. When following the below
instructions, the application will use fake prepared data to help demonstrate the tool's functionality.

1. Clone and navigate into the repository.

    ```
    git clone https://github.com/tl-its-umich-edu/student_explorer.git # HTTPS
    git clone git@github.com:tl-its-umich-edu/student_explorer.git # SSH
    
    cd student_explorer
    ```

2. Create a `.env` using `.env.sample` as a template.

    ```
    mv .env.sample .env
    ```

3. Build and bring up the development server using `docker-compose`.

    ```
    docker-compose build
    docker-compose up
    ```
    
    Use `^C` and `docker-compose down` to bring the application down.

4. Browse the application on localhost.

    - Navigate to [http://localhost:2082/](http://localhost:2082/).
    - Log in as `admin` or an advisor (e.g. `burl`). All passwords are the same as the user's username.
    
    Not all pages will have complete data. The pages for 
    [Grace Devilbiss](http://localhost:2082/students/grace/) provide a comprehensive example of how the tool
    presents and visualizes student data.
    
### Running the Tests
    
When working on the application, you should periodically run and update the unit tests. To run them, use
the following command while the development server is up.

```
docker exec -it student_explorer /bin/bash -c "echo yes | python manage.py test"
```

You can also enter the running Docker container &mdash; and then run your own commands &mdash; by using the first part 
of the above command, `docker exec -it student_explorer /bin/bash`.

### Django Debug Toolbar

The application is currently configured to use the
[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) to assist with development. The toolbar
will only appear if `DJANGO_DEBUG` is set to `true` in the `.env` and the user is logged in as a superuser.

### Note on Settings

By default, Django's `manage.py` process looks for the `student_explorer.local.settings_override module`. This file is 
created automatically when using `docker-compose` based on instructions in the `Dockerfile`. In addition, `wsgi.py` 
(which is used by `start.sh`) looks by default for the `student_explorer.settings` module. This file is versioned as 
part of the repository. This behavior can be changed for both `manage.py` and `wsgi.py` by setting the 
`DJANGO_SETTINGS_MODULE` environment variable.